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
Thrift SAI interface QoSMap tests
"""
import socket
from switch import *
import sai_base_test
import pdb


def _QosMapCreateMapId(client, map_type=None, key_list1=[], key_list2=[], value_list=[]):
    max_num   = len(value_list)
    attr_list = []
    map_list  = []

    attr_value = sai_thrift_attribute_value_t(s32 = map_type)
    attr       = sai_thrift_attribute_t(id = SAI_QOS_MAP_ATTR_TYPE, value = attr_value)
    attr_list.append(attr)

    for i in range(max_num):
        if map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            key   = sai_thrift_qos_map_params_t(dot1p = key_list1[i])
            value = sai_thrift_qos_map_params_t(tc = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            key   = sai_thrift_qos_map_params_t(dot1p = key_list1[i])
            value = sai_thrift_qos_map_params_t(color = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            key   = sai_thrift_qos_map_params_t(dscp = key_list1[i])
            value = sai_thrift_qos_map_params_t(tc = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            key   = sai_thrift_qos_map_params_t(dscp = key_list1[i])
            value = sai_thrift_qos_map_params_t(color = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            key   = sai_thrift_qos_map_params_t(tc = key_list1[i], color = key_list2[i])
            value = sai_thrift_qos_map_params_t(dscp = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            key   = sai_thrift_qos_map_params_t(tc = key_list1[i], color = key_list2[i])
            value = sai_thrift_qos_map_params_t(dot1p = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
            key   = sai_thrift_qos_map_params_t(tc = key_list1[i])
            value = sai_thrift_qos_map_params_t(queue_index = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            key   = sai_thrift_qos_map_params_t(mpls_exp = key_list1[i])
            value = sai_thrift_qos_map_params_t(tc = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            key   = sai_thrift_qos_map_params_t(mpls_exp = key_list1[i])
            value = sai_thrift_qos_map_params_t(color = value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            key   = sai_thrift_qos_map_params_t(tc = key_list1[i], color = key_list2[i])
            value = sai_thrift_qos_map_params_t(mpls_exp = value_list[i])
        map_list.append(sai_thrift_qos_map_t(key = key, value = value))
        
    qosmap     = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
    attr_value = sai_thrift_attribute_value_t(qosmap = qosmap)
    attr       = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value=attr_value)
    attr_list.append(attr)
    
    return client.sai_thrift_create_qos_map(attr_list)


def _QosMapShowAttribute(client, map_id):
    key_list1_temp   = []
    key_list2_temp   = []
    value_list_temp  = [] 
    
    attrs = client.sai_thrift_get_qos_map_attribute(map_id)

    for a in attrs.attr_list:
        if a.id == SAI_QOS_MAP_ATTR_TYPE:
            map_type = a.value.s32
        if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
            map_count = a.value.qosmap.count
            for i in range(map_count):
                if map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.dot1p)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.tc)
                elif map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.dot1p)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.color)
                elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.dscp)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.tc)
                elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.dscp)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.color)
                elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.tc)
                    key_list2_temp.append(a.value.qosmap.map_list[i].key.color)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.dscp)
                elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.tc)
                    key_list2_temp.append(a.value.qosmap.map_list[i].key.color)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.dot1p)
                elif map_type == SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.tc)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.queue_index)
                elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.mpls_exp)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.tc)
                elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.mpls_exp)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.color)
                elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
                    key_list1_temp.append(a.value.qosmap.map_list[i].key.tc)
                    key_list2_temp.append(a.value.qosmap.map_list[i].key.color)
                    value_list_temp.append(a.value.qosmap.map_list[i].value.mpls_exp)

    sys_logging("### qos_map type = %d ###" %map_type)
    sys_logging("### qos_map value count = %d ###" %map_count)

    if(key_list2_temp):
        print "got key_list1:  ",key_list1_temp
        print "got key_list2:  ",key_list2_temp
    else:
        print "got key_list:   ",key_list1_temp

    print "got value_list: ",value_list_temp


@group('QosMap')
class func_01_create_qos_map_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        create qos_map with correct attribute
        """
        sys_logging("### ----------create qos_map with correct attribute---------- ###")
        
        switch_init(self.client)

        attr_list  = []
        map_type   = SAI_QOS_MAP_TYPE_DOT1P_TO_TC
        attr_value = sai_thrift_attribute_value_t(s32 = map_type)
        attr       = sai_thrift_attribute_t(id = SAI_QOS_MAP_ATTR_TYPE, value = attr_value)
        attr_list.append(attr)

        map_list   = []
        key_list   = [0, 3, 6]
        value_list = [7, 5, 2]
        for i in range(len(key_list)):
            key   = sai_thrift_qos_map_params_t(dot1p = key_list[i])
            value = sai_thrift_qos_map_params_t(tc = value_list[i])
            map_list.append(sai_thrift_qos_map_t(key = key, value = value))
        qosmap = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
        attr_value = sai_thrift_attribute_value_t(qosmap = qosmap)
        attr = sai_thrift_attribute_t(id = SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value = attr_value)
        attr_list.append(attr)
        
        warmboot(self.client)
        
        try:
            map_id = self.client.sai_thrift_create_qos_map(attr_list)
            sys_logging("### qos_map_oid = %d ###" %map_id)
            assert(SAI_NULL_OBJECT_ID != map_id)

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_qos_map(map_id)


@group('QosMap')
class func_02_create_qos_map_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        create qos_map without MANDATORY_ON_CREATE attribute
        """
        sys_logging("### ----------create qos_map without MANDATORY_ON_CREATE attribute---------- ###")
        
        switch_init(self.client)

        #use ttr_list1 to create qos_map without attribute: SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST
        attr_list1 = []
        map_type   = SAI_QOS_MAP_TYPE_DOT1P_TO_TC
        attr_value = sai_thrift_attribute_value_t(s32 = map_type)
        attr       = sai_thrift_attribute_t(id = SAI_QOS_MAP_ATTR_TYPE, value = attr_value)
        attr_list1.append(attr)

        #use ttr_list2 to create qos_map without attribute: SAI_QOS_MAP_ATTR_TYPE
        attr_list2 = []
        map_list   = []
        key_list   = [0, 3, 6]
        value_list = [7, 5, 2]
        for i in range(len(key_list)):
            key   = sai_thrift_qos_map_params_t(dot1p = key_list[i])
            value = sai_thrift_qos_map_params_t(tc = value_list[i])
            map_list.append(sai_thrift_qos_map_t(key = key, value = value))
        qosmap     = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
        attr_value = sai_thrift_attribute_value_t(qosmap = qosmap)
        attr       = sai_thrift_attribute_t(id = SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value = attr_value)
        attr_list2.append(attr)
        
        warmboot(self.client)
        
        try:
            map_id1 = self.client.sai_thrift_create_qos_map(attr_list1)
            sys_logging("### qos_map_oid = %d ###" %map_id1)
            assert(SAI_NULL_OBJECT_ID == map_id1)

            map_id2 = self.client.sai_thrift_create_qos_map(attr_list2)
            sys_logging("### qos_map_oid = %d ###" %map_id2)
            assert(SAI_NULL_OBJECT_ID == map_id2)

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_qos_map(map_id1)
            self.client.sai_thrift_remove_qos_map(map_id2)


@group('QosMap')
class func_03_create_qos_map_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        create multiple qos_map
        """
        sys_logging("### ----------create multiple qos_map---------- ###")
        
        switch_init(self.client)

        map_id   = []
        
        map_type0 = [SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                     SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP]
        
        map_type = [SAI_QOS_MAP_TYPE_DOT1P_TO_TC, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, 
                    SAI_QOS_MAP_TYPE_DSCP_TO_TC, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, 
                    SAI_QOS_MAP_TYPE_TC_TO_QUEUE, 
                    SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR]    
                    
        key_list   = [0, 1, 2]
        value_list = [0, 1, 2]

        warmboot(self.client)
        
        try:
            for i in range(len(map_type)):        
                map_id.append(_QosMapCreateMapId(self.client, map_type[i], key_list, [], value_list))
               
            for i in range(len(map_id)):        
                sys_logging("### qos_map_oid = %d ###" %map_id[i])
                _QosMapShowAttribute(self.client, map_id[i])
                assert(SAI_NULL_OBJECT_ID != map_id[i])
                for j in range((i+1),len(map_id)):
                    if(map_id[i] == map_id[j]):
                        raise NotImplementedError()

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            for i in range(len(map_id)):        
                self.client.sai_thrift_remove_qos_map(map_id[i])


@group('QosMap')
class func_04_remove_qos_map_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        remove qos_map
        """
        sys_logging("### ----------remove qos_map---------- ###")
        
        switch_init(self.client)

        key_list   = [3]
        value_list = [3]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
        sys_logging("### qos_map_oid = %d ###" %map_id)
        
        warmboot(self.client)
        
        try:
            status = self.client.sai_thrift_remove_qos_map(map_id)
            assert(SAI_STATUS_SUCCESS == status)
            
        finally:
            sys_logging("### status = %d ###" %status)


@group('QosMap')
class func_05_remove_qos_map_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        remove not exist qos_map
        """
        sys_logging("### ----------remove not exist qos_map---------- ###")

        not_exist_map_id = 8589934612
        
        switch_init(self.client)

        warmboot(self.client)
        
        try:
            status = self.client.sai_thrift_remove_qos_map(not_exist_map_id)
            assert(SAI_STATUS_SUCCESS != status)
            
        finally:
            sys_logging("### status = %d ###" %status)
          

