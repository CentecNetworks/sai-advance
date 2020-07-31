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
Thrift SAI VLAN interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *


class func_01_create_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create vlan###")
        
        switch_init(self.client)
        first_vlan_oid = 8589934630
        vlan_id = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("###vlan_oid1 = %d###" %vlan_oid1)             
        warmboot(self.client)
        try:
            if vlan_oid1 != first_vlan_oid:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            
class func_02_create_same_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create samevlan###")
        
        switch_init(self.client)
        vlan_id = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("###vlan_oid2 = %d###" %vlan_oid2)             
        warmboot(self.client)
        try:
            if vlan_oid2 != 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
class func_03_create_max_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create max vlan###")
        
        switch_init(self.client)
        stats_enable = 0
        vlan_oid = [0 for i in range(0,4096)]
        for a in range(2,4095):
            sys_logging("###creat vlan id %d ###" %a) 
            vlan_oid[a] = sai_thrift_create_vlan(self.client, a, stats_enable)
            sys_logging("###vlan_oid =%d ###" %vlan_oid[a])
        warmboot(self.client)
        try:
            sys_logging("###creat vlan id 4095 ###") 
            vlan_oid[4095] = sai_thrift_create_vlan(self.client, 4095, stats_enable)
            sys_logging("###vlan 4095 oid =%d ###" %vlan_oid[4095])
            if vlan_oid[4095] != 0:
                raise NotImplementedError()
        finally:
            for a in range(2,4095):
                sys_logging("###remove vlan %d###" %a)
                self.client.sai_thrift_remove_vlan(vlan_oid[a])            
            
            
class func_04_remove_vlan_fn (sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###remove vlan###")
        
        switch_init(self.client)
        vlan_id = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("###vlan_oid1 = %d###" %vlan_oid1)             
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_vlan(vlan_oid1)            
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()
        finally:
            sys_logging("###status = %d###" %status)
            
            
class func_05_remove_not_exist_vlan_fn (sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###remove not exist vlan###")
        not_exist_vlan_oid = 8589934631
        switch_init(self.client)         
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_vlan(not_exist_vlan_oid)            
            if status == SAI_STATUS_SUCCESS:
                raise NotImplementedError()
        finally:
            sys_logging("###status = %d###" %status)            
            
            
            
class func_06_set_and_get_vlan_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
              
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_VLAN_ID:
                    sys_logging("###SAI_VLAN_ATTR_VLAN_ID = %d ###" %a.value.u16)
                    if vlan_id != a.value.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
           
            
class func_06_set_and_get_vlan_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
                
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MEMBER_LIST:
                    sys_logging("###SAI_VLAN_ATTR_MEMBER_LIST count = %d ###" %a.value.objlist.count)
                    if 1 != a.value.objlist.count:
                        raise NotImplementedError()
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_VLAN_ATTR_MEMBER_LIST = %d ###" %b)
                        if vlan_member1 != b:
                            raise NotImplementedError()          
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)            
            
            
class func_06_set_and_get_vlan_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
              
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
                sys_logging("###SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                if 0 != a.value.u32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            value = 1234
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    if value != a.value.u32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)          
            
            
class func_06_set_and_get_vlan_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        default_stp_oid = 16        
        
        vlan_list1 = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list1)
        
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_STP_INSTANCE:
                sys_logging("###SAI_VLAN_ATTR_STP_INSTANCE = %d ###" %a.value.oid)
                if default_stp_oid != a.value.oid:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_STP_INSTANCE:
                    sys_logging("###SAI_VLAN_ATTR_STP_INSTANCE = %d ###" %a.value.oid)
                    if stp_oid != a.value.oid:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)            
            
            
