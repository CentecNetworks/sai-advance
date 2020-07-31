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
import pdb
            
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
        elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            key = sai_thrift_qos_map_params_t(mpls_exp=key_list1[i])
            value = sai_thrift_qos_map_params_t(tc=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            key = sai_thrift_qos_map_params_t(mpls_exp=key_list1[i])
            value = sai_thrift_qos_map_params_t(color=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            key = sai_thrift_qos_map_params_t(tc=key_list1[i], color=key_list2[i])
            value = sai_thrift_qos_map_params_t(mpls_exp=value_list[i])

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
        
        rif_id = []
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        for ii in range(port_num):
            rif_id.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[ii], 0, v4_enabled, v6_enabled, mac))
            print "rif_id  0x%x" %rif_id[ii]

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
        #self.client.sai_thrift_dump_log("dump_0.txt")
        try:
            #apply to ports
            for ii in range(port_num):
                print "Port[0x%x] bind ---->>>>"%port_list[ii]
                attr_value = sai_thrift_attribute_value_t(booldata=True)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[ii],attr) 
        
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
                    
            #self.client.sai_thrift_dump_log("dump_1.txt")
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
                    
                attr_value = sai_thrift_attribute_value_t(booldata=False)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[ii],attr) 
                    
            #self.client.sai_thrift_dump_log("dump_2.txt")
            
            for ii in range(port_num):
                self.client.sai_thrift_remove_router_interface(rif_id[ii])
            self.client.sai_thrift_remove_virtual_router(vr_id)
    
            for ii in range(domain_num):
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc[ii])
                self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p[ii])
                self.client.sai_thrift_remove_qos_map(map_id_dscp_tc[ii])
                self.client.sai_thrift_remove_qos_map(map_id_tc_dscp[ii])