@group('QosMap')
class func_06_remove_qos_map_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        remove binded qos_map
        """
        sys_logging("### ----------remove binded qos_map---------- ###")

        switch_init(self.client)

        port = port_list[0]
        vr_id  = sai_thrift_get_default_router_id(self.client)
        rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port, 0, 1, 1, '')
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id,
                                                     SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, 1, 1, '')
        inseg = sai_thrift_inseg_entry_t(400)

        key_list   = [3]
        key_list1  = [SAI_PACKET_COLOR_GREEN]
        value_list = [3]
        
        try:
            
            map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS != status)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS != status)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS != status)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            ipda3 = '3.3.3.1'
            dmac3 = '00:33:33:33:33:33'
            sai_thrift_create_neighbor(self.client, addr_family, rif_id, ipda3, dmac3)
            label_list = [(100<<12) | 8]
            outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM 
            outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
            outseg_type     = SAI_OUTSEG_TYPE_PUSH
            map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                     key_list, key_list1, value_list)
            next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id, label_list,
                                                   None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                   map_id, outseg_type)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS != status)
            self.client.sai_thrift_remove_next_hop(next_hop)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            sai_thrift_create_inseg_entry(self.client, 400, 1, None, rif_id1, SAI_PACKET_ACTION_FORWARD,
                                                       None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                       False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                       SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)
            map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS != status)
            self.client.sai_thrift_remove_inseg_entry(inseg)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)
                                                       
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id, ipda3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id)
          

@group('QosMap')
class func_07_get_qos_map_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        get qos_map attribute
        """
        sys_logging("### ----------get qos_map attribute---------- ###")
        
        switch_init(self.client)

        key_list   = [3, 5, 7]
        value_list = [SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_type   = SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR
        map_id     = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list, [], value_list)
        sys_logging("### qos_map_oid = %d ###" %map_id)
        
        warmboot(self.client)
        
        try:
            key_list_temp   = [None] * len(key_list)
            value_list_temp = [None] * len(key_list)
            
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id)
            
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    sys_logging("### qos_map type = %s ###" %a.value.s32)
                    if a.value.s32 != map_type:
                        print "map type error!!! %d" % a.value.s32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    sys_logging("### qos_map value count = %d ###" %a.value.qosmap.count)
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i]   = a.value.qosmap.map_list[i].key.dot1p
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list: ",key_list_temp
                    print "got value_list: ",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_qos_map(map_id)


@group('QosMap')
class func_08_set_qos_map_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        set qos_map attribute: SAI_QOS_MAP_ATTR_TYPE
        """
        sys_logging("### ----------set qos_map attribute: SAI_QOS_MAP_ATTR_TYPE---------- ###")
        
        switch_init(self.client)

        key_list   = [3,6]
        value_list = [3,6]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list, [], value_list)
        sys_logging("### qos_map_oid = %d ###" %map_id)
        
        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(u32=SAI_QOS_MAP_TYPE_DSCP_TO_TC)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_qos_map_attribute(map_id, attr)
            assert(status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sys_logging("### status = %d ###" %status)
            self.client.sai_thrift_remove_qos_map(map_id)


@group('QosMap')
class func_09_set_qos_map_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        set qos_map attribute: SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST
        """
        sys_logging("### ----------set qos_map attribute: SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST---------- ###")
        
        switch_init(self.client)

        key_list   = [2, 4]
        value_list = [SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_RED]
        map_id     = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)
        sys_logging("### qos_map_oid = %d ###" %map_id)

        warmboot(self.client)
        
        try:
            key_list_temp   = [None] * len(key_list)
            value_list_temp = [None] * len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    sys_logging("### qos_map type = %s ###" %a.value.s32)
                    if a.value.s32 != SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                        print "map type error!!! %d" %a.value.s32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    sys_logging("### qos_map value count = %d ###" %a.value.qosmap.count)
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" %a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i]   = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list: ",key_list_temp
                    print "got value_list: ",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()

            map_list    = []
            key_list1   = [3, 5, 7]
            value_list1 = [SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
            for i in range(len(key_list1)):
                key   = sai_thrift_qos_map_params_t(dscp = key_list1[i])
                value = sai_thrift_qos_map_params_t(color = value_list1[i])
                map_list.append(sai_thrift_qos_map_t(key = key, value = value))
            qosmap = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
            attr_value = sai_thrift_attribute_value_t(qosmap = qosmap)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value = attr_value)
            self.client.sai_thrift_set_qos_map_attribute(map_id, attr)

            
            key_list_temp   = [None] * len(key_list1)
            value_list_temp = [None] * len(key_list1)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    sys_logging("### qos_map type = %s ###" %a.value.s32)
                    if a.value.s32 != SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                        print "map type error!!! %d" % a.value.s32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    sys_logging("### qos_map value count = %d ###" %a.value.qosmap.count)
                    if a.value.qosmap.count != len(key_list1):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i]   = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list: ",key_list_temp
                    print "got value_list: ",value_list_temp
                    if key_list_temp != key_list1:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list1:
                        print "get value list error!!!"
                        raise NotImplementedError()

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_qos_map(map_id)