class func_06_set_and_get_vlan_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_LEARN_DISABLE:
                sys_logging("###SAI_VLAN_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                if 0 != a.value.booldata:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_VLAN_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)      

            
class func_06_set_and_get_vlan_attribute_fn_5(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if 0 != a.value.s32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(s32=2)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("###SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if 2 != a.value.s32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)             
            
            
class func_06_set_and_get_vlan_attribute_fn_6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if 0 != a.value.s32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(s32=3)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("###SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if 3 != a.value.s32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)               
            
            
# Wait ACL design finish           
#class func_06_set_and_get_vlan_attribute_fn_7(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_INGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,            
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_INGRESS_ACL:
#                sys_logging("###SAI_VLAN_ATTR_INGRESS_ACL = %d ###" %a.value.oid)
#                if SAI_NULL_OBJECT_ID != a.value.oid:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_INGRESS_ACL:
#                    sys_logging("###SAI_VLAN_ATTR_INGRESS_ACL = %d ###" %a.value.oid)
#                    if acl_table_id != a.value.oid:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)             
#            
#            
#            
#            
#class func_06_set_and_get_vlan_attribute_fn_8(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_EGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_EGRESS_ACL:
#                sys_logging("###SAI_VLAN_ATTR_EGRESS_ACL = %d ###" %a.value.oid)
#                if SAI_NULL_OBJECT_ID != a.value.oid:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_EGRESS_ACL, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_EGRESS_ACL:
#                    sys_logging("###SAI_VLAN_ATTR_EGRESS_ACL = %d ###" %a.value.oid)
#                    if acl_table_id != a.value.oid:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_EGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)                 
#            
#            
#            
#class func_06_set_and_get_vlan_attribute_fn_9(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_INGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#                        
#        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#        status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#        sys_logging("###status = %d###" %status) 
#        if status != SAI_STATUS_SUCCESS:
#            raise NotImplementedError()
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_META_DATA:
#                sys_logging("###SAI_VLAN_ATTR_META_DATA = %d ###" %a.value.u32)
#                if 0 != a.value.u32:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(u32=254)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_META_DATA, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_META_DATA:
#                    sys_logging("###SAI_VLAN_ATTR_META_DATA = %d ###" %a.value.u32)
#                    if 254 != a.value.u32:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)             
            
 


class func_06_set_and_get_vlan_attribute_fn_10(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                sys_logging("###SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                if 0 != a.value.s32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if 1 != a.value.s32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 





class func_06_set_and_get_vlan_attribute_fn_11(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                sys_logging("###SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                if 0 != a.value.s32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if 1 != a.value.s32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 






class func_06_set_and_get_vlan_attribute_fn_12(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                sys_logging("###SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                if 0 != a.value.s32:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if 1 != a.value.s32:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 






class func_06_set_and_get_vlan_attribute_fn_13(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_attribute###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
                sys_logging("###SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = %d ###" %a.value.booldata)
                if 0 != a.value.booldata:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
                    sys_logging("###SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = %d ###" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 





class func_07_create_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_vlan_member###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        warmboot(self.client)
        try:
            vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            sys_logging("###vlan_member1 oid = %d ###" %vlan_member1)
            if SAI_NULL_OBJECT_ID == vlan_member1:
                raise NotImplementedError()         
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid) 


            
class func_08_create_same_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_same_vlan_member###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("###vlan_member1 oid = %d ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("###vlan_member2 oid = %d ###" %vlan_member2)
        warmboot(self.client)
        try:
            if SAI_NULL_OBJECT_ID == vlan_member1:
                raise NotImplementedError()   
            if vlan_member1 != vlan_member2:
                raise NotImplementedError()                  
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid) 



class func_09_remove_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###remove_vlan_member###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_vlan_member(vlan_member1)
            sys_logging("###status = %d ###" %status)
            if SAI_STATUS_SUCCESS != status:
                raise NotImplementedError()         
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 

            
class func_10_remove_not_exist_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###remove_not_exist_vlan_member###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)        
        not_exist_vlan_member = 131111
        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_vlan_member(not_exist_vlan_member)
            sys_logging("###status = %d ###" %status)
            if SAI_STATUS_SUCCESS == status:
                raise NotImplementedError()         
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 



            
class func_11_set_and_get_vlan_member_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_member_attribute###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
                
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_ID:
                    sys_logging("###SAI_VLAN_MEMBER_ATTR_VLAN_ID  = %d ###" %a.value.oid)
                    if vlan_oid != a.value.oid:
                        raise NotImplementedError()                      
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)  



class func_11_set_and_get_vlan_member_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_member_attribute###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        bport_id = sai_thrift_get_bridge_port_by_port(self.client, port1)       
         
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID:
                    sys_logging("###SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID  = %d ###" %a.value.oid)
                    if bport_id != a.value.oid:
                        raise NotImplementedError()                      
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid) 




class func_11_set_and_get_vlan_member_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_vlan_member_attribute###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        tag_mode = SAI_VLAN_TAGGING_MODE_UNTAGGED
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, tag_mode)       
         
        attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE:
                sys_logging("###SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE  = %d ###" %a.value.s32)
                if tag_mode != a.value.s32:
                    raise NotImplementedError()     
        warmboot(self.client)
        try:
            tag_mode = SAI_VLAN_TAGGING_MODE_TAGGED
            attr_value = sai_thrift_attribute_value_t(s32=tag_mode)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, value=attr_value)
            self.client.sai_thrift_set_vlan_member_attribute(vlan_member1, attr)
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE:
                    sys_logging("###SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE  = %d ###" %a.value.s32)
                    if tag_mode != a.value.s32:
                        raise NotImplementedError()                        
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid) 





  
class func_12_get_vlan_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###get_vlan_stats###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS, SAI_VLAN_STAT_IN_UCAST_PKTS]
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
           
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)
        
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)  



class func_13_get_vlan_stats_ext_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###clear_vlan_stats###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS, SAI_VLAN_STAT_IN_UCAST_PKTS]
            mode = SAI_STATS_MODE_READ
            list1 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
           
            list2 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)
            
            list3 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            sys_logging("###list3[0]= %d###" %list3[0])
            sys_logging("###list3[1]= %d###" %list3[1])
            sys_logging("###list3[2]= %d###" %list3[2])
            sys_logging("###list3[3]= %d###" %list3[3])            
            assert (list3[0] == 104)
            assert (list3[1] == 1)
            assert (list3[2] == 104)
            assert (list3[3] == 1)
            
            status = self.client.sai_thrift_clear_vlan_stats(vlan_oid1, counter_ids, 5)

            list4 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            sys_logging("###list4[0]= %d###" %list4[0])
            sys_logging("###list4[1]= %d###" %list4[1])
            sys_logging("###list4[2]= %d###" %list4[2])
            sys_logging("###list4[3]= %d###" %list4[3])            
            assert (list4[0] == 0)
            assert (list4[1] == 0)
            assert (list4[2] == 0)
            assert (list4[3] == 0)
            
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)


class func_13_get_vlan_stats_ext_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###clear_vlan_stats###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS, SAI_VLAN_STAT_IN_UCAST_PKTS]
            mode = SAI_STATS_MODE_READ_AND_CLEAR
            list1 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
           
            list2 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)
            
            list3 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            sys_logging("###list3[0]= %d###" %list3[0])
            sys_logging("###list3[1]= %d###" %list3[1])
            sys_logging("###list3[2]= %d###" %list3[2])
            sys_logging("###list3[3]= %d###" %list3[3])            
            assert (list3[0] == 0)
            assert (list3[1] == 0)
            assert (list3[2] == 0)
            assert (list3[3] == 0)
                   
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)



