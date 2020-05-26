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
Thrift SAI interface Debug Counter tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('debugcounter')    

class DebugCounterCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
            sys_logging( "get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_DEBUG_COUNTER_ATTR_TYPE:
                    sys_logging( "set type = 0x%x" %type)
                    sys_logging( "get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST:
                    sys_logging ("set in drop list =  ", in_drop_list)
                    sys_logging ("get in drop list =  ", a.value.s32list.s32list)
                    if in_drop_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                    sys_logging( "get debug index = %d" %a.value.u32)
                    assert (a.value.u32 != 0)
        
        finally:
            self.client.sai_thrift_remove_debug_counter(counter_id)

class DebugCounterRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        status = self.client.sai_thrift_remove_debug_counter(counter_id)
        sys_logging("remove status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        
        finally:
            sys_logging("DebugCounterRemoveTest finally.")
            #sai_thrift_remove_counter(self.client, counter_id)
            
class DebugCounterInPortDropTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        #port1 set to drop tagged mode
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), packet from port3 without vlan")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [2])
            
            debug_index_list = [debug_counter_index+SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 0)
            
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(droppkt1))
            self.ctc_verify_no_packet(droppkt1, 2)

            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            sys_logging("Sending L2 packet port 1 -> port 3 [with access vlan=10]), discard by SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED")
            self.ctc_send_packet(0, str(droppkt2))
            self.ctc_verify_no_packet(droppkt2, 2)
            
            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 2)
        
        finally:
            self.client.sai_thrift_clear_port_all_stats(port1)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            
            self.client.sai_thrift_remove_debug_counter(counter_id)
            
class DebugCounterInPortDropExtTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        #port1 set to drop tagged mode
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(droppkt1))
            self.ctc_verify_no_packet(droppkt1, 2)
            
            debug_index_list = [debug_counter_index+SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list, SAI_STATS_MODE_READ_AND_CLEAR)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            sys_logging("Sending L2 packet port 1 -> port 3 [with access vlan=10]), discard by SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED")
            self.ctc_send_packet(0, str(droppkt2))
            self.ctc_verify_no_packet(droppkt2, 2)
            
            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
        
        finally:
            self.client.sai_thrift_clear_port_all_stats(port1)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            
            self.client.sai_thrift_remove_debug_counter(counter_id)
            
class DebugCounterInSwitchDropTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        sw_counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat sw_counter_id = %d" %sw_counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32
                
        attrs = self.client.sai_thrift_get_debug_counter_attribute(sw_counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get switch debug index = %d" %a.value.u32)
                sw_debug_counter_index = a.value.u32
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        #port1 set to drop tagged mode
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            debug_index_list = [debug_counter_index+SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE]
            
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(droppkt1))
            self.ctc_verify_no_packet(droppkt1, 2)

            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            sys_logging("Sending L2 packet port 2 -> port 3 [with access vlan=10]), discard by SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED")
            self.ctc_send_packet(1, str(droppkt2))
            self.ctc_verify_no_packet(droppkt2, 2)
            
            counters_results = sai_thrift_read_port_debug_counters(self.client, port2, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 2)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats_ext(debug_index_list2, 1, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 2)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 0)
            
            
        finally:
            self.client.sai_thrift_clear_port_all_stats(port1)
            self.client.sai_thrift_clear_port_all_stats(port2)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            
            self.client.sai_thrift_remove_debug_counter(counter_id)
            self.client.sai_thrift_remove_debug_counter(sw_counter_id)

class DebugCounterInSwitchDropClearTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        sw_counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat sw_counter_id = %d" %sw_counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32
                
        attrs = self.client.sai_thrift_get_debug_counter_attribute(sw_counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get switch debug index = %d" %a.value.u32)
                sw_debug_counter_index = a.value.u32
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        #port1 set to drop tagged mode
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            debug_index_list = [debug_counter_index+SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE]
            
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(droppkt1))
            self.ctc_verify_no_packet(droppkt1, 2)

            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            sys_logging("Sending L2 packet port 2 -> port 3 [with access vlan=10]), discard by SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED")
            self.ctc_send_packet(1, str(droppkt2))
            self.ctc_verify_no_packet(droppkt2, 2)
            
            counters_results = sai_thrift_read_port_debug_counters(self.client, port2, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 2)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            status = self.client.sai_thrift_clear_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch clear status = %d " %(status))
            assert (status == SAI_STATUS_SUCCESS)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 0)
            
            
        finally:
            self.client.sai_thrift_clear_port_all_stats(port1)
            self.client.sai_thrift_clear_port_all_stats(port2)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            
            self.client.sai_thrift_remove_debug_counter(counter_id)
            self.client.sai_thrift_remove_debug_counter(sw_counter_id)
            
class DebugCounterOutPortDropTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS
        drop_list = [SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list=None, out_drop_list=drop_list)
        sys_logging("creat counter_id = %d" %counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32
                
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS
        drop_list = [SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER]
        sw_counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list=None, out_drop_list=drop_list)
        sys_logging("creat sw_counter_id = %d" %sw_counter_id)
        
        attrs = self.client.sai_thrift_get_debug_counter_attribute(sw_counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get switch debug index = %d" %a.value.u32)
                sw_debug_counter_index = a.value.u32
        
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        #vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        
        bp = sai_thrift_get_bridge_port_by_port(self.client, port3)
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bp, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), packet from port3 without vlan")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 2)
            
            debug_index_list = [debug_counter_index+SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE]
            counters_results = sai_thrift_read_port_debug_counters(self.client, port3, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
        
        finally:
            self.client.sai_thrift_clear_port_all_stats(port3)
            status = self.client.sai_thrift_clear_switch_stats(debug_index_list2, len(debug_index_list2))
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            bp = sai_thrift_get_bridge_port_by_port(self.client, port3)
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bp, attr)
            

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            #self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            
            self.client.sai_thrift_remove_debug_counter(counter_id)