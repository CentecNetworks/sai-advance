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
Thrift SAI Samplepacket tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('Samplepacket')
class SamplepacketCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)

        samplepacket_attrs = []

        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=20)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        print "create samplepacket"
        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print "success to create samplepacket"

        try:
            print "get attribute samplepacket 0x%lx" %samplepacket_id
            attrs = self.client.sai_thrift_get_samplepacket_attribute(samplepacket_id)
            print "success to get attribute samplepacket"
            for a in attrs.attr_list:
                if a.id == SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE:
                    print "reate %d" %a.value.u32
                    if 20 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_SAMPLEPACKET_ATTR_TYPE:
                    print "type %d" %a.value.s32
                    if SAI_SAMPLEPACKET_TYPE_SLOW_PATH != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_SAMPLEPACKET_ATTR_MODE:
                    print "mode %d" %a.value.s32
                    if SAI_SAMPLEPACKET_MODE_EXCLUSIVE != a.value.s32:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)
            
class SamplepacketRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create and Remove test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)

        samplepacket_attrs = []

        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=20)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        self.client.sai_thrift_remove_samplepacket(samplepacket_id)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_samplepacket_attribute(samplepacket_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            print "Success!"
            
class SamplepacketIngressPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        samplepacket_attrs = []

        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print samplepacket_id
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                        eth_src=mac2,
                        ip_dst='10.0.0.1',
                        ip_id=102,
                        ip_ttl=64,
                        dl_vlan_enable=True,
                        vlan_vid=1)
        attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port0,attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        
        warmboot(self.client)
        try:
            print "Sending packet to  port 0"
            self.ctc_send_packet( 0, str(pkt1), 50)
            time.sleep(10)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port0,attr)
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)

class SamplepacketEgressPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        samplepacket_attrs = []
        vlan_id = 10
        
        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print samplepacket_id
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port0, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                        eth_src=mac2,
                        ip_dst='10.0.0.1',
                        ip_id=102,
                        ip_ttl=64,
                        dl_vlan_enable=True,
                        vlan_vid=vlan_id)
        attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        
        warmboot(self.client)
        try:
            print "Sending packet to  port 0"
            self.ctc_send_packet( 0, str(pkt1), 50)
            time.sleep(10)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port0,attr)
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)

class SamplepacketReceiveCpuPacketAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        samplepacket_attrs = []
        vlan_id = 10
        
        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)

        trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
        print "samplepacket trap id: 0x%lx"  %trap_id
        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=20)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print samplepacket_id
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port0, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                        eth_src=mac2,
                        ip_dst='10.0.0.1',
                        ip_id=102,
                        ip_ttl=64,
                        dl_vlan_enable=True,
                        vlan_vid=vlan_id)
        attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        warmboot(self.client)
        try:
            print "Sending packet to  port 0"
            self.ctc_send_packet( 0, str(pkt1), 20)
            time.sleep(5)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
            else:
                attrs = self.client.sai_thrift_get_cpu_packet_attribute(0)
                print "success to get packet attribute"
                for a in attrs.attr_list:
                    if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                        print "trap id 0x%lx" %a.value.oid
                        if trap_id != a.value.oid:
                            raise NotImplementedError()
                    if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                        print "ingress port 0x%lx" %a.value.oid
                        if port0 != a.value.oid:
                            raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port0,attr)
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)
            self.client.sai_thrift_remove_hostif_trap(trap_id)
            self.client.sai_thrift_remove_hostif_trap_group(trap_group)
            
class SamplepacketMultiPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        samplepacket_attrs = []

        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print samplepacket_id
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                        eth_src=mac2,
                        ip_dst='10.0.0.1',
                        ip_id=102,
                        ip_ttl=64,
                        dl_vlan_enable=True,
                        vlan_vid=1)
        attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port0,attr)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        self.client.sai_thrift_set_port_attribute(port2,attr)
        self.client.sai_thrift_set_port_attribute(port3,attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        warmboot(self.client)
        try:
            print "Sending packet to  port 0"
            self.ctc_send_packet( 0, str(pkt1), 50)
            time.sleep(10)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port0,attr)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_set_port_attribute(port2,attr)
            self.client.sai_thrift_set_port_attribute(port3,attr)
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)

class SamplepacketIngressAclTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)
        samplepacket_attrs = []

        samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
        samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                              value=samplepacket_attr_value)
        samplepacket_attrs.append(samplepacket_attr)

        samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
        print samplepacket_id
        
        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
            
        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = [port1, port2]
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.255"
        ip_dst = '10.10.10.1'
        ip_dst_mask = "255.255.255.255"
        is_ipv6 = False
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
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
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn, ingress_samplepacket=samplepacket_id)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'
            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 0, str(pkt), 100)
            time.sleep(10)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # remove samplepacket
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)

class SamplepacketStressCreateAndRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create samplepacket test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)

        warmboot(self.client)
        try:
            for rate_value in range(1, 8000):
                samplepacket_attrs = []

                samplepacket_attr_value = sai_thrift_attribute_value_t(u32=rate_value)
                samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,
                                                        value=samplepacket_attr_value)
                samplepacket_attrs.append(samplepacket_attr)

                samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)
                self.client.sai_thrift_remove_samplepacket(samplepacket_id)
        
        finally:
            print "rate_value is %d" %rate_value