class func_14_clear_vlan_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###clear_vlan_stats###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS, SAI_VLAN_STAT_IN_UCAST_PKTS]
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
           
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)
            
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list3[0]= %d###" %list3[0])
            sys_logging("###list3[1]= %d###" %list3[1])
            sys_logging("###list3[2]= %d###" %list3[2])
            sys_logging("###list3[3]= %d###" %list3[3])            
            assert (list3[0] == 104)
            assert (list3[1] == 1)
            assert (list3[2] == 104)
            assert (list3[3] == 1)
            
            status = self.client.sai_thrift_clear_vlan_stats(vlan_oid1, counter_ids, 5)

            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5) 
            sys_logging("###list4[0]= %d###" %list4[0])
            sys_logging("###list4[1]= %d###" %list4[1])
            sys_logging("###list4[2]= %d###" %list4[2])
            sys_logging("###list4[3]= %d###" %list4[3])            
            assert (list4[0] == 0)
            assert (list4[1] == 0)
            assert (list4[2] == 0)
            assert (list4[3] == 0)
            
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)


 
class func_15_create_and_remove_vlan_members_fn_mode(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_vlan_members###")
        
        switch_init(self.client)
               
        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        
        vlan_oid_list = [vlan_oid1,vlan_oid2,vlan_oid3,vlan_oid4]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        tagging_mode_list = [0,0,0,0]
       
        sys_logging("###create 4 vlan member###")
        results =  sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list, 4, 0)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:            
            for object_id in object_id_list:
                assert( object_id != SAI_NULL_OBJECT_ID ) 
            for status in statuslist:
                assert( status == SAI_STATUS_SUCCESS )    
            sys_logging("###remove 4 vlan member###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list, 0)            
            for status in statuslist1:
                assert( status == SAI_STATUS_SUCCESS )             
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)            
            self.client.sai_thrift_remove_vlan(vlan_oid4)             

            
            
            