@group('QosMap')
class func_10_set_qos_map_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        set attribute: SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST of qos_map binded on port
        """
        sys_logging("### set ---attribute: SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST of qos_map binded on port--- ###")
        
        switch_init(self.client)

        key_list   = [2, 4]
        value_list = [SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id     = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)
        sys_logging("### qos_map_oid = %d ###" %map_id)
        _QosMapShowAttribute(self.client, map_id)
        
        warmboot(self.client)
        
        try:
            port = port_list[0]
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)
            
            map_list1   = []
            key_list1   = [1, 2, 3]
            value_list1 = [SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
            for i in range(len(key_list1)):
                key   = sai_thrift_qos_map_params_t(dscp = key_list1[i])
                value = sai_thrift_qos_map_params_t(color = value_list1[i])
                map_list1.append(sai_thrift_qos_map_t(key = key, value = value))
            qosmap = sai_thrift_qos_map_list_t(count = len(map_list1), map_list = map_list1)
            attr_value = sai_thrift_attribute_value_t(qosmap = qosmap)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value = attr_value)
            self.client.sai_thrift_set_qos_map_attribute(map_id, attr)
            
            key_list_temp   = [None] * len(key_list1)
            value_list_temp = [None] * len(key_list1)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    sys_logging("### qos_map type = %s ###" %a.value.s32)
                    if a.value.s32 != SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                        print "map type error!!! %d" % a.value.s32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    sys_logging("### qos_map value count = %d ###" %a.value.qosmap.count)
                    if a.value.qosmap.count != len(key_list1):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i]   = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list: ",key_list_temp
                    print "got value_list: ",value_list_temp
                    if key_list_temp != key_list1:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list1:
                        print "get value list error!!!"
                        raise NotImplementedError()
            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)

            self.client.sai_thrift_remove_qos_map(map_id)


@group('QosMap')
class func_11_port_dot1p_max_domain(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        SAI Bug 112061
        """
        sys_logging("### ----------func_11_port_max_domain---------- ###")
        
        switch_init(self.client)

        actual_max_domain = 7

        dot1p_max_domain = 6
        
        port_attrs = []
        ports = []
        port_num = (dot1p_max_domain)*2
        for i in range(port_num):
            ports.append(port_list[i])

        map_id_dot1p_tc = []
        for i in range(dot1p_max_domain+1):
            sys_logging("### Create QosMap and get: dot1p --> tc ###")
            key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
            map_id_dot1p_tc.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, 
                                                      key_list1, [], value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc[i])
            _QosMapShowAttribute(self.client, map_id_dot1p_tc[i])

        map_id_dot1p_color = []
        for i in range(dot1p_max_domain+1):
            sys_logging("### Create QosMap and get: dot1p --> color ###")
            key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            map_id_dot1p_color.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, 
                                                         key_list1, [], value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color[i])
            _QosMapShowAttribute(self.client, map_id_dot1p_color[i])

        map_id_tc_and_color_dot1p = []
        for i in range(dot1p_max_domain+1):
            sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
            key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
            key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
            map_id_tc_and_color_dot1p.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P,
                                                                key_list1, key_list2 , value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p[i])
            _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p[i])

        warmboot(self.client)
        
        try:
            
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            for i in range(port_num):
                port_attrs.append(self.client.sai_thrift_get_port_attribute(ports[i]))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
            
            #apply QosMap to port
            for i in range(0, port_num, 2):
                attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### set port %d attr: QOS_TC_AND_COLOR_TO_DOT1P_MAP, status = 0x%x ###" %(i+1, status))
                if i<(actual_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                sys_logging("### set port %d attr: QOS_TC_AND_COLOR_TO_DOT1P_MAP, status = 0x%x ###" %(i+1+1, status))
                if i<(actual_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)

            for i in range(0, port_num, 2):
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### set port %d attr: QOS_DOT1P_TO_TC_MAP, status = 0x%x ###" %(i+1, status))
                if i<((actual_max_domain)*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                    
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### set port %d attr: QOS_DOT1P_TO_COLOR_MAP, status = 0x%x ###" %(i+1, status))
                if i<((actual_max_domain)*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                    
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                sys_logging("### set port %d attr: QOS_DOT1P_TO_TC_MAP, status = 0x%x ###" %(i+1+1, status))
                if i<((actual_max_domain-1)*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)

                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                sys_logging("### set port %d attr: QOS_DOT1P_TO_COLOR_MAP, status = 0x%x ###" %(i+1+1, status))
                if i<((actual_max_domain-1)*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
            
            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            for i in range(port_num):
                port_attrs[i] = (self.client.sai_thrift_get_port_attribute(ports[i]))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            for i in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### clean port %d attr: QOS_TC_AND_COLOR_TO_DOT1P_MAP, status = 0x%x ###" %(i+1, status))
            
            for i in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### clean port %d attr: QOS_DOT1P_TO_TC_MAP, status = 0x%x ###" %(i+1, status))
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                sys_logging("### clean port %d attr: QOS_DOT1P_TO_COLOR_MAP, status = 0x%x ###" %(i+1, status))

            sys_logging("### ----------get ports attribute after clean up---------- ###")
            for i in range(port_num):
                port_attrs[i] = (self.client.sai_thrift_get_port_attribute(ports[i]))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
            
            for i in range(dot1p_max_domain+1):
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc[i])
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_color[i])
                self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p[i])

'''
@group('QosMap')
class bug(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------bug---------- ###")
        
        switch_init(self.client)

        switch_init(self.client)

        dot1p_max_domain = 7
        port_attrs = []

        ports = []
        port_num = dot1p_max_domain*2
        for i in range(port_num):
            ports.append(port_list[i])

        map_id_dot1p_tc = []
        for i in range(dot1p_max_domain):
            sys_logging("### Create QosMap and get: dot1p --> tc ###")
            key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
            map_id_dot1p_tc.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC,
                                                      key_list1, [], value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc[i])
            _QosMapShowAttribute(self.client, map_id_dot1p_tc[i])

        map_id_dot1p_color = []
        for i in range(dot1p_max_domain):
            sys_logging("### Create QosMap and get: dot1p --> color ###")
            key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            map_id_dot1p_color.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR,
                                                         key_list1, [], value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color[i])
            _QosMapShowAttribute(self.client, map_id_dot1p_color[i])

        map_id_tc_and_color_dot1p = []
        for i in range(dot1p_max_domain):
            sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
            key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
            key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
            map_id_tc_and_color_dot1p.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list))
            sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p[i])
            _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p[i])

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            for i in range(port_num):
                port_attrs.append(self.client.sai_thrift_get_port_attribute(ports[i]))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
            
            #apply QosMap to port
            for i in range(0, port_num-2, 2):
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)

            for i in range(0, port_num-2, 2):
                pdb.set_trace()
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)

            for i in range(0, port_num, 2):
                attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p[i/2])
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
                status = self.client.sai_thrift_set_port_attribute(ports[i], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)
                status = self.client.sai_thrift_set_port_attribute(ports[i+1], attr)
                if i<(dot1p_max_domain*2):
                    assert(SAI_STATUS_SUCCESS == status)
                else:
                    assert(SAI_STATUS_SUCCESS != status)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            for i in range(port_num):
                port_attrs[i] = (self.client.sai_thrift_get_port_attribute(ports[i]))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            for i in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
                self.client.sai_thrift_set_port_attribute(ports[i], attr)
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
                self.client.sai_thrift_set_port_attribute(ports[i], attr)
                attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
                attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
                self.client.sai_thrift_set_port_attribute(ports[i], attr)

            for i in range(dot1p_max_domain):
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc[i])
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_color[i])
                self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p[i])
'''

@group('QosMap')
class scenario_01_bridging_port_dot1p_tagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_01_bridging_port_dot1p_tagged---------- ###")
        
        switch_init(self.client)

        port_attrs = []
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_id  = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)
            
            #apply QosMap to port
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            
            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dot1p == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt2, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            

@group('QosMap')
class scenario_02_bridging_port_dot1p_untagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_02_bridging_port_dot1p_untagged---------- ###")
        
        switch_init(self.client)

        vlan_id1  = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_id2  = 200
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        port_attrs = []
        
        port1      = port_list[0]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)

        port2 = port_list[1]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id2)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                     pktlen = 104)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                     pktlen = 104)

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                 pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                     pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                     pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)              
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)

            #apply QosMap to port
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dot1p == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)

            sys_logging("### -----send packet from port 1 to port 2 without setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 without setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])
                                
            attr_value = sai_thrift_attribute_value_t(u8 = 5)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (5 == port_attrs[a].attr_list[b].value.u8)
                    
            sys_logging("### -----send packet from port 1 to port 2 with setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            attr_value = sai_thrift_attribute_value_t(u16 = 1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u8 = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)


@group('QosMap')
class scenario_03_bridging_port_dot1p_and_dscp_tagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_05_bridging_port_dot1p_and_dscp_tagged---------- ###")
        
        switch_init(self.client)

        port_attrs = []
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_id  = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [1, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 7]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                 ip_dscp = 0, pktlen = 104)
                                 
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                     ip_dscp = 7, pktlen = 104)

        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                     ip_dscp = 5, pktlen = 104)
                                     
        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                 ip_dscp = 0,  pktlen = 104)
                                 
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 7, pktlen = 104)

        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 5, pktlen = 104)

        warmboot(self.client)

        try:
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dot1p == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))
                        assert (True == port_attrs[a].attr_list[b].value.booldata)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            #comment: set port qos attribute as SAI_NULL_OBJECT_ID can modify qos_turst of port
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


       
@group('QosMap')
class scenario_04_bridging_port_dot1p_and_dscp_untagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_06_bridging_port_dot1p_and_dscp_untagged---------- ###")
        
        switch_init(self.client)

        vlan_id1  = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_id2  = 200
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        port_attrs = []
        
        port1      = port_list[0]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)

        port2 = port_list[1]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id2)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [5]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [5]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [1, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 7]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)
                                 
        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                 ip_dscp = 0, ip_ttl = 64, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                     ip_dscp = 7, ip_ttl = 64, pktlen = 104)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                     ip_dscp = 5, ip_ttl = 64, pktlen = 104)
                                     

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                 ip_ttl = 64, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 3,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                     ip_dscp = 7, ip_ttl = 64, pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                     ip_dscp = 5, ip_ttl = 64, pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u8 = 5)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dot1p_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dot1p == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (5 == port_attrs[a].attr_list[b].value.u8)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == port_attrs[a].attr_list[b].value.oid)         
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == port_attrs[a].attr_list[b].value.oid)                
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###"
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))
                        assert (True == port_attrs[a].attr_list[b].value.booldata)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            attr_value = sai_thrift_attribute_value_t(u16 = 1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u8 = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_05_bridging_switch_dot1p_tagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_03_bridging_switch_dot1p_tagged---------- ###")
        
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]

        vlan_id  = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)         
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_tc == a.value.oid)         
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_color == a.value.oid)                
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dot1p == a.value.oid)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt2, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)


