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
Thrift SAI interface TWAMP tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
import pdb

@group('twamp')
def ip6_to_integer(ip6):
    ip6 = socket.inet_pton(socket.AF_INET6, ip6)
    a, b = unpack(">QQ", ip6)
    return (a << 64) | b

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton('10.10.10.1').encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))
    
class func_01_create_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create twamp session###")
        
        switch_init(self.client)
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 0
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_FULL

        twamp_session_oid1 = sai_thrift_create_twamp_session(self.client, port_id, role, udp_dst_port, udp_src_port, dst_ip, src_ip, tc, vpn, encap_type, enable_transmit, hw_lookup_vaild, padding_length, state, auth_mode, next_hop_id, tx_pkt_period, tx_rate, tx_pkt_cnt, tx_pkt_duration, mode)
        sys_logging("###twamp_session_oid1 = %d###" %twamp_session_oid1)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)

class func_08_remove_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###remove twamp session###")
        
        switch_init(self.client)
        twamp_session_oid = 0x100000057 
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 0
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_FULL

        status = sai_thrift_remove_twamp_session(self.client, twamp_session_oid)
        sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)
			
class func_02_create_twamp_hw_lookup_session_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create twamp session###")
        
        switch_init(self.client)
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 1
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_FULL

        twamp_session_oid1 = sai_thrift_create_twamp_session(self.client, port_id, role, udp_dst_port, udp_src_port, dst_ip, src_ip, tc, vpn, encap_type, enable_transmit, hw_lookup_vaild, padding_length, state, auth_mode, next_hop_id, tx_pkt_period, tx_rate, tx_pkt_cnt, tx_pkt_duration, mode)
        sys_logging("###twamp_session_oid1 = %d###" %twamp_session_oid1)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)

class func_03_remove_twamp_hw_lookup_session_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###remove twamp session###")
        
        switch_init(self.client)
        twamp_session_oid = 0x100000057 
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 0
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_FULL

        status = sai_thrift_remove_twamp_session(self.client, twamp_session_oid)
        sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)
			
			
class func_04_create_twamp_receiver_full_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create twamp session###")
        switch_init(self.client)
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_REFLECTOR
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '20.4.5.6'
        src_ip = '10.1.2.3'
        tc = 3
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 0
        hw_lookup_vaild = 1
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 110
        tx_pkt_period = 0
        tx_rate = 0
        tx_pkt_cnt = 0
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_TWAMP_FULL		
		
        twamp_session_oid1 = sai_thrift_create_twamp_session(self.client, port_id, role, udp_dst_port, udp_src_port, dst_ip, src_ip, tc, vpn, encap_type, enable_transmit, hw_lookup_vaild, padding_length, state, auth_mode, next_hop_id, tx_pkt_period, tx_rate, tx_pkt_cnt, tx_pkt_duration, mode)
        sys_logging("###twamp_session_oid1 = %d###" %twamp_session_oid1)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid1)
				
class func_05_remove_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create twamp session###")
        
        switch_init(self.client)
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 1
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_LIGHT

        twamp_session_oid1 = sai_thrift_create_twamp_session(self.client, port_id, role, udp_dst_port, udp_src_port, dst_ip, src_ip, tc, vpn, encap_type, enable_transmit, hw_lookup_vaild, padding_length, state, auth_mode, next_hop_id, tx_pkt_period, tx_rate, tx_pkt_cnt, tx_pkt_duration, mode)
        sys_logging("###twamp_session_oid1 = %d###" %twamp_session_oid1)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)

class func_06_set_twamp_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###set twamp session attr###")
        
        switch_init(self.client)
        twamp_session_oid = 0x100000057 
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 0
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_FULL

		#attr_value = sai_thrift_attribute_value_t(booldata=1)
		#attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)		
		#status=self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
        #sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)             
		#attr_value = sai_thrift_attribute_value_t(booldata=0)
		#attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)		
		#status=self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
        try:
            if twamp_session_oid == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_set_twamp_attribute(twamp_session_oid)

class func_03_create_twamp_light_mode_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        sys_logging("###create twamp session###")
        
        switch_init(self.client)
        port_id = 0x800000001
        role = SAI_TWAMP_SESSION_SENDER
        udp_dst_port = 4789
        udp_src_port = 45193
        dst_ip = '10.1.2.3'
        src_ip = '20.4.5.6'
        tc = 5
        vpn = 12
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup_vaild = 1
        padding_length = 20
        state = SAI_TWAMP_SESSION_STATE_ACTIVE
        auth_mode = SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED
        next_hop_id = 3
        tx_pkt_period = 100
        tx_rate = 200000
        tx_pkt_cnt = 30000000
        tx_pkt_duration = 1234567890
        mode = SAI_TWAMP_MODE_TWAMP_LIGHT

        twamp_session_oid1 = sai_thrift_create_twamp_session(self.client, port_id, role, udp_dst_port, udp_src_port, dst_ip, src_ip, tc, vpn, encap_type, enable_transmit, hw_lookup_vaild, padding_length, state, auth_mode, next_hop_id, tx_pkt_period, tx_rate, tx_pkt_cnt, tx_pkt_duration, mode)
        sys_logging("###twamp_session_oid1 = %d###" %twamp_session_oid1)             
        try:
            if twamp_session_oid1 == 0:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_twamp_session(vlan_twamp_session_oid1oid1)
			