class func_15_create_and_remove_vlan_members_fn_mode_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_vlan_members_mode_0###")
        
        switch_init(self.client)
               
        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        
        vlan_oid_fail = vlan_oid3 + 1
        
        vlan_oid_list = [vlan_oid1,vlan_oid2,vlan_oid_fail,vlan_oid4]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        tagging_mode_list = [0,0,0,0]
       
        sys_logging("###create 4 vlan member, and 3rd is fail ###")
        results =  sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list, 4, 0)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:
            assert( object_id_list[0] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[1] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[2] == SAI_NULL_OBJECT_ID )  
            assert( object_id_list[3] == SAI_NULL_OBJECT_ID ) 
            
            assert( statuslist[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist[2] != SAI_STATUS_SUCCESS ) 
            assert( statuslist[3] == SAI_STATUS_NOT_EXECUTED )             

            sys_logging("###remove 4 vlan member, and 3rd is fail ###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list, 0)
            
            assert( statuslist1[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist1[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID ) 
            assert( statuslist1[3] == SAI_STATUS_NOT_EXECUTED ) 
            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)            
            self.client.sai_thrift_remove_vlan(vlan_oid4)
            
            
            
            
            
            
class func_15_create_and_remove_vlan_members_fn_mode_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_vlan_members_mode_1###")
        
        switch_init(self.client)
               
        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        
        vlan_oid_fail = vlan_oid3 + 1
        
        vlan_oid_list = [vlan_oid1,vlan_oid2,vlan_oid_fail,vlan_oid4]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        tagging_mode_list = [0,0,0,0]
       
        sys_logging("###create 4 vlan member, and 3rd is fail ###")
        results =  sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list, 4, 1)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:
            assert( object_id_list[0] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[1] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[2] == SAI_NULL_OBJECT_ID )  
            assert( object_id_list[3] != SAI_NULL_OBJECT_ID ) 
            
            assert( statuslist[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist[2] != SAI_STATUS_SUCCESS ) 
            assert( statuslist[3] == SAI_STATUS_SUCCESS )             

            sys_logging("###remove 4 vlan member, and 3rd is fail ###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list, 1)
            
            assert( statuslist1[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist1[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID ) 
            assert( statuslist1[3] == SAI_STATUS_SUCCESS ) 
            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)            
            self.client.sai_thrift_remove_vlan(vlan_oid4)            
            
                       

class func_16_create_vlan_with_stats_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_vlan_with_stats_disable###")
        
        switch_init(self.client)
        
        vlan_id = 100
        stats_enable = 0
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id, stats_enable)
              
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                sys_logging("###SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                if  0!= a.value.booldata:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("###SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if value != a.value.booldata:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)   
            

class func_17_create_vlan_and_set_stats_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_vlan_and_set_stats_disable###")
        
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
              
                    
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                sys_logging("###SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                if  1!= a.value.booldata:
                    raise NotImplementedError()
        warmboot(self.client)
        try:
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("###SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if value != a.value.booldata:
                        raise NotImplementedError()            
        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)             
 
 


  
class func_18_create_vlan_and_set_stats_01(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_vlan_and_set_stats_01###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        sys_logging("### vlan stats control is default enable ###")
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS]
            
            sys_logging("###step1: do not send packet, so all stats is zero ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            sys_logging("###step2: send packet, so all stats is not zero ###")            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
          
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)
            
            sys_logging("###step3: disable vlan stats and send packet, all stats is zero ###")
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0]) 
            
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list3[0]= %d###" %list3[0])
            sys_logging("###list3[1]= %d###" %list3[1])
            sys_logging("###list3[2]= %d###" %list3[2])
            sys_logging("###list3[3]= %d###" %list3[3])
            assert (list3[0] == 0)
            assert (list3[1] == 0)
            assert (list3[2] == 0)
            assert (list3[3] == 0)

            sys_logging("###step4: enable vlan stats and send packet, all stats is not zero ###")
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])
            
            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)            
            sys_logging("###list4[0]= %d###" %list4[0])
            sys_logging("###list4[1]= %d###" %list4[1])
            sys_logging("###list4[2]= %d###" %list4[2])
            sys_logging("###list4[3]= %d###" %list4[3])
            assert (list4[0] == 104)
            assert (list4[1] == 1)
            assert (list4[2] == 104)
            assert (list4[3] == 1)            
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)  
            
            
            