@group('QosMap')
class scenario_06_bridging_switch_dot1p_untagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_04_bridging_switch_dot1p_untagged---------- ###")
        
        switch_init(self.client)

        vlan_id1  = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_id2  = 200
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        port_attrs = []
        
        port1      = port_list[0]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)

        port2 = port_list[1]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id2)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                     pktlen = 104)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_dst = '10.0.0.1', ip_id = 101, ip_ttl = 64,
                                     pktlen = 104)

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                 pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                     pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_dst = '10.0.0.1', ip_id = 102, ip_ttl = 64,
                                     pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)              
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == port_attrs[a].attr_list[b].value.oid)
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (0 == port_attrs[a].attr_list[b].value.u8)

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_tc == a.value.oid)         
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_color == a.value.oid)                
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dot1p == a.value.oid)
            
            sys_logging("### -----send packet from port 1 to port 2 without setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 without setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])
                                
            attr_value = sai_thrift_attribute_value_t(u8 = 5)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### -----get ports attribute after modify SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY----- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.u8))
                        assert (5 == port_attrs[a].attr_list[b].value.u8)
                    
            sys_logging("### -----send packet from port 1 to port 2 with setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with setting DEFAULT_VLAN_PRIORITY----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            attr_value = sai_thrift_attribute_value_t(u16 = 1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u8 = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)


@group('QosMap')
class scenario_07_bridging_switch_dot1p_and_dscp_tagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_07_bridging_switch_dot1p_and_dscp_tagged---------- ###")
        
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]

        vlan_id  = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [1, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 7]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                 ip_dscp = 0, pktlen = 104)
                                 
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                     ip_dscp = 7, pktlen = 104)

        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101, ip_ttl = 64,
                                     ip_dscp = 5, pktlen = 104)
                                     
        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                 ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                 ip_dscp = 0,  pktlen = 104)
                                 
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 7, pktlen = 104)

        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 5, pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_tc == a.value.oid)         
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dot1p == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_tc == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dscp == a.value.oid)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            #comment: set switch qos attribute as SAI_NULL_OBJECT_ID can modify qos_turst
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_08_bridging_switch_dot1p_and_dscp_untagged(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_08_bridging_switch_dot1p_and_dscp_untagged---------- ###")
        
        switch_init(self.client)

        vlan_id1  = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_id2  = 200
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        port_attrs = []
        
        port1      = port_list[0]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)

        port2 = port_list[1]
        attr_value = sai_thrift_attribute_value_t(u16 = vlan_id2)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [1, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 7]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)
                                 
        pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                 ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                 ip_dscp = 0, ip_ttl = 64, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 3,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                     ip_dscp = 7, ip_ttl = 64, pktlen = 104)
        exp_pkt2 = simple_tcp_packet(eth_dst = '00:22:22:22:22:22', eth_src = '00:11:11:11:11:11',
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '10.10.10.1', ip_dst = '10.10.10.2', ip_id = 101,
                                     ip_dscp = 5, ip_ttl = 64, pktlen = 104)
                                     

        pkt2 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                 ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                 ip_ttl = 64, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 3,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                     ip_dscp = 7, ip_ttl = 64, pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = '00:11:11:11:11:11', eth_src = '00:22:22:22:22:22',
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.2', ip_dst = '10.10.10.1', ip_id = 102,
                                     ip_dscp = 5, ip_ttl = 64, pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_tc == a.value.oid)         
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dot1p_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dot1p == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_tc == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dscp == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            #comment: set switch qos attribute as SAI_NULL_OBJECT_ID can modify qos_turst
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            attr_value = sai_thrift_attribute_value_t(u16 = 1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u8 = 0)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_11_routing_rif_dscp_phy(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_11_routing_rif_dscp_phy---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        rif_attrs = []
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        dmac1       = '00:11:11:11:11:11'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        ip_addr2    = '20.20.20.1'
        dmac2       = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
        
        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (False == rif_attrs[a].attr_list[b].value.booldata)
            
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 without enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_12_routing_rif_dscp_vlanif(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_12_routing_rif_dscp_vlanif---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        port1      = port_list[0]
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        port2      = port_list[1]
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oids[0], dmac1, port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oids[1], dmac2, port2, SAI_PACKET_ACTION_FORWARD)
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[0], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[1], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (False == rif_attrs[a].attr_list[b].value.booldata)
            
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        #assert (map_id_tc_and_color_dscp == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### send packet from port 2 to port 1 without enabling update_dscp ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, vlan_oids[0], dmac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oids[1], dmac2, port2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_13_routing_rif_dscp_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_13_routing_rif_dscp_subport---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        port1      = port_list[0]
        port2      = port_list[1]

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[0])
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[1])
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 104)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 104)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 104)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (False == rif_attrs[a].attr_list[b].value.booldata)
            
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        #assert (map_id_tc_and_color_dscp == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 without enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            attr_value = sai_thrift_attribute_value_t(u16 = 1)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_PORT_VLAN_ID, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_14_routing_port_and_rif_dscp_phy(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_14_routing_port_and_rif_dscp_phy---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 7]
        value_list  = [7, 0]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [7, 0]
        map_id_tc_and_color_dscp1 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp1)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp1)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 3]
        map_id_tc_and_color_dscp2 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp2)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp2)

        port_attrs = []
        port1 = port_list[0]
        port2 = port_list[1]

        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #apply QosMap to port
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
        
        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))

        rif_attrs = []
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        dmac1       = '00:11:11:11:11:11'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        ip_addr2    = '20.20.20.1'
        dmac2       = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
        
        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt6 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp2)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp2 == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 without enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt6, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp1)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp2)


@group('QosMap')
class scenario_15_routing_port_and_rif_dscp_vlanif(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_15_routing_port_and_rif_dscp_vlanif---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 7]
        value_list  = [7, 0]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [7, 0]
        map_id_tc_and_color_dscp1 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp1)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp1)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 3]
        map_id_tc_and_color_dscp2 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp2)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp2)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]

        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))

        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oids[0], dmac1, port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oids[1], dmac2, port2, SAI_PACKET_ACTION_FORWARD)
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[0], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[1], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt6 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (False == rif_attrs[a].attr_list[b].value.booldata)
            
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp2)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp2 == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 without enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt6, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, vlan_oids[0], dmac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oids[1], dmac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp1)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp2)


@group('QosMap')
class scenario_16_routing_port_and_rif_dscp_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_16_routing_port_and_rif_dscp_subport---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 7]
        value_list  = [7, 0]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [7, 0]
        map_id_tc_and_color_dscp1 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp1)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp1)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [7, 0]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list = [5, 3]
        map_id_tc_and_color_dscp2 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp2)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp2)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]

        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp1)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))

        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[0])
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[1])
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt6 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### -----get rifs attribute before apply QosMap----- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (SAI_NULL_OBJECT_ID == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (False == rif_attrs[a].attr_list[b].value.booldata)
            
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp2)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_tc == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_dscp_color == rif_attrs[a].attr_list[b].value.oid)              
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                        assert (map_id_tc_and_color_dscp2 == rif_attrs[a].attr_list[b].value.oid)
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))
                        assert (True == rif_attrs[a].attr_list[b].value.booldata)

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                                
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sys_logging("### -----send packet from port 1 to port 2 without enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 without enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt6, [0])

                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp1)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp2)


