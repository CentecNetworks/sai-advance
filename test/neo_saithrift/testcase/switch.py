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
Thrift SAI interface basic tests
"""

import switch_sai
from sai_base_test import *
import time
import sys
import logging

import unittest
import random

import sai_base_test

from ptf import config
from ptf.testutils import *
from ptf.thriftutils import *

import os

from switch_sai.ttypes import  *

from switch_sai.sai_headers import  *
import ctypes
import pdb


import socket

from struct import pack, unpack


from ptf.mask import Mask


this_dir = os.path.dirname(os.path.abspath(__file__))

class VlanObj:
    def __init__(self):
        self.oid = 0
        self.vid = 0

class SwitchObj:
    def __init__(self):
        self.default_1q_bridge = SAI_NULL_OBJECT_ID
        self.default_vlan = VlanObj()

"""
0xFFFF cannot pass the validation,
the reason is that sai u16 is mapped to thrift i16 which is checked to be in [-32768, 32767] range
but "-1" is serialized to 0xFFFF.
"""
U16MASKFULL = -1
U8MASKFULL = -1

switch_inited=0
warmbooten=0
port_list = {}
sai_port_list = []
table_attr_list = []
default_time_out = 5
router_mac='00:77:66:55:44:00'
rewrite_mac1='00:77:66:55:44:01'
rewrite_mac2='00:77:66:55:44:02'

#profile_file = "/data01/users/systest/fangsl/cmodel_sai_trunk/sai/test/neo_saithrift/profile_tm.ini"
profile_file = "/data01/users/systest/shanz/sdk/cmodelsai/cmodel_sai_trunk/sai/test/neo_saithrift/profile_tm.ini"

switch = SwitchObj()

is_bmv2 = ('BMV2_TEST' in os.environ) and (int(os.environ['BMV2_TEST']) == 1)

def alter(client,file,old_str,new_str):
    file_data = ""
    with open(file, "r") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w") as f:
        f.write(file_data)

def warmboot(client):
        print ""
        global warmbooten
        if warmbooten == 0:
            return;
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_RESTART_WARM, value=attr_value)
        client.sai_thrift_set_switch_attribute(attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_PRE_SHUTDOWN, value=attr_value)
        client.sai_thrift_set_switch_attribute(attr)

        attr_value = sai_thrift_attribute_value_t(booldata=0)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL, value=attr_value)
        client.sai_thrift_set_switch_attribute(attr)

        client.sai_thrift_dump_log("dump_before.txt")
        #pdb.set_trace()
        client.sai_thrift_remove_switch()
        alter(client,profile_file,"SAI_BOOT_TYPE=0","SAI_BOOT_TYPE=1")
        #pdb.set_trace()
        client.sai_thrift_create_switch()
        #pdb.set_trace()
        client.sai_thrift_dump_log("dump_after.txt")
        alter(client,profile_file,"SAI_BOOT_TYPE=1","SAI_BOOT_TYPE=0")

def switch_init(client):
    global switch_inited

    if switch_inited:
        return

    switch.default_1q_bridge = client.sai_thrift_get_default_1q_bridge_id()
    assert (switch.default_1q_bridge != SAI_NULL_OBJECT_ID)
    ret = client.sai_thrift_get_default_vlan_id()
    assert (ret.status == SAI_STATUS_SUCCESS), "Failed to get default vlan"
    switch.default_vlan.oid = ret.data.oid

    ret = client.sai_thrift_get_vlan_id(switch.default_vlan.oid)
    assert (ret.status == SAI_STATUS_SUCCESS), "Failed obtain default vlan id"
    switch.default_vlan.vid = ret.data.u16

    for interface,front in interface_to_front_mapping.iteritems():
        sai_port_id = client.sai_thrift_get_port_id_by_front_port(front);
        port_list[int(interface)]=sai_port_id
        print " port_list[%d] = %d" %(int(interface),sai_port_id)

    ids_list = [SAI_SWITCH_ATTR_PORT_NUMBER, SAI_SWITCH_ATTR_PORT_LIST]
    switch_attr_list = client.sai_thrift_get_switch_attribute(ids_list)
    attr_list = switch_attr_list.attr_list
    for attribute in attr_list:
        if attribute.id == SAI_SWITCH_ATTR_PORT_NUMBER:
            print "max ports: %d" % attribute.value.u32
        elif attribute.id == SAI_SWITCH_ATTR_PORT_LIST:
            for port_id in attribute.value.objlist.object_id_list:
                if port_id in port_list.values():
                    attr_value = sai_thrift_attribute_value_t(booldata=1)
                    attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
                    client.sai_thrift_set_port_attribute(port_id, attr)
                    sai_port_list.append(port_id)
        else:
            print "unknown switch attribute"

    attr_value = sai_thrift_attribute_value_t(mac=router_mac)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    unknown_unicast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=unknown_unicast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    unknown_multicast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=unknown_multicast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    broadcast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=broadcast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    all_ports_are_up = True

    if not all_ports_are_up:
        raise RuntimeError('Not all of the  ports are up')

    if switch_inited==0:
        dump_status = client.sai_thrift_dump_log("dump_golden.txt")
        print "dump_status = %d" % dump_status

    switch_inited = 1


def switch_init_without_port(client):
    global switch_inited

    if switch_inited:
        return

    switch.default_1q_bridge = client.sai_thrift_get_default_1q_bridge_id()
    assert (switch.default_1q_bridge != SAI_NULL_OBJECT_ID)
    ret = client.sai_thrift_get_default_vlan_id()
    assert (ret.status == SAI_STATUS_SUCCESS), "Failed to get default vlan"
    switch.default_vlan.oid = ret.data.oid

    ret = client.sai_thrift_get_vlan_id(switch.default_vlan.oid)
    assert (ret.status == SAI_STATUS_SUCCESS), "Failed obtain default vlan id"
    switch.default_vlan.vid = ret.data.u16

    attr_value = sai_thrift_attribute_value_t(mac=router_mac)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    unknown_unicast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=unknown_unicast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    unknown_multicast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=unknown_multicast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    broadcast = SAI_PACKET_ACTION_FORWARD
    attr_value = sai_thrift_attribute_value_t(s32=broadcast)
    attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION, value=attr_value)
    client.sai_thrift_set_switch_attribute(attr)

    if switch_inited==0:
        dump_status = client.sai_thrift_dump_log("dump_golden.txt")
        print "dump_status = %d" % dump_status

    switch_inited = 1


def sai_thrift_get_cpu_packet_count(client, mode=0):
    '''
    mode 0 is READ, mode 1 is READ_AND_CLEAR
    '''
    cpu_packet_count = client.sai_thrift_get_cpu_packet_count()
    if mode == 1:
        client.sai_thrift_clear_cpu_packet_info()
    sys_logging("### received rx packet = %d ###" %cpu_packet_count.data.u16)
    return cpu_packet_count.data.u16


def sai_thrift_get_cpu_port_id(client):
    cpu_port = client.sai_thrift_get_cpu_port_id()
    return cpu_port

def sai_thrift_get_default_vlan_id(client):
    result = client.sai_thrift_get_default_vlan_id()
    return result.data.oid

def sai_thrift_get_default_router_id(client):
    default_router_id = client.sai_thrift_get_default_router_id()
    return default_router_id


def sai_thrift_create_port(client, front, speed, lane_list):

    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(u32=speed)
    attr0 = sai_thrift_attribute_t(id=SAI_PORT_ATTR_SPEED, value=attr_value0)
    attr_list.append(attr0)

    lane_list1 = sai_thrift_u32_list_t(count=len(lane_list), u32list=lane_list)
    attr_value1 = sai_thrift_attribute_value_t(u32list=lane_list1)
    attr1 = sai_thrift_attribute_t(id=SAI_PORT_ATTR_HW_LANE_LIST, value=attr_value1)
    attr_list.append(attr1)

    return client.sai_thrift_create_port(front, attr_list)


def sai_thrift_get_bridge_port_by_port(client, port_id):
    ret = client.sai_thrift_get_bridge_port_list(switch.default_1q_bridge)
    assert (ret.status == SAI_STATUS_SUCCESS)
    print "### port_oid: 0x%010x ###" %port_id
    for bp in ret.data.objlist.object_id_list:
        attrs = client.sai_thrift_get_bridge_port_attribute(bp)
        bport_id = SAI_NULL_OBJECT_ID
        is_port = False
        for a in attrs.attr_list:
            if a.id == SAI_BRIDGE_PORT_ATTR_PORT_ID:
                bport_id = a.value.oid
            if a.id == SAI_BRIDGE_PORT_ATTR_TYPE:
                is_port = a.value.s32 == SAI_BRIDGE_PORT_TYPE_PORT

        if is_port and bport_id == port_id:
            return bp

    return SAI_NULL_OBJECT_ID


def sai_thrift_get_bridge_port_by_sub_port(client, port_id, vlan_id, bridge_id):
    ret = client.sai_thrift_get_bridge_port_list(bridge_id)
    assert (ret.status == SAI_STATUS_SUCCESS)
    for bp in ret.data.objlist.object_id_list:
        attrs = client.sai_thrift_get_bridge_port_attribute(bp)
        bport_id = SAI_NULL_OBJECT_ID
        is_port = False
        for a in attrs.attr_list:
            if a.id == SAI_BRIDGE_PORT_ATTR_PORT_ID:
                bport_id = a.value.oid
            if a.id == SAI_BRIDGE_PORT_ATTR_TYPE:
                is_port = a.value.s32 == SAI_BRIDGE_PORT_TYPE_SUB_PORT
            if a.id == SAI_BRIDGE_PORT_ATTR_VLAN_ID:
                bvlan_id = a.value.u16
        if is_port and bport_id == port_id and bvlan_id == vlan_id:
            return bp

    return SAI_NULL_OBJECT_ID


def sai_thrift_get_port_by_bridge_port(client, bp):
    attrs = client.sai_thrift_get_bridge_port_attribute(bp)
    port = SAI_NULL_OBJECT_ID

    for a in attrs.attr_list:
        if a.id == SAI_BRIDGE_PORT_ATTR_PORT_ID:
            return a.value.oid

    return SAI_NULL_OBJECT_ID


def sai_thrift_create_bridge(client, type, max_learned_addresses=None, learn_disable=None):
    bridge_attrs = []

    bridge_attr_type_value = sai_thrift_attribute_value_t(s32=type)
    bridge_attr_type = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_TYPE, value=bridge_attr_type_value)
    bridge_attrs.append(bridge_attr_type)

    if max_learned_addresses is not None:
        bridge_attr_max_learned_addresses_value = sai_thrift_attribute_value_t(u32=max_learned_addresses)
        bridge_attr_max_learned_addresses = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES,
                                                                   value=bridge_attr_max_learned_addresses_value)
        bridge_attrs.append(bridge_attr_max_learned_addresses)

    if learn_disable is not None:
        bridge_attr_learn_disable_value = sai_thrift_attribute_value_t(booldata=learn_disable)
        bridge_attr_learn_disable = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE,
                                                           value=bridge_attr_learn_disable_value)
        bridge_attrs.append(bridge_attr_learn_disable)

    ret = client.sai_thrift_create_bridge(bridge_attrs)
    return ret.data.oid


def sai_thrift_create_bridge_port(client, port_id=None, type=SAI_BRIDGE_PORT_TYPE_PORT, bridge_id=None, vlan_id=None,
                                  rif_id=None, admin_state=True, oamEn=None, policer_id=None, service_id=None,
                                  customer_vlan_id=None, tagging_mode=None,service_vlan_id=None, service_vlan_cos_mode = None, service_vlan_cos=None, need_flood = None, learn_mode = None):
    bport_attr_list = []

    bport_attr_type_value = sai_thrift_attribute_value_t(s32=type)
    bport_attr_type = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TYPE,
                                             value=bport_attr_type_value)
    bport_attr_list.append(bport_attr_type)

    if port_id is not None:
         bport_attr_port_id_value = sai_thrift_attribute_value_t(oid=port_id)
         bport_attr_port_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_PORT_ID,
                                                     value=bport_attr_port_id_value)
         bport_attr_list.append(bport_attr_port_id)

    if tagging_mode is not None:
         bport_attr_tagging_mode_value = sai_thrift_attribute_value_t(s32=tagging_mode)
         bport_attr_tagging_mode = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TAGGING_MODE,
                                                          value=bport_attr_tagging_mode_value)
         bport_attr_list.append(bport_attr_tagging_mode)

    if vlan_id is not None:
        bport_attr_vlan_id_value = sai_thrift_attribute_value_t(u16=vlan_id)
        bport_attr_vlan_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_VLAN_ID,
                                                    value=bport_attr_vlan_id_value)
        bport_attr_list.append(bport_attr_vlan_id)

    if rif_id is not None:
        bport_attr_rif_id_value = sai_thrift_attribute_value_t(oid=rif_id)
        bport_attr_rif_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_RIF_ID,
                                                   value=bport_attr_rif_id_value)
        bport_attr_list.append(bport_attr_rif_id)

    if bridge_id is not None:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=bridge_id)
    else:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=switch.default_1q_bridge)
    bport_attr_bridge_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID,
                                                  value=bport_attr_bridge_id_value)
    bport_attr_list.append(bport_attr_bridge_id)

    bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=admin_state)
    bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_admin_state_value)
    bport_attr_list.append(bport_attr_admin_state)

    if oamEn is not None:
        bport_attr_oam_value = sai_thrift_attribute_value_t(booldata=oamEn)
        bport_attr_oam_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE,
                                                   value=bport_attr_oam_value)
        bport_attr_list.append(bport_attr_oam_id)

    if policer_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if service_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(u16=service_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if service_vlan_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(u16=service_vlan_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_ID,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)
        
    if service_vlan_cos_mode is not None:
            bport_attr_value = sai_thrift_attribute_value_t(s32=service_vlan_cos_mode)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS_MODE,
                                                        value=bport_attr_value)
            bport_attr_list.append(bport_attr)

    if service_vlan_cos is not None:
        bport_attr_value = sai_thrift_attribute_value_t(s32=service_vlan_cos)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if customer_vlan_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(u16=customer_vlan_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CUSTOMER_VLAN_ID,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if need_flood is not None:
        bport_attr_value = sai_thrift_attribute_value_t(booldata=need_flood)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_NEED_FLOOD,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)
        
    if learn_mode is not None:
        bport_attr_value = sai_thrift_attribute_value_t(s32=learn_mode)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)
        
    ret = client.sai_thrift_create_bridge_port(bport_attr_list)
    return ret.data.oid


def sai_thrift_create_bridge_sub_port(client, port_id, bridge_id, vlan_id, admin_state=True, oamEn=None,
                                      policer_id=None, service_id=None, tagging_mode=None, service_vlan_id = None, service_vlan_cos_mode = None, service_vlan_cos = None, need_flood = None, learn_mode = None):
    return sai_thrift_create_bridge_port(client, port_id, SAI_BRIDGE_PORT_TYPE_SUB_PORT, bridge_id, vlan_id,
                                         admin_state=  admin_state, oamEn=oamEn, policer_id=policer_id, service_id=service_id, tagging_mode=tagging_mode,
                                         service_vlan_id = service_vlan_id, service_vlan_cos_mode = service_vlan_cos_mode, service_vlan_cos = service_vlan_cos, need_flood = need_flood, learn_mode = learn_mode)


def sai_thrift_create_bridge_rif_port(client, bridge_id, rif_id, admin_state=True):
    return sai_thrift_create_bridge_port(client, None, SAI_BRIDGE_PORT_TYPE_1D_ROUTER,
                                         bridge_id, None, rif_id, admin_state)


def sai_thrift_create_bridge_tunnel_port(client, tunnel_id=None, bridge_id=None,
                                         admin_state=True, oamEn=None, policer_id=None, service_id=None, need_flood = None, learn_mode = None):
    bport_attr_list = []

    bport_attr_type_value = sai_thrift_attribute_value_t(s32=SAI_BRIDGE_PORT_TYPE_TUNNEL)
    bport_attr_type = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TYPE,
                                             value=bport_attr_type_value)
    bport_attr_list.append(bport_attr_type)

    if tunnel_id is not None:
         bport_attr_tunnel_id_value = sai_thrift_attribute_value_t(oid=tunnel_id)
         bport_attr_tunnel_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TUNNEL_ID,
                                                value=bport_attr_tunnel_id_value)
         bport_attr_list.append(bport_attr_tunnel_id)

    bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=admin_state)
    bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_admin_state_value)
    bport_attr_list.append(bport_attr_admin_state)

    if bridge_id is not None:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=bridge_id)
    else:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=switch.default_1q_bridge)
    bport_attr_bridge_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID,
                                                  value=bport_attr_bridge_id_value)
    bport_attr_list.append(bport_attr_bridge_id)

    if oamEn is not None:
         bport_attr_oam_en_value = sai_thrift_attribute_value_t(booldata=oamEn)
         bport_attr_oam_en = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE,
                                                value=bport_attr_oam_en_value)
         bport_attr_list.append(bport_attr_oam_en)

    if policer_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID,
                                                    value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if service_id is not None:
        bport_attr_value = sai_thrift_attribute_value_t(u16=service_id)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID,
                                                    value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    if need_flood is not None:
        bport_attr_value = sai_thrift_attribute_value_t(booldata=need_flood)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_NEED_FLOOD,
                                                    value=bport_attr_value)
        bport_attr_list.append(bport_attr)
        
    if learn_mode is not None:
        bport_attr_value = sai_thrift_attribute_value_t(s32=learn_mode)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE,
                                            value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    ret = client.sai_thrift_create_bridge_port(bport_attr_list)
    return ret.data.oid


def sai_thrift_create_bridge_frr_port(client, frr_nhp_grp_id, bridge_id=None, admin_state=True, need_flood = None):
    bport_attr_list = []

    bport_attr_type_value = sai_thrift_attribute_value_t(s32=SAI_BRIDGE_PORT_TYPE_FRR)
    bport_attr_type = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TYPE,
                                             value=bport_attr_type_value)
    bport_attr_list.append(bport_attr_type)

    bport_attr_frr_id_value = sai_thrift_attribute_value_t(oid=frr_nhp_grp_id)
    bport_attr_frr_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FRR_NHP_GRP,
                                           value=bport_attr_frr_id_value)
    bport_attr_list.append(bport_attr_frr_id)

    bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=admin_state)
    bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_admin_state_value)
    bport_attr_list.append(bport_attr_admin_state)

    if bridge_id is not None:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=bridge_id)
    else:
        bport_attr_bridge_id_value = sai_thrift_attribute_value_t(oid=switch.default_1q_bridge)

    bport_attr_bridge_id = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID,
                                                  value=bport_attr_bridge_id_value)
    bport_attr_list.append(bport_attr_bridge_id)

    if need_flood is not None:
        bport_attr_value = sai_thrift_attribute_value_t(booldata=need_flood)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_NEED_FLOOD,
                                                    value=bport_attr_value)
        bport_attr_list.append(bport_attr)

    ret = client.sai_thrift_create_bridge_port(bport_attr_list)
    return ret.data.oid


def sai_thrift_create_bridge_double_vlan_sub_port(client, port_id, bridge_id, vlan_id, customer_vlan_id,
                                                  admin_state=True, oamEn=None, policer_id=None,
                                                  service_id=None, is_lag=None, service_vlan_id = None, service_vlan_cos_mode = None, service_vlan_cos = None, need_flood = None, learn_mode = None):
    return sai_thrift_create_bridge_port(client, port_id, SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT,
                                         bridge_id, vlan_id, None, admin_state, oamEn, policer_id=policer_id,
                                         service_id=service_id, customer_vlan_id=customer_vlan_id, service_vlan_id = service_vlan_id, 
                                         service_vlan_cos_mode = service_vlan_cos_mode, service_vlan_cos = service_vlan_cos, need_flood = need_flood, learn_mode = learn_mode)


def sai_thrift_remove_bridge_sub_port(client, sub_port_id, port_id):
    bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=False)
    bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_admin_state_value)
    client.sai_thrift_set_bridge_port_attribute(sub_port_id, bport_attr_admin_state)
    sai_thrift_flush_fdb_by_bridge_port(client, sub_port_id)
    client.sai_thrift_remove_bridge_port(sub_port_id)
    sai_thrift_create_bridge_port(client, port_id)


def sai_thrift_remove_bridge_sub_port_2(client, sub_port_id, port_id=None):
    bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=False)
    bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_admin_state_value)
    client.sai_thrift_set_bridge_port_attribute(sub_port_id, bport_attr_admin_state)
    sai_thrift_flush_fdb_by_bridge_port(client, sub_port_id)
    client.sai_thrift_remove_bridge_port(sub_port_id)
    #sai_thrift_create_bridge_port(client, port_id)


def sai_thrift_create_fdb_bport(client, bv_id, mac, bport_id=None, mac_action=None, type=None,
                                ip_addr=None, mac_move=None):
    fdb_attr_list = []
    fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac, bv_id=bv_id)

    if type is None:
        type = SAI_FDB_ENTRY_TYPE_STATIC
    fdb_attr_value = sai_thrift_attribute_value_t(s32=type)
    fdb_attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=fdb_attr_value)
    fdb_attr_list.append(fdb_attr)

    if mac_action is not None:
        fdb_attr_value = sai_thrift_attribute_value_t(s32=mac_action)
        fdb_attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=fdb_attr_value)
        fdb_attr_list.append(fdb_attr)

    if bport_id is not None:
        fdb_attr_value = sai_thrift_attribute_value_t(oid=bport_id)
        fdb_attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=fdb_attr_value)
        fdb_attr_list.append(fdb_attr)

    if ip_addr is not None:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
        #addr = sai_thrift_ip_t(ip6=ip_addr)
        #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        fdb_attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
        fdb_attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_ENDPOINT_IP, value=fdb_attr_value)
        fdb_attr_list.append(fdb_attr)

    if mac_move is not None:
        fdb_attr_value = sai_thrift_attribute_value_t(booldata=mac_move)
        fdb_attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_ALLOW_MAC_MOVE, value=fdb_attr_value)
        fdb_attr_list.append(fdb_attr)

    return client.sai_thrift_create_fdb_entry(thrift_fdb_entry=fdb_entry, thrift_attr_list=fdb_attr_list)

def sai_thrift_create_fdb(client, bv_id, mac, port, mac_action=None, is_lag=None):
    if is_lag == None:
        bport_id = sai_thrift_get_bridge_port_by_port(client, port)
        assert(bport_id != SAI_NULL_OBJECT_ID)
    else:
        bport_id = port

    return sai_thrift_create_fdb_bport(client, bv_id, mac, bport_id, mac_action)

def sai_thrift_create_fdb_subport(client, bridge_id, mac, subport_id, mac_action, type):
    '''
    exist for compatibility, do not use this function
    '''
    return sai_thrift_create_fdb_bport(client, bridge_id, mac, subport_id, mac_action, type)

def sai_thrift_create_fdb_tunnel(client, bv_id, mac, bport_id, mac_action, ip_addr):
    '''
    exist for compatibility, do not use this function
    '''
    return sai_thrift_create_fdb_bport(client, bv_id, mac, bport_id, mac_action, ip_addr=ip_addr)


def sai_thrift_delete_fdb(client, bv_id, mac, port=None):
    '''
    no need to assign port, exist for compatibility
    '''
    fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac, bv_id=bv_id)
    return client.sai_thrift_delete_fdb_entry(thrift_fdb_entry=fdb_entry)


def sai_thrift_check_fdb_exist(client, bv_id, mac):
    fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac, bv_id=bv_id)
    fdb_attr_list = client.sai_thrift_get_fdb_entry_attribute(fdb_entry)

    if fdb_attr_list.status == SAI_STATUS_ITEM_NOT_FOUND:
        print "### not found the fdb entry: mac = %s, bv_id = 0x%x ###" %(mac, bv_id)
        return 0

    print "### *** found the fdb entry: mac = %s, bv_id = 0x%x ###" %(mac, bv_id)
    return 1


def sai_thrift_flush_fdb(client, bport_id=None, bv_id=None, type=None):
    fdb_flush_attr_list = []

    if bport_id is not None:
        fdb_flush_attr_value = sai_thrift_attribute_value_t(oid=bport_id)
        fdb_flush_attr = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID, value=fdb_flush_attr_value)
        fdb_flush_attr_list.append(fdb_flush_attr)

    if bv_id is not None:
        fdb_flush_attr_value = sai_thrift_attribute_value_t(oid=bv_id)
        fdb_flush_attr = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_BV_ID, value=fdb_flush_attr_value)
        fdb_flush_attr_list.append(fdb_flush_attr)

    if type is not None:
        fdb_flush_attr_value = sai_thrift_attribute_value_t(s32=type)
        fdb_flush_attr = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_flush_attr_value)
        fdb_flush_attr_list.append(fdb_flush_attr)

    return client.sai_thrift_flush_fdb_entries(thrift_attr_list=fdb_flush_attr_list)

def sai_thrift_flush_fdb_by_vlan(client, bv_id):
    '''
    exist for compatibility, better not to use this function
    '''
    return sai_thrift_flush_fdb(client, bv_id=bv_id)

def sai_thrift_flush_fdb_by_bridge_port(client, bport_id):
    '''
    exist for compatibility, better not to use this function
    '''
    return sai_thrift_flush_fdb(client, bport_id=bport_id)


def sai_thrift_create_virtual_router(client, v4_enabled, v6_enabled):
    #v4 enabled
    vr_attribute1_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
    vr_attribute1 = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE,
                                           value=vr_attribute1_value)
    #v6 enabled
    vr_attribute2_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
    vr_attribute2 = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE,
                                           value=vr_attribute2_value)
    vr_attr_list = [vr_attribute1, vr_attribute2]
    vr_id = client.sai_thrift_create_virtual_router(thrift_attr_list=vr_attr_list)
    return vr_id

def sai_thrift_create_router_interface(client, vr_oid, type, port_oid, vlan_oid, v4_enabled, v6_enabled, mac,
                                       outer_vlan_id=0, dot1d_bridge_id=0, is_virtual=False, stats_state=True):
    #vrf attribute
    rif_attr_list = []
    rif_attribute1_value = sai_thrift_attribute_value_t(oid=vr_oid)
    rif_attribute1 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID,
                                            value=rif_attribute1_value)
    rif_attr_list.append(rif_attribute1)

    rif_attribute2_value = sai_thrift_attribute_value_t(s32=type)
    rif_attribute2 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_TYPE,
                                            value=rif_attribute2_value)
    rif_attr_list.append(rif_attribute2)

    rif_attribute3_value = sai_thrift_attribute_value_t(oid=dot1d_bridge_id)
    rif_attribute3 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID, value=rif_attribute3_value)
    rif_attr_list.append(rif_attribute3)

    if 'goldengate' != testutils.test_params_get()['chipname']:
        rif_attribute_virtual_value = sai_thrift_attribute_value_t(booldata=is_virtual)
        rif_attribute_virtual = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL, value=rif_attribute_virtual_value)
        rif_attr_list.append(rif_attribute_virtual)

    if type == SAI_ROUTER_INTERFACE_TYPE_PORT:
        #port type and port id
        rif_attribute3_value = sai_thrift_attribute_value_t(oid=port_oid)
        rif_attribute3 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_PORT_ID,
                                                value=rif_attribute3_value)
        rif_attr_list.append(rif_attribute3)

    elif type == SAI_ROUTER_INTERFACE_TYPE_VLAN:
        #vlan type and vlan id
        rif_attribute3_value = sai_thrift_attribute_value_t(oid=vlan_oid)
        rif_attribute3 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_VLAN_ID,
                                                value=rif_attribute3_value)
        rif_attr_list.append(rif_attribute3)

    elif type == SAI_ROUTER_INTERFACE_TYPE_BRIDGE:
        #no need to specify port or vlan
        pass

    elif type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT:
        rif_attribute3_value = sai_thrift_attribute_value_t(oid=port_oid)
        rif_attribute3 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_PORT_ID,
                                                value=rif_attribute3_value)
        rif_attr_list.append(rif_attribute3)

        rif_attribute4_value = sai_thrift_attribute_value_t(u16=outer_vlan_id)
        rif_attribute4 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID,
                                                value=rif_attribute4_value)
        rif_attr_list.append(rif_attribute4)

    if(not is_virtual):
        '''
        #v4_enabled
        rif_attribute4_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
        rif_attribute4 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE,
                                                value=rif_attribute4_value)
        rif_attr_list.append(rif_attribute4)

        rif_attribute4_1_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
        rif_attribute4_1 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE,
                                                value=rif_attribute4_1_value)
        rif_attr_list.append(rif_attribute4_1)
        #v6_enabled
        rif_attribute5_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
        rif_attribute5 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE,
                                                value=rif_attribute5_value)
        rif_attr_list.append(rif_attribute5)

        rif_attribute5_1_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
        rif_attribute5_1 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE,
                                                value=rif_attribute5_1_value)
        rif_attr_list.append(rif_attribute5_1)
        '''
        rif_attribute6_value = sai_thrift_attribute_value_t(booldata=stats_state)
        rif_attribute6 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE,
                                                value=rif_attribute6_value)
        rif_attr_list.append(rif_attribute6)

    if mac:
        rif_attribute7_value = sai_thrift_attribute_value_t(mac=mac)
        rif_attribute7 = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS,
                                                value=rif_attribute7_value)
        rif_attr_list.append(rif_attribute7)

    rif_id = client.sai_thrift_create_router_interface(rif_attr_list)
    return rif_id


def sai_thrift_create_route(client, vr_id, addr_family, ip_addr, ip_mask, nhop, packet_action=None, counter_oid = None, cid = None):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        mask = sai_thrift_ip_t(ip4=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        mask = sai_thrift_ip_t(ip6=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
    route_attribute1_value = sai_thrift_attribute_value_t(oid=nhop)
    route_attribute1 = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID,
                                              value=route_attribute1_value)

    route = sai_thrift_route_entry_t(vr_id, ip_prefix)
    route_attr_list = [route_attribute1]

    if packet_action != None:
        route_packet_action_value = sai_thrift_attribute_value_t(s32=packet_action)
        route_packet_action_attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION,
                                                          value=route_packet_action_value)
        route_attr_list.append(route_packet_action_attr)

    if counter_oid != None:
        rt_attribute_value = sai_thrift_attribute_value_t(oid=counter_oid)
        rt_attribute = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_COUNTER_ID,
                                                value=rt_attribute_value)
        route_attr_list.append(rt_attribute)

    if cid != None:
        rt_attribute_value = sai_thrift_attribute_value_t(u32=cid)
        rt_attribute = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_META_DATA,
                                                value=rt_attribute_value)
        route_attr_list.append(rt_attribute)

    return client.sai_thrift_create_route(thrift_route_entry=route, thrift_attr_list=route_attr_list)

def sai_thrift_create_routes(client, vr_id_list, addr_family_list, ip_addr_list, ip_mask_list, nhop_list, packet_action_list, counter_oid_list, cid_list, mode):
    num = len(vr_id_list)
    route_list = []
    route_attr_list =[]
    attr_count_list =[]
    for i in range(num):
        if addr_family_list[i] == SAI_IP_ADDR_FAMILY_IPV4:
            addr = sai_thrift_ip_t(ip4=ip_addr_list[i])
            mask = sai_thrift_ip_t(ip4=ip_mask_list[i])
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
        else:
            addr = sai_thrift_ip_t(ip6=ip_addr_list[i])
            mask = sai_thrift_ip_t(ip6=ip_mask_list[i])
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
        route = sai_thrift_route_entry_t(vr_id_list[i], ip_prefix)
        route_list.append(route)

        route_attribute1_value = sai_thrift_attribute_value_t(oid=nhop_list[i])
        route_attribute1 = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID,
                                              value=route_attribute1_value)
        route_attr_list.append(route_attribute1)
        attr_count = 1
        if packet_action_list[i] != None:
            route_packet_action_value = sai_thrift_attribute_value_t(s32=packet_action_list[i])
            route_packet_action_attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION,
                                                          value=route_packet_action_value)
            route_attr_list.append(route_packet_action_attr)
            attr_count = attr_count + 1

        if counter_oid_list[i] != None:
            rt_attribute_value = sai_thrift_attribute_value_t(oid=counter_oid_list[i])
            rt_attribute = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_COUNTER_ID,
                                                value=rt_attribute_value)
            route_attr_list.append(rt_attribute)
            attr_count = attr_count + 1
        if cid_list[i] != None:
            rt_attribute_value = sai_thrift_attribute_value_t(u32=cid)
            rt_attribute = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_META_DATA,
                                                value=rt_attribute_value)
            route_attr_list.append(rt_attribute)
            attr_count = attr_count + 1

        attr_count_list.append(attr_count)

    return client.sai_thrift_create_routes(thrift_route_entry_list=route_list, thrift_attr_list=route_attr_list, thrift_attr_count_lists = attr_count_list, mode = mode)

def sai_thrift_remove_route(client, vr_id, addr_family, ip_addr, ip_mask, nhop):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        mask = sai_thrift_ip_t(ip4=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        mask = sai_thrift_ip_t(ip6=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
    route = sai_thrift_route_entry_t(vr_id, ip_prefix)
    return client.sai_thrift_remove_route(thrift_route_entry=route)

def sai_thrift_remove_routes(client, vr_id_list, addr_family_list, ip_addr_list, ip_mask_list, nhop_list, mode):
    num = len(vr_id_list)
    route_list = []
    for i in range(num):
        if addr_family_list[i] == SAI_IP_ADDR_FAMILY_IPV4:
            addr = sai_thrift_ip_t(ip4=ip_addr_list[i])
            mask = sai_thrift_ip_t(ip4=ip_mask_list[i])
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
        else:
            addr = sai_thrift_ip_t(ip6=ip_addr_list[i])
            mask = sai_thrift_ip_t(ip6=ip_mask_list[i])
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
        route = sai_thrift_route_entry_t(vr_id_list[i], ip_prefix)
        route_list.append(route)
    return client.sai_thrift_remove_routes(thrift_route_entry_list=route_list, mode = mode)

def sai_thrift_create_nhop(client, addr_family, ip_addr, rif_id):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    nhop_attribute1_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP,
                                             value=nhop_attribute1_value)
    nhop_attribute2_value = sai_thrift_attribute_value_t(oid=rif_id)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID,
                                             value=nhop_attribute2_value)
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_IP)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list = [nhop_attribute1, nhop_attribute2, nhop_attribute3]
    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    return nhop


def sai_thrift_create_mpls_nhop(client, addr_family, ip_addr, rif_id, label_list, counter_oid=None, next_level_nhop_oid=None, tunnel_id=None,outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE,outseg_exp_mode= SAI_OUTSEG_EXP_MODE_PIPE, exp_map_id=None,outseg_type=SAI_OUTSEG_TYPE_PUSH, ttl_value=None,exp_value=None):

    nhop_attr_list=[]
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        
    nhop_attribute1_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP,
                                             value=nhop_attribute1_value)
                                             
    nhop_attribute2_value = sai_thrift_attribute_value_t(oid=rif_id)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID,
                                             value=nhop_attribute2_value)
    if next_level_nhop_oid == None:
        nhop_attr_list.append(nhop_attribute1)
        nhop_attr_list.append(nhop_attribute2)
        
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_MPLS)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list.append(nhop_attribute3)

    mpls_label_list = sai_thrift_u32_list_t(count=len(label_list), u32list=label_list)
    nhop_attribute4_value = sai_thrift_attribute_value_t(u32list=mpls_label_list)
    nhop_attribute4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_LABELSTACK,
                                            value=nhop_attribute4_value)
    nhop_attr_list.append(nhop_attribute4)

    nhop_attribute5_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    nhop_attribute5 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID,
                                             value=nhop_attribute5_value)
    nhop_attr_list.append(nhop_attribute5)

    if counter_oid != None:
        nhop_attribute6_value = sai_thrift_attribute_value_t(oid=counter_oid)
        nhop_attribute6 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID,
                                                 value=nhop_attribute6_value)
        nhop_attr_list.append(nhop_attribute6)
        
    if next_level_nhop_oid != None:
        nhop_attribute7_value = sai_thrift_attribute_value_t(oid=next_level_nhop_oid)
        nhop_attribute7 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
                                                value=nhop_attribute7_value)
        nhop_attr_list.append(nhop_attribute7)
        
    if exp_map_id != None:
        nhop_attribute7_value = sai_thrift_attribute_value_t(oid=exp_map_id)
        nhop_attribute7 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP,
                                                value=nhop_attribute7_value)
        nhop_attr_list.append(nhop_attribute7)

    nhop_attribute8_value = sai_thrift_attribute_value_t(s32=outseg_ttl_mode)
    nhop_attribute8 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE,
                                             value=nhop_attribute8_value)
    nhop_attr_list.append(nhop_attribute8)
    
    nhop_attribute9_value = sai_thrift_attribute_value_t(s32=outseg_exp_mode)
    nhop_attribute9 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE,
                                             value=nhop_attribute9_value)
    nhop_attr_list.append(nhop_attribute9)

    nhop_attribute10_value = sai_thrift_attribute_value_t(s32=outseg_type)
    nhop_attribute10 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_OUTSEG_TYPE,
                                             value=nhop_attribute10_value)
    nhop_attr_list.append(nhop_attribute10)

    if ttl_value != None:
        nhop_attribute6_value = sai_thrift_attribute_value_t(u8=ttl_value)
        nhop_attribute6 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE,
                                                 value=nhop_attribute6_value)
        nhop_attr_list.append(nhop_attribute6)
        
    if exp_value != None:
        nhop_attribute6_value = sai_thrift_attribute_value_t(u8=exp_value)
        nhop_attribute6 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE,
                                                 value=nhop_attribute6_value)
        nhop_attr_list.append(nhop_attribute6)


    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    
    return nhop

def sai_thrift_create_tunnel_mpls_nhop(client, tunnel_id, label_list, next_level_nhop_oid=None):
    nhop_attribute1_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID,
                                             value=nhop_attribute1_value)
    mpls_label_list = sai_thrift_u32_list_t(count=len(label_list), u32list=label_list)
    nhop_attribute2_value = sai_thrift_attribute_value_t(u32list=mpls_label_list)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_LABELSTACK,
                                            value=nhop_attribute2_value)
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_MPLS)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list = [nhop_attribute1, nhop_attribute2, nhop_attribute3]
    if next_level_nhop_oid != None:
        nhop_attribute4_value = sai_thrift_attribute_value_t(oid=next_level_nhop_oid)
        nhop_attribute4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
                                                value=nhop_attribute4_value)
        nhop_attr_list.append(nhop_attribute4)
    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    return nhop

def sai_thrift_create_tunnel_mpls_l3vpn_nhop(client, tunnel_id, label_list, next_level_nhop_oid=None, counter_oid=None, exp_map_id=None):
    nhop_attribute1_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID,
                                             value=nhop_attribute1_value)
    mpls_label_list = sai_thrift_u32_list_t(count=len(label_list), u32list=label_list)
    nhop_attribute2_value = sai_thrift_attribute_value_t(u32list=mpls_label_list)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_LABELSTACK,
                                            value=nhop_attribute2_value)
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list = [nhop_attribute1, nhop_attribute2, nhop_attribute3]
    if next_level_nhop_oid:
        nhop_attribute4_value = sai_thrift_attribute_value_t(oid=next_level_nhop_oid)
        nhop_attribute4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
                                                value=nhop_attribute4_value)
        nhop_attr_list.append(nhop_attribute4)

    if counter_oid != None:
        nhop_attribute5_value = sai_thrift_attribute_value_t(oid=counter_oid)
        nhop_attribute5 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID,
                                                 value=nhop_attribute5_value)
        nhop_attr_list.append(nhop_attribute5)
        
    if exp_map_id != None:
        nhop_attribute7_value = sai_thrift_attribute_value_t(oid=exp_map_id)
        nhop_attribute7 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP,
                                                value=nhop_attribute7_value)
        nhop_attr_list.append(nhop_attribute7)
        
    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    return nhop
    
def sai_thrift_create_tunnel_mpls_l2vpn_nhop(client, tunnel_id, label_list, next_level_nhop_oid=None, counter_oid=None, exp_map_id=None):
    nhop_attribute1_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID,
                                             value=nhop_attribute1_value)
    mpls_label_list = sai_thrift_u32_list_t(count=len(label_list), u32list=label_list)
    nhop_attribute2_value = sai_thrift_attribute_value_t(u32list=mpls_label_list)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_LABELSTACK,
                                            value=nhop_attribute2_value)
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list = [nhop_attribute1, nhop_attribute2, nhop_attribute3]
    if next_level_nhop_oid:
        nhop_attribute4_value = sai_thrift_attribute_value_t(oid=next_level_nhop_oid)
        nhop_attribute4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
                                                value=nhop_attribute4_value)
        nhop_attr_list.append(nhop_attribute4)

    if counter_oid != None:
        nhop_attribute5_value = sai_thrift_attribute_value_t(oid=counter_oid)
        nhop_attribute5 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID,
                                                 value=nhop_attribute5_value)
        nhop_attr_list.append(nhop_attribute5)
        
    if exp_map_id != None:
        nhop_attribute7_value = sai_thrift_attribute_value_t(oid=exp_map_id)
        nhop_attribute7 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP,
                                                value=nhop_attribute7_value)
        nhop_attr_list.append(nhop_attribute7)
        
    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    return nhop

def sai_thrift_create_tunnel_nhop(client, addr_family, ip_addr, tunnel_id, dest_vni=None, tunnel_mac=None, counter_oid=None):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    nhop_attribute1_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    nhop_attribute1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP,
                                             value=nhop_attribute1_value)
    nhop_attribute2_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    nhop_attribute2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TUNNEL_ID,
                                             value=nhop_attribute2_value)
    nhop_attribute3_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP)
    nhop_attribute3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TYPE,
                                             value=nhop_attribute3_value)
    nhop_attr_list = [nhop_attribute1, nhop_attribute2, nhop_attribute3]
    if dest_vni:
        nhop_attribute4_value = sai_thrift_attribute_value_t(u32=dest_vni)
        nhop_attribute4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TUNNEL_VNI,
                                                value=nhop_attribute4_value)
        nhop_attr_list.append(nhop_attribute4)
        if (tunnel_mac):
            nhop_attribute5_value = sai_thrift_attribute_value_t(mac=tunnel_mac)
            nhop_attribute5 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_TUNNEL_MAC,
                                                value=nhop_attribute5_value)
            nhop_attr_list.append(nhop_attribute5)
        if counter_oid:
            nhop_attribute6_value = sai_thrift_attribute_value_t(oid=counter_oid)
            nhop_attribute6 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID,
                                                value=nhop_attribute6_value)
            nhop_attr_list.append(nhop_attribute6)

    nhop = client.sai_thrift_create_next_hop(thrift_attr_list=nhop_attr_list)
    return nhop

def sai_thrift_remove_nhop(client, nhop_list):
    for nhop in nhop_list:
        client.sai_thrift_remove_next_hop(nhop)

def sai_thrift_create_neighbor(client, addr_family, rif_id, ip_addr, dmac, no_host_route = False):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    neighbor_attribute1_value = sai_thrift_attribute_value_t(mac=dmac)
    neighbor_attribute1 = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS,
                                                 value=neighbor_attribute1_value)
    neighbor_attribute2_value = sai_thrift_attribute_value_t(booldata=no_host_route)
    neighbor_attribute2 = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE,
                                                 value=neighbor_attribute2_value)
    neighbor_attr_list = [neighbor_attribute1, neighbor_attribute2]
    neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id, ip_address=ipaddr)
    return client.sai_thrift_create_neighbor_entry(neighbor_entry, neighbor_attr_list)

def sai_thrift_remove_neighbor(client, addr_family, rif_id, ip_addr, dmac):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=ip_addr)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id, ip_address=ipaddr)
    return client.sai_thrift_remove_neighbor_entry(neighbor_entry)

def sai_thrift_create_next_hop_group(client, type=SAI_NEXT_HOP_GROUP_TYPE_ECMP,counter_id = None):
    nhop_group_atr1_value = sai_thrift_attribute_value_t(s32=type)
    nhop_group_atr1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_TYPE,
                                             value=nhop_group_atr1_value)
    nhop_group_attr_list = [nhop_group_atr1]
    if counter_id != None:
        nhop_group_atr2_value = sai_thrift_attribute_value_t(oid=counter_id)
        nhop_group_atr2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID,
                                                value=nhop_group_atr2_value)
        nhop_group_attr_list.append(nhop_group_atr2)
    return client.sai_thrift_create_next_hop_group(nhop_group_attr_list)

def sai_thrift_create_next_hop_protection_group(client):
    nhop_group_atr1_value = sai_thrift_attribute_value_t(s32=SAI_NEXT_HOP_GROUP_TYPE_PROTECTION)
    nhop_group_atr1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_TYPE,
                                             value=nhop_group_atr1_value)
    nhop_group_attr_list = [nhop_group_atr1]
    return client.sai_thrift_create_next_hop_group(nhop_group_attr_list)

def sai_thrift_remove_next_hop_group(client, nhop_group_list):
    for nhop_group in nhop_group_list:
        client.sai_thrift_remove_next_hop_group(nhop_group)

def sai_thrift_create_next_hop_group_member(client, nhop_group, nhop, weight=None, cfg_role=None):
    nhop_gmember_atr1_value = sai_thrift_attribute_value_t(oid=nhop_group)
    nhop_gmember_atr1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID,
                                               value=nhop_gmember_atr1_value)
    nhop_gmember_atr2_value = sai_thrift_attribute_value_t(oid=nhop)
    nhop_gmember_atr2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID,
                                               value=nhop_gmember_atr2_value)
    nhop_gmember_attr_list = [nhop_gmember_atr1, nhop_gmember_atr2]
    
    if None != weight:
        nhop_gmember_atr3_value = sai_thrift_attribute_value_t(u32=weight)
        nhop_gmember_atr3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT,
                                                   value=nhop_gmember_atr3_value)
        nhop_gmember_attr_list.append(nhop_gmember_atr3)
    if None != cfg_role:
        #u8 = ctypes.c_uint8(cfg_role)
        nhop_gmember_atr4_value = sai_thrift_attribute_value_t(s32=cfg_role)
        nhop_gmember_atr4 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE,
                                                   value=nhop_gmember_atr4_value)
        nhop_gmember_attr_list.append(nhop_gmember_atr4)
        
    return client.sai_thrift_create_next_hop_group_member(nhop_gmember_attr_list)

def sai_thrift_create_next_hop_group_members(client, nhop_group_list, nhop_list, weight_list, mode):
    num = len(nhop_group_list)
    nhop_gmember_attr_list = []
    nhop_gmember_attr_count_list = []
    for i in range(num):
        nhop_gmember_atr1_value = sai_thrift_attribute_value_t(oid=nhop_group_list[i])
        nhop_gmember_atr1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID,
                                                value=nhop_gmember_atr1_value)
        nhop_gmember_attr_list.append(nhop_gmember_atr1)
        nhop_gmember_atr2_value = sai_thrift_attribute_value_t(oid=nhop_list[i])
        nhop_gmember_atr2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID,
                                                value=nhop_gmember_atr2_value)
        nhop_gmember_attr_list.append(nhop_gmember_atr2)
        if weight_list[i] != None:
            nhop_gmember_atr3_value = sai_thrift_attribute_value_t(u32=weight_list[i])
            nhop_gmember_atr3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT,
                                                   value=nhop_gmember_atr3_value)
            nhop_gmember_attr_list.append(nhop_gmember_atr3)
            nhop_gmember_attr_count_list.append(3)
            continue
        nhop_gmember_attr_count_list.append(2)

    ret = client.sai_thrift_create_next_hop_group_members(nhop_gmember_attr_list, nhop_gmember_attr_count_list, mode)
    #ret = client.sai_thrift_create_stp_ports(stp_port_attr_lists, stp_port_cnt_list, mode)
    return [ret.objlist.object_id_list, ret.statuslist.status_list]

def sai_thrift_create_next_hop_protection_group_member(client, nhop_group, nhop, role):
    nhop_gmember_atr1_value = sai_thrift_attribute_value_t(oid=nhop_group)
    nhop_gmember_atr1 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID,
                                               value=nhop_gmember_atr1_value)
    nhop_gmember_atr2_value = sai_thrift_attribute_value_t(oid=nhop)
    nhop_gmember_atr2 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID,
                                               value=nhop_gmember_atr2_value)
    nhop_gmember_atr3_value = sai_thrift_attribute_value_t(s32=role)
    nhop_gmember_atr3 = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE,
                                               value=nhop_gmember_atr3_value)

    nhop_gmember_attr_list = [nhop_gmember_atr1, nhop_gmember_atr2, nhop_gmember_atr3]
    return client.sai_thrift_create_next_hop_group_member(nhop_gmember_attr_list)

def sai_thrift_remove_next_hop_group_members(client, nhop_gmember_list, mode):
    ret = client.sai_thrift_remove_next_hop_group_members(nhop_gmember_list, mode)
    return ret.status_list


def sai_thrift_remove_next_hop_from_group(client, nhop_list):
    for hnop in nhop_list:
        client.sai_thrift_remove_next_hop_from_group(hnop)


def sai_thrift_create_lag(client, lag_mode=None, pvid=None, default_vlan_pri=None,drop_untagged=None, drop_tagged=None, max_member=None):
    attr_list = []

    if lag_mode != None:
        lag_attr_value = sai_thrift_attribute_value_t(s32=lag_mode)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_MODE, value=lag_attr_value)
        attr_list.append(attribute)

    if pvid != None:
        lag_attr_value = sai_thrift_attribute_value_t(u16=pvid)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=lag_attr_value)
        attr_list.append(attribute)

    if default_vlan_pri != None:
        lag_attr_value = sai_thrift_attribute_value_t(u8=default_vlan_pri)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY, value=lag_attr_value)
        attr_list.append(attribute)

    if drop_untagged != None:
        lag_attr_value = sai_thrift_attribute_value_t(booldata=drop_untagged)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_UNTAGGED, value=lag_attr_value)
        attr_list.append(attribute)

    if drop_tagged != None:
        lag_attr_value = sai_thrift_attribute_value_t(booldata=drop_tagged)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_TAGGED, value=lag_attr_value)
        attr_list.append(attribute)

    if max_member != None:
        lag_attr_value = sai_thrift_attribute_value_t(u16=max_member)
        attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM, value=lag_attr_value)
        attr_list.append(attribute)

    lag_id = client.sai_thrift_create_lag(attr_list)
    return lag_id


def sai_thrift_remove_lag(client, lag_id):
    return client.sai_thrift_remove_lag(lag_id)


def sai_thrift_create_bport_by_lag(client, lag_id):
    '''
    Exist for compatibility, no need to use this function
    '''
    return sai_thrift_create_bridge_port(client, lag_id)


def sai_thrift_remove_bport_by_lag(client, lag_bridge_port_id):
    '''
    Exist for compatibility, no need to use this function
    '''
    return client.sai_thrift_remove_bridge_port(lag_bridge_port_id)


def sai_thrift_create_lag_member(client, lag_id, port_id, egress_disable=False, ingress_disable=False):
    bport_id = sai_thrift_get_bridge_port_by_port(client, port_id)
    client.sai_thrift_remove_bridge_port(bport_id)

    lag_member_attr1_value = sai_thrift_attribute_value_t(oid=lag_id)
    lag_member_attr1 = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_LAG_ID,
                                              value=lag_member_attr1_value)

    lag_member_attr2_value = sai_thrift_attribute_value_t(oid=port_id)
    lag_member_attr2 = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_PORT_ID,
                                              value=lag_member_attr2_value)

    lag_member_attr3_value = sai_thrift_attribute_value_t(booldata=egress_disable)
    lag_member_attr3 = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE,
                                              value=lag_member_attr3_value)

    lag_member_attr4_value = sai_thrift_attribute_value_t(booldata=ingress_disable)
    lag_member_attr4 = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE,
                                              value=lag_member_attr4_value)

    lag_member_attr_list = [lag_member_attr1, lag_member_attr2, lag_member_attr3, lag_member_attr4]
    lag_member_id = client.sai_thrift_create_lag_member(lag_member_attr_list)

    if SAI_NULL_OBJECT_ID == lag_member_id:
        sai_thrift_create_bridge_port(client, port_id)
    return lag_member_id


def sai_thrift_remove_lag_member(client, lag_member_id):
    attrs = client.sai_thrift_get_lag_member_attribute(lag_member_id)
    port_id = SAI_NULL_OBJECT_ID
    for a in attrs.attr_list:
        if a.id == SAI_LAG_MEMBER_ATTR_PORT_ID:
            port_id = a.value.oid
            break

    status = client.sai_thrift_remove_lag_member(lag_member_id)
    if SAI_STATUS_SUCCESS == status:
        sai_thrift_create_bridge_port(client, port_id)
    return status


def sai_thrift_create_stp_entry(client, vlan_list=[0]):
    '''
    No need to create stp with any attribute actually
    For compatibility, there is no change in switch.py and server.cpp
    '''
    vlanlist=sai_thrift_vlan_list_t(vlan_count=len(vlan_list), vlan_list=vlan_list)
    stp_attr_value = sai_thrift_attribute_value_t(vlanlist=vlanlist)
    stp_attr = sai_thrift_attribute_t(id=SAI_STP_ATTR_VLAN_LIST, value=stp_attr_value)
    stp_attr_list = [stp_attr]
    stp_id = client.sai_thrift_create_stp_entry(stp_attr_list)
    return stp_id


def sai_thrift_create_stp_port(client, stp_oid, port_oid, state, is_lag=None):
    if is_lag == None:
        bport_oid = sai_thrift_get_bridge_port_by_port(client, port_oid)
    else:
        bport_oid = port_oid

    stp_port_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(oid=stp_oid)
    attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_STP,
                                           value=attribute_value)
    stp_port_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(oid=bport_oid)
    attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_BRIDGE_PORT,
                                           value=attribute_value)
    stp_port_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(s32=state)
    attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_STATE,
                                           value=attribute_value)
    stp_port_attr_list.append(attribute)

    stp_port_id = client.sai_thrift_create_stp_port(stp_port_attr_list)
    return stp_port_id


def sai_thrift_create_stp_ports(client, stp_oid_list, port_oid_list, state_list, count, mode):
    stp_port_attr_lists = []
    stp_port_cnt_list = []

    for a in range(0,count):
        attribute_value = sai_thrift_attribute_value_t(oid=stp_oid_list[a])
        attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_STP, value=attribute_value)
        stp_port_attr_lists.append(attribute)

        bport_oid = sai_thrift_get_bridge_port_by_port(client, port_oid_list[a])
        #assert (bport_oid != SAI_NULL_OBJECT_ID)
        attribute_value = sai_thrift_attribute_value_t(oid=bport_oid)
        attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_BRIDGE_PORT, value=attribute_value)
        stp_port_attr_lists.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(s32=state_list[a])
        attribute = sai_thrift_attribute_t(id=SAI_STP_PORT_ATTR_STATE, value=attribute_value)
        stp_port_attr_lists.append(attribute)

        stp_port_cnt_list.append(3)

    ret = client.sai_thrift_create_stp_ports(stp_port_attr_lists, stp_port_cnt_list, mode)
    return [ret.objlist.object_id_list, ret.statuslist.status_list]


def sai_thrift_remove_stp_ports(client, object_id_list, mode):
    ret = client.sai_thrift_remove_stp_ports(object_id_list, mode)
    return ret.status_list


def sai_thrift_create_hostif(client,
                             hif_type,
                             hif_obj_id,
                             hif_name):
    attr_list=[]

    atr_value=sai_thrift_attribute_value_t(s32=hif_type)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_ATTR_TYPE,
                               value=atr_value)
    attr_list.append(atr)

    atr_value=sai_thrift_attribute_value_t(oid=hif_obj_id)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_ATTR_OBJ_ID,
                               value=atr_value)
    attr_list.append(atr)

    atr_value=sai_thrift_attribute_value_t(chardata=hif_name)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_ATTR_NAME,
                               value=atr_value)
    attr_list.append(atr)

    return client.sai_thrift_create_hostif(attr_list)

def sai_thrift_create_hostif_trap(client,
                                  trap_type,
                                  packet_action,
                                  trap_priority=None,
                                  exclude_port_list=None,
                                  trap_group=None,
                                  trap_counter_oid=None):
    attr_list=[]

    atr_value=sai_thrift_attribute_value_t(s32=trap_type)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE,
                               value=atr_value)
    attr_list.append(atr)

    atr_value=sai_thrift_attribute_value_t(s32=packet_action)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION,
                               value=atr_value)
    attr_list.append(atr)

    if trap_priority != None:
        atr_value=sai_thrift_attribute_value_t(u32=trap_priority)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY,
                                   value=atr_value)
        attr_list.append(atr)

    if trap_priority != None:
        atr_value=sai_thrift_attribute_value_t(objlist=exclude_port_list)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST,
                                   value=atr_value)
        attr_list.append(atr)

    if trap_group != None:
        atr_value=sai_thrift_attribute_value_t(oid=trap_group)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP,
                                   value=atr_value)
        attr_list.append(atr)

    if trap_counter_oid != None:
        print "switch trap_counter_oid0x%lx" %trap_counter_oid
        atr_value=sai_thrift_attribute_value_t(oid=trap_counter_oid)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_COUNTER_ID,
                                   value=atr_value)
        attr_list.append(atr)

    trap_id = client.sai_thrift_create_hostif_trap(attr_list)
    return trap_id

def sai_thrift_remove_hostif_trap(client,
                                  trap_id):
    client.sai_thrift_remove_hostif_trap(trap_id)

def sai_thrift_set_hostif_trap_attribute(client,
                                         trap_type,
                                         packet_action,
                                         trap_priority=None,
                                         exclude_port_list=None,
                                         trap_group=None):
    attr_list=[]

    atr_value=sai_thrift_attribute_value_t(s32=trap_type)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE,
                               value=atr_value)
    attr_list.append(atr)

    atr_value=sai_thrift_attribute_value_t(s32=packet_action)
    atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION,
                               value=atr_value)
    attr_list.append(atr)

    if trap_priority != None:
        atr_value=sai_thrift_attribute_value_t(u32=trap_priority)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY,
                                   value=atr_value)
        attr_list.append(atr)

    if exclude_port_list != None:
        atr_value=sai_thrift_attribute_value_t(objlist=exclude_port_list)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST,
                                   value=atr_value)
        attr_list.append(atr)

    if trap_group != None:
        atr_value=sai_thrift_attribute_value_t(oid=trap_group)
        atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP,
                                   value=atr_value)
        attr_list.append(atr)

    client.sai_thrift_set_hostif_trap_attribute(attr_list)

def sai_thrift_create_hostif_trap_group(client, queue_id, policer_id=None):
    attr_list = []
    attribute_value = sai_thrift_attribute_value_t(u32=queue_id)
    attribute = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE, value=attribute_value)
    attr_list.append(attribute)

    if policer_id != None:
        policer_attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        policer_attr = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER, value=policer_attr_value)
        attr_list.append(policer_attr)

    trap_group = client.sai_thrift_create_hostif_trap_group(thrift_attr_list=attr_list)
    return trap_group

def sai_thrift_remove_hostif_trap_group(client,
                                        trap_group):
    client.sai_thrift_remove_hostif_trap_group(trap_group)

def sai_thrift_set_hostif_trap_group(client, trap_group_id, policer_id):
    policer_attr_value = sai_thrift_attribute_value_t(oid=policer_id)
    policer_attr = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER, value=policer_attr_value)
    status = client.sai_thrift_set_hostif_trap_group(trap_group_id, thrift_attr=policer_attr)
    return status

def sai_thrift_create_policer(client,
                              meter_type,
                              mode,
                              cir,
                              red_action):
    attr_list = []

    meter_attr_value = sai_thrift_attribute_value_t(s32=meter_type)
    meter_attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_METER_TYPE, value=meter_attr_value)

    mode_attr_value = sai_thrift_attribute_value_t(s32=mode)
    mode_attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_MODE, value=mode_attr_value)

    cir_attr_value = sai_thrift_attribute_value_t(u64=cir)
    cir_attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=cir_attr_value)

    red_action_attr_val = sai_thrift_attribute_value_t(s32=red_action)
    red_action_attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=red_action_attr_val)

    attr_list.append(meter_attr)
    attr_list.append(mode_attr)
    attr_list.append(cir_attr)
    attr_list.append(red_action_attr)
    policer_id = client.sai_thrift_create_policer(attr_list)

    return policer_id

def sai_thrift_create_acl_table(client,
                                table_stage,
                                table_bind_point_list,
                                addr_family,
                                mac_src, mac_dst,
                                ip_src, ip_dst,
                                in_ports, out_ports,
                                in_port, out_port,
                                svlan_id, svlan_pri, svlan_cfi,
                                cvlan_id, cvlan_pri, cvlan_cfi,
                                ip_type,
                                mpls_label0_label, mpls_label0_ttl, mpls_label0_exp, mpls_label0_bos,
                                mpls_label1_label, mpls_label1_ttl, mpls_label1_exp, mpls_label1_bos,
                                mpls_label2_label, mpls_label2_ttl, mpls_label2_exp, mpls_label2_bos,
                                mpls_label3_label, mpls_label3_ttl, mpls_label3_exp, mpls_label3_bos,
                                mpls_label4_label, mpls_label4_ttl, mpls_label4_exp, mpls_label4_bos,
                                ip_protocol,
                                src_l4_port, dst_l4_port,
                                ipv6_src=None, ipv6_dst=None,
                                ip_tos=None, 
                                ip_ecn=None,
                                ip_dscp=None,
                                ip_ttl=None,
                                acl_range_type_list=None,
                                user_define_filed_group0=None,
                                user_define_filed_group1=None,
                                user_define_filed_group2=None,
                                user_define_filed_group3=None,
                                user_define_filed_group4=None,
                                user_define_filed_group5=None,
                                user_define_filed_group6=None,
                                user_define_filed_group7=None,
                                user_define_filed_group8=None,
                                user_define_filed_group9=None,
                                user_define_filed_group10=None,
                                user_define_filed_group11=None,
                                user_define_filed_group12=None,
                                user_define_filed_group13=None,
                                user_define_filed_group14=None,
                                user_define_filed_group15=None,
                                ether_type=None,
                                metadata_port_user=None,
                                metadata_vlan_user=None,
                                router_interface=None,
                                gre_key=None,
                                icmp_type=None,
                                icmp_code=None):

    acl_attr_list = []
    
    if icmp_type != None:
        attribute_value = sai_thrift_attribute_value_t(s32=icmp_type)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)
        
    if icmp_code != None:
        attribute_value = sai_thrift_attribute_value_t(s32=icmp_code)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if table_stage != None:
        attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if table_bind_point_list != None:
        acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if mac_src != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if mac_dst != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_DST_MAC,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_src != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_SRC_IP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_dst != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_DST_IP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    
    if ipv6_src != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ipv6_dst != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6,
                                           value=attribute_value)
        acl_attr_list.append(attribute)
    
    
    if in_ports:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if out_ports:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if in_port != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IN_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if out_port != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if svlan_id != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if svlan_pri != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if svlan_cfi != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if cvlan_id != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if cvlan_pri != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if cvlan_cfi != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #ip type
    if ip_type != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 label
    if mpls_label0_label != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 ttl
    if mpls_label0_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 exp
    if mpls_label0_exp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 bos
    if mpls_label0_bos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 label
    if mpls_label1_label != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 ttl
    if mpls_label1_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 exp
    if mpls_label1_exp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 bos
    if mpls_label1_bos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 label
    if mpls_label2_label != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 ttl
    if mpls_label2_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 exp
    if mpls_label2_exp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 bos
    if mpls_label2_bos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 label
    if mpls_label3_label != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 ttl
    if mpls_label3_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 exp
    if mpls_label3_exp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 bos
    if mpls_label3_bos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 label
    if mpls_label4_label != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 ttl
    if mpls_label4_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 exp
    if mpls_label4_exp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 bos
    if mpls_label4_bos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_protocol != None:
        if ip_type == SAI_ACL_IP_TYPE_IPV4ANY:
            attribute_value = sai_thrift_attribute_value_t(booldata=1)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL,
                                               value=attribute_value)
        elif ip_type == SAI_ACL_IP_TYPE_IPV6ANY:
            attribute_value = sai_thrift_attribute_value_t(booldata=1)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER,
                                               value=attribute_value)
        acl_attr_list.append(attribute)

    if gre_key != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_GRE_KEY,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_tos != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_TOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_ecn != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ECN,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_dscp != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_DSCP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)
    
    
    if src_l4_port != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if dst_l4_port != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)


    if acl_range_type_list != None:
        acl_range_list = sai_thrift_s32_list_t(count=len(acl_range_type_list), s32list=acl_range_type_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_range_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    '''
    if acl_range_type_list != None:
        acl_range_list = sai_thrift_object_list_t(count=len(acl_range_type_list), object_id_list=acl_range_type_list)
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(objlist=acl_range_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE,
                                           value=attribute_value)
    '''

    if user_define_filed_group0 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN, value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group1 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+1), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group2 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+2), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group3 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+3), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group4 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+4), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group5 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+5), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group6 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+6), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group7 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+7), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group8 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+8), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group9 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+9), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group10 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+10), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group11 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+11), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group12 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+12), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group13 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+13), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group14 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+14), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group15 != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+15), value=attribute_value)
        acl_attr_list.append(attribute)

    if ether_type != None:
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

    if metadata_port_user != None:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!sai_thrift_create_acl_table:metadata_port_user"
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META, value=attribute_value)
        acl_attr_list.append(attribute)

    if metadata_vlan_user != None:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!sai_thrift_create_acl_table:metadata_vlan_user"
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META, value=attribute_value)
        acl_attr_list.append(attribute)

    if router_interface != None:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!sai_thrift_create_acl_table:router_interface"
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID, value=attribute_value)
        acl_attr_list.append(attribute)

    acl_table_id = client.sai_thrift_create_acl_table(acl_attr_list)
    return acl_table_id

def sai_thrift_create_acl_entry(client,
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
                                mpls_label0_label, mpls_label0_ttl, mpls_label0_exp, mpls_label0_bos,
                                mpls_label1_label, mpls_label1_ttl, mpls_label1_exp, mpls_label1_bos,
                                mpls_label2_label, mpls_label2_ttl, mpls_label2_exp, mpls_label2_bos,
                                mpls_label3_label, mpls_label3_ttl, mpls_label3_exp, mpls_label3_bos,
                                mpls_label4_label, mpls_label4_ttl, mpls_label4_exp, mpls_label4_bos,
                                ip_src, ip_src_mask,
                                ip_dst, ip_dst_mask,
                                ip_protocol,
                                ip_tos, ip_ecn,
                                ip_dscp, ip_ttl,
                                in_port_list, out_port_list,
                                in_port, out_port,
                                src_l4_port, dst_l4_port,
                                ingress_mirror, egress_mirror,
                                new_svlan, new_scos,
                                new_cvlan, new_ccos,
                                deny_learn,  
                                ipv6_src=None, ipv6_src_mask=None,  
                                ipv6_dst=None, ipv6_dst_mask=None,  
                                ingress_samplepacket=None,
                                acl_range_id_list=None,
                                redirect=None,
                                user_define_filed_group0_data=None,
                                user_define_filed_group0_mask=None,
                                user_define_filed_group1_data=None,
                                user_define_filed_group1_mask=None,
                                user_define_filed_group2_data=None,
                                user_define_filed_group2_mask=None,
                                user_define_filed_group3_data=None,
                                user_define_filed_group3_mask=None,
                                user_define_filed_group4_data=None,
                                user_define_filed_group4_mask=None,
                                user_define_filed_group5_data=None,
                                user_define_filed_group5_mask=None,
                                user_define_filed_group6_data=None,
                                user_define_filed_group6_mask=None,
                                user_define_filed_group7_data=None,
                                user_define_filed_group7_mask=None,
                                user_define_filed_group8_data=None,
                                user_define_filed_group8_mask=None,
                                user_define_filed_group9_data=None,
                                user_define_filed_group9_mask=None,
                                user_define_filed_group10_data=None,
                                user_define_filed_group10_mask=None,
                                user_define_filed_group11_data=None,
                                user_define_filed_group11_mask=None,
                                user_define_filed_group12_data=None,
                                user_define_filed_group12_mask=None,
                                user_define_filed_group13_data=None,
                                user_define_filed_group13_mask=None,
                                user_define_filed_group14_data=None,
                                user_define_filed_group14_mask=None,
                                user_define_filed_group15_data=None,
                                user_define_filed_group15_mask=None,
                                ether_type=None,
                                metadata_port_user=None,
                                metadata_vlan_user=None,
                                color=None,
                                gre_key=None):
    acl_attr_list = []

    #ACL table OID
    attribute_value = sai_thrift_attribute_value_t(oid=acl_table_id)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    #Priority
    if entry_priority != None:
        attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    # Admin State
    attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE,
                                           value=attribute_value)
    acl_attr_list.append(attribute)
    #MAC source
    if mac_src != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(mac=mac_src), mask = sai_thrift_acl_mask_t(mac=mac_src_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #MAC destination
    if mac_dst != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(mac=mac_dst), mask = sai_thrift_acl_mask_t(mac=mac_dst_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #svlan id
    if svlan_id != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u16=svlan_id), mask =sai_thrift_acl_mask_t(u16=U16MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #svlan pri
    if svlan_pri != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=svlan_pri), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #svlan cfi
    if svlan_cfi != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=svlan_cfi), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #cvlan id
    if cvlan_id != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u16=cvlan_id), mask =sai_thrift_acl_mask_t(u16=U16MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #cvlan pri
    if cvlan_pri != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=cvlan_pri), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #cvlan cfi
    if cvlan_cfi != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=cvlan_cfi), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #ip type
    if ip_type != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask =sai_thrift_acl_mask_t(0)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 label
    if mpls_label0_label != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=mpls_label0_label), mask =sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 ttl
    if mpls_label0_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label0_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 exp
    if mpls_label0_exp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label0_exp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label0 bos
    if mpls_label0_bos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(booldata=mpls_label0_bos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 label
    if mpls_label1_label != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=mpls_label1_label), mask =sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 ttl
    if mpls_label1_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label1_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 exp
    if mpls_label1_exp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label1_exp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label1 bos
    if mpls_label1_bos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(booldata=mpls_label1_bos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 label
    if mpls_label2_label != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=mpls_label2_label), mask =sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 ttl
    if mpls_label2_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label2_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 exp
    if mpls_label2_exp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label2_exp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label2 bos
    if mpls_label2_bos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(booldata=mpls_label2_bos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 label
    if mpls_label3_label != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=mpls_label3_label), mask =sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 ttl
    if mpls_label3_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label3_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 exp
    if mpls_label3_exp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label3_exp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label3 bos
    if mpls_label3_bos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(booldata=mpls_label3_bos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 label
    if mpls_label4_label != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=mpls_label4_label), mask =sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 ttl
    if mpls_label4_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label4_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 exp
    if mpls_label4_exp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=mpls_label4_exp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #mpls label4 bos
    if mpls_label4_bos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(booldata=mpls_label4_bos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_src != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(ip4=ip_src), mask =sai_thrift_acl_mask_t(ip4=ip_src_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP, value=attribute_value)
        acl_attr_list.append(attribute)

    if ip_dst != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(ip4=ip_dst), mask =sai_thrift_acl_mask_t(ip4=ip_dst_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_DST_IP, value=attribute_value)
        acl_attr_list.append(attribute)

    
    if ipv6_src != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(ip6=ipv6_src), mask =sai_thrift_acl_mask_t(ip6=ipv6_src_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6, value=attribute_value)
        acl_attr_list.append(attribute)

    if ipv6_dst != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(ip6=ipv6_dst), mask =sai_thrift_acl_mask_t(ip6=ipv6_dst_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6, value=attribute_value)
        acl_attr_list.append(attribute)
    
    
    #Ip tos
    if ip_tos != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_tos), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_TOS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ip ecn
    if ip_ecn != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_ecn), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ECN,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ip dscp
    if ip_dscp != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_dscp), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_DSCP,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ip ttl
    if ip_ttl != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_ttl), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_TTL,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Input ports
    if in_port_list:
        acl_port_list = sai_thrift_object_list_t(count=len(in_port_list), object_id_list=in_port_list)
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(objlist=acl_port_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Output ports
    if out_port_list:
        acl_port_list = sai_thrift_object_list_t(count=len(out_port_list), object_id_list=out_port_list)
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(objlist=acl_port_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Input port
    if in_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(oid=in_port)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Output port
    if out_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(oid=out_port)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ip protocol
    if ip_protocol != None:
        if ip_type == SAI_ACL_IP_TYPE_IPV4ANY:
            attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_protocol), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL,
                                               value=attribute_value)
        elif ip_type == SAI_ACL_IP_TYPE_IPV6ANY:
            attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ip_protocol), mask =sai_thrift_acl_mask_t(u8=U8MASKFULL)))
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER,
                                               value=attribute_value)
        acl_attr_list.append(attribute)

    #GRE Key
    if gre_key != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u32=gre_key),
                                                                                            mask = sai_thrift_acl_mask_t(u32=U32MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_GRE_KEY,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #L4 Source port
    if src_l4_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u16=src_l4_port),
                                                                                            mask = sai_thrift_acl_mask_t(u16=U16MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #L4 Destination port
    if dst_l4_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u16=dst_l4_port),
                                                                                            mask = sai_thrift_acl_mask_t(u16=U16MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Range id list
    if acl_range_id_list != None:
        acl_range_list = sai_thrift_object_list_t(count=len(acl_range_id_list), object_id_list=acl_range_id_list)
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(objlist=acl_range_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group0_data != None:
        user_define_filed_group0_data_list = sai_thrift_u8_list_t(count=len(user_define_filed_group0_data), u8list=user_define_filed_group0_data)
        user_define_filed_group0_mask_list = sai_thrift_u8_list_t(count=len(user_define_filed_group0_mask), u8list=user_define_filed_group0_mask)

        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group0_data_list),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group0_mask_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN, value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group1_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group1_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group1_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+1), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group2_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group2_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group2_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+2), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group3_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group3_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group3_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+3), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group4_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group4_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group4_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+4), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group5_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group5_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group5_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+5), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group6_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group6_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group6_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+6), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group7_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group7_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group7_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+7), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group8_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group8_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group8_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+8), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group9_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group9_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group9_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+9), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group10_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group10_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group10_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+10), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group11_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group11_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group11_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+11), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group12_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group12_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group12_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+12), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group13_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group13_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group13_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+13), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group14_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group14_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group14_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+14), value=attribute_value)
        acl_attr_list.append(attribute)

    if user_define_filed_group15_data != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group15_data),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group15_mask)))
        attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+15), value=attribute_value)
        acl_attr_list.append(attribute)

    if ether_type != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u16=ether_type),
                                                                                            mask = sai_thrift_acl_mask_t(u16=U16MASKFULL)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if metadata_port_user != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u32=metadata_port_user),
                                                                                            mask = sai_thrift_acl_mask_t(u32=metadata_port_user)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META, value=attribute_value)
        acl_attr_list.append(attribute)

    if metadata_vlan_user != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u32=metadata_vlan_user),
                                                                                            mask = sai_thrift_acl_mask_t(u32=metadata_vlan_user)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META, value=attribute_value)
        acl_attr_list.append(attribute)

    #Packet action
    if action != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ingress mirroring
    if ingress_mirror:
        igs_mirror_list = sai_thrift_object_list_t(count=len(ingress_mirror), object_id_list=ingress_mirror)
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(enable = True,
                                                                                              parameter = sai_thrift_acl_parameter_t(objlist=igs_mirror_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Egress mirroring
    if egress_mirror:
        egs_mirror_list = sai_thrift_object_list_t(count=len(egress_mirror), object_id_list=egress_mirror)
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(objlist=egs_mirror_list),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #new svlan
    if new_svlan != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u16=new_svlan),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #new scos
    if new_scos != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u8=new_scos),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #new cvlan
    if new_cvlan != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u16=new_cvlan),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #new ccos
    if new_ccos != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u8=new_ccos),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #deny learning
    if deny_learn != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    #Ingress samplepacket
    if ingress_samplepacket != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(oid=ingress_samplepacket), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE, value=attribute_value)
        acl_attr_list.append(attribute)

    if redirect != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(oid=redirect), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT, value=attribute_value)
        acl_attr_list.append(attribute)

    if color != None:
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=color), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR, value=attribute_value)
        acl_attr_list.append(attribute)

    acl_entry_id = client.sai_thrift_create_acl_entry(acl_attr_list)
    return acl_entry_id

def sai_thrift_create_acl_table_group(client,
                                      group_stage,
                                      group_bind_point_list,
                                      group_type):
    acl_attr_list = []

    if group_stage != None:
        attribute_value = sai_thrift_attribute_value_t(s32=group_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if group_bind_point_list != None:
        acl_group_bind_point_list = sai_thrift_s32_list_t(count=len(group_bind_point_list), s32list=group_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_group_bind_point_list)

        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if group_type != None:
        attribute_value = sai_thrift_attribute_value_t(s32=group_type)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_ATTR_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    acl_table_group_id = client.sai_thrift_create_acl_table_group(acl_attr_list)
    return acl_table_group_id

def sai_thrift_create_acl_table_group_member(client,
                                             acl_table_group_id,
                                             acl_table_id,
                                             group_member_priority):
    acl_attr_list = []

    if acl_table_group_id != None:
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if acl_table_id != None:
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    if group_member_priority != None:
        attribute_value = sai_thrift_attribute_value_t(u32=group_member_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

    acl_table_group_member_id = client.sai_thrift_create_acl_table_group_member(acl_attr_list)
    return acl_table_group_member_id

def sai_thrift_create_acl_range(client,
                                range_type,
                                stage,
                                range_min,
                                range_max):
    acl_attr_list = []

    attribute_value = sai_thrift_attribute_value_t(s32=range_type)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_RANGE_ATTR_TYPE,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(s32=stage)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_RANGE_ATTR_STAGE,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(u32range=sai_thrift_u32_range_t(min=range_min, max=range_max))
    attribute = sai_thrift_attribute_t(id=SAI_ACL_RANGE_ATTR_LIMIT,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    acl_range_type_id = client.sai_thrift_create_acl_range(acl_attr_list)
    return acl_range_type_id

def sai_thrift_create_acl_counter(client,
                                table_id,
                                pkt_cnt_en=True,
                                byte_cnt_en=True):
    acl_attr_list = []

    attribute_value = sai_thrift_attribute_value_t(oid=table_id)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_COUNTER_ATTR_TABLE_ID,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(booldata=pkt_cnt_en)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT,
                                       value=attribute_value)
    acl_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(booldata=byte_cnt_en)
    attribute = sai_thrift_attribute_t(id=SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT,
                                       value=attribute_value)
    acl_attr_list.append(attribute)
    
    acl_counter_oid = client.sai_thrift_create_acl_counter(acl_attr_list)
    return acl_counter_oid


def sai_thrift_create_hash(client, field_list, udf_group_list):
    hash_attr_list = []

    #Hash field list
    if field_list:
        hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
        attribute1_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
        attribute1 = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attribute1_value)
        hash_attr_list.append(attribute1)

    #UDF group list
    if udf_group_list:
        hash_udf_group_list = sai_thrift_object_list_t(count=len(udf_group_list), object_id_list=udf_group_list)
        attribute2_value = sai_thrift_attribute_value_t(objlist=hash_udf_group_list)
        attribute2 = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
                                            value=attribute2_value)
        hash_attr_list.append(attribute2)

    hash_id = client.sai_thrift_create_hash(hash_attr_list)
    return hash_id

def sai_thrift_create_udf_group(client, group_type, group_length):
    udf_group_attr_list = []

    #group_type
    attribute1_value = sai_thrift_attribute_value_t(s32=group_type)
    attribute1 = sai_thrift_attribute_t(id=SAI_UDF_GROUP_ATTR_TYPE,
                                        value=attribute1_value)
    udf_group_attr_list.append(attribute1)

    #group_length
    attribute2_value = sai_thrift_attribute_value_t(u16=group_length)
    attribute2 = sai_thrift_attribute_t(id=SAI_UDF_GROUP_ATTR_LENGTH,
                                        value=attribute2_value)
    udf_group_attr_list.append(attribute2)

    udf_group_id = client.sai_thrift_create_udf_group(udf_group_attr_list)
    return udf_group_id

def sai_thrift_create_udf_match(client,
                               l2_type,
                               l2_type_mask,
                               l3_type,
                               l3_type_mask,
                               gre_type,
                               gre_type_mask,
                               l4_src_port,
                               l4_src_port_mask,
                               l4_dst_port,
                               l4_dst_port_mask,
                               mpls_label_num,
                               priority):
    udf_match_attr_list = []

    #l2_type
    if l2_type != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(data = sai_thrift_acl_data_t(u16=l2_type),
                                                                                            mask = sai_thrift_acl_mask_t(u16=l2_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_L2_TYPE,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #l3_type
    if l3_type != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(data = sai_thrift_acl_data_t(u8=l3_type),
                                                                                            mask = sai_thrift_acl_mask_t(u8=l3_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_L3_TYPE,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #gre_type
    if gre_type != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(data = sai_thrift_acl_data_t(u16=gre_type),
                                                                                            mask = sai_thrift_acl_mask_t(u16=gre_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_GRE_TYPE,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #l4_src_port
    if l4_src_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(data = sai_thrift_acl_data_t(u16=l4_src_port),
                                                                                            mask = sai_thrift_acl_mask_t(u16=l4_src_port_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #l4_dst_port
    if l4_dst_port != None:
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(data = sai_thrift_acl_data_t(u16=l4_dst_port),
                                                                                            mask = sai_thrift_acl_mask_t(u16=l4_dst_port_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #mpls_label_num
    if mpls_label_num != None:
        attribute_value = sai_thrift_attribute_value_t(u8=mpls_label_num)
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    #priority
    if priority != None:
        attribute_value = sai_thrift_attribute_value_t(u8=priority)
        attribute = sai_thrift_attribute_t(id=SAI_UDF_MATCH_ATTR_PRIORITY,
                                           value=attribute_value)
        udf_match_attr_list.append(attribute)

    udf_match_id = client.sai_thrift_create_udf_match(udf_match_attr_list)

    return udf_match_id

def sai_thrift_create_udf(client, match_id, group_id, base, offset, hash_mask_list):
    udf_attr_list = []

    #match_id
    attribute1_value = sai_thrift_attribute_value_t(oid=match_id)
    attribute1 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_MATCH_ID,
                                        value=attribute1_value)
    udf_attr_list.append(attribute1)

    #group_id
    attribute2_value = sai_thrift_attribute_value_t(oid=group_id)
    attribute2 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_GROUP_ID,
                                        value=attribute2_value)
    udf_attr_list.append(attribute2)

    #base
    attribute3_value = sai_thrift_attribute_value_t(s32=base)
    attribute3 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_BASE,
                                        value=attribute3_value)
    udf_attr_list.append(attribute3)

    #offset
    attribute4_value = sai_thrift_attribute_value_t(u16=offset)
    attribute4 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_OFFSET,
                                        value=attribute4_value)
    udf_attr_list.append(attribute4)

    #Hash mask list
    if hash_mask_list:
        hash_mask_list_tmp = sai_thrift_u8_list_t(count=len(hash_mask_list), u8list=hash_mask_list)
        attribute5_value = sai_thrift_attribute_value_t(u8list=hash_mask_list_tmp)
        attribute5 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_HASH_MASK,
                                            value=attribute5_value)
        udf_attr_list.append(attribute5)

    udf_id = client.sai_thrift_create_udf(udf_attr_list)
    return udf_id

def sai_thrift_create_mirror_session(client, mirror_type, port, port_list, port_list_valid,
                                     vlan, vlan_priority, vlan_tpid, vlan_header_valid,
                                     src_mac, dst_mac,
                                     src_ip, dst_ip,
                                     encap_type, iphdr_version, ttl, tos, gre_type):
    mirror_attr_list = []

    #Mirror type
    attribute1_value = sai_thrift_attribute_value_t(s32=mirror_type)
    attribute1 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TYPE,
                                        value=attribute1_value)
    mirror_attr_list.append(attribute1)

    #Monitor port
    attribute2_value = sai_thrift_attribute_value_t(oid=port)
    attribute2 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT,
                                        value=attribute2_value)
    mirror_attr_list.append(attribute2)

    attribute21_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=len(port_list),object_id_list=port_list))
    attribute21 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST,
                                        value=attribute21_value)
    mirror_attr_list.append(attribute21)

    attribute22_value = sai_thrift_attribute_value_t(booldata=port_list_valid)
    attribute22 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID,
                                        value=attribute22_value)
    mirror_attr_list.append(attribute22)

    if mirror_type == SAI_MIRROR_SESSION_TYPE_REMOTE:
        #vlan
        attribute3_value = sai_thrift_attribute_value_t(u16=vlan)
        attribute3 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_ID,
                                            value=attribute3_value)
        mirror_attr_list.append(attribute3)

        #vlan tpid
        if vlan_tpid is not None:
            attribute4_value = sai_thrift_attribute_value_t(u32=vlan_tpid)
            attribute4 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_TPID,
                                               value=attribute4_value)
            mirror_attr_list.append(attribute4)

        #vlan priority
        attribute5_value = sai_thrift_attribute_value_t(u8=vlan_priority)
        attribute5 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_PRI,
                                            value=attribute5_value)
        mirror_attr_list.append(attribute5)
    elif mirror_type == SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE:
        #encap type
        attribute3_value = sai_thrift_attribute_value_t(s32=encap_type)
        attribute3 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE,
                                            value=attribute3_value)
        mirror_attr_list.append(attribute3)

        #ip header version
        attribute4_value = sai_thrift_attribute_value_t(u8=iphdr_version)
        attribute4 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION,
                                            value=attribute4_value)
        mirror_attr_list.append(attribute4)

        assert((iphdr_version == 4) or (iphdr_version == 6))
        if iphdr_version == 4:
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            
            #source ip
            addr = sai_thrift_ip_t(ip4=src_ip)
            src_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute5_value = sai_thrift_attribute_value_t(ipaddr=src_ip_addr)
            attribute5 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS,
                                                value=attribute5_value)
            mirror_attr_list.append(attribute5)
            
            #dst ip
            addr = sai_thrift_ip_t(ip4=dst_ip)
            dst_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute6_value = sai_thrift_attribute_value_t(ipaddr=dst_ip_addr)
            attribute6 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS,
                                                value=attribute6_value)
        elif iphdr_version == 6:
            addr_family = SAI_IP_ADDR_FAMILY_IPV6

            #source ip
            addr = sai_thrift_ip_t(ip6=src_ip)
            src_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute5_value = sai_thrift_attribute_value_t(ipaddr=src_ip_addr)
            attribute5 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS,
                                                value=attribute5_value)
            mirror_attr_list.append(attribute5)

            #dst ip
            addr = sai_thrift_ip_t(ip6=dst_ip)
            dst_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute6_value = sai_thrift_attribute_value_t(ipaddr=dst_ip_addr)
            attribute6 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS,
                                                value=attribute6_value)
        mirror_attr_list.append(attribute6)

        #source mac
        attribute7_value = sai_thrift_attribute_value_t(mac=src_mac)
        attribute7 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS,
                                            value=attribute7_value)
        mirror_attr_list.append(attribute7)

        #dst mac
        attribute8_value = sai_thrift_attribute_value_t(mac=dst_mac)
        attribute8 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS,
                                            value=attribute8_value)
        mirror_attr_list.append(attribute8)

        attribute9_value = sai_thrift_attribute_value_t(u16=gre_type)
        attribute9 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE,value=attribute9_value)
        mirror_attr_list.append(attribute9)

        attribute10_value = sai_thrift_attribute_value_t(u8=ttl)
        attribute10 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TTL,value=attribute10_value)
        mirror_attr_list.append(attribute10)

        if vlan_tpid is not None:
            attribute11_value = sai_thrift_attribute_value_t(u32=vlan_tpid)
            attribute11 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_TPID,
                                                value=attribute11_value)
            mirror_attr_list.append(attribute11)

        #vlan
        if vlan is not None:
            attribute12_value = sai_thrift_attribute_value_t(u16=vlan)
            attribute12 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_ID,
                                                value=attribute12_value)
            mirror_attr_list.append(attribute12)

        #tos
        attribute13_value = sai_thrift_attribute_value_t(u8=tos)
        attribute13 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TOS,
                                            value=attribute13_value)
        mirror_attr_list.append(attribute13)

        if vlan_header_valid is True:
            attribute14_value = sai_thrift_attribute_value_t(booldata=vlan_header_valid)
            attribute14 = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID,
                                                value=attribute14_value)
            mirror_attr_list.append(attribute14)

    mirror_id = client.sai_thrift_create_mirror_session(mirror_attr_list)
    return mirror_id

def sai_thrift_create_inseg_entry(client, label, pop_nums, trip_prioroty, nhop, packet_action, tunnel_id=None,frr_nhp_grp=None,frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = False,pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM,counter_id=None, pop_qos_mode = None, psc_type = None, policer_id = None, service_id = None):
    mpls_attr_list = []

    mpls = sai_thrift_inseg_entry_t(label)

    #pop_nums
    if pop_nums != None:
        mpls_attribute1_value = sai_thrift_attribute_value_t(u8=pop_nums)
        mpls_attribute1 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NUM_OF_POP,
                                            value=mpls_attribute1_value)
        mpls_attr_list.append(mpls_attribute1)

    #trip_prioroty
    if trip_prioroty != None:
        mpls_attribute2_value = sai_thrift_attribute_value_t(u8=trip_prioroty)
        mpls_attribute2 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY,
                                            value=mpls_attribute2_value)
        mpls_attr_list.append(mpls_attribute2)

    #nhop
    if nhop != None:
        mpls_attribute3_value = sai_thrift_attribute_value_t(oid=nhop)
        mpls_attribute3 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID,
                                            value=mpls_attribute3_value)
        mpls_attr_list.append(mpls_attribute3)

    #packet_action
    if packet_action != None:
        mpls_action_value = sai_thrift_attribute_value_t(s32=packet_action)
        mpls_action_attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PACKET_ACTION,
                                                        value=mpls_action_value)
        mpls_attr_list.append(mpls_action_attr)

    if tunnel_id != None:
        mpls_attribute4_value = sai_thrift_attribute_value_t(oid=tunnel_id)
        mpls_attribute4 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID,
                                                        value=mpls_attribute4_value)
        mpls_attr_list.append(mpls_attribute4)
        
    if None != frr_nhp_grp:
        mpls_attribute5_value = sai_thrift_attribute_value_t(oid=frr_nhp_grp)
        mpls_attribute5 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP,
                                                        value=mpls_attribute5_value)
        mpls_attr_list.append(mpls_attribute5)
        
        u8 = ctypes.c_uint8(frr_cfg_role)        
        mpls_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
        mpls_attribute6 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE,
                                                        value=mpls_attribute6_value)
        mpls_attr_list.append(mpls_attribute6)
        
        mpls_attribute7_value = sai_thrift_attribute_value_t(booldata=frr_inactive_discard)
        mpls_attribute7 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD,
                                                value=mpls_attribute7_value)
        mpls_attr_list.append(mpls_attribute7)
        
    mpls_attribute8_value = sai_thrift_attribute_value_t(s32=pop_ttl_mode)
    mpls_attribute8 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE,
                                                        value=mpls_attribute8_value)
    mpls_attr_list.append(mpls_attribute8)        

    if counter_id != None:
        mpls_attribute9_value = sai_thrift_attribute_value_t(oid=counter_id)
        mpls_attribute9 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID,
                                                 value=mpls_attribute9_value)
        mpls_attr_list.append(mpls_attribute9)

    if pop_qos_mode != None:
        mpls_attribute10_value = sai_thrift_attribute_value_t(s32=pop_qos_mode)
        mpls_attribute10 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE,
                                                 value=mpls_attribute10_value)
        mpls_attr_list.append(mpls_attribute10)
    
    if psc_type != None:
        mpls_attribute11_value = sai_thrift_attribute_value_t(s32=psc_type)
        mpls_attribute11 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PSC_TYPE,
                                                 value=mpls_attribute11_value)
        mpls_attr_list.append(mpls_attribute11)    

    if policer_id != None:
        mpls_attribute12_value = sai_thrift_attribute_value_t(oid=policer_id)
        mpls_attribute12 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_POLICER_ID,
                                                 value=mpls_attribute12_value)
        mpls_attr_list.append(mpls_attribute12)    

    if service_id != None:
        mpls_attribute13_value = sai_thrift_attribute_value_t(u16=service_id)
        mpls_attribute13 = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_SERVICE_ID,
                                                 value=mpls_attribute13_value)
        mpls_attr_list.append(mpls_attribute13)    
        
    return client.sai_thrift_create_inseg_entry(thrift_inseg_entry=mpls, thrift_attr_list=mpls_attr_list)

def sai_thrift_create_scheduler_profile(client, max_rate, algorithm=0):
    scheduler_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(u64=max_rate)
    attribute = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE ,
                                       value=attribute_value)
    scheduler_attr_list.append(attribute)
    attribute_value = sai_thrift_attribute_value_t(s32=algorithm)
    attribute = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_ALGORITHM ,
                                       value=attribute_value)
    scheduler_attr_list.append(attribute)
    scheduler_profile_id = client.sai_thrift_create_scheduler_profile(scheduler_attr_list)
    return scheduler_profile_id

def sai_thrift_create_buffer_profile(client, pool_id, size, threshold, xoff_th, xon_th):
    buffer_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(oid=pool_id)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_POOL_ID ,
                                           value=attribute_value)
    buffer_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(u32=size)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_BUFFER_SIZE ,
                                           value=attribute_value)
    buffer_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(s8=threshold)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH ,
                                           value=attribute_value)
    buffer_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(u64=xoff_th)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH ,
                                           value=attribute_value)
    buffer_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(u64=xon_th)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH ,
                                           value=attribute_value)
    buffer_attr_list.append(attribute)

    buffer_profile_id = client.sai_thrift_create_buffer_profile(buffer_attr_list)
    return buffer_profile_id

def sai_thrift_create_pool_profile(client, pool_type, size, threshold_mode):
    pool_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(s32=pool_type)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_POOL_ATTR_TYPE ,
                                           value=attribute_value)
    pool_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(u32=size)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_POOL_ATTR_SIZE ,
                                           value=attribute_value)
    pool_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(s32=threshold_mode)
    attribute = sai_thrift_attribute_t(id=SAI_BUFFER_POOL_ATTR_TH_MODE ,
                                           value=attribute_value)
    pool_attr_list.append(attribute)
    pool_id = client.sai_thrift_create_pool_profile(pool_attr_list)
    return pool_id

def sai_thrift_clear_all_counters(client):
    for port in sai_port_list:
        queue_list=[]
        client.sai_thrift_clear_port_all_stats(port)
        port_attr_list = client.sai_thrift_get_port_attribute(port)
        attr_list = port_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for queue_id in attribute.value.objlist.object_id_list:
                    queue_list.append(queue_id)

        cnt_ids=[]
        cnt_ids.append(SAI_QUEUE_STAT_PACKETS)
        for queue in queue_list:
            client.sai_thrift_clear_queue_stats(queue,cnt_ids,len(cnt_ids))

def sai_thrift_read_port_counters(client,port):
    port_cnt_ids=[]
    port_cnt_ids.append(SAI_PORT_STAT_IF_OUT_DISCARDS)
    port_cnt_ids.append(SAI_PORT_STAT_ETHER_STATS_DROP_EVENTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_0_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_1_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_2_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_3_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_4_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_5_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_6_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_PFC_7_TX_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_IF_OUT_OCTETS)
    port_cnt_ids.append(SAI_PORT_STAT_IF_OUT_UCAST_PKTS)
    port_cnt_ids.append(SAI_PORT_STAT_IF_IN_UCAST_PKTS)
    counters_results=[]
    counters_results = client.sai_thrift_get_port_stats(port,port_cnt_ids,len(port_cnt_ids))
    queue_list=[]
    port_attr_list = client.sai_thrift_get_port_attribute(port)
    attr_list = port_attr_list.attr_list
    for attribute in attr_list:
        if attribute.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
            for queue_id in attribute.value.objlist.object_id_list:
                queue_list.append(queue_id)
    cnt_ids=[]
    thrift_results=[]
    queue_counters_results=[]
    cnt_ids.append(SAI_QUEUE_STAT_PACKETS)
    queue1=0
    for queue in queue_list:
        if queue1 <= 7:
            thrift_results=client.sai_thrift_get_queue_stats(queue,cnt_ids,len(cnt_ids))
            queue_counters_results.append(thrift_results[0])
            queue1+=1
    return (counters_results, queue_counters_results)

def sai_thrift_create_vlan(client, vlan_id, stats_enable = 1):

    vlan_attr_list = []
    
    attribute_value = sai_thrift_attribute_value_t(u16=vlan_id)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_VLAN_ID, value=attribute_value)
    vlan_attr_list.append(attribute)
    
    attribute_value = sai_thrift_attribute_value_t(booldata=stats_enable)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attribute_value)
    vlan_attr_list.append(attribute)

    vlan_oid = client.sai_thrift_create_vlan(vlan_attr_list)
    
    return vlan_oid

def sai_thrift_create_vlan_with_stats_disable(client, vlan_id):
    vlan_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(u16=vlan_id)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_VLAN_ID, value=attribute_value)
    vlan_attr_list.append(attribute)
    attribute_value = sai_thrift_attribute_value_t(booldata=0)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attribute_value)
    vlan_attr_list.append(attribute)
    vlan_oid = client.sai_thrift_create_vlan(vlan_attr_list)
    return vlan_oid


def sai_thrift_create_vlan_member(client, vlan_oid, port_oid, tagging_mode=None, is_lag=None):
    if is_lag == None:
        bport_oid = sai_thrift_get_bridge_port_by_port(client, port_oid)
        assert(bport_oid != SAI_NULL_OBJECT_ID)
    else:
        bport_oid = port_oid

    vlan_member_attr_list = []

    attribute_value = sai_thrift_attribute_value_t(oid=vlan_oid)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_ID, value=attribute_value)
    vlan_member_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(oid=bport_oid)
    attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, value=attribute_value)
    vlan_member_attr_list.append(attribute)

    if tagging_mode is not None:
        attribute_value = sai_thrift_attribute_value_t(s32=tagging_mode)
        attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, value=attribute_value)
        vlan_member_attr_list.append(attribute)

    vlan_member_id = client.sai_thrift_create_vlan_member(vlan_member_attr_list)
    return vlan_member_id


def sai_thrift_create_vlan_members(client, vlan_oid_list, port_oid_list, tagging_mode_list, count, mode):

    vlan_member_attr_lists = []
    vlan_member_cnt_list = []

    for a in range(0,count):
        attribute_value = sai_thrift_attribute_value_t(oid=vlan_oid_list[a])
        attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_ID, value=attribute_value)
        vlan_member_attr_lists.append(attribute)

        bport_oid = sai_thrift_get_bridge_port_by_port(client, port_oid_list[a])
        #assert (bport_oid != SAI_NULL_OBJECT_ID)
        attribute_value = sai_thrift_attribute_value_t(oid=bport_oid)
        attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, value=attribute_value)
        vlan_member_attr_lists.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(s32=tagging_mode_list[a])
        attribute = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, value=attribute_value)
        vlan_member_attr_lists.append(attribute)

        vlan_member_cnt_list.append(3)

    ret = client.sai_thrift_create_vlan_members(vlan_member_attr_lists, vlan_member_cnt_list, mode)
    return [ret.objlist.object_id_list, ret.statuslist.status_list]

def sai_thrift_remove_vlan_members(client, object_id_list, mode):

    ret = client.sai_thrift_remove_vlan_members(object_id_list, mode)
    return ret.status_list

def sai_thrift_vlan_remove_all_ports(client, vlan_oid):
        vlan_members_list = []

        vlan_attr_list = client.sai_thrift_get_vlan_attribute(vlan_oid)
        attr_list = vlan_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_VLAN_ATTR_MEMBER_LIST:
                for vlan_member in attribute.value.objlist.object_id_list:
                    vlan_members_list.append(vlan_member)

        for vlan_member in vlan_members_list:
            client.sai_thrift_remove_vlan_member(vlan_member)

def sai_thrift_vlan_remove_ports(client, vlan_oid, ports):
    vlan_members_list = []

    vlan_attr_list = client.sai_thrift_get_vlan_attribute(vlan_oid)
    attr_list = vlan_attr_list.attr_list
    for attribute in attr_list:
        if attribute.id == SAI_VLAN_ATTR_MEMBER_LIST:
            for vlan_member in attribute.value.objlist.object_id_list:
                attrs = client.sai_thrift_get_vlan_member_attribute(vlan_member)
                for a in attrs.attr_list:
                    if a.id == SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID:
                        port = sai_thrift_get_port_by_bridge_port(client, a.value.oid)
                        if port in ports:
                            vlan_members_list.append(vlan_member)

    for vlan_member in vlan_members_list:
        client.sai_thrift_remove_vlan_member(vlan_member)


def sai_thrift_set_port_shaper(client, port_id, max_rate):
    sched_prof_id=sai_thrift_create_scheduler_profile(client, max_rate)
    attr_value = sai_thrift_attribute_value_t(oid=sched_prof_id)
    attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
    client.sai_thrift_set_port_attribute(port_id,attr)


def sai_thrift_create_l2mc_group_member(client, grp_id, port_id, is_lag=None):
    if is_lag == None:
        bport_oid = sai_thrift_get_bridge_port_by_port(client, port_id)
        #assert(bport_oid != SAI_NULL_OBJECT_ID)
    else:
        bport_oid = port_id

    l2mc_group_member_attr_list = []
    attr_value = sai_thrift_attribute_value_t(oid=grp_id)
    attr = sai_thrift_attribute_t(id=SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID, value=attr_value)
    l2mc_group_member_attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=bport_oid)
    attr = sai_thrift_attribute_t(id=SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID, value=attr_value)
    l2mc_group_member_attr_list.append(attr)

    member_id = client.sai_thrift_create_l2mc_group_member(l2mc_group_member_attr_list)
    sys_logging("### L2MC_GROUP_MEMBER_ID = 0x%010x ###" %member_id)
    return member_id


def sai_thrift_create_l2mc_entry(client, l2mc_entry, grp_id=None, packet_action=SAI_PACKET_ACTION_FORWARD):
    l2mc_entry_attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=packet_action)
    attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
    l2mc_entry_attr_list.append(attr)

    if grp_id is not None:
        attr_value = sai_thrift_attribute_value_t(oid=grp_id)
        attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
        l2mc_entry_attr_list.append(attr)

    return client.sai_thrift_create_l2mc_entry(l2mc_entry, l2mc_entry_attr_list)


def sai_thrift_create_mcast_fdb_entry(client, mcast_fdb_entry, grp_id,
                                      packet_action=SAI_PACKET_ACTION_FORWARD, meta_data=None):
    mcast_fdb_entry_attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=packet_action)
    attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
    mcast_fdb_entry_attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=grp_id)
    attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
    mcast_fdb_entry_attr_list.append(attr)

    if meta_data is not None:
        attr_value = sai_thrift_attribute_value_t(u32=meta_data)
        attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_META_DATA, value=attr_value)
        mcast_fdb_entry_attr_list.append(attr)

    return client.sai_thrift_create_mcast_fdb_entry(mcast_fdb_entry, mcast_fdb_entry_attr_list)


def sai_thrift_create_ipmc_group_member(client, grp_id, output_id):
    member_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(oid=grp_id)
    attribute = sai_thrift_attribute_t(id=SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID,
                                           value=attribute_value)
    member_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(oid=output_id)
    attribute = sai_thrift_attribute_t(id=SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID,
                                           value=attribute_value)
    member_attr_list.append(attribute)

    member_id = client.sai_thrift_create_ipmc_group_member(member_attr_list)
    return member_id

def sai_thrift_create_rpf_group_member(client, grp_id, l3if_id):
    member_attr_list = []
    attribute_value = sai_thrift_attribute_value_t(oid=grp_id)
    attribute = sai_thrift_attribute_t(id=SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID,
                                           value=attribute_value)
    member_attr_list.append(attribute)

    attribute_value = sai_thrift_attribute_value_t(oid=l3if_id)
    attribute = sai_thrift_attribute_t(id=SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID,
                                           value=attribute_value)
    member_attr_list.append(attribute)

    member_id = client.sai_thrift_create_rpf_group_member(member_attr_list)
    return member_id

def sai_thrift_create_ipmc_entry(client, ipmc_entry, grp_id = 0, packet_action = SAI_PACKET_ACTION_FORWARD, rpf_grp_id = 0):
    entry_attr_list = []

    attribute_value = sai_thrift_attribute_value_t(s32=packet_action)
    attribute = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION,
                                            value=attribute_value)
    entry_attr_list.append(attribute)

    if grp_id != 0:
        attribute_value = sai_thrift_attribute_value_t(oid=grp_id)
        attribute = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID,
                                                value=attribute_value)
        entry_attr_list.append(attribute)

    if rpf_grp_id != 0:
		attribute_value = sai_thrift_attribute_value_t(oid=rpf_grp_id)
		attribute = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID,
												value=attribute_value)
		entry_attr_list.append(attribute)

    return client.sai_thrift_create_ipmc_entry(ipmc_entry, entry_attr_list)

def sai_thrift_create_tunnel_map(client, type):
    tunnel_attr_list = []

    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=type)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)

    return client.sai_thrift_create_tunnel_map(tunnel_attr_list)

def sai_thrift_create_tunnel_map_entry(client, type, tunnel_map_oid, key, value):
    tunnel_attr_list = []

    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=type)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)

    if SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(u16=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(u32=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)
    elif SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(u32=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(u16=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)
    elif SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(oid=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(u32=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)
    elif SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(u32=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(oid=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)
    elif SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(oid=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(u32=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)
    elif SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI == type:
        tunnel_attribute2_value = sai_thrift_attribute_value_t(u32=value)
        tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE,
                                            value=tunnel_attribute2_value)
        tunnel_attr_list.append(tunnel_attribute2)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(oid=key)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)

    tunnel_attribute5_value = sai_thrift_attribute_value_t(oid=tunnel_map_oid)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)

    return client.sai_thrift_create_tunnel_map_entry(tunnel_attr_list)

def sai_thrift_create_tunnel(client, underlay_if, overlay_if, ip_addr, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, encap_ttl_val=0, encap_dscp_mode=SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL, encap_dscp_val=0, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, decap_dscp_mode=SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL):
    tunnel_attr_list = []

    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_TUNNEL_TYPE_IPINIP)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)
    tunnel_attribute2_value = sai_thrift_attribute_value_t(oid=underlay_if)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(oid=overlay_if)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_OVERLAY_INTERFACE,
                                            value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)

    addr = sai_thrift_ip_t(ip4=ip_addr)
    ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    #addr = sai_thrift_ip_t(ip6=ip_addr)
    #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    tunnel_attribute4_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_SRC_IP,
                                             value=tunnel_attribute4_value)
    tunnel_attr_list.append(tunnel_attribute4)



    u8 = ctypes.c_int8(decap_ttl_mode)
    tunnel_attribute5_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_TTL_MODE,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)
    u8 = ctypes.c_int8(decap_dscp_mode)
    tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_DSCP_MODE,
                                            value=tunnel_attribute6_value)
    tunnel_attr_list.append(tunnel_attribute6)



    if encap_ttl_mode != SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL:
        u8 = ctypes.c_int8(encap_ttl_mode)
        tunnel_attribute5_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_MODE,
                                                value=tunnel_attribute5_value)
        tunnel_attr_list.append(tunnel_attribute5)

        u8 = ctypes.c_int8(encap_ttl_val)
        tunnel_attribute_ttl_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute_ttl = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_VAL,
                                                value=tunnel_attribute_ttl_value)
        tunnel_attr_list.append(tunnel_attribute_ttl)

    if encap_dscp_mode != SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL:
        u8 = ctypes.c_int8(encap_dscp_mode)
        tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE,
                                                value=tunnel_attribute6_value)
        tunnel_attr_list.append(tunnel_attribute6)
        u8 = ctypes.c_int8(encap_dscp_val)
        tunnel_attribute_dscp_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute_dscp = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL,
                                                value=tunnel_attribute_dscp_value)
        tunnel_attr_list.append(tunnel_attribute_dscp)

    return client.sai_thrift_create_tunnel(tunnel_attr_list)

def sai_thrift_create_tunnel_mpls(client, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, encap_ttl_val=0, decap_exp_mode=SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL, encap_exp_val=0):
    tunnel_attr_list = []
    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_TUNNEL_TYPE_MPLS)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)
    u8 = ctypes.c_int8(decap_ttl_mode)
    tunnel_attribute2_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_TTL_MODE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)
    u8 = ctypes.c_int8(encap_ttl_mode)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_MODE,
                                            value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)
    if encap_ttl_val:
        u8 = ctypes.c_int8(encap_ttl_val)
        tunnel_attribute4_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_VAL,
                                            value=tunnel_attribute4_value)
        tunnel_attr_list.append(tunnel_attribute4)
    u8 = ctypes.c_int8(decap_exp_mode)
    tunnel_attribute5_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_EXP_MODE,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)
    u8 = ctypes.c_int8(encap_exp_mode)
    tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_EXP_MODE,
                                            value=tunnel_attribute6_value)
    tunnel_attr_list.append(tunnel_attribute6)
    if encap_exp_val:
        u8 = ctypes.c_int8(encap_exp_val)
        tunnel_attribute7_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute7 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_EXP_VAL,
                                            value=tunnel_attribute7_value)
        tunnel_attr_list.append(tunnel_attribute7)
    return client.sai_thrift_create_tunnel(tunnel_attr_list)

def sai_thrift_create_tunnel_mpls_l2vpn(client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=0, decap_esi_label_valid=False, encap_esi_label_valid=False, encap_ttl_mode=None, encap_exp_mode=None, encap_exp_val=None, decap_exp_mode=SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL):
    tunnel_attr_list = []
    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_TUNNEL_TYPE_MPLS_L2)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)

    u8 = ctypes.c_int8(decap_pw_mode)
    tunnel_attribute2_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)
    u8 = ctypes.c_int8(encap_pw_mode)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE,
                                            value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)
    tunnel_attribute4_value = sai_thrift_attribute_value_t(booldata=decap_cw_en)
    tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,
                                            value=tunnel_attribute4_value)
    tunnel_attr_list.append(tunnel_attribute4)
    tunnel_attribute5_value = sai_thrift_attribute_value_t(booldata=encap_cw_en)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)
    
    if encap_ttl_val:
        u8 = ctypes.c_int8(encap_ttl_val)
        tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_VAL,
                                            value=tunnel_attribute6_value)
        tunnel_attr_list.append(tunnel_attribute6)
        
    if encap_tagged_vlan:
        u16 = ctypes.c_int16(encap_tagged_vlan)
        tunnel_attribute7_value = sai_thrift_attribute_value_t(u16=u16.value)
        tunnel_attribute7 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,
                                            value=tunnel_attribute7_value)
        tunnel_attr_list.append(tunnel_attribute7)

    if encap_ttl_mode:
        u8 = ctypes.c_int8(encap_ttl_mode)
        tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_TTL_MODE,
                                            value=tunnel_attribute6_value)
        tunnel_attr_list.append(tunnel_attribute6)
        
    if encap_exp_mode:
        u8 = ctypes.c_int8(encap_exp_mode)
        tunnel_attribute7_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute7 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_EXP_MODE,
                                            value=tunnel_attribute7_value)
        tunnel_attr_list.append(tunnel_attribute7)

    if encap_exp_val:
        u8 = ctypes.c_int8(encap_exp_val)
        tunnel_attribute7_value = sai_thrift_attribute_value_t(u8=u8.value)
        tunnel_attribute7 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_EXP_VAL,
                                            value=tunnel_attribute7_value)
        tunnel_attr_list.append(tunnel_attribute7)

    tunnel_attribute8_value = sai_thrift_attribute_value_t(booldata=decap_esi_label_valid)
    tunnel_attribute8 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,
                                            value=tunnel_attribute8_value)
    tunnel_attr_list.append(tunnel_attribute8)
    tunnel_attribute9_value = sai_thrift_attribute_value_t(booldata=encap_esi_label_valid)
    tunnel_attribute9 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,
                                            value=tunnel_attribute9_value)
    tunnel_attr_list.append(tunnel_attribute9)

    u8 = ctypes.c_int8(decap_exp_mode)
    tunnel_attribute10_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute10 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_EXP_MODE,
                                            value=tunnel_attribute10_value)
    tunnel_attr_list.append(tunnel_attribute10)
    
    return client.sai_thrift_create_tunnel(tunnel_attr_list)

def sai_thrift_create_tunnel_gre(client, underlay_if, overlay_if, ip_addr, gre_key, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, decap_dscp_mode=SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL):
    tunnel_attr_list = []

    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_TUNNEL_TYPE_IPINIP_GRE)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)
    tunnel_attribute2_value = sai_thrift_attribute_value_t(oid=underlay_if)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(oid=overlay_if)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_OVERLAY_INTERFACE,
                                            value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)

    addr = sai_thrift_ip_t(ip4=ip_addr)
    ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    #addr = sai_thrift_ip_t(ip6=ip_addr)
    #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    tunnel_attribute4_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_SRC_IP,
                                             value=tunnel_attribute4_value)
    tunnel_attr_list.append(tunnel_attribute4)
    u8 = ctypes.c_int8(decap_ttl_mode)
    tunnel_attribute5_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_TTL_MODE,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)
    u8 = ctypes.c_int8(decap_dscp_mode)
    tunnel_attribute6_value = sai_thrift_attribute_value_t(u8=u8.value)
    tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_DSCP_MODE,
                                            value=tunnel_attribute6_value)
    tunnel_attr_list.append(tunnel_attribute6)

    tunnel_attribute7_value = sai_thrift_attribute_value_t(booldata=1)
    tunnel_attribute7 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID,
                                            value=tunnel_attribute7_value)
    tunnel_attr_list.append(tunnel_attribute7)

    tunnel_attribute8_value = sai_thrift_attribute_value_t(u32=gre_key)
    tunnel_attribute8 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_GRE_KEY,
                                            value=tunnel_attribute8_value)
    tunnel_attr_list.append(tunnel_attribute8)

    return client.sai_thrift_create_tunnel(tunnel_attr_list)

def sai_thrift_create_tunnel_vxlan(client, ip_addr, encap_mapper_list, decap_mapper_list, underlay_if):
    tunnel_attr_list = []

    tunnel_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_TUNNEL_TYPE_VXLAN)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_TYPE,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)

    tunnel_attribute2_value = sai_thrift_attribute_value_t(oid=underlay_if)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)

    addr = sai_thrift_ip_t(ip4=ip_addr)
    ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    #addr = sai_thrift_ip_t(ip6=ip_addr)
    #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_SRC_IP,
                                             value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)

    #Encap mapper list
    if encap_mapper_list:
        tunnel_encap_mapper_list = sai_thrift_object_list_t(count=len(encap_mapper_list), object_id_list=encap_mapper_list)
        tunnel_attribute3_value = sai_thrift_attribute_value_t(objlist=tunnel_encap_mapper_list)
        tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MAPPERS,
                                            value=tunnel_attribute3_value)
        tunnel_attr_list.append(tunnel_attribute3)

    #Decap mapper list
    if decap_mapper_list:
        tunnel_decap_mapper_list = sai_thrift_object_list_t(count=len(decap_mapper_list), object_id_list=decap_mapper_list)
        tunnel_attribute4_value = sai_thrift_attribute_value_t(objlist=tunnel_decap_mapper_list)
        tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MAPPERS,
                                            value=tunnel_attribute4_value)
        tunnel_attr_list.append(tunnel_attribute4)

    return client.sai_thrift_create_tunnel(tunnel_attr_list)

def sai_thrift_create_tunnel_term_table_entry(client, vr_id, ip_sa, ip_da, tunnel_id, type=SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P, tunnel_type=SAI_TUNNEL_TYPE_IPINIP):
    tunnel_attr_list = []
    tunnel_attribute1_value = sai_thrift_attribute_value_t(oid=vr_id)
    tunnel_attribute1 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID,
                                            value=tunnel_attribute1_value)
    tunnel_attr_list.append(tunnel_attribute1)
    tunnel_attribute2_value = sai_thrift_attribute_value_t(s32=type)
    tunnel_attribute2 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE,
                                            value=tunnel_attribute2_value)
    tunnel_attr_list.append(tunnel_attribute2)
    addr = sai_thrift_ip_t(ip4=ip_sa)
    ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    #addr = sai_thrift_ip_t(ip6=ip_addr)
    #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    tunnel_attribute3_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    tunnel_attribute3 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP,
                                             value=tunnel_attribute3_value)
    tunnel_attr_list.append(tunnel_attribute3)

    addr = sai_thrift_ip_t(ip4=ip_da)
    ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    #addr = sai_thrift_ip_t(ip6=ip_addr)
    #ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    tunnel_attribute4_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    tunnel_attribute4 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP,
                                             value=tunnel_attribute4_value)
    tunnel_attr_list.append(tunnel_attribute4)
    tunnel_attribute5_value = sai_thrift_attribute_value_t(s32=tunnel_type)
    tunnel_attribute5 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE,
                                            value=tunnel_attribute5_value)
    tunnel_attr_list.append(tunnel_attribute5)
    tunnel_attribute6_value = sai_thrift_attribute_value_t(oid=tunnel_id)
    tunnel_attribute6 = sai_thrift_attribute_t(id=SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID,
                                            value=tunnel_attribute6_value)
    tunnel_attr_list.append(tunnel_attribute6)

    return client.sai_thrift_create_tunnel_term_table_entry(tunnel_attr_list)

def sai_thrift_create_isolation_group(client, type):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(u32=type)
    attr = sai_thrift_attribute_t(id=SAI_ISOLATION_GROUP_ATTR_TYPE,
                                            value=attr_value)
    attr_list.append(attr)
    return client.sai_thrift_create_isolation_group(attr_list)

def sai_thrift_remove_isolation_group(client, iso_grp_oid):
    return client.sai_thrift_remove_isolation_group(iso_grp_oid)

def sai_thrift_create_isolation_group_member(client, group_oid, member_oid):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(oid=group_oid)
    attr = sai_thrift_attribute_t(id=SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=member_oid)
    attr = sai_thrift_attribute_t(id=SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT, value=attr_value)
    attr_list.append(attr)

    return client.sai_thrift_create_isolation_group_member(attr_list)

def sai_thrift_remove_isolation_group_member(client, member_oid):
    return client.sai_thrift_remove_isolation_group_member(member_oid)

def sai_thrift_get_isolation_group_attributes(client, isolation_group_oid):
    attr_list = client.sai_thrift_get_isolation_group_attributes(isolation_group_oid)
    return attr_list

def sai_thrift_get_isolation_group_member_attributes(client, member_oid):
    return client.sai_thrift_get_isolation_group_member_attributes(member_oid)

def sai_thrift_create_nat(client, vr_id, nat_type, keylist, masklist, mod_srcip_addr=None, mod_dstip_addr=None, mod_l4_srcport=None, mod_l4_dstport=None):

    srcip = keylist[0]
    dstip = keylist[1]
    masksrcip = masklist[0]
    maskdstip = masklist[1]

    nat = sai_thrift_nat_entry_t(vr_id, srcip, dstip, keylist[2], keylist[3], keylist[4], masksrcip, maskdstip, masklist[2], masklist[3], masklist[4], nat_type)

    nat_attribute1_value = sai_thrift_attribute_value_t(s32=nat_type)
    nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_NAT_TYPE,
                                              value=nat_attribute1_value)
    nat_attr_list = [nat_attribute1]


    if mod_srcip_addr != None:
        nat_attribute1_value = sai_thrift_attribute_value_t(ip4=mod_srcip_addr)
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_SRC_IP,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

        nat_attribute1_value = sai_thrift_attribute_value_t(ip4='255.255.255.255')
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_SRC_IP_MASK,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

    if mod_dstip_addr != None:
        nat_attribute1_value = sai_thrift_attribute_value_t(ip4=mod_dstip_addr)
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_DST_IP,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

        nat_attribute1_value = sai_thrift_attribute_value_t(ip4='255.255.255.255')
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_DST_IP_MASK,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

    if mod_l4_srcport != None:
        nat_attribute1_value = sai_thrift_attribute_value_t(u16=mod_l4_srcport)
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_L4_SRC_PORT,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

    if mod_l4_dstport != None:
        nat_attribute1_value = sai_thrift_attribute_value_t(u16=mod_l4_dstport)
        nat_attribute1 = sai_thrift_attribute_t(id=SAI_NAT_ENTRY_ATTR_L4_DST_PORT,
                                              value=nat_attribute1_value)
        nat_attr_list.append(nat_attribute1)

    return client.sai_thrift_create_nat(thrift_nat_entry=nat, thrift_attr_list=nat_attr_list)

def sai_thrift_remove_nat(client, vr_id, keylist, masklist, nat_type):
    srcip = keylist[0]
    dstip = keylist[1]
    masksrcip = masklist[0]
    maskdstip = masklist[1]

    nat = sai_thrift_nat_entry_t(vr_id, srcip, dstip, keylist[2], keylist[3], keylist[4], masksrcip, maskdstip, masklist[2], masklist[3], masklist[4], nat_type)

    return client.sai_thrift_remove_nat(thrift_nat_entry=nat)

def sai_thrift_create_counter(client, type):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=type)
    attr = sai_thrift_attribute_t(id=SAI_COUNTER_ATTR_TYPE,
                                            value=attr_value)
    attr_list.append(attr)
    return client.sai_thrift_create_counter(attr_list)

def sai_thrift_remove_counter(client, counter_oid):
    return client.sai_thrift_remove_counter(counter_oid)

def sai_thrift_create_debugcounter(client, type, in_drop_list=None, out_drop_list=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=0)
    attr0 = sai_thrift_attribute_t(id=SAI_DEBUG_COUNTER_ATTR_BIND_METHOD,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(s32=type)
    attr1 = sai_thrift_attribute_t(id=SAI_DEBUG_COUNTER_ATTR_TYPE,
                                            value=attr_value1)
    attr_list.append(attr1)

    if in_drop_list:
        in_list = sai_thrift_s32_list_t(count=len(in_drop_list), s32list=in_drop_list)
        attr_value2 = sai_thrift_attribute_value_t(s32list=in_list)
        attr2 = sai_thrift_attribute_t(id=SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST,
                                                value=attr_value2)
        attr_list.append(attr2)

    if out_drop_list:
        out_list = sai_thrift_s32_list_t(count=len(out_drop_list), s32list=out_drop_list)
        attr_value3 = sai_thrift_attribute_value_t(s32list=out_list)
        attr3 = sai_thrift_attribute_t(id=SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST,
                                                value=attr_value3)
        attr_list.append(attr3)

    return client.sai_thrift_create_debug_counter(attr_list)

def sai_thrift_read_port_debug_counters(client,port, debug_index_list, ext_mode=None):
    port_cnt_ids=[]
    for debugidx in debug_index_list:
        port_cnt_ids.append(debugidx)

    counters_results=[]
    if ext_mode!=None:
        counters_results = client.sai_thrift_get_port_stats_ext(port,port_cnt_ids,ext_mode,len(port_cnt_ids))
    else:
        counters_results = client.sai_thrift_get_port_stats(port,port_cnt_ids,len(port_cnt_ids))

    return counters_results




def sai_thrift_create_twamp_session_sender(client, receive_port_list, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period=None, tx_pkt_cnt=None, tx_pkt_duration=None, port_oid=None):

    attr_list = []

    attr_value = sai_thrift_attribute_value_t(oid=port_oid)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_PORT,
                                            value=attr_value)
    attr_list.append(attr)  
    

    receive_port_obj_list = sai_thrift_object_list_t(count=len(receive_port_list), object_id_list=receive_port_list)
    attr_value = sai_thrift_attribute_value_t(objlist=receive_port_obj_list)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT,
                                        value=attr_value)
    attr_list.append(attr) 

    
    attr_value = sai_thrift_attribute_value_t(s32=SAI_TWAMP_SESSION_ROLE_SENDER)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ROLE,
                                            value=attr_value)
    attr_list.append(attr)  
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_src_port)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_dst_port)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT,
                                            value=attr_value)
    attr_list.append(attr)
    
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        src_addr = sai_thrift_ip_t(ip4=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip4=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=dst_addr)        
    else:
        src_addr = sai_thrift_ip_t(ip6=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip6=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=dst_addr) 
        
    attr_value = sai_thrift_attribute_value_t(ipaddr=src_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SRC_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(ipaddr=dst_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_DST_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=tc)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TC,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(oid=vrf_oid)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(s32=encap_type)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(booldata=hw_lookup)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u32=pkt_len)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(s32=SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_AUTH_MODE,
                                            value=attr_value)
    attr_list.append(attr)
    

    attr_value = sai_thrift_attribute_value_t(s32=mode)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_MODE,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(s32=tx_mode)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u32=tx_rate)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TX_RATE,
                                            value=attr_value)
    attr_list.append(attr)    

    attr_value = sai_thrift_attribute_value_t(u32=tx_period)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD,
                                           value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u32=tx_pkt_cnt)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=tx_pkt_duration)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION,
                                            value=attr_value)
    attr_list.append(attr)
    
    twamp_session_id = client.sai_thrift_create_twamp_session(attr_list)

    return twamp_session_id
    

def sai_thrift_create_twamp_session_reflector(client, receive_port_list, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=None ):

    attr_list = []

    attr_value = sai_thrift_attribute_value_t(oid=port_oid)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_PORT,
                                            value=attr_value)
    attr_list.append(attr)
          
    receive_port_obj_list = sai_thrift_object_list_t(count=len(receive_port_list), object_id_list=receive_port_list)
    attr_value = sai_thrift_attribute_value_t(objlist=receive_port_obj_list)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT,
                                        value=attr_value)
    attr_list.append(attr) 

    
    attr_value = sai_thrift_attribute_value_t(s32=SAI_TWAMP_SESSION_ROLE_REFLECTOR)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ROLE,
                                            value=attr_value)
    attr_list.append(attr)  
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_src_port)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_dst_port)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT,
                                            value=attr_value)
    attr_list.append(attr)
    
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        src_addr = sai_thrift_ip_t(ip4=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip4=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=dst_addr)        
    else:
        src_addr = sai_thrift_ip_t(ip6=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip6=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=dst_addr) 
        
    attr_value = sai_thrift_attribute_value_t(ipaddr=src_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SRC_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(ipaddr=dst_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_DST_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=tc)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TC,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(oid=vrf_oid)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(s32=encap_type)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(booldata=hw_lookup)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(s32=mode)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TWAMP_MODE,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(s32=SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_AUTH_MODE,
                                            value=attr_value)
    attr_list.append(attr)
    
    if nexthop != None:
        attr_value = sai_thrift_attribute_value_t(oid=nexthop)
        attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID,
                                                value=attr_value)
        attr_list.append(attr)
    
    twamp_session_id = client.sai_thrift_create_twamp_session(attr_list)

    return twamp_session_id



def sai_thrift_remove_twamp_session(client, session_id):
    return client.sai_thrift_remove_twamp_session(session_id)

def sai_thrift_set_twamp_attribute(client, session_id, enable):
    attr_value = sai_thrift_attribute_value_t(booldata=enable)
    attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
    client.sai_thrift_set_twamp_attribute(session_id,attr)




def sai_thrift_create_npm_session_sender(client, encap_type, test_port_oid, receive_port_list, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration):

    attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=SAI_NPM_SESSION_ROLE_SENDER)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ROLE,
                                            value=attr_value)
    attr_list.append(attr)  

    attr_value = sai_thrift_attribute_value_t(s32=encap_type)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,
                                            value=attr_value)
    attr_list.append(attr)
    
    
    attr_value = sai_thrift_attribute_value_t(oid=test_port_oid)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_TEST_PORT,
                                            value=attr_value)
    attr_list.append(attr)  


    receive_port_obj_list = sai_thrift_object_list_t(count=len(receive_port_list), object_id_list=receive_port_list)
    attr_value = sai_thrift_attribute_value_t(objlist=receive_port_obj_list)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT,
                                        value=attr_value)
    attr_list.append(attr)  


    attr_value = sai_thrift_attribute_value_t(mac=src_mac)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SRC_MAC,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(mac=dst_mac)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_DST_MAC,
                                            value=attr_value)
    attr_list.append(attr)

    if( outer_vlanid != None):    
        attr_value = sai_thrift_attribute_value_t(u16=outer_vlanid)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_OUTER_VLANID,
                                                value=attr_value)
        attr_list.append(attr)

    if( inner_vlan_id != None):    
        attr_value = sai_thrift_attribute_value_t(u16=inner_vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_INNER_VLANID,
                                                value=attr_value)
        attr_list.append(attr)
        

    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        src_addr = sai_thrift_ip_t(ip4=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip4=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=dst_addr)        
    else:
        src_addr = sai_thrift_ip_t(ip6=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip6=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=dst_addr) 
        
    attr_value = sai_thrift_attribute_value_t(ipaddr=src_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SRC_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(ipaddr=dst_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_DST_IP,
                                            value=attr_value)
    attr_list.append(attr)
    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_src_port)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_dst_port)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_UDP_DST_PORT,
                                            value=attr_value)
    attr_list.append(attr)
    
    if( ttl != None):   
        attr_value = sai_thrift_attribute_value_t(u8=ttl)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TTL,
                                                value=attr_value)
        attr_list.append(attr)
    
    if( tc != None):     
        attr_value = sai_thrift_attribute_value_t(u8=tc)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TC,
                                                value=attr_value)
        attr_list.append(attr)

    if( enable_transmit != None): 
        attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
                                                value=attr_value)
        attr_list.append(attr)

    if( vrf_oid != None):         
        attr_value = sai_thrift_attribute_value_t(oid=vrf_oid)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
                                                value=attr_value)
        attr_list.append(attr)    
    
    if( hw_lookup != None):  
        attr_value = sai_thrift_attribute_value_t(booldata=hw_lookup)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,
                                                value=attr_value)
        attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u32=pkt_len)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_PACKET_LENGTH,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u32=tx_rate)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TX_RATE,
                                            value=attr_value)
    attr_list.append(attr)  
   
    attr_value = sai_thrift_attribute_value_t(s32=tx_mode)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_PKT_TX_MODE,
                                            value=attr_value)
    attr_list.append(attr)

    if( tx_period != None):      
        attr_value = sai_thrift_attribute_value_t(u32=tx_period)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,
                                               value=attr_value)
        attr_list.append(attr)

    if( tx_pkt_cnt != None):         
        attr_value = sai_thrift_attribute_value_t(u32=tx_pkt_cnt)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TX_PKT_CNT,
                                                value=attr_value)
        attr_list.append(attr)

    if( tx_pkt_duration != None):         
        attr_value = sai_thrift_attribute_value_t(u64=tx_pkt_duration)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,
                                                value=attr_value)
        attr_list.append(attr)
    
    npm_session_id = client.sai_thrift_create_npm_session(attr_list)

    return npm_session_id
    


def sai_thrift_create_npm_session_reflector(client, encap_type, test_port_oid, receive_port_list, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup):

    attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=SAI_NPM_SESSION_ROLE_REFLECTOR)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ROLE,
                                            value=attr_value)
    attr_list.append(attr)  

    attr_value = sai_thrift_attribute_value_t(s32=encap_type)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,
                                            value=attr_value)
    attr_list.append(attr)
    
    
    attr_value = sai_thrift_attribute_value_t(oid=test_port_oid)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_TEST_PORT,
                                            value=attr_value)
    attr_list.append(attr)  
    
    receive_port_obj_list = sai_thrift_object_list_t(count=len(receive_port_list), object_id_list=receive_port_list)
    attr_value = sai_thrift_attribute_value_t(objlist=receive_port_obj_list)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT,
                                        value=attr_value)
    attr_list.append(attr)  

    

    attr_value = sai_thrift_attribute_value_t(mac=src_mac)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SRC_MAC,
                                            value=attr_value)
    attr_list.append(attr)
    
    attr_value = sai_thrift_attribute_value_t(mac=dst_mac)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_DST_MAC,
                                            value=attr_value)
    attr_list.append(attr)

    if( outer_vlanid != None):    
        attr_value = sai_thrift_attribute_value_t(u16=outer_vlanid)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_OUTER_VLANID,
                                                value=attr_value)
        attr_list.append(attr)

    if( inner_vlan_id != None):    
        attr_value = sai_thrift_attribute_value_t(u16=inner_vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_INNER_VLANID,
                                                value=attr_value)
        attr_list.append(attr)
        

    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        src_addr = sai_thrift_ip_t(ip4=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip4=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=dst_addr)        
    else:
        src_addr = sai_thrift_ip_t(ip6=src_ip)
        src_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=src_addr)
        dst_addr = sai_thrift_ip_t(ip6=dst_ip)
        dst_ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=dst_addr) 
        
    attr_value = sai_thrift_attribute_value_t(ipaddr=src_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SRC_IP,
                                            value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(ipaddr=dst_ipaddr)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_DST_IP,
                                            value=attr_value)
    attr_list.append(attr)
    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_src_port)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value)
    attr_list.append(attr)    
    
    attr_value = sai_thrift_attribute_value_t(u32=udp_dst_port)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_UDP_DST_PORT,
                                            value=attr_value)
    attr_list.append(attr)
    
   
    if( tc != None):     
        attr_value = sai_thrift_attribute_value_t(u8=tc)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_TC,
                                                value=attr_value)
        attr_list.append(attr)

    if( vrf_oid != None):         
        attr_value = sai_thrift_attribute_value_t(oid=vrf_oid)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,
                                                value=attr_value)
        attr_list.append(attr)    
    
    if( hw_lookup != None):  
        attr_value = sai_thrift_attribute_value_t(booldata=hw_lookup)
        attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,
                                                value=attr_value)
        attr_list.append(attr)

    npm_session_id = client.sai_thrift_create_npm_session(attr_list)

    return npm_session_id



def sai_thrift_remove_npm_session(client, session_id):
    return client.sai_thrift_remove_npm_session(session_id)

def sai_thrift_set_npm_attribute(client, session_id, enable):
    attr_value = sai_thrift_attribute_value_t(booldata=enable)
    attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
    client.sai_thrift_set_npm_attribute(session_id,attr)



def sai_thrift_create_ip_bfd_session(client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx=1, min_rx=1, multip=3, tos=None, ttl=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_ENCAPSULATION_TYPE_NONE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=l_disc)
    attr1 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u32=r_disc)
    attr2 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(u32=udp_srcport)
    attr3 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value3)
    attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(booldata=multihop)
    attr4 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIHOP,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(oid=vr_id)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        attr_value5 = sai_thrift_attribute_value_t(u8=4)
    else:
        attr_value5 = sai_thrift_attribute_value_t(u8=6)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_IPHDR_VERSION,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        
    attr_value6 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr6 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,
                                            value=attr_value6)
    attr_list.append(attr6)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        
    attr_value7 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr7 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(u32=min_tx)
    attr8 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_TX,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u32=min_rx)
    attr9 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_RX,
                                            value=attr_value9)
    attr_list.append(attr9)

    attr_value10 = sai_thrift_attribute_value_t(u8=multip)
    attr10 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIPLIER,
                                            value=attr_value10)
    attr_list.append(attr10)

    if( tos != None):
        attr_value14 = sai_thrift_attribute_value_t(u8=tos)
        attr14 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TOS,
                                                value=attr_value14)
        attr_list.append(attr14)        

    if( ttl != None):
        attr_value15 = sai_thrift_attribute_value_t(u8=ttl)
        attr15 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TTL,
                                                value=attr_value15)
        attr_list.append(attr15)
        

    return client.sai_thrift_create_bfd(attr_list)


def sai_thrift_create_ip_bfd_session_with_nh(client, l_disc, r_disc, udp_srcport, multihop, nh_oid, addr_family, src_ip, dst_ip, min_tx=1, min_rx=1, multip=3, tos=None, ttl=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_ENCAPSULATION_TYPE_NONE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=l_disc)
    attr1 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u32=r_disc)
    attr2 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(u32=udp_srcport)
    attr3 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value3)
    attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(booldata=multihop)
    attr4 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIHOP,
                                            value=attr_value4)
    attr_list.append(attr4)

    #attr_value5 = sai_thrift_attribute_value_t(oid=vr_id)
    #attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER,
    #                                        value=attr_value5)
    #attr_list.append(attr5)

    attr_value5 = sai_thrift_attribute_value_t(booldata=0)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID,
                                            value=attr_value5)
    attr_list.append(attr5)
    

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        attr_value5 = sai_thrift_attribute_value_t(u8=4)
    else:
        attr_value5 = sai_thrift_attribute_value_t(u8=6)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_IPHDR_VERSION,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        
    attr_value6 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr6 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,
                                            value=attr_value6)
    attr_list.append(attr6)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        
    attr_value7 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr7 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(u32=min_tx)
    attr8 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_TX,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u32=min_rx)
    attr9 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_RX,
                                            value=attr_value9)
    attr_list.append(attr9)

    attr_value10 = sai_thrift_attribute_value_t(u8=multip)
    attr10 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIPLIER,
                                            value=attr_value10)
    attr_list.append(attr10)

    attr_value11 = sai_thrift_attribute_value_t(oid=nh_oid)
    attr11 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_NEXT_HOP_ID,
                                            value=attr_value11)
    attr_list.append(attr11)
    
    if( tos != None):
        attr_value14 = sai_thrift_attribute_value_t(u8=tos)
        attr14 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TOS,
                                                value=attr_value14)
        attr_list.append(attr14)        

    if( ttl != None):
        attr_value15 = sai_thrift_attribute_value_t(u8=ttl)
        attr15 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TTL,
                                                value=attr_value15)
        attr_list.append(attr15)
        
    return client.sai_thrift_create_bfd(attr_list)
    

def sai_thrift_create_micro_bfd_session(client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, dst_port, dst_mac, src_mac, min_tx=1, min_rx=1, multip=3, tos=None, ttl=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_ENCAPSULATION_TYPE_NONE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=l_disc)
    attr1 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u32=r_disc)
    attr2 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(u32=udp_srcport)
    attr3 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value3)
    attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(booldata=multihop)
    attr4 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIHOP,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(booldata=0)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        attr_value5 = sai_thrift_attribute_value_t(u8=4)
    else:
        attr_value5 = sai_thrift_attribute_value_t(u8=6)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_IPHDR_VERSION,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    attr_value6 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr6 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,
                                            value=attr_value6)
    attr_list.append(attr6)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    attr_value7 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr7 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(u32=min_tx)
    attr8 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_TX,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u32=min_rx)
    attr9 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_RX,
                                            value=attr_value9)
    attr_list.append(attr9)

    attr_value10 = sai_thrift_attribute_value_t(u8=multip)
    attr10 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIPLIER,
                                            value=attr_value10)
    attr_list.append(attr10)

    attr_value11 = sai_thrift_attribute_value_t(oid=dst_port)
    attr11 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_PORT,
                                            value=attr_value11)
    attr_list.append(attr11)

    attr_value12 = sai_thrift_attribute_value_t(mac=src_mac)
    attr12 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS,
                                            value=attr_value12)
    attr_list.append(attr12)

    attr_value13 = sai_thrift_attribute_value_t(mac=dst_mac)
    attr13 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS,
                                            value=attr_value13)
    attr_list.append(attr13)

    if( tos != None):
        attr_value14 = sai_thrift_attribute_value_t(u8=tos)
        attr14 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TOS,
                                                value=attr_value14)
        attr_list.append(attr14)        

    if( ttl != None):
        attr_value15 = sai_thrift_attribute_value_t(u8=ttl)
        attr15 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TTL,
                                                value=attr_value15)
        attr_list.append(attr15)


    return client.sai_thrift_create_bfd(attr_list)

def sai_thrift_remove_bfd(client, bfd_oid):
    return client.sai_thrift_remove_bfd(bfd_oid)


def sai_thrift_create_mpls_bfd_session(client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label, nh_id, ach_type=None, min_tx=1, min_rx=1, multip=3, cv_en=0, src_mepid=None, without_gal=0, l3if_oid=None, aps_group=None, is_protection=None, protection_en=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=SAI_BFD_ENCAPSULATION_TYPE_MPLS)
    attr0 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=l_disc)
    attr1 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u32=r_disc)
    attr2 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(u32=udp_srcport)
    attr3 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,
                                            value=attr_value3)
    attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(booldata=0)
    attr4 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value4 = sai_thrift_attribute_value_t(booldata=0)
    attr4 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIHOP,
                                            value=attr_value4)
    attr_list.append(attr4)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        attr_value5 = sai_thrift_attribute_value_t(u8=4)
    else:
        attr_value5 = sai_thrift_attribute_value_t(u8=6)
    attr5 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_IPHDR_VERSION,
                                            value=attr_value5)
    attr_list.append(attr5)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=src_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    attr_value6 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr6 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,
                                            value=attr_value6)
    attr_list.append(attr6)

    if addr_family==SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dst_ip)
        ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
    attr_value7 = sai_thrift_attribute_value_t(ipaddr=ipaddr)
    attr7 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(u32=min_tx)
    attr8 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_TX,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u32=min_rx)
    attr9 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_RX,
                                            value=attr_value9)
    attr_list.append(attr9)

    attr_value10 = sai_thrift_attribute_value_t(u8=multip)
    attr10 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIPLIER,
                                            value=attr_value10)
    attr_list.append(attr10)

    attr_value11 = sai_thrift_attribute_value_t(s32=mpls_encap_type)
    attr11 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_MPLS_TYPE,
                                            value=attr_value11)
    attr_list.append(attr11)

    if( label != None ):
        attr_value12 = sai_thrift_attribute_value_t(u32=label)
        attr12 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL,
                                            value=attr_value12)
        attr_list.append(attr12)

    attr_value12 = sai_thrift_attribute_value_t(u8=64)
    attr12 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_TTL,
                                            value=attr_value12)
    attr_list.append(attr12)

    attr_value12 = sai_thrift_attribute_value_t(u8=7)
    attr12 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_EXP,
                                            value=attr_value12)
    attr_list.append(attr12)

    if ach_type != None:
        attr_value13 = sai_thrift_attribute_value_t(booldata=1)
        attr13 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID,
                                            value=attr_value13)
        attr_list.append(attr13)

        attr_value14 = sai_thrift_attribute_value_t(s32=ach_type)
        attr14 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_BFD_ACH_CHANNEL_TYPE,
                                            value=attr_value14)
        attr_list.append(attr14)
    else:
        attr_value13 = sai_thrift_attribute_value_t(booldata=0)
        attr13 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID,
                                            value=attr_value13)
        attr_list.append(attr13)

    attr_value15 = sai_thrift_attribute_value_t(oid=nh_id)
    attr15 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_NEXT_HOP_ID,
                                            value=attr_value15)
    attr_list.append(attr15)

    attr_value16 = sai_thrift_attribute_value_t(booldata=cv_en)
    attr16 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_CV_ENABLE,
                                        value=attr_value16)
    attr_list.append(attr16)

    if cv_en:
        attr_value17 = sai_thrift_attribute_value_t(chardata=src_mepid)
        attr17 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID,
                                        value=attr_value17)
        attr_list.append(attr17)

    attr_value18 = sai_thrift_attribute_value_t(booldata=without_gal)
    attr18 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL,
                                        value=attr_value18)
    attr_list.append(attr18)

    if l3if_oid != None:    
        attr_value19 = sai_thrift_attribute_value_t(oid=l3if_oid)
        attr19 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,
                                            value=attr_value19)
        attr_list.append(attr19)


    if aps_group != None:    
        attr_value19 = sai_thrift_attribute_value_t(oid=aps_group)
        attr19 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,
                                            value=attr_value19)
        attr_list.append(attr19)
        

    if is_protection != None:    
        attr_value19 = sai_thrift_attribute_value_t(booldata=is_protection)
        attr19 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,
                                            value=attr_value19)
        attr_list.append(attr19)

        
    if protection_en != None:    
        attr_value19 = sai_thrift_attribute_value_t(booldata=protection_en)
        attr19 = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN,
                                            value=attr_value19)
        attr_list.append(attr19)

        
    return client.sai_thrift_create_bfd(attr_list)

def sai_thrift_create_y1731_meg(client, meg_type, meg_name, level):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=meg_type)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_MEG_ATTR_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(chardata=meg_name)
    attr1 = sai_thrift_attribute_t(id=SAI_Y1731_MEG_ATTR_NAME,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u8=level)
    attr2 = sai_thrift_attribute_t(id=SAI_Y1731_MEG_ATTR_LEVEL,
                                            value=attr_value2)
    attr_list.append(attr2)

    return client.sai_thrift_create_y1731_meg(attr_list)

def sai_thrift_create_y1731_eth_session(client, meg_oid, dir, local_mep_id, ccm_period, ccm_en, lm_en=0, lm_type=0, dm_en=0, tx_cos=1, port_id=None, vlan_id=None, bridge_id=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=meg_oid)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_MEG,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=dir)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DIR,
                                            value=attr_value0)
    attr_list.append(attr0)

    if port_id != None:
        attr_value1 = sai_thrift_attribute_value_t(oid=port_id)
        attr1 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_PORT_ID,
                                                value=attr_value1)
        attr_list.append(attr1)

    if vlan_id != None:
         attr_value2 = sai_thrift_attribute_value_t(u32=vlan_id)
         attr2 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_VLAN_ID,
                                                    value=attr_value2)
         attr_list.append(attr2)

    if bridge_id != None:
        attr_value3 = sai_thrift_attribute_value_t(oid=bridge_id)
        attr3 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_BRIDGE_ID,
                                                value=attr_value3)
        attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(u32=local_mep_id)
    attr4 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value4 = sai_thrift_attribute_value_t(s32=ccm_period)
    attr4 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_PERIOD,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(booldata=ccm_en)
    attr5 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE,
                                            value=attr_value5)
    attr_list.append(attr5)

    attr_value6 = sai_thrift_attribute_value_t(booldata=lm_en)
    attr6 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_ENABLE,
                                            value=attr_value6)
    attr_list.append(attr6)

    attr_value7 = sai_thrift_attribute_value_t(s32=lm_type)
    attr7 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_TYPE,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(booldata=dm_en)
    attr8 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_ENABLE,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u8=tx_cos)
    attr9 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS,
                                            value=attr_value9)
    attr_list.append(attr9)


    return client.sai_thrift_create_y1731_session(attr_list)

def sai_thrift_create_y1731_tp_session(client, mpls_in_label, meg_oid, dir, local_mep_id, ccm_period, ccm_en, next_hop_id, nogal, lm_en=0, lm_type=0, dm_en=0, tx_cos=0, tx_ttl=64):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=meg_oid)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_MEG,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value0 = sai_thrift_attribute_value_t(s32=dir)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DIR,
                                            value=attr_value0)
    attr_list.append(attr0)


    attr_value1 = sai_thrift_attribute_value_t(u32=mpls_in_label)
    attr1 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(oid=next_hop_id)
    attr2 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(booldata=nogal)
    attr3 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL,
                                            value=attr_value3)
    attr_list.append(attr3)


    attr_value4 = sai_thrift_attribute_value_t(u32=local_mep_id)
    attr4 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value4 = sai_thrift_attribute_value_t(s32=ccm_period)
    attr4 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_PERIOD,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(booldata=ccm_en)
    attr5 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE,
                                            value=attr_value5)
    attr_list.append(attr5)

    attr_value6 = sai_thrift_attribute_value_t(booldata=lm_en)
    attr6 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_ENABLE,
                                            value=attr_value6)
    attr_list.append(attr6)

    attr_value7 = sai_thrift_attribute_value_t(s32=lm_type)
    attr7 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_TYPE,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value8 = sai_thrift_attribute_value_t(booldata=dm_en)
    attr8 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_ENABLE,
                                            value=attr_value8)
    attr_list.append(attr8)

    attr_value9 = sai_thrift_attribute_value_t(u8=tx_cos)
    attr9 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS,
                                            value=attr_value9)
    attr_list.append(attr9)

    attr_value10 = sai_thrift_attribute_value_t(u8=tx_ttl)
    attr10 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_TTL,
                                            value=attr_value10)
    attr_list.append(attr10)


    return client.sai_thrift_create_y1731_session(attr_list)

def sai_thrift_create_y1731_tp_section_session(client, meg_oid, rif_oid, dir, local_mep_id, ccm_period, ccm_en, next_hop_id):

    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=meg_oid)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_MEG,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(oid=rif_oid)
    attr1 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,
                                            value=attr_value1)
    attr_list.append(attr1)    
    
    attr_value2 = sai_thrift_attribute_value_t(s32=dir)
    attr2 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DIR,
                                            value=attr_value2)
    attr_list.append(attr2)

    attr_value3 = sai_thrift_attribute_value_t(u32=local_mep_id)
    attr3 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID,
                                            value=attr_value3)
    attr_list.append(attr3)

    attr_value4 = sai_thrift_attribute_value_t(s32=ccm_period)
    attr4 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_PERIOD,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(booldata=ccm_en)
    attr5 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE,
                                            value=attr_value5)
    attr_list.append(attr5)


    attr_value6 = sai_thrift_attribute_value_t(oid=next_hop_id)
    attr6 = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID,
                                            value=attr_value6)
    attr_list.append(attr6)
    

    return client.sai_thrift_create_y1731_session(attr_list)


def sai_thrift_create_y1731_rmep(client, session_id, rmep_id, mac=None, aps_group=None, is_protection=None, protection_en=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=session_id)
    attr0 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=rmep_id)
    attr1 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID,
                                            value=attr_value1)
    attr_list.append(attr1)

    if( mac != None):
        attr_value2 = sai_thrift_attribute_value_t(mac=mac)
        attr2 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS,
                                            value=attr_value2)
        attr_list.append(attr2)

    if( aps_group != None):
        attr_value2 = sai_thrift_attribute_value_t(oid=aps_group)
        attr2 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,
                                            value=attr_value2)
        attr_list.append(attr2)


    if( is_protection != None):
        attr_value2 = sai_thrift_attribute_value_t(booldata=is_protection)
        attr2 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,
                                            value=attr_value2)
        attr_list.append(attr2)


    if( protection_en != None):
        attr_value2 = sai_thrift_attribute_value_t(booldata=protection_en)
        attr2 = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN,
                                            value=attr_value2)
        attr_list.append(attr2)

    return client.sai_thrift_create_y1731_rmep(attr_list)




def sai_thrift_send_hostif_packet(client, hostif_id, packet, oam_tx_type, host_if_tx_type, egress_port=None, oam_session=None, dm_offset=None, ptp_tx_op_type=None, sec=None, nsec=None):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=oam_tx_type)
    attr0 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_TX_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(s32=host_if_tx_type)
    attr1 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE,
                                            value=attr_value1)
    attr_list.append(attr1)

    if egress_port!=None:
        attr_value2 = sai_thrift_attribute_value_t(oid=egress_port)
        attr2 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG,
                                                value=attr_value2)
        attr_list.append(attr2)

    if oam_session!=None:
        attr_value2 = sai_thrift_attribute_value_t(oid=oam_session)
        attr2 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_CUSTOM_OAM_Y1731_SESSION_ID,
                                                value=attr_value2)
        attr_list.append(attr2)

    if dm_offset!=None:
        attr_value2 = sai_thrift_attribute_value_t(u32=dm_offset)
        attr2 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_CUSTOM_TIMESTAMP_OFFSET,
                                                value=attr_value2)
        attr_list.append(attr2)
        
    if ptp_tx_op_type!=None:
        attr_value2 = sai_thrift_attribute_value_t(s32=ptp_tx_op_type)
        attr2 = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_CUSTOM_PTP_TX_PACKET_OP_TYPE,
                                                value=attr_value2)
        attr_list.append(attr2)
    if sec!=None and nsec!=None:    
        attr_value = sai_thrift_attribute_value_t(timespec=sai_thrift_timespec_t(tv_sec=sec,tv_nsec=nsec))
        attr = sai_thrift_attribute_t(id=SAI_HOSTIF_PACKET_ATTR_TX_TIMESTAMP, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_send_hostif_packet(hostif_id, packet.encode('hex'), attr_list)


def sai_thrift_create_ptp(client, enable_type, device_type, drift_is_negative = 0, time_is_negative = 0, driftoffset = 0, timeoffset = 0, tod_foramt = 0, tod_leap_second = 0, tod_pps_status = 0, tod_pps_accuracy = 0, tod_mode = 2, tod_enable = False):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(s32=enable_type)
    attr0 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(s32=device_type)
    attr1 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = drift_is_negative, value = driftoffset))
    attr2 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET,
                                            value=attr_value2)
    attr_list.append(attr2)
    
    attr_value3 = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = time_is_negative, value = timeoffset))
    attr3 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,
                                            value=attr_value3)
    attr_list.append(attr3)
    
    attr_value4 = sai_thrift_attribute_value_t(s32=tod_foramt)
    attr4 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE,
                                            value=attr_value4)
    attr_list.append(attr4)

    attr_value5 = sai_thrift_attribute_value_t(s8=tod_leap_second)
    attr5 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND,
                                            value=attr_value5)
    attr_list.append(attr5)

    attr_value6 = sai_thrift_attribute_value_t(u8=tod_pps_status)
    attr6 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS,
                                            value=attr_value6)
    attr_list.append(attr6)

    attr_value7 = sai_thrift_attribute_value_t(u8=tod_pps_accuracy)
    attr7 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY,
                                            value=attr_value7)
    attr_list.append(attr7)

    attr_value10 = sai_thrift_attribute_value_t(s32=tod_mode)
    attr10 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE,
                                            value=attr_value10)
    attr_list.append(attr10)

    attr_value11 = sai_thrift_attribute_value_t(booldata=tod_enable)
    attr11 = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE,
                                            value=attr_value11)
    attr_list.append(attr11)

    return client.sai_thrift_create_ptp_domain(attr_list)

def sai_thrift_create_es(client, esi_label):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(u32=esi_label)
    attr0 = sai_thrift_attribute_t(id=SAI_ES_ATTR_ESI_LABEL,
                                            value=attr_value0)
    attr_list.append(attr0)

    return client.sai_thrift_create_es(attr_list)

# add by fangsl for SAI INT test


def config_vlan(client,vlan_num):

        stats_enable = 0
        vlan_oid_list = range(vlan_num)
        for a in range(2,vlan_num+2):
            sys_logging("###creat vlan id %d ###" %a)
            vlan_oid_list[a-2] = sai_thrift_create_vlan(client, a, stats_enable)
            sys_logging("###vlan_oid[%d] is %d ###" %(a-2,vlan_oid_list[a-2]))

        return vlan_oid_list


def config_port_vlan_member(client,port_oid,vlan_oid_list):

        num = len(vlan_oid_list)
        vlan_member_oid_list = range(num)
        for a in range(0,num):
            sys_logging("###creat port %d allow vlan %d ###" %(port_oid,vlan_oid_list[a]))
            vlan_member_oid_list[a] = sai_thrift_create_vlan_member(client, vlan_oid_list[a], port_oid, SAI_VLAN_TAGGING_MODE_TAGGED)
            sys_logging("###vlan_member_oid[%d] is %d ###" %(a,vlan_member_oid_list[a]))

        return vlan_member_oid_list

def config_fdb(client,vlan_oid_list,port_oid_list,num):

        mac_action = SAI_PACKET_ACTION_FORWARD
        vlan_oid = []
        port_oid = []
        dest_mac_list = []
        dmac_start = '00:02:03:04:'
        for i in range(num):
            dest_mac_list.append(dmac_start + str(i/25).zfill(2) + ':' + str((i%100)*4).zfill(2))
        for a in range(0,num):
            vlan_oid = vlan_oid_list[a]
            port_oid = port_oid_list[a]
            mac = dest_mac_list[a]
            print vlan_oid
            print port_oid
            print mac
            sys_logging("###creat fdb ###" )
            status = sai_thrift_create_fdb(client, vlan_oid, mac, port_oid, mac_action)
            sys_logging("###status = %d ###" %status)

        return status

def config_fdb_test(client,vlan_oid_list,macda,port_oid_list,num):

        mac_action = SAI_PACKET_ACTION_FORWARD
        vlan_oid = []
        port_oid = []

        for a in range(0,num):
            vlan_oid = vlan_oid_list[a]
            port_oid = port_oid_list[a]
            sys_logging("###creat fdb ###" )
            status = sai_thrift_create_fdb(client, vlan_oid, macda, port_oid, mac_action)
            sys_logging("###status = %d ###" %status)

        return status



def config_stp_instance(client,stp_oid,vlan_oid_list):

        for a in vlan_oid_list:
            attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            client.sai_thrift_set_vlan_attribute(a, attr)


def delete_vlan(client,vlan_oid_list):

        for a in vlan_oid_list:
            client.sai_thrift_remove_vlan(a)



def delete_port_vlan_member(client,vlan_member_list):

        for a in vlan_member_list:
            sys_logging("### delete vlan member %d ###" %a)
            client.sai_thrift_remove_vlan_member(a)

def delete_fdb(client,vlan_oid_list,port_oid_list,num):

        vlan_oid = []
        dest_mac_list = []
        dmac_start = '00:02:03:04:'
        for i in range(num):
            dest_mac_list.append(dmac_start + str(i/25).zfill(2) + ':' + str((i%100)*4).zfill(2))
        for a in range(0,num):
            vlan_oid = vlan_oid_list[a]
            port_oid = port_oid_list[a]
            mac = dest_mac_list[a]
            sys_logging("###delete fdb ###" )
            status = sai_thrift_delete_fdb(client, vlan_oid, mac, port_oid)
            sys_logging("###status = %d ###" %status)

        return status


def flush_all_fdb(client):

        fdb_attr_list = []
        fdb_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
        fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_attribute1_value)
        fdb_attr_list.append(fdb_attribute1)
        sys_logging("###flush fdb ###" )
        status = client.sai_thrift_flush_fdb_entries(fdb_attr_list)


def create_vrfs(client, num):
    vrf_oid_list = []
    vrf_oid = sai_thrift_get_default_router_id(client)
    sys_logging("###vrf_oid[0] is 0x%x ###" %vrf_oid)
    vrf_oid_list.append(vrf_oid)
    for i in range(1,num):
        vrf_oid = sai_thrift_create_virtual_router(client, 1, 1)
        sys_logging("###vrf_oid[%d] is 0x%x ###" %(i,vrf_oid))
        vrf_oid_list.append(vrf_oid)
    return vrf_oid_list

def remove_vrfs(client, vrf_oid_list):
    vrf_num = len(vrf_oid_list)
    for i in range(1,vrf_num):
        client.sai_thrift_remove_virtual_router(vrf_oid_list[i])

def create_vlan_ifs(client, vlanif_num,vrf_oid_list,vlan_oid_list):
    vrf_num = len(vrf_oid_list)
    vlanif_oid_list = []
    per_vrf_vlanif_num = vlanif_num/vrf_num
    for i in range(vlanif_num):
        j = i/per_vrf_vlanif_num
        vlan_if_oid = sai_thrift_create_router_interface(client, vrf_oid_list[j], SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid_list[i], 1, 1, '', stats_state = False)
        sys_logging("###vlanif_oid[%d] is 0x%x ###" %(i,vlan_if_oid))
        vlanif_oid_list.append(vlan_if_oid)
    return vlanif_oid_list

def remove_vlan_ifs(client, vlanif_oid_list):
    for i in vlanif_oid_list:

        client.sai_thrift_remove_router_interface(i)

def create_neighbors(client, rif_oid_list, arp_num):
    #rif_num = len(rif_oid_list)
    ipv4_addr_list = []
    ipv6_addr_list = []
    dest_mac_list = []
    addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
    addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
    dmac_start = '00:02:03:04:'
    for i in range(arp_num/2):
        dest_mac_list.append(dmac_start + str(i/100).zfill(2) + ':' + str(i%100).zfill(2))

    for i in range(arp_num/8):
        for j in range(1,5):
            ipv4_addr_list.append(integer_to_ip4(i*256+j))
            ipv6_addr_list.append(integer_to_ip6(i*(2**16)+j))
    for i in range(arp_num/2):
        sai_thrift_create_neighbor(client, addr_family1, rif_oid_list[i/4], ipv4_addr_list[i], dest_mac_list[i])
        sai_thrift_create_neighbor(client, addr_family2, rif_oid_list[i/4], ipv6_addr_list[i], dest_mac_list[i])


def remove_neighbors(client, rif_oid_list, arp_num):
    #rif_num = len(rif_oid_list)
    ipv4_addr_list = []
    ipv6_addr_list = []
    dest_mac_list = []
    addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
    addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
    dmac_start = '00:02:03:04:'
    for i in range(arp_num/2):
       dest_mac_list.append(dmac_start + str(i/100).zfill(2) + ':' + str(i%100).zfill(2))

    for i in range(arp_num/8):
        for j in range(1,5):
            ipv4_addr_list.append(integer_to_ip4(i*256+j))
            ipv6_addr_list.append(integer_to_ip6(i*(2**16)+j))
    for i in range(arp_num/2):
        sai_thrift_remove_neighbor(client, addr_family1, rif_oid_list[i/4], ipv4_addr_list[i], dest_mac_list[i])
        sai_thrift_remove_neighbor(client, addr_family2, rif_oid_list[i/4], ipv6_addr_list[i], dest_mac_list[i])

def create_nexthops(client, rif_oid_list, arp_num):
    #rif_num = len(rif_oid_list)
    ipv4_addr_list = []
    ipv6_addr_list = []
    dest_mac_list = []
    nhop_oid_list = []
    addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
    addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
    dmac_start = '00:02:03:04:'

    for i in range(arp_num/8):
        for j in range(1,5):
            ipv4_addr_list.append(integer_to_ip4(i*256+j))
            ipv6_addr_list.append(integer_to_ip6(i*(2**16)+j))

    for i in range(arp_num/2):
        nexthop_oid = sai_thrift_create_nhop(client, addr_family1, ipv4_addr_list[i], rif_oid_list[i/4])
        nhop_oid_list.append(nexthop_oid)
        nexthop_oid = sai_thrift_create_nhop(client, addr_family2, ipv6_addr_list[i], rif_oid_list[i/4])
        nhop_oid_list.append(nexthop_oid)
    return nhop_oid_list

def remove_nexthops(client, nhop_oid_list):
    for i in nhop_oid_list:

        client.sai_thrift_remove_next_hop(i)

def create_routes(client, nhop_oid_list, vrf_oid_list):
    nexthop_num = len(nhop_oid_list)
    ipv4_addr_list = []
    host_ipv4_addr_list = []
    ipv6_addr_list = []
    host_ipv6_addr_list = []
    dest_mac_list = []
    addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
    addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
    ip_mask_v4 = '255.255.255.0'
    ip_mask_v4_host = '255.255.255.255'
    ip_mask_v6 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0000'
    ip_mask_v6_host = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'



    for i in range(nexthop_num/2):
        ipv4_addr_list.append(integer_to_ip4(10*(2**24)+10*(2**16)+i*256)) #10.10.i.0/24
        ipv4_addr_list.append(integer_to_ip4(20*(2**24)+10*(2**16)+i*256)) #20.10.i.0/24
        host_ipv4_addr_list.append(integer_to_ip4(10*(2**24)+20*(2**16)+i)) #10.20.0.i/32
        host_ipv4_addr_list.append(integer_to_ip4(20*(2**24)+20*(2**16)+i)) #20.20.0.i/32
        ipv6_addr_list.append(integer_to_ip6(16*(2**32)+i*(2**16))) #::0010:i:0/112
        ipv6_addr_list.append(integer_to_ip6(32*(2**32)+i*(2**16))) #::0020:i:0/112
        host_ipv6_addr_list.append(integer_to_ip6(16*(2**32)+i))    #::0010:0:i/128
        host_ipv6_addr_list.append(integer_to_ip6(32*(2**32)+i))    #::0020:0:i/128

    a =0
    for i in range(nexthop_num/2):
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family1, ipv4_addr_list[a], ip_mask_v4, nhop_oid_list[2*i])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family1, host_ipv4_addr_list[a], ip_mask_v4_host, nhop_oid_list[2*i])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family2, ipv6_addr_list[a], ip_mask_v6, nhop_oid_list[2*i+1])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family2, host_ipv6_addr_list[a], ip_mask_v6_host, nhop_oid_list[2*i+1])
        a = a+1
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family1, ipv4_addr_list[a], ip_mask_v4, nhop_oid_list[2*i])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family1, host_ipv4_addr_list[a], ip_mask_v4_host, nhop_oid_list[2*i])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family2, ipv6_addr_list[a], ip_mask_v6, nhop_oid_list[2*i+1])
        sai_thrift_create_route(client, vrf_oid_list[i/16], addr_family2, host_ipv6_addr_list[a], ip_mask_v6_host, nhop_oid_list[2*i+1])
        a = a+1

def remove_routes(client, nhop_oid_list, vrf_oid_list):
    nexthop_num = len(nhop_oid_list)
    ipv4_addr_list = []
    host_ipv4_addr_list = []
    ipv6_addr_list = []
    host_ipv6_addr_list = []
    dest_mac_list = []
    addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
    addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
    ip_mask_v4 = '255.255.255.0'
    ip_mask_v4_host = '255.255.255.255'
    ip_mask_v6 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0000'
    ip_mask_v6_host = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'



    for i in range(nexthop_num/2):
        ipv4_addr_list.append(integer_to_ip4(10*(2**24)+10*(2**16)+i*256)) #10.10.i.0/24
        ipv4_addr_list.append(integer_to_ip4(20*(2**24)+10*(2**16)+i*256)) #20.10.i.0/24
        host_ipv4_addr_list.append(integer_to_ip4(10*(2**24)+20*(2**16)+i)) #10.20.0.i/32
        host_ipv4_addr_list.append(integer_to_ip4(20*(2**24)+20*(2**16)+i)) #20.20.0.i/32
        ipv6_addr_list.append(integer_to_ip6(16*(2**32)+i*(2**16))) #::0010:i:0/112
        ipv6_addr_list.append(integer_to_ip6(32*(2**32)+i*(2**16))) #::0020:i:0/112
        host_ipv6_addr_list.append(integer_to_ip6(16*(2**32)+i))    #::0010:0:i/128
        host_ipv6_addr_list.append(integer_to_ip6(32*(2**32)+i))    #::0020:0:i/128

    a =0
    for i in range(nexthop_num/2):
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family1, ipv4_addr_list[a], ip_mask_v4, nhop_oid_list[2*i])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family1, host_ipv4_addr_list[a], ip_mask_v4_host, nhop_oid_list[2*i])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family2, ipv6_addr_list[a], ip_mask_v6, nhop_oid_list[2*i+1])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family2, host_ipv6_addr_list[a], ip_mask_v6_host, nhop_oid_list[2*i+1])
        a = a+1
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family1, ipv4_addr_list[a], ip_mask_v4, nhop_oid_list[2*i])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family1, host_ipv4_addr_list[a], ip_mask_v4_host, nhop_oid_list[2*i])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family2, ipv6_addr_list[a], ip_mask_v6, nhop_oid_list[2*i+1])
        sai_thrift_remove_route(client, vrf_oid_list[i/16], addr_family2, host_ipv6_addr_list[a], ip_mask_v6_host, nhop_oid_list[2*i+1])
        a = a+1

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))


def sai_thrift_create_syncE(client, recovered_port = 0, clock_divider = 0):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=recovered_port)
    attr0 = sai_thrift_attribute_t(id=SAI_SYNCE_ATTR_RECOVERED_PORT,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u16=clock_divider)
    attr1 = sai_thrift_attribute_t(id=SAI_SYNCE_ATTR_CLOCK_DIVIDER,
                                            value=attr_value1)
    attr_list.append(attr1)


    return client.sai_thrift_create_synce(attr_list)

#QoS
def sai_thrift_qos_create_policer(client,
                                   meter_type, mode, color_source, 
                                   cir, cbs, pir, pbs, 
                                   green_act, yellow_act, red_act, act_valid = [], stats_en_list = None):
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
        if (SAI_POLICER_MODE_STORM_CONTROL != mode)and(None!=color_source):  
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
            attr_value = sai_thrift_attribute_value_t(s32=green_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_GREEN_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)

        #set yellow action
        if act_valid[1]:
            attr_value = sai_thrift_attribute_value_t(s32=yellow_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_YELLOW_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)

        #set red action
        if act_valid[2]:
            attr_value = sai_thrift_attribute_value_t(s32=red_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)
            
        if stats_en_list != None:
            attr_value_list = sai_thrift_s32_list_t(count=len(stats_en_list), s32list=stats_en_list)
            attr_value = sai_thrift_attribute_value_t(s32list=attr_value_list)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_ENABLE_COUNTER_LIST, value=attr_value)
            attr_list.append(attr)

        #create policer id
        return client.sai_thrift_create_policer(attr_list)
        
def sai_thrift_qos_create_wred(client, color_en = [None]*3, min_thrd = [None]*3, max_thrd = [None]*3, drop_prob = [None]*3, ecn_thrd = [None]*3):
    attr_list = []

    #0:green,1:yellow,2:red
    for i in range(3):
        attr_shift = i*4
        attr_shift2 = i*3
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
        if ecn_thrd[i]:
            attr_value = sai_thrift_attribute_value_t(u32=ecn_thrd[i])
            attr = sai_thrift_attribute_t(id=(SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD+attr_shift2), value=attr_value)
            attr_list.append(attr)
         

    return client.sai_thrift_create_wred_profile(attr_list) 
    
def sai_thrift_create_queue_id(client, queue_type, port, index, wred_id=0, parent_id=0, service_id=0, buffer_id=0, sche_id=0, pfc_dldr_en=0):
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
        
    if service_id:
        attr_value = sai_thrift_attribute_value_t(u16=service_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SERVICE_ID, value=attr_value)
        attr_list.append(attr)
        
    if parent_id:
        attr_value = sai_thrift_attribute_value_t(oid=parent_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        attr_list.append(attr)

    if buffer_id:
        attr_value = sai_thrift_attribute_value_t(oid=buffer_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        attr_list.append(attr)

    if sche_id:
        attr_value = sai_thrift_attribute_value_t(oid=sche_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        attr_list.append(attr)

    if pfc_dldr_en:
        attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_en)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_queue(attr_list)
    
def sai_thrift_qos_create_buffer_profile(client, 
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
        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

    if dynamic_th:
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)        

    if xon_th:
        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr) 

    if xoff_th:
        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_buffer_profile(attr_list)

def sai_thrift_qos_create_scheduler_profile(client,
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
    
def sai_thrift_qos_create_scheduler_group(client, 
                                           port_id, 
                                           level, 
                                           max_childs, 
                                           parent_id, 
                                           sched_id = 0,
                                           service_id = 0):
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
        
    if service_id :
        attr_value = sai_thrift_attribute_value_t(u16=service_id)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_scheduler_group(attr_list)

def sai_thrift_monitor_create_buffer(client, port, threshold_min = 150000, threshold_max =  300000, ingr_port_perio_monitor_enable = False, egr_port_perio_monitor_enable = False ):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=port)
    attr0 = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT,
                                            value=attr_value0)
    attr_list.append(attr0)

    attr_value1 = sai_thrift_attribute_value_t(u32=threshold_min)
    attr1 = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD,
                                            value=attr_value1)
    attr_list.append(attr1)

    attr_value2 = sai_thrift_attribute_value_t(u32=threshold_max)
    attr2 = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD,
                                            value=attr_value2)
    attr_list.append(attr2)
    
    attr_value3 = sai_thrift_attribute_value_t(booldata=ingr_port_perio_monitor_enable)
    attr3 = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE,
                                            value=attr_value3)
    attr_list.append(attr3)
    
    attr_value4 = sai_thrift_attribute_value_t(booldata=egr_port_perio_monitor_enable)
    attr4 = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE,
                                            value=attr_value4)
    attr_list.append(attr4)    
    print attr_list
    return client.sai_thrift_create_monitor_buffer(attr_list)


def sai_thrift_monitor_create_latency(client, port, microburst_event, monitor_discard, micorburst_enable = False, perio_monitor_enable = False ):
    attr_list = []

    attr_value0 = sai_thrift_attribute_value_t(oid=port)
    attr0 = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT,
                                            value=attr_value0)
    attr_list.append(attr0)

    microburst_event1 = sai_thrift_bool_list_t(count=len(microburst_event), boollist=microburst_event)
    attr_value1 = sai_thrift_attribute_value_t(boollist=microburst_event1)
    attr1 = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT, 
                                            value=attr_value1)
    attr_list.append(attr1)
    
    monitor_discard2 = sai_thrift_bool_list_t(count=len(monitor_discard), boollist=monitor_discard)
    attr_value2 = sai_thrift_attribute_value_t(boollist=monitor_discard2)
    attr2 = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD, 
                                            value=attr_value2)
    attr_list.append(attr2) 
    
    attr_value3 = sai_thrift_attribute_value_t(booldata=micorburst_enable)
    attr3 = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE,
                                            value=attr_value3)
    attr_list.append(attr3)
    
    attr_value4 = sai_thrift_attribute_value_t(booldata=perio_monitor_enable)
    attr4 = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE,
                                            value=attr_value4)
    attr_list.append(attr4)
    
    print attr_list
    return client.sai_thrift_create_monitor_latency(attr_list)

def sai_thrift_get_wtd_factor(client, dynamic_th):

    threshold = (dynamic_th+7)
    f = 0.0

    if threshold == 0:
        f = (1.0/128)
    elif threshold == 1:
        f = (1.0/64)
    elif threshold == 2:
        f = (1.0/32)
    elif threshold == 3:
        f = (1.0/16)
    elif threshold == 4:
        f = (1.0/8)
    elif threshold == 5:
        f = (1.0/4)
    elif threshold == 6:
        f = (1.0/2)
    elif threshold == 7:
        f = 1.0
    elif threshold == 8:
        f = 2.0
    elif threshold == 9:
        f = 4.0
    elif threshold == 10:
        f = 8.0

    factor = (f/(1.0+f))
    return factor

def sai_thrift_get_remain_cnt(client, sc_thrd=0, sc_cnt=0):

    #read DsErmScThrd 0
    #sc_thrd = 1536
    #read DsErmScCnt 0
    #sc_cnt = 0

    remain_cnt = sc_thrd - sc_cnt
    return remain_cnt