class func_18_create_vlan_and_set_stats_02(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_vlan_and_set_stats###")
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        sys_logging("### vlan stats control is disable ###")
        stats_enable = 0
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1, stats_enable)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2, stats_enable)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64,
                                pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64,
                                pktlen=100)                                                                                                    
        warmboot(self.client)
        try:    
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS, SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS]
            
            sys_logging("###step1: all stats is zero ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            
            sys_logging("###step2: send packet but vlan stats is disable, so all stats is zero ###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])  
           
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])            
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
            
            sys_logging("###step3: enable vlan stats and send packet, so all stats is not zero ###")
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0]) 
            
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            sys_logging("###list3[0]= %d###" %list3[0])
            sys_logging("###list3[1]= %d###" %list3[1])
            sys_logging("###list3[2]= %d###" %list3[2])
            sys_logging("###list3[3]= %d###" %list3[3])
            assert (list3[0] == 104)
            assert (list3[1] == 1)
            assert (list3[2] == 104)
            assert (list3[3] == 1)

            sys_logging("###step4: disable vlan stats and send packet, all stats is  zero ###")
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])
            
            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)            
            sys_logging("###list4[0]= %d###" %list4[0])
            sys_logging("###list4[1]= %d###" %list4[1])
            sys_logging("###list4[2]= %d###" %list4[2])
            sys_logging("###list4[3]= %d###" %list4[3])
            assert (list4[0] == 0)
            assert (list4[1] == 0)
            assert (list4[2] == 0)
            assert (list4[3] == 0)            
        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)  
                       
            



class scenario_01_access_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        
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
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
        
        
class scenario_02_trunk_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("trunk port to trunk port")
        
        switch_init(self.client)
        
        vlan_id1 = 100
        vlan_id2 = 200
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)       
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED) 
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=200,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            
            
class scenario_03_hybrid_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("hybrid port to hybrid port")
        
        switch_init(self.client)
        
        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED) 
        vlan_member5 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member6 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac2, port2, mac_action)
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=200,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=300,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=104)                                
        exp_pkt2 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=100)
        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets( str(exp_pkt2), [1], 1)
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac2, port2)           
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan_member(vlan_member5)
            self.client.sai_thrift_remove_vlan_member(vlan_member6)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)            
            self.client.sai_thrift_remove_vlan(vlan_oid3)            
            
            