@group('QosMap')
class scenario_17_routing_port_dot1p_and_rif_dscp_phy(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_17_routing_port_dot1p_and_rif_dscp_phy---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
        
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sys_logging("### ----------get ports attribute---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))

        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_18_routing_port_dot1p_and_rif_dscp_vlanif(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_18_routing_port_dot1p_and_rif_dscp_vlanif---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
        
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sys_logging("### ----------get ports attribute---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))

        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oids[0], dmac1, port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oids[1], dmac2, port2, SAI_PACKET_ACTION_FORWARD)
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[0], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[1], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, vlan_oids[0], dmac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oids[1], dmac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)
            

@group('QosMap')
class scenario_19_routing_port_dot1p_and_rif_dscp_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_19_routing_port_dot1p_and_rif_dscp_subport---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
        
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
        attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sys_logging("### ----------get ports attribute---------- ###")
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
        port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))

        for a in range(len(port_attrs)):
            for b in range(len(port_attrs[a].attr_list)):
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                         %(a+1, port_attrs[a].attr_list[b].value.booldata))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.u16))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))
                if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" 
                                 %(a+1, port_attrs[a].attr_list[b].value.oid))

        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[0])
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[1])
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            #rif update dscp
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            #apply QosMap to rif
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1 with port and l3if enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### -----send packet from port 1 to port 2 with port enabling update_dscp----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1 with port enabling update_dscp----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_21_routing_switch_dscp_phy(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_21_routing_switch_dscp_phy---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        rif_attrs = []
        port_attrs = []
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        dmac1       = '00:11:11:11:11:11'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        ip_addr2    = '20.20.20.1'
        dmac2       = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
        
        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_tc == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dscp == a.value.oid)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------get rifs attribute after modify---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------get ports attribute after modify---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_22_routing_switch_dscp_vlanif(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_22_routing_switch_dscp_vlanif---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        rif_attrs  = []
        port_attrs = []
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan_ids   = [100, 200]
        vlan_oids  = []
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oids[0], dmac1, port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oids[1], dmac2, port2, SAI_PACKET_ACTION_FORWARD)
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[0], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[1], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_tc == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dscp == a.value.oid)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------get rifs attribute after modify---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------get ports attribute after modify---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, vlan_oids[0], dmac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oids[1], dmac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_23_routing_switch_dscp_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_23_routing_switch_dscp_subport---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2, 3, 4, 5, 6, 7]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                       SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                      SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
        value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        rif_attrs  = []
        port_attrs = []
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan_ids   = [100, 200]
        vlan_oids  = []
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[0])
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[1])
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 0, pktlen = 100)

        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt3 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 7, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 7,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 0, pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------get switch attribute before apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

            sys_logging("### ----------get ports attribute before apply QosMap---------- ###")
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port1))
            port_attrs.append(self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute before apply QosMap---------- ###")
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs.append(self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            #apply QosMap to switch
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attribute after apply QosMap---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_tc == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_dscp_color == a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)
                    assert (map_id_tc_and_color_dscp == a.value.oid)

            sys_logging("### ----------get ports attribute after apply QosMap---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, port_attrs[a].attr_list[b].value.oid))
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### ----------get rifs attribute after apply QosMap---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.oid))
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------get rifs attribute after modify---------- ###")
            rif_attrs[0] = (self.client.sai_thrift_get_router_interface_attribute(rif_id1))
            rif_attrs[1] = (self.client.sai_thrift_get_router_interface_attribute(rif_id2))
            for a in range(len(rif_attrs)):
                for b in range(len(rif_attrs[a].attr_list)):
                    if rif_attrs[a].attr_list[b].id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                        sys_logging("### rif_id %d attribute: SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP = %d ###" 
                                     %(a+1, rif_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt3, [0])

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------get ports attribute after modify---------- ###")
            port_attrs[0] = (self.client.sai_thrift_get_port_attribute(port1))
            port_attrs[1] = (self.client.sai_thrift_get_port_attribute(port2))
            for a in range(len(port_attrs)):
                for b in range(len(port_attrs[a].attr_list)):
                    if port_attrs[a].attr_list[b].id == SAI_PORT_ATTR_UPDATE_DSCP:
                        sys_logging("### port %d attribute: SAI_PORT_ATTR_UPDATE_DSCP = %d ###" 
                             %(a+1, port_attrs[a].attr_list[b].value.booldata))

            sys_logging("### -----send packet from port 1 to port 2----- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### -----send packet from port 2 to port 1----- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
                            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)
            

@group('QosMap')
class scenario_24_routing_switch_dot1p_and_dscp_phy(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_24_routing_switch_dot1p_and_dscp_phy---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
                
        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 104)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attributes---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)
            

@group('QosMap')
class scenario_25_routing_switch_dot1p_and_dscp_vlanif(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_25_routing_switch_dot1p_and_dscp_vlanif---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
                
        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oids[0], dmac1, port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oids[1], dmac2, port2, SAI_PACKET_ACTION_FORWARD)
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[0], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 
                                                     0, vlan_oids[1], v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attributes---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, vlan_oids[0], dmac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oids[1], dmac2, port2)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_26_routing_switch_dot1p_and_dscp_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        """
        sys_logging("### ----------scenario_26_routing_switch_dot1p_and_dscp_subport---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [1, 2, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, 
                                                       key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1  = [5, 7, 3]
        key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list = [4, 5, 6]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, 
                                                      key_list1, key_list2 , value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port_attrs = []
        port1      = port_list[0]
        port2      = port_list[1]
                
        vlan_ids  = [100, 200]
        vlan_oids  = []
        rif_attrs  = []
        
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[0]))
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oids[0])
        vlan_oids.append(sai_thrift_create_vlan(self.client, vlan_ids[1]))
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oids[1])

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oids[0], port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oids[1], port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        dmac1 = '00:11:11:11:11:11'
        dmac2 = '00:22:22:22:22:22'
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id   = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[0])
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, 
                                                     port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_ids[1])
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1    = '10.10.10.1'
        ip_addr2    = '20.20.20.1'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_mask = '255.255.255.0'
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

        pkt1     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 0,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 64, 
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 2,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 1,
                                     ip_src = '10.10.10.100', ip_dst = '20.20.20.100', ip_id = 101, ip_ttl = 63, 
                                     ip_dscp = 4, pktlen = 100)
                                     
        pkt2     = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac2,
                                     dl_vlan_enable = True, vlan_vid = 200, vlan_pcp = 0,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 64,
                                     ip_dscp = 0, pktlen = 100)
        exp_pkt4 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 2,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 5, pktlen = 100)
        exp_pkt5 = simple_tcp_packet(eth_dst = dmac1, eth_src = router_mac,
                                     dl_vlan_enable = True, vlan_vid = 100, vlan_pcp = 1,
                                     ip_src = '20.20.20.100', ip_dst = '10.10.10.100', ip_id = 102, ip_ttl = 63,
                                     ip_dscp = 4, pktlen = 100)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("### ----------get switch attributes---------- ###")
            ids_list = [SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP,
                        SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP,
                        SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in switch_attr_list.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                if a.id == SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging("### switch attribute: SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = 0x%x ###" %a.value.oid)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt4, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(exp_pkt5, [0])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            self.client.sai_thrift_remove_vlan(vlan_oids[0])
            self.client.sai_thrift_remove_vlan(vlan_oids[1])

            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_31_mpls_basic_uniform_encap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_31_mpls_basic_uniform_encap---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                         key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                            key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5]
        key_list2   = [SAI_PACKET_COLOR_RED]
        value_list1 = [1]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda3 = '3.3.3.1'
        dmac3 = '00:33:33:33:33:33'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label_list = [(label1<<12) | 32]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM 
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        outseg_type     = SAI_OUTSEG_TYPE_PUSH
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                map_id_tc_and_color_exp, outseg_type)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        dmac1 = '00:11:11:11:11:11'
        pkt1 = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                 ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                 ip_dscp = 0, ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        
        mpls1 = [{'label':label1, 'tc':1, 'ttl':63, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        exp_pkt1 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac,
                                      mpls_type = 0x8847, mpls_tags = mpls1,
                                      inner_frame = inner_ip_pkt1) 

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            sai_thrift_remove_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class scenario_32_mpls_basic_uniform_swap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_32_mpls_basic_uniform_swap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1,
                                                                  0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2,
                                                                  0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda4 = '4.4.4.1'
        dmac4 = '00:44:44:44:44:44'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda4, dmac4)

        label1     = 100
        label2     = 200
        label_list = [(label2<<12) | 32]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        outseg_type     = SAI_OUTSEG_TYPE_SWAP
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda4, rif_id2, label_list,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                map_id_tc_and_color_exp, outseg_type)

        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)

        mpls1 = [{'label':label1, 'tc':0, 'ttl':63, 's':1}]
        pkt1  = simple_mpls_packet(eth_dst = router_mac, eth_src = '00:22:22:22:22:22',
                                   mpls_type = 0x8847, mpls_tags = mpls1,
                                   inner_frame = inner_ip_pkt1)

        mpls2     = [{'label':label2, 'tc':7, 'ttl':62, 's':1}]
        exp_pkt1  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls2,
                                       inner_frame = inner_ip_pkt1)

        mpls3     = [{'label':label2, 'tc':5, 'ttl':62, 's':1}]
        exp_pkt2  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls3,
                                       inner_frame = inner_ip_pkt1)

        mpls4     = [{'label':label2, 'tc':0, 'ttl':62, 's':1}]
        exp_pkt3  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls4,
                                       inner_frame = inner_ip_pkt1)

        warmboot(self.client)
        
        try:
            inseg = sai_thrift_inseg_entry_t(label1)
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_LLSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            qos_tc = 7
            attr_value = sai_thrift_attribute_value_t(u8 = qos_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_QOS_TC, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
        finally:
            #pdb.set_trace()
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_inseg_entry(inseg)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda4, dmac4)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class scenario_33_mpls_basic_uniform_decap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_33_mpls_basic_uniform_decap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list1 = [7, 5]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)

        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inseg = sai_thrift_inseg_entry_t(label3)
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 
        
        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':0, 'ttl':62, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 1, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 7, ip_id = 101, ip_ttl = 61,
                                     pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg)
            
            sai_thrift_remove_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_34_mpls_basic_pipe_encap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_34_mpls_basic_pipe_encap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                         key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                            key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5]
        key_list2   = [SAI_PACKET_COLOR_RED]
        value_list1 = [3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda3 = '3.3.3.1'
        dmac3 = '00:33:33:33:33:33'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1    = 100
        exp_value = 7
        ttl_value = 32
        label_list = [(label1<<12) | (exp_value<<9) | (ttl_value)]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_PIPE
        outseg_type     = SAI_OUTSEG_TYPE_PUSH
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                None, outseg_type, ttl_value, exp_value)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        dmac1 = '00:11:11:11:11:11'
        pkt1 = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                 ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                 ip_dscp = 0, ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        
        mpls1 = [{'label':label1, 'tc':7, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        exp_pkt1 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac,
                                      mpls_type = 0x8847, mpls_tags = mpls1,
                                      inner_frame = inner_ip_pkt1) 

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sai_thrift_remove_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_35_mpls_basic_pipe_decap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_35_mpls_basic_pipe_decap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)

        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inseg = sai_thrift_inseg_entry_t(label3)
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':0, 'ttl':62, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 1, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1,
                                  inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 1, ip_id = 101, ip_ttl = 61,
                                     pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg)
            
            sai_thrift_remove_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)


@group('QosMap')
class scenario_36_mpls_basic_short_pipe_decap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_36_mpls_basic_short_pipe_decap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1]
        value_list  = [5, 3]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW]
        value_list1 = [7, 5]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)

        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':0, 'ttl':62, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 1, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1,
                                  inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 1, ip_id = 101, ip_ttl = 61,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 5, ip_id = 101, ip_ttl = 61,
                                     pktlen = 100)
        warmboot(self.client)
        
        try:
            inseg = sai_thrift_inseg_entry_t(label3)
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg)
            
            sai_thrift_remove_route(self.client, vr_id1, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_37_mpls_l3vpn_uniform_encap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_37_mpls_l3vpn_uniform_encap---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                         key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                            key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5]
        key_list2   = [SAI_PACKET_COLOR_RED]
        value_list1 = [7]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda3 = '3.3.3.1'
        dmac3 = '00:33:33:33:33:33'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_val = 0
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_val = 0
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        label1  = 100
        label2  = 200
        ttl_val = 0
        label_list1 = [(label1<<12) | ttl_val]
        label_list2 = [(label2<<12) | ttl_val]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM 
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        outseg_type     = SAI_OUTSEG_TYPE_PUSH
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                map_id_tc_and_color_exp, outseg_type)

        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_hop2,
                                                                          None, map_id_tc_and_color_exp)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        dmac1 = '00:11:11:11:11:11'
        pkt1 = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                 ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                 ip_dscp = 0, ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        
        mpls1 = [{'label':label1, 'tc':7, 'ttl':63, 's':0}, {'label':label2, 'tc':7, 'ttl':63, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        exp_pkt1 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac,
                                      mpls_type = 0x8847, mpls_tags = mpls1,
                                      inner_frame = inner_ip_pkt1) 

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class scenario_38_mpls_l3vpn_uniform_swap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_38_mpls_l3vpn_uniform_swap---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1,
                                                                  0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2,
                                                                  0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda4 = '4.4.4.1'
        dmac4 = '00:44:44:44:44:44'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda4, dmac4)

        label1     = 100
        label2     = 200
        label3     = 300
        label_list = [(label2<<12) | 32]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        outseg_type     = SAI_OUTSEG_TYPE_SWAP
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda4, rif_id2, label_list,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                map_id_tc_and_color_exp, outseg_type)

        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)

        mpls1 = [{'label':label1, 'tc':0, 'ttl':63, 's':0}, {'label':label3, 'tc':0, 'ttl':32, 's':1}]
        pkt1  = simple_mpls_packet(eth_dst = router_mac, eth_src = '00:22:22:22:22:22',
                                   mpls_type = 0x8847, mpls_tags = mpls1,
                                   inner_frame = inner_ip_pkt1)

        mpls2     = [{'label':label2, 'tc':7, 'ttl':62, 's':0}, {'label':label3, 'tc':0, 'ttl':32, 's':1}]
        exp_pkt1  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls2,
                                       inner_frame = inner_ip_pkt1)

        mpls3     = [{'label':label2, 'tc':5, 'ttl':62, 's':0}, {'label':label3, 'tc':0, 'ttl':32, 's':1}]
        exp_pkt2  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls3,
                                       inner_frame = inner_ip_pkt1)

        mpls4     = [{'label':label2, 'tc':0, 'ttl':62, 's':0}, {'label':label3, 'tc':0, 'ttl':32, 's':1}]
        exp_pkt3  = simple_mpls_packet(eth_dst = dmac4, eth_src = router_mac,
                                       mpls_type = 0x8847, mpls_tags = mpls4,
                                       inner_frame = inner_ip_pkt1)

        warmboot(self.client)
        
        try:
            inseg = sai_thrift_inseg_entry_t(label1)

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr) 

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_LLSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            qos_tc = 7
            attr_value = sai_thrift_attribute_value_t(u8 = qos_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_QOS_TC, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])
            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            self.client.sai_thrift_remove_inseg_entry(inseg)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda4, dmac4)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class scenario_39_mpls_l3vpn_uniform_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        """
        SDK Bug 111790
        """
        sys_logging("### ----------scenario_39_mpls_l3vpn_uniform_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda3  = '3.3.3.1'
        dmac3 = '00:33:33:33:33:33'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label2 = 200
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_UNIFORM
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        outseg_type     = SAI_OUTSEG_TYPE_PHP
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, [],
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                None, outseg_type)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, next_hop1, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inseg3 = sai_thrift_inseg_entry_t(label3)
        
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
        
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':1, 'ttl':62, 's':0}, {'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        mpls2 = [{'label':label4, 'tc':2, 'ttl':61, 's':1}]
        inner_ip_pkt2 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 3, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        exp_pkt1 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac,
                                  mpls_type = 0x8847, mpls_tags = mpls2, inner_frame = inner_ip_pkt2) 

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            self.client.sai_thrift_remove_inseg_entry(inseg3)
                        
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_40_mpls_l3vpn_uniform_decap_with_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_40_mpls_l3vpn_uniform_decap_with_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)
        
        sys_logging("### Create QosMap and get: tc & color --> dscp ###")

        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_val = 0
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_val = 0
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inseg4 = sai_thrift_inseg_entry_t(label4)
        
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        #attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        #attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        #self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label4, 'tc':1, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 7, ip_id = 101, ip_ttl = 31,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 5, ip_id = 101, ip_ttl = 31,
                                     pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_41_mpls_l3vpn_uniform_decap_without_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_41_mpls_l3vpn_uniform_decap_without_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL
        encap_ttl_val = 0
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL
        encap_exp_val = 0
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)

        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)

        inseg3 = sai_thrift_inseg_entry_t(label3)
        inseg4 = sai_thrift_inseg_entry_t(label4)
        
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)

        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':1, 'ttl':62, 's':0}, {'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 5, ip_id = 101, ip_ttl = 61,
                                     pktlen = 100)
        
        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg3)
            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_42_mpls_l3vpn_pipe_encap(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_42_mpls_l3vpn_pipe_encap---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0]
        value_list  = [5]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                         key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0]
        value_list  = [SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                            key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5]
        key_list2   = [SAI_PACKET_COLOR_RED]
        value_list1 = [7]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda3 = '3.3.3.1'
        dmac3 = '00:33:33:33:33:33'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_val = 16
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_val = 5
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        label1  = 100
        label2  = 200
        exp_val = 3
        ttl_val = 32
        label_list1 = [(label1<<12) | (exp_val<<9) | ttl_val]
        label_list2 = [(label2<<12) | ttl_val]
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_PIPE
        outseg_type     = SAI_OUTSEG_TYPE_PUSH
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                None, None, None, outseg_ttl_mode, outseg_exp_mode,
                                                None, outseg_type, None, None)

        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_hop2,
                                                                          None, None)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        dmac1 = '00:11:11:11:11:11'
        pkt1 = simple_tcp_packet(eth_dst = router_mac, eth_src = dmac1,
                                 ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                 ip_dscp = 0, ip_id = 101, ip_ttl = 64,
                                 pktlen = 100)
        
        mpls1 = [{'label':label1, 'tc':3, 'ttl':32, 's':0}, {'label':label2, 'tc':5, 'ttl':16, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        exp_pkt1 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac,
                                      mpls_type = 0x8847, mpls_tags = mpls1,
                                      inner_frame = inner_ip_pkt1) 

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class scenario_43_mpls_l3vpn_pipe_decap_with_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_43_mpls_l3vpn_pipe_decap_with_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_val = 16
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_val = 5
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)

        inseg4 = sai_thrift_inseg_entry_t(label4)

        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 3, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 0, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        warmboot(self.client)
        
        try:
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        

        finally:
            sys_logging("### ---------------clean up--------------- ###")

            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_44_mpls_l3vpn_pipe_decap_without_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_44_mpls_l3vpn_pipe_decap_without_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_val = 16
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_val = 5
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM)

        inseg3 = sai_thrift_inseg_entry_t(label3)
        inseg4 = sai_thrift_inseg_entry_t(label4)
        
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
                
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':1, 'ttl':48, 's':0}, {'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 3, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 0, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)
        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)


            self.client.sai_thrift_remove_inseg_entry(inseg3)
            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_45_mpls_l3vpn_short_pipe_decap_with_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_45_mpls_l3vpn_short_pipe_decap_with_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_val = 16
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_val = 5
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)

        inseg4 = sai_thrift_inseg_entry_t(label4)
        
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata = True)
        attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
        attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 7, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 0, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])
        

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class scenario_46_mpls_l3vpn_short_pipe_decap_without_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_46_mpls_l3vpn_short_pipe_decap_without_php---------- ###")
        
        switch_init(self.client)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: dscp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC,
                                                        key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_tc)
        _QosMapShowAttribute(self.client, map_id_dscp_tc)

        sys_logging("### Create QosMap and get: dscp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dscp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR,
                                                           key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dscp_color)
        _QosMapShowAttribute(self.client, map_id_dscp_color)

        sys_logging("### Create QosMap and get: tc & color --> dscp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [7, 5, 3]
        map_id_tc_and_color_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dscp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dscp)

        port1 = port_list[0]
        port2 = port_list[1]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        vr_id2  = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id1 = 0x%x ###" %rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ipda2 = '2.2.2.1'
        dmac2 = '00:22:22:22:22:22'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

        decap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL
        encap_ttl_val = 16
        decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL
        encap_exp_val = 5
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode, encap_ttl_mode, encap_ttl_val,
                                                               decap_exp_mode, encap_exp_mode, encap_exp_val)

        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ipda2, rif_id2)

        ip_mask = '255.255.255.0'
        ipda2_subnet = '2.2.2.0'
        sai_thrift_create_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1) 

        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                                  0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)

        label3 = 300
        label4 = 400
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action,
                                                   None, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id, None, SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,
                                                   False, SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE, None,
                                                   SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE)

        inseg3 = sai_thrift_inseg_entry_t(label3)
        inseg4 = sai_thrift_inseg_entry_t(label4)
                        
        dmac1 = '00:11:11:11:11:11'
        mpls1 = [{'label':label3, 'tc':1, 'ttl':48, 's':0}, {'label':label4, 'tc':2, 'ttl':32, 's':1}]
        inner_ip_pkt1 = simple_ip_only_packet(ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                              ip_dscp = 0, ip_id = 101, ip_ttl = 63, ip_ihl = 5,
                                              pktlen = 86)
        pkt1 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac1,
                                  mpls_type = 0x8847, mpls_tags = mpls1, inner_frame = inner_ip_pkt1) 

        exp_pkt1 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 7, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        exp_pkt2 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 3, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)

        exp_pkt3 = simple_tcp_packet(eth_dst = dmac2, eth_src = router_mac,
                                     ip_src = '1.1.1.1', ip_dst = '2.2.2.1',
                                     ip_dscp = 0, ip_id = 101, ip_ttl = 62,
                                     pktlen = 100)
        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_tc)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg4, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt1, [1])
            
            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg3, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(exp_pkt3, [1])

        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)

            self.client.sai_thrift_remove_inseg_entry(inseg3)
            self.client.sai_thrift_remove_inseg_entry(inseg4)
            
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ipda2_subnet, ip_mask, next_hop1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda2, dmac2)

            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp)


@group('QosMap')
class  scenario_47_mpls_vpls_raw_encap_uniform_and_decap_without_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        """
        SDK Bug 112049
        """
        sys_logging("### ----------scenario_47_mpls_vpls_raw_uniform_encap_and_decap_without_php---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1   = [5, 3, 7, 0]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_GREEN]
        value_list1 = [6, 4, 5, 3]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### bridge_id = 0x%x ###" %bridge_id)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client,
                                                         encap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_RAW,
                                                         decap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_RAW,
                                                         encap_ttl_val = 48, encap_tagged_vlan = 99,
                                                         encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL,
                                                         encap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL,
                                                         encap_exp_val = 6, 
                                                         decap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL)
        sys_logging("### tunnel_id1 = 0x%x ###" %tunnel_id1)

        v4_enabled = 1
        v6_enabled = 1
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        sys_logging("### vr_id1 = 0x%x ###" %vr_id1)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("### vr_id2 = 0x%x ###" %vr_id2)
        
        mac = ''
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac,
                                                     dot1d_bridge_id = bridge_id)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)
        
        ipda3 = '3.3.3.3'
        dmac3 = '00:33:33:33:33:00'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | (4<<9) | 32]
        label_list2 = [(label2<<12) | 16]
        
        counter_oid = None
        next_level_nhop_oid = None
        tunnel_oid = None
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                             counter_oid, next_level_nhop_oid, tunnel_oid,
                                                             outseg_ttl_mode, outseg_exp_mode,
                                                             exp_map_id = map_id_tc_and_color_exp,
                                                             outseg_type = SAI_OUTSEG_TYPE_PUSH,
                                                             ttl_value = 127)
        sys_logging("### next_hop2 = 0x%x ###" %next_hop2)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_hop2,
                                                                          exp_map_id = map_id_tc_and_color_exp)
        sys_logging("### next_hop1 = 0x%x ###" %next_hop1)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id = tunnel_id1)

        vlan_id1 = 100
        vlan_id2 = 200
        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        sys_logging("### bport = 0x%x ###" %bport)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id1, bridge_id)
        sys_logging("### tunnel_bport = 0x%x ###" %tunnel_bport)
        
        dmac1 = '00:11:11:11:11:00'
        dmac2 = '00:22:22:22:22:00'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac2, tunnel_bport, mac_action)

        inseg1 = sai_thrift_inseg_entry_t(label1)
        inseg2 = sai_thrift_inseg_entry_t(label2)
        
        pkt1 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        mpls1 = [{'label':label1,'tc':6,'ttl':32,'s':0}, {'label':label2,'tc':6,'ttl':16,'s':1}]
        inner_ip_pkt = simple_tcp_packet(pktlen = 96, eth_dst = dmac2, eth_src = dmac1, dl_vlan_enable = True,
                                         vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                         ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                         ip_id = 1, ip_ttl = 64, ip_ihl = 5)
        pkt2 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac, mpls_type = 0x8847,
                                  mpls_tags = mpls1, inner_frame = inner_ip_pkt)

        mpls2 = [{'label':label1,'tc':1,'ttl':32,'s':0}, {'label':label2,'tc':2,'ttl':16,'s':1}]
        inner_ip_pkt2 = simple_tcp_packet(pktlen = 96, eth_dst = dmac1, eth_src = dmac2, dl_vlan_enable = True,
                                          vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                          ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                          ip_id = 1, ip_ttl = 64, ip_ihl = 5)
        pkt3 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac3, mpls_type = 0x8847,
                                  mpls_tags = mpls2, inner_frame = inner_ip_pkt2)

        pkt4 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 4, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt5 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 3, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt6 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 4, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)
        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [0])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt5, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt6, [0])
        
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_inseg_entry(inseg1)
            self.client.sai_thrift_remove_inseg_entry(inseg2)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class  scenario_48_mpls_vpls_raw_encap_pipe_and_decap_with_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_48_mpls_vpls_raw_uniform_encap_and_decap_with_php---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### bridge_id = 0x%x ###" %bridge_id)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client,
                                                         encap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_RAW,
                                                         decap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_RAW,
                                                         encap_ttl_val = 48, encap_tagged_vlan = 99,
                                                         encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL,
                                                         encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL,
                                                         encap_exp_val = 3, 
                                                         decap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL)
        sys_logging("### tunnel_id1 = 0x%x ###" %tunnel_id1)

        v4_enabled = 1
        v6_enabled = 1
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        sys_logging("### vr_id1 = 0x%x ###" %vr_id1)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("### vr_id2 = 0x%x ###" %vr_id2)
        
        mac = ''
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac,
                                                     dot1d_bridge_id = bridge_id)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)
        
        ipda3 = '3.3.3.3'
        dmac3 = '00:33:33:33:33:00'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | (7<<9) | 32]
        label_list2 = [(label2<<12) | 16]
        
        counter_oid = None
        next_level_nhop_oid = None
        tunnel_oid = None
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_PIPE
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                             counter_oid, next_level_nhop_oid, tunnel_oid,
                                                             outseg_ttl_mode, outseg_exp_mode,
                                                             exp_map_id = None,
                                                             outseg_type = SAI_OUTSEG_TYPE_PUSH,
                                                             ttl_value = 127)
        sys_logging("### next_hop2 = 0x%x ###" %next_hop2)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_hop2,
                                                                          exp_map_id = None)
        sys_logging("### next_hop1 = 0x%x ###" %next_hop1)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id = tunnel_id1)

        vlan_id1 = 100
        vlan_id2 = 200
        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        sys_logging("### bport = 0x%x ###" %bport)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id1, bridge_id)
        sys_logging("### tunnel_bport = 0x%x ###" %tunnel_bport)
        
        dmac1 = '00:11:11:11:11:00'
        dmac2 = '00:22:22:22:22:00'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac2, tunnel_bport, mac_action)

        inseg1 = sai_thrift_inseg_entry_t(label1)
        inseg2 = sai_thrift_inseg_entry_t(label2)
        
        pkt1 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        mpls1 = [{'label':label1,'tc':7,'ttl':32,'s':0}, {'label':label2,'tc':3,'ttl':16,'s':1}]
        inner_ip_pkt = simple_tcp_packet(pktlen = 96, eth_dst = dmac2, eth_src = dmac1, dl_vlan_enable = True,
                                         vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                         ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                         ip_id = 1, ip_ttl = 64, ip_ihl = 5)
        pkt2 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac, mpls_type = 0x8847,
                                  mpls_tags = mpls1, inner_frame = inner_ip_pkt)

        mpls2 = [{'label':label2,'tc':2,'ttl':16,'s':1}]
        inner_ip_pkt2 = simple_tcp_packet(pktlen = 96, eth_dst = dmac1, eth_src = dmac2, dl_vlan_enable = True,
                                          vlan_vid = vlan_id2, vlan_pcp = 7, dl_vlan_cfi = 1,
                                          ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                          ip_id = 1, ip_ttl = 64, ip_ihl = 5)
        pkt3 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac3, mpls_type = 0x8847,
                                  mpls_tags = mpls2, inner_frame = inner_ip_pkt2)

        pkt4 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 5, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 7, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt5 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 7, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt6 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 7, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 7, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
        
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [0])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt5, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt6, [0])
        
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_inseg_entry(inseg2)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class  scenario_49_mpls_vpls_tagged_encap_uniform_and_decap_without_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_49_mpls_vpls_tagged_encap_uniform_and_decap_without_php---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### bridge_id = 0x%x ###" %bridge_id)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client,
                                                         encap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_TAGGED,
                                                         decap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_TAGGED,
                                                         encap_ttl_val = 48, encap_tagged_vlan = vlan_id3,
                                                         encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL,
                                                         encap_exp_mode = SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL,
                                                         encap_exp_val = 6, 
                                                         decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL)
        sys_logging("### tunnel_id1 = 0x%x ###" %tunnel_id1)

        v4_enabled = 1
        v6_enabled = 1
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        sys_logging("### vr_id1 = 0x%x ###" %vr_id1)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("### vr_id2 = 0x%x ###" %vr_id2)
        
        mac = ''
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac,
                                                     dot1d_bridge_id = bridge_id)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)
        
        ipda3 = '3.3.3.3'
        dmac3 = '00:33:33:33:33:00'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | (4<<9) | 32]
        label_list2 = [(label2<<12) | 16]
        
        counter_oid = None
        next_level_nhop_oid = None
        tunnel_oid = None
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_UNIFORM
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                             counter_oid, next_level_nhop_oid, tunnel_oid,
                                                             outseg_ttl_mode, outseg_exp_mode,
                                                             exp_map_id = map_id_tc_and_color_exp,
                                                             outseg_type = SAI_OUTSEG_TYPE_PUSH,
                                                             ttl_value = 127)
        sys_logging("### next_hop2 = 0x%x ###" %next_hop2)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_hop2,
                                                                          exp_map_id = map_id_tc_and_color_exp)
        sys_logging("### next_hop1 = 0x%x ###" %next_hop1)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id = tunnel_id1)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        sys_logging("### bport = 0x%x ###" %bport)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id1, bridge_id)
        sys_logging("### tunnel_bport = 0x%x ###" %tunnel_bport)
        
        dmac1 = '00:11:11:11:11:00'
        dmac2 = '00:22:22:22:22:00'
        dmac4 = '00:44:44:44:44:00'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac2, tunnel_bport, mac_action)

        inseg1 = sai_thrift_inseg_entry_t(label1)
        inseg2 = sai_thrift_inseg_entry_t(label2)
        
        pkt1 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        mpls1 = [{'label':label1,'tc':6,'ttl':32,'s':0}, {'label':label2,'tc':6,'ttl':16,'s':1}]
        inner_ip_pkt = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                              dl_vlan_outer = vlan_id3, dl_vlan_pcp_outer = 6, dl_vlan_cfi_outer = 0,
                                              vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                              ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                              ip_ttl = 64, ip_ihl = 5)
        pkt2 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac, mpls_type = 0x8847,
                                  mpls_tags = mpls1, inner_frame = inner_ip_pkt)

        mpls2 = [{'label':label1,'tc':1,'ttl':32,'s':0}, {'label':label2,'tc':2,'ttl':16,'s':1}]
        inner_ip_pkt2 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                              dl_vlan_outer = vlan_id3, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                              vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                              ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                              ip_ttl = 64, ip_ihl = 5)
        pkt3 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac3, mpls_type = 0x8847,
                                  mpls_tags = mpls2, inner_frame = inner_ip_pkt2)

        pkt4 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 5, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt5 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 6, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt6 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [0])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt5, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt6, [0])
        
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_inseg_entry(inseg1)
            self.client.sai_thrift_remove_inseg_entry(inseg2)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)


@group('QosMap')
class  scenario_50_mpls_vpls_tagged_encap_pipe_and_decap_with_php(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging("### ----------scenario_50_mpls_vpls_tagged_encap_pipe_and_decap_with_php---------- ###")

        switch_init(self.client)

        sys_logging("### Create QosMap and get: dot1p --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_tc)
        _QosMapShowAttribute(self.client, map_id_dot1p_tc)

        sys_logging("### Create QosMap and get: dot1p --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_dot1p_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_dot1p_color)
        _QosMapShowAttribute(self.client, map_id_dot1p_color)

        sys_logging("### Create QosMap and get: tc & color --> dot1p ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_dot1p)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_dot1p)

        sys_logging("### Create QosMap and get: exp --> tc ###")
        key_list1   = [0, 1, 2]
        value_list  = [5, 3, 7]
        map_id_exp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_tc)
        _QosMapShowAttribute(self.client, map_id_exp_tc)

        sys_logging("### Create QosMap and get: exp --> color ###")
        key_list1   = [0, 1, 2]
        value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        map_id_exp_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list1, [], value_list)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_exp_color)
        _QosMapShowAttribute(self.client, map_id_exp_color)

        sys_logging("### Create QosMap and get: tc & color --> exp ###")
        key_list1   = [5, 3, 7]
        key_list2   = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]
        value_list1 = [6, 4, 5]
        map_id_tc_and_color_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP,
                                                                  key_list1, key_list2, value_list1)
        sys_logging("### qos_map_oid = 0x%x ###" %map_id_tc_and_color_exp)
        _QosMapShowAttribute(self.client, map_id_tc_and_color_exp)

        port1 = port_list[0]
        port2 = port_list[1]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### bridge_id = 0x%x ###" %bridge_id)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client,
                                                         encap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_TAGGED,
                                                         decap_pw_mode = SAI_TUNNEL_MPLS_PW_MODE_TAGGED,
                                                         encap_ttl_val = 48, encap_tagged_vlan = vlan_id3,
                                                         encap_ttl_mode = SAI_TUNNEL_TTL_MODE_PIPE_MODEL,
                                                         encap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL,
                                                         encap_exp_val = 3, 
                                                         decap_exp_mode = SAI_TUNNEL_EXP_MODE_PIPE_MODEL)
        sys_logging("### tunnel_id1 = 0x%x ###" %tunnel_id1)

        v4_enabled = 1
        v6_enabled = 1
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        vr_id1  = sai_thrift_get_default_router_id(self.client)
        sys_logging("### vr_id1 = 0x%x ###" %vr_id1)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("### vr_id2 = 0x%x ###" %vr_id2)
        
        mac = ''
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                                  port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id2 = 0x%x ###" %rif_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### rif_id3 = 0x%x ###" %rif_id3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac,
                                                     dot1d_bridge_id = bridge_id)
        sys_logging("### rif_id4 = 0x%x ###" %rif_id4)
        
        ipda3 = '3.3.3.3'
        dmac3 = '00:33:33:33:33:00'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | (4<<9) | 32]
        label_list2 = [(label2<<12) | (4<<9) | 16]
        
        counter_oid = None
        next_level_nhop_oid = None
        tunnel_oid = None
        outseg_ttl_mode = SAI_OUTSEG_TTL_MODE_PIPE
        outseg_exp_mode = SAI_OUTSEG_EXP_MODE_PIPE
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ipda3, rif_id2, label_list1,
                                                             counter_oid, next_level_nhop_oid, tunnel_oid,
                                                             outseg_ttl_mode, outseg_exp_mode,
                                                             exp_map_id = None,
                                                             outseg_type = SAI_OUTSEG_TYPE_PUSH,
                                                             ttl_value = 127)
        sys_logging("### next_hop2 = 0x%x ###" %next_hop2)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_hop2,
                                                                          exp_map_id = None)
        sys_logging("### next_hop1 = 0x%x ###" %next_hop1)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action,
                                                   tunnel_id = tunnel_id1)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        sys_logging("### bport = 0x%x ###" %bport)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id1, bridge_id)
        sys_logging("### tunnel_bport = 0x%x ###" %tunnel_bport)
        
        dmac1 = '00:11:11:11:11:00'
        dmac2 = '00:22:22:22:22:00'
        dmac4 = '00:44:44:44:44:00'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac2, tunnel_bport, mac_action)

        inseg1 = sai_thrift_inseg_entry_t(label1)
        inseg2 = sai_thrift_inseg_entry_t(label2)
        
        pkt1 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        mpls1 = [{'label':label1,'tc':4,'ttl':32,'s':0}, {'label':label2,'tc':3,'ttl':16,'s':1}]
        inner_ip_pkt = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac2, eth_src = dmac1,
                                              dl_vlan_outer = vlan_id3, dl_vlan_pcp_outer = 6, dl_vlan_cfi_outer = 0,
                                              vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                              ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                              ip_ttl = 64, ip_ihl = 5)
        pkt2 = simple_mpls_packet(eth_dst = dmac3, eth_src = router_mac, mpls_type = 0x8847,
                                  mpls_tags = mpls1, inner_frame = inner_ip_pkt)

        mpls2 = [{'label':label2,'tc':2,'ttl':16,'s':1}]
        inner_ip_pkt2 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                              dl_vlan_outer = vlan_id3, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                              vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                              ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                              ip_ttl = 64, ip_ihl = 5)
        pkt3 = simple_mpls_packet(eth_dst = router_mac, eth_src = dmac3, mpls_type = 0x8847,
                                  mpls_tags = mpls2, inner_frame = inner_ip_pkt2)

        pkt4 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 5, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt5 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 6, dl_vlan_cfi_outer = 0,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        pkt6 = simple_qinq_tcp_packet(pktlen = 100, eth_dst = dmac1, eth_src = dmac2,
                                      dl_vlan_outer = vlan_id1, dl_vlan_pcp_outer = 0, dl_vlan_cfi_outer = 1,
                                      vlan_vid = vlan_id2, vlan_pcp = 4, dl_vlan_cfi = 1,
                                      ip_dst = '1.1.1.1', ip_src = '2.2.2.2',
                                      ip_ttl = 64, ip_ihl = 5)

        warmboot(self.client)
        
        try:
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 1 to port 2---------- ###")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_tc)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_exp_color)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dot1p)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [0])

            attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg1, attr)
            self.client.sai_thrift_set_inseg_entry_attribute(inseg2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_tc)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dot1p_color)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt5, [0])
            
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            sys_logging("### ----------send packet from port 2 to port 1---------- ###")
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt6, [0])
        
        finally:
            sys_logging("### ---------------clean up--------------- ###")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value = attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_inseg_entry(inseg1)
            self.client.sai_thrift_remove_inseg_entry(inseg2)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ipda3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dot1p)
            self.client.sai_thrift_remove_qos_map(map_id_exp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_exp_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_exp)