class scenario_13_basic_mpls_swap_set_qosmap_elsp(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300
        
        #Create QosMap, exp -- > TC
        key_list =    [0, 1, 2, 3, 4, 5, 6, 7]
        value_list = [7, 1, 2, 3, 4, 5, 6, 7]
        print "Create QosMap:exp -- > TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list, [], value_list)
        
        
        key_list_temp = [None]*len(key_list)
        value_list_temp = [None]*len(key_list)
        attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
        for a in attrs.attr_list:
            if a.id == SAI_QOS_MAP_ATTR_TYPE:
                if a.value.u32 != SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
                    print "map type error!!! %d" % a.value.u32
                    raise NotImplementedError()
            if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                if a.value.qosmap.count != len(key_list):
                    print "get map list error!!! count: %d" % a.value.qosmap.count
                    raise NotImplementedError()
                for i in range(a.value.qosmap.count):
                    key_list_temp[i] = a.value.qosmap.map_list[i].key.mpls_exp
                    value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                print "got key_list:  ",key_list_temp
                print "got value_list:",value_list_temp
                if key_list_temp != key_list:
                    print "get key list error!!!"
                    raise NotImplementedError()
                if value_list_temp != value_list:
                    print "get value list error!!!"
                    raise NotImplementedError()
                        
                        
        key_list =    [0, 1, 2, 3, 4, 5, 6, 7]
        value_list = [7, 6, 5, 3, 4, 5, 6, 7]
        print "Create QosMap2 :exp -- > TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id2 = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list, [], value_list)
        
        key_list_temp = [None]*len(key_list)
        value_list_temp = [None]*len(key_list)
        attrs = self.client.sai_thrift_get_qos_map_attribute(map_id2) 
        for a in attrs.attr_list:
            if a.id == SAI_QOS_MAP_ATTR_TYPE:
                if a.value.u32 != SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
                    print "map type error!!! %d" % a.value.u32
                    raise NotImplementedError()
            if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                if a.value.qosmap.count != len(key_list):
                    print "get map list error!!! count: %d" % a.value.qosmap.count
                    raise NotImplementedError()
                for i in range(a.value.qosmap.count):
                    key_list_temp[i] = a.value.qosmap.map_list[i].key.mpls_exp
                    value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                print "got key_list:  ",key_list_temp
                print "got value_list:",value_list_temp
                if key_list_temp != key_list:
                    print "get key list error!!!"
                    raise NotImplementedError()
                if value_list_temp != value_list:
                    print "get value list error!!!"
                    raise NotImplementedError()
                    
        
        
        #Create QosMap, exp -- > color
        key_list =    [0, 1, 2, 3, 4, 5, 6, 7]
        value_list = [SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN]
        print "Create QosMap:exp -- > color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list, [], value_list)
                        
        #attr_value = sai_thrift_attribute_value_t(oid=map_id)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> exp
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [5]
        map_id_tc_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP, key_list1, key_list2 , value_list1)
        
        
        #attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr) 
        

        label_list = [(label1<<12) | 32]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, exp_map_id=map_id_tc_exp)
        
        
        attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop2)
        sys_logging("status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_NEXT_HOP_ATTR_TYPE:
                if SAI_NEXT_HOP_TYPE_MPLS != a.value.s32:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_LABELSTACK:
                if label_list != a.value.u32list.u32list:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_IP:
                sys_logging("get ip = %s" %a.value.ipaddr.addr.ip4)
                if ip_da != a.value.ipaddr.addr.ip4:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
                if rif_id1 != a.value.oid:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP:
                if map_id_tc_exp != a.value.oid:
                    raise NotImplementedError()
        

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        
        mpls_inseg = sai_thrift_inseg_entry_t(label2)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls_inseg, attr)
                
        attr_value = sai_thrift_attribute_value_t(oid=map_id_color)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls_inseg, attr)
        
        
        attr_value = sai_thrift_attribute_value_t(oid=map_id2)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls_inseg, attr)
        
        
        
        
        mpls1 = [{'label':200,'tc':0,'ttl':32,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:33',
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
                               
        mpls2 = [{'label':100,'tc':5,'ttl':31,'s':1}]
        #sai bug,actually label ttl should be 31 ,ip ttl should be 64
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=31,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            

            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_color)
            self.client.sai_thrift_remove_qos_map(map_id2)
            self.client.sai_thrift_remove_qos_map(map_id_tc_exp)
            
class scenario_14_l3vpn_ipdscp_to_pw_exp(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300
        
        #Create QosMap, exp -- > TC
        key_list =    [0, 1, 2, 3, 4, 5, 6, 7]
        value_list = [7, 1, 2, 3, 4, 5, 6, 7]
        print "Create QosMap:exp -- > TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, key_list, [], value_list)
        
        
        key_list_temp = [None]*len(key_list)
        value_list_temp = [None]*len(key_list)
        attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
        for a in attrs.attr_list:
            if a.id == SAI_QOS_MAP_ATTR_TYPE:
                if a.value.u32 != SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
                    print "map type error!!! %d" % a.value.u32
                    raise NotImplementedError()
            if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                if a.value.qosmap.count != len(key_list):
                    print "get map list error!!! count: %d" % a.value.qosmap.count
                    raise NotImplementedError()
                for i in range(a.value.qosmap.count):
                    key_list_temp[i] = a.value.qosmap.map_list[i].key.mpls_exp
                    value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                print "got key_list:  ",key_list_temp
                print "got value_list:",value_list_temp
                if key_list_temp != key_list:
                    print "get key list error!!!"
                    raise NotImplementedError()
                if value_list_temp != value_list:
                    print "get value list error!!!"
                    raise NotImplementedError()
                        
        
        #Create QosMap, exp -- > color
        key_list =    [0, 1, 2, 3, 4, 5, 6, 7]
        value_list = [SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_GREEN]
        print "Create QosMap:exp -- > color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id_color = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, key_list, [], value_list)
                        
        #attr_value = sai_thrift_attribute_value_t(oid=map_id)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> exp
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [5]
        map_id_tc_exp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP, key_list1, key_list2 , value_list1)
        
        
        #attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr) 
        
        
        
        

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        #Create QosMap, DSCP-->TC
        key_list =    [16]
        value_list = [7]
        print "Create QosMap:DSCP-->TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        dscp_map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
        #attr_value = sai_thrift_attribute_value_t(oid=dscp_map_id)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=dscp_map_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        
        ##Create QosMap, TC&Color --> DSCP
        #key_list1 = [7]
        #key_list2 = [SAI_PACKET_COLOR_GREEN]
        #value_list1 = [20]
        #map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        #attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr) 

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr) 
        
        

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        
        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop2, exp_map_id=map_id_tc_exp)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)
        
        
        attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop2)
        sys_logging("status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_NEXT_HOP_ATTR_TYPE:
                if SAI_NEXT_HOP_TYPE_MPLS != a.value.s32:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_LABELSTACK:
                if label_list != a.value.u32list.u32list:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_IP:
                sys_logging("get ip = %s" %a.value.ipaddr.addr.ip4)
                if ip_da != a.value.ipaddr.addr.ip4:
                    raise NotImplementedError()
            if a.id == SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
                if rif_id1 != a.value.oid:
                    raise NotImplementedError()
            #if a.id == SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP:
            #    if map_id_tc_exp != a.value.oid:
            #        raise NotImplementedError()
        

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        
        mpls_inseg = sai_thrift_inseg_entry_t(label2)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls_inseg, attr)
                
        attr_value = sai_thrift_attribute_value_t(oid=map_id_color)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls_inseg, attr)
        
        
        
        
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':7,'ttl':63,'s':0}, {'label':200,'tc':5,'ttl':63,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2,attr) 

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_color)
            self.client.sai_thrift_remove_qos_map(map_id_tc_exp)
            self.client.sai_thrift_remove_qos_map(dscp_map_id)