class scenario_04_stp_rstp(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_list = [10]
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###state 1 mean forward###")
        state = 1
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###stp port state is forwarding, all packets should be forward###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])

            sys_logging("###state 2 mean block###")
            state = 2
            stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 1)                      
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_no_packet(exp_pkt2, 0)
            
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_stp_entry(stp_oid)            
            
            
            
class scenario_05_mstp(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_list = [10]
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr) 
        
        sys_logging("###state 1 mean forward###")
        state = 1
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, port1, state)

        sys_logging("###state 2 mean block###")
        state = 2
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, port1, state)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###stpid1 is forward and stpid2 is block###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(exp_pkt2, 1)
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)                    
            self.client.sai_thrift_remove_stp_entry(stp_oid2)             
        

class scenario_06_unknown_ucast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
              
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
         
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###enable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            sys_logging("###disable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            
        finally:           
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)           
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            
            
            
class scenario_07_unknown_mcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
              
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_tcp_packet(eth_dst='01:00:5e:7f:01:01',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###enable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            sys_logging("###disable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            
        finally:           
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)           
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)            
            
            
            
class scenario_08_broadcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
              
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###enable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            sys_logging("###disable flood###")
            attr_value = sai_thrift_attribute_value_t(s32=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            
        finally:           
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)           
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)            
            
            
            
class scenario_09_max_learning_address(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        sys_logging ("step1: no fdb entry")
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        warmboot(self.client)
        try:
            sys_logging ("step2: mac learnning address num is 1, so only can learning one fdb entry")
            limit_num = 1
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(0 == result)            
            
            sys_logging ("step3: flush all fdb entry")
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            time.sleep(3)
            sys_logging ("step4: mac learnning address num is 0 means disable ")
            limit_num = 0
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)              
            
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)            
            
            
            
class scenario_10_mac_learning_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        sys_logging ("step1: no fdb entry")
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        warmboot(self.client)
        try:
            sys_logging ("step2: mac learnning enable")
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
            
            sys_logging ("step3: flush all fdb entry")
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            time.sleep(3)
            sys_logging ("step4: mac learnning disable ")

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)            

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(0 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(0 == result)              
            
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)                       


class scenario_11_igmp_snooping_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
      
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
               
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                
        pkt = simple_igmpv2_packet(eth_dst='01:00:5e:01:01:01',
                                  eth_src='00:00:00:00:00:01',
                                  ip_src='10.1.1.1',
                                  ip_dst='225.1.1.1',
                                  ip_ttl=1)
        
        warmboot(self.client)
        try:
            
            sys_logging("###step1: igmp snooping disable ###")
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError()

            sys_logging("###step2: igmp snooping enable ###")
            
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 == 0:
                raise NotImplementedError()
                
        finally:
        
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  

            
class scenario_12_vlan_stats_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
           
        switch_init(self.client)
        
        vlan_oid = [0 for i in range(0,4096)]

        warmboot(self.client)
        try:
        
            for a in range(2,2048):
                sys_logging("###creat vlan id %d ###" %a) 
                vlan_oid[a] = sai_thrift_create_vlan(self.client, a)
                assert(SAI_NULL_OBJECT_ID != vlan_oid[a])
        
            vlan_oid[2048] = sai_thrift_create_vlan(self.client, 2048)
            assert(SAI_NULL_OBJECT_ID == vlan_oid[2048])
        
        finally:            
             for a in range(2,2048):
                sys_logging("###remove vlan id %d ###" %a) 
                self.client.sai_thrift_remove_vlan(vlan_oid[a])
              

               
class scenario_13_vlan_member_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)        
        
        vlan_member_list = [vlan_member1,vlan_member2]
        
        warmboot(self.client)
        
        try:     

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MEMBER_LIST:
                    sys_logging("###SAI_VLAN_ATTR_MEMBER_LIST count = %d ###" %a.value.objlist.count)
                    assert ( a.value.objlist.count == 2 )
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_VLAN_ATTR_MEMBER_LIST = %d ###" %b)
                        assert ( b in vlan_member_list)
            
        finally:
            

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)                  

            




                       
                        