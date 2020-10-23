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
Thrift SAI interface Counter tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('counter')

class fun_01_counter_create_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        type = 1
        counter_id = sai_thrift_create_counter(self.client, type)
        assert (counter_id == SAI_NULL_OBJECT_ID)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        assert (counter_id > 0)
        sys_logging("creat counter_id = %d" %counter_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_COUNTER_ATTR_TYPE:
                    sys_logging("set type = 0x%x" %type)
                    sys_logging("get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()

        finally:
            sai_thrift_remove_counter(self.client, counter_id)

class fun_02_counter_remove_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        status = sai_thrift_remove_counter(self.client, counter_id)
        sys_logging("remove status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("CounterRemoveTest finally.")

class fun_03_counter_set_attr_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        assert (counter_id > 0)
        sys_logging("creat counter_id = %d" %counter_id)

        warmboot(self.client)
        try:
            attribute_value = sai_thrift_attribute_value_t(s32=1)
            attribute = sai_thrift_attribute_t(id=SAI_COUNTER_ATTR_TYPE, value=attribute_value)

            status = self.client.sai_thrift_set_counter_attribute(counter_id, attribute)
            assert (status == SAI_STATUS_INVALID_PARAMETER)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_COUNTER_ATTR_TYPE:
                    sys_logging("set type = 0x%x" %type)
                    sys_logging("get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()

        finally:
            sai_thrift_remove_counter(self.client, counter_id)

class fun_04_counter_get_attr_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        assert (counter_id > 0)
        sys_logging("creat counter_id = %d" %counter_id)

        warmboot(self.client)
        try:
            attribute_value = sai_thrift_attribute_value_t(s32=1)
            attribute = sai_thrift_attribute_t(id=SAI_COUNTER_ATTR_TYPE, value=attribute_value)

            status = self.client.sai_thrift_set_counter_attribute(counter_id, attribute)
            assert (status == SAI_STATUS_INVALID_PARAMETER)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_COUNTER_ATTR_TYPE:
                    sys_logging("set type = 0x%x" %type)
                    sys_logging("get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()

            attribute_value = sai_thrift_attribute_value_t(s32=SAI_COUNTER_TYPE_REGULAR)
            attribute = sai_thrift_attribute_t(id=SAI_COUNTER_ATTR_TYPE, value=attribute_value)

            status = self.client.sai_thrift_set_counter_attribute(counter_id, attribute)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_COUNTER_ATTR_TYPE:
                    sys_logging("set type = 0x%x" %type)
                    sys_logging("get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()

        finally:
            sai_thrift_remove_counter(self.client, counter_id)

class fun_05_router_counter_set_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)


        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        #rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)

            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class fun_06_router_counter_clear_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)


        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)


        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt), count=10)
            self.ctc_verify_packets( exp_pkt, [0])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 10)
            assert (counters_results[1] == 1240)

            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class fun_07_invalid_counter_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        assert (counter_id > 0)
        sys_logging("creat counter_id = %d" %counter_id)

        status = sai_thrift_remove_counter(self.client, counter_id)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            attribute_value = sai_thrift_attribute_value_t(s32=SAI_COUNTER_TYPE_REGULAR)
            attribute = sai_thrift_attribute_t(id=SAI_COUNTER_ATTR_TYPE, value=attribute_value)

            status = self.client.sai_thrift_set_counter_attribute(counter_id, attribute)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            type = SAI_COUNTER_TYPE_REGULAR
            counter_id = sai_thrift_create_counter(self.client, type)
            assert (counter_id > 0)
            sys_logging("creat counter_id = %d" %counter_id)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sai_thrift_remove_counter(self.client, counter_id)

class fun_08_route_share_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        #rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.11.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '10.10.11.0'
        ip_mask = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:66'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)

            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()

            addr = sai_thrift_ip_t(ip4=ip_addr2_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)

            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove all counter id")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove one counter id")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            addr = sai_thrift_ip_t(ip4=ip_addr2_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)

            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()

            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove all counter id")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_09_ecmp_group_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        nhop_group = sai_thrift_create_next_hop_group(self.client, SAI_NEXT_HOP_GROUP_TYPE_ECMP, counter_id)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, nhop2)

        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove ecmp group")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_next_hop_group(nhop_group)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove ecmp group")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class fun_10_vpls_encap_lsp_label_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create a mpls nexthop======")

        type = SAI_COUNTER_TYPE_REGULAR
        lsp_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat lsp_counter_id = %d" %lsp_counter_id)

        #def sai_thrift_create_mpls_nhop(client, addr_family, ip_addr, rif_id, label_list, counter_oid=None, next_level_nhop_oid=None, tunnel_id=None,outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE,outseg_exp_mode= SAI_OUTSEG_EXP_MODE_PIPE, exp_map_id=None,outseg_type=SAI_OUTSEG_TYPE_PUSH):
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, lsp_counter_id)
        sys_logging("create nhop = 0x%x" %next_hop)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %lsp_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if lsp_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove lsp nexthop")
            status = sai_thrift_remove_counter(self.client, lsp_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_next_hop(next_hop)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(lsp_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove lsp nexthop")
            status = sai_thrift_remove_counter(self.client, lsp_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(lsp_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_11_vpls_encap_pw_label_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        tunnel_id = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")

        #def sai_thrift_create_mpls_nhop(client, addr_family, ip_addr, rif_id, label_list, counter_oid=None, next_level_nhop_oid=None, tunnel_id=None,outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE,outseg_exp_mode= SAI_OUTSEG_EXP_MODE_PIPE, exp_map_id=None,outseg_type=SAI_OUTSEG_TYPE_PUSH):
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        sys_logging("create lsp nhop = 0x%x" %lsp_next_hop)

        type = SAI_COUNTER_TYPE_REGULAR
        pw_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw_counter_id = %d" %pw_counter_id)

        pw_next_hop = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list1, lsp_next_hop, pw_counter_id)
        sys_logging("create pw nhop = 0x%x" %pw_next_hop)
        assert (pw_next_hop%0x100000000 == 0x4004)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_next_hop_attribute(pw_next_hop)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %pw_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if pw_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove pw nexthop")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_next_hop(pw_next_hop)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove pw nexthop")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)


class fun_12_hostif_trap_l3_mtu_error_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=0)
        print "trap group 0x%lx" %trap_group

        trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                                packet_action=SAI_PACKET_ACTION_TRAP,
                                                trap_group=trap_group)
        print "trap id 0x%lx" %trap_id

        attr_value = sai_thrift_attribute_value_t(oid=counter_id)
        attr = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_COUNTER_ID, value=attr_value)
        status = self.client.sai_thrift_set_hostif_trap_attribute(trap_id, attr)
        print "set hostif trap attr status %d" %status
        assert (status == SAI_STATUS_SUCCESS)

        attrs = self.client.sai_thrift_get_hostif_trap_attribute(trap_id)
        sys_logging("get hostif trap attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_HOSTIF_TRAP_ATTR_COUNTER_ID:
                sys_logging("set counterid = 0x%x" %counter_id)
                sys_logging("get counterid = 0x%x" %a.value.oid)
                if counter_id != a.value.oid:
                    raise NotImplementedError()

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        attr_value = sai_thrift_attribute_value_t(u32=600)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_MTU, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask1, nhop, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=700)

        warmboot(self.client)
        try:
            '''
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(5)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
            else:
                attrs = self.client.sai_thrift_get_cpu_packet_attribute()
                print "success to get packet attribute"
                for a in attrs.attr_list:
                    if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                        print "trap id 0x%lx" %a.value.oid
                        if trap_id != a.value.oid:
                            raise NotImplementedError()
                    if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                        print "ingress port 0x%lx" %a.value.oid
                        if port2 != a.value.oid:
                            raise NotImplementedError()

            sys_logging("remove counter before remove trap")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 704)

            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            '''

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_hostif_trap_attribute(trap_id, attr)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter set trap SAI_HOSTIF_TRAP_ATTR_COUNTER_ID to SAI_NULL_OBJECT_ID")
            status = sai_thrift_remove_counter(self.client, counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            status = self.client.sai_thrift_remove_hostif_trap(trap_id)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_hostif_trap_group(trap_group)
            assert (status == SAI_STATUS_SUCCESS)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask1, nhop)
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_remove_counter(self.client, counter_id)

class fun_13_hostif_trap_ipv6_bgp_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id1 = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id1 = %d" %counter_id1)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id2 = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id2 = %d" %counter_id2)

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=0)

        trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                trap_type=SAI_HOSTIF_TRAP_TYPE_BGPV6,
                                                packet_action=SAI_PACKET_ACTION_TRAP,
                                                trap_group=trap_group,
                                                trap_counter_oid=counter_id1)
        print "trap id 0x%lx" %trap_id

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id2, SAI_PACKET_ACTION_COPY)
        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                  eth_src='00:22:22:22:22:22',
                                  ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                  ipv6_src='2000::1',
                                  ipv6_hlim=64,
                                  tcp_dport=179,
                                  pktlen=120)

        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(oid=counter_id2)
            attr = sai_thrift_attribute_t(id=SAI_HOSTIF_TRAP_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_hostif_trap_attribute(trap_id, attr)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after trap change counter id")
            status = sai_thrift_remove_counter(self.client, counter_id1)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_hostif_trap_attribute(trap_id)
            sys_logging("get hostif trap attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_TRAP_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id2)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id2 != a.value.oid:
                        raise NotImplementedError()

            '''
            sys_logging("======port type rif send dest ip hit v6 packet to port type rif======")
            self.ctc_send_packet(0, str(pkt))
            #self.ctc_verify_packets(exp_pkt, [1])

            time.sleep(5)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet %d" %ret.data.u16
            if ret.data.u16 == 0:
                raise NotImplementedError()
            else:
                attrs = self.client.sai_thrift_get_cpu_packet_attribute()
                print "success to get packet attribute"
                for a in attrs.attr_list:
                    if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                        print "trap id 0x%lx" %a.value.oid
                        if trap_id != a.value.oid:
                            raise NotImplementedError()
                    if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                        print "ingress port 0x%lx" %a.value.oid
                        if port1 != a.value.oid:
                            raise NotImplementedError()

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id2,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)

            status = self.client.sai_thrift_clear_counter_stats(counter_id2,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id2,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            '''

            sys_logging("remove counter after trap change counter id")
            status = sai_thrift_remove_counter(self.client, counter_id2)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_hostif_trap(trap_id)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_hostif_trap_group(trap_group)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after trap change counter id")
            status = sai_thrift_remove_counter(self.client, counter_id2)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(counter_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_14_vpls_create_decap_pw_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        type = SAI_COUNTER_TYPE_REGULAR
        pw_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw_counter_id = 0x%lx" %pw_counter_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        #tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        #next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        #next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        assert (status == SAI_STATUS_SUCCESS)
        status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1, counter_id=pw_counter_id)
        assert (status == SAI_STATUS_SUCCESS)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        #tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            mpls2 = sai_thrift_inseg_entry_t(label2)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)

            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %pw_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if pw_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls2)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)

            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_15_vpls_set_decap_pw_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        type = SAI_COUNTER_TYPE_REGULAR
        pw1_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw1_counter_id = 0x%lx" %pw1_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        pw2_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw2_counter_id = 0x%lx" %pw2_counter_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        #tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        #next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        #next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        assert (status == SAI_STATUS_SUCCESS)
        status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        assert (status == SAI_STATUS_SUCCESS)

        mpls2 = sai_thrift_inseg_entry_t(label2)
        attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)

        attr_value = sai_thrift_attribute_value_t(oid=pw1_counter_id)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
        status = self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)
        assert (status == SAI_STATUS_SUCCESS)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        #tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            mpls2 = sai_thrift_inseg_entry_t(label2)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)

            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %pw1_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if pw1_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw1_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=pw2_counter_id)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after ilm entry change to pw2_counter_id")
            status = sai_thrift_remove_counter(self.client, pw1_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter before remove pw2 ilm entry")
            status = sai_thrift_remove_counter(self.client, pw2_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls2)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw2_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove pw2 ilm entry")
            status = sai_thrift_remove_counter(self.client, pw2_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)

            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_16_vpls_create_decap_lsp_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        type = SAI_COUNTER_TYPE_REGULAR
        pw_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw_counter_id = 0x%lx" %pw_counter_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        #tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        #next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        #next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action, counter_id=pw_counter_id)
        assert (status == SAI_STATUS_SUCCESS)
        status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        assert (status == SAI_STATUS_SUCCESS)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        #tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            mpls1 = sai_thrift_inseg_entry_t(label1)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)

            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %pw_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if pw_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)

            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_17_vpls_set_decap_lsp_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        type = SAI_COUNTER_TYPE_REGULAR
        pw1_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw1_counter_id = 0x%lx" %pw1_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        pw2_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw2_counter_id = 0x%lx" %pw2_counter_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        #tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        #next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        #next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        assert (status == SAI_STATUS_SUCCESS)
        status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        assert (status == SAI_STATUS_SUCCESS)

        mpls1 = sai_thrift_inseg_entry_t(label1)
        attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)

        attr_value = sai_thrift_attribute_value_t(oid=pw1_counter_id)
        attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
        status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
        assert (status == SAI_STATUS_SUCCESS)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        #tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            mpls1 = sai_thrift_inseg_entry_t(label1)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)

            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %pw1_counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if pw1_counter_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("remove counter before remove pw ilm entry")
            status = sai_thrift_remove_counter(self.client, pw1_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=pw2_counter_id)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after ilm entry change to pw2_counter_id")
            status = sai_thrift_remove_counter(self.client, pw1_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter before remove pw2 ilm entry")
            status = sai_thrift_remove_counter(self.client, pw2_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw2_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("remove counter after remove pw2 ilm entry")
            status = sai_thrift_remove_counter(self.client, pw2_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            assert (status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, bport)

            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_18_different_counter_exclude_each_other_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        ecmp_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat ecmp_counter_id = %d" %ecmp_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        router_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat router_counter_id = %d" %router_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        trap_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat trap_counter_id = %d" %trap_counter_id)

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=0)
        print "trap group 0x%lx" %trap_group

        trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                                packet_action=SAI_PACKET_ACTION_TRAP,
                                                trap_group=trap_group,
                                                trap_counter_oid=trap_counter_id)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '10.10.11.0'
        ip_mask = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        warmboot(self.client)
        try:
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1, counter_oid = router_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            nhop_group = sai_thrift_create_next_hop_group(self.client, SAI_NEXT_HOP_GROUP_TYPE_ECMP, router_counter_id)
            assert (nhop_group == SAI_NULL_OBJECT_ID)

            nhop_group = sai_thrift_create_next_hop_group(self.client, SAI_NEXT_HOP_GROUP_TYPE_ECMP, trap_counter_id)
            assert (nhop_group == SAI_NULL_OBJECT_ID)

            nhop_group = sai_thrift_create_next_hop_group(self.client, SAI_NEXT_HOP_GROUP_TYPE_ECMP, ecmp_counter_id)
            assert (nhop_group != SAI_NULL_OBJECT_ID)

            nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, nhop1)
            assert (nhop_gmember1 != SAI_NULL_OBJECT_ID)
            nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, nhop2)
            assert (nhop_gmember2 != SAI_NULL_OBJECT_ID)
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1)
            assert (status == SAI_STATUS_SUCCESS)
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1, counter_oid = trap_counter_id)
            assert (status != SAI_STATUS_SUCCESS)
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1, counter_oid = ecmp_counter_id)
            assert (status != SAI_STATUS_SUCCESS)

            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1, counter_oid = router_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_hostif_trap(trap_id)
            assert (status == SAI_STATUS_SUCCESS)

            trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                    trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                                    packet_action=SAI_PACKET_ACTION_TRAP,
                                                    trap_group=trap_group,
                                                    trap_counter_oid=router_counter_id)
            assert (trap_id == SAI_NULL_OBJECT_ID)

            trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                    trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                                    packet_action=SAI_PACKET_ACTION_TRAP,
                                                    trap_group=trap_group,
                                                    trap_counter_oid=ecmp_counter_id)
            assert (trap_id == SAI_NULL_OBJECT_ID)

            trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                    trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                                    packet_action=SAI_PACKET_ACTION_TRAP,
                                                    trap_group=trap_group,
                                                    trap_counter_oid=trap_counter_id)
            assert (trap_id != SAI_NULL_OBJECT_ID)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_hostif_trap(trap_id)
            self.client.sai_thrift_remove_hostif_trap_group(trap_group)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, router_counter_id)
            sai_thrift_remove_counter(self.client, ecmp_counter_id)
            sai_thrift_remove_counter(self.client, trap_counter_id)

class scenario_01_router_counter_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)


        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)

            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class scenario_02_router_counter_ext_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            mode = SAI_STATS_MODE_READ_AND_CLEAR
            counters_results = self.client.sai_thrift_get_counter_stats_ext(counter_id,cnt_ids,mode,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)

            self.ctc_send_packet( 1, str(pkt), count=2)
            self.ctc_verify_packets( exp_pkt, [0], cmpSeq=1)
            self.ctc_verify_packets( exp_pkt, [0], cmpSeq=2)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class scenario_03_l3vpn_encap_lsp_pw_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        pw_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("create pw_counter_id = %d" %pw_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        lsp_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("create lsp_counter_id = %d" %lsp_counter_id)

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

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 5<<9 | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        #tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=32, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, counter_oid=lsp_counter_id)
        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop2, counter_oid=pw_counter_id)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=1,
                               ip_id=105,
                               ip_ttl=64)

        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':200,'tc':3,'ttl':32,'s':1}]
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=1,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5)

        pkt2 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls1,
                                 inner_frame = ip_only_pkt1)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(pw_counter_id, cnt_ids, len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 112)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(lsp_counter_id, cnt_ids, len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 112)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            self.client.sai_thrift_remove_counter(pw_counter_id)
            self.client.sai_thrift_remove_counter(lsp_counter_id)

class scenario_04_nexthop_tunnel_vxlan_counter_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vr_id = sai_thrift_get_default_router_id(self.client)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        print "rif_lp_inner_id = %lx" %rif_lp_inner_id

        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        print "rif_encap_id = %lx" %rif_encap_id

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        sys_logging("tunnel_map_decap_id = %lx" %tunnel_map_decap_id)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        sys_logging("tunnel_map_encap_id = %lx" %tunnel_map_encap_id)
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)

       # encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
       # decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        encap_mapper_list=[tunnel_map_encap_id]
        decap_mapper_list=[tunnel_map_decap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_encap_id)
        sys_logging("tunnel_id = %lx" %tunnel_id)

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        sys_logging("tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id)

        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id, vni_id, '00:11:22:33:44:55', counter_id);
        sys_logging("tunnel_nexthop_id = %lx" %tunnel_nexthop_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, vlan_oid, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)

        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)

        sai_thrift_create_fdb(self.client, vlan_oid, inner_mac_sa, port1, mac_action)

        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        replace_da_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst='00:11:22:33:44:55',
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)

        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=62,
                        ip_id=0x0001,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = replace_da_pkt1)
        m_exp_pkt1=Mask(exp_pkt1)
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m_exp_pkt1, 2)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 154)

            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            sai_thrift_remove_counter(self.client, counter_id)

class scenario_05_vpls_decap_pw_and_lsp_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        type = SAI_COUNTER_TYPE_REGULAR
        pw_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat pw_counter_id = 0x%lx" %pw_counter_id)

        type = SAI_COUNTER_TYPE_REGULAR
        lsp_counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat lsp_counter_id = 0x%lx" %lsp_counter_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        #tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac, stats_state = False)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id, stats_state = False)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, stats_state = False)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        #next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        #next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        #pdb.set_trace()
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action, counter_id=lsp_counter_id)
        #pdb.set_trace()
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1, counter_id=pw_counter_id)
        #pdb.set_trace()

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        #tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)

        #pdb.set_trace()

        warmboot(self.client)
        try:
            mpls1 = sai_thrift_inseg_entry_t(label1)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)

            sys_logging("get lsp status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set lsp counterid = 0x%x" %lsp_counter_id)
                    sys_logging("get lsp counterid = 0x%x" %a.value.oid)
                    if lsp_counter_id != a.value.oid:
                        raise NotImplementedError()

            mpls2 = sai_thrift_inseg_entry_t(label2)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)

            sys_logging("get pw status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set pw counterid = 0x%x" %pw_counter_id)
                    sys_logging("get pw counterid = 0x%x" %a.value.oid)
                    if pw_counter_id != a.value.oid:
                        raise NotImplementedError()

            self.ctc_send_packet(1, str(pkt3))
            self.ctc_verify_packets(pkt4, [2])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(pw_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("pw packets = %d " %(counters_results[0]))
            sys_logging("pw bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 122)

            counters_results = self.client.sai_thrift_get_counter_stats(lsp_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("lsp packets = %d " %(counters_results[0]))
            sys_logging("lsp bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 122)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
            assert (status == SAI_STATUS_SUCCESS)

            mpls2 = sai_thrift_inseg_entry_t(label2)
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)
            assert (status == SAI_STATUS_SUCCESS)

            #pdb.set_trace()

            self.ctc_send_packet(1, str(pkt3))
            self.ctc_verify_packets(pkt4, [2])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(pw_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("pw packets = %d " %(counters_results[0]))
            sys_logging("pw bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            counters_results = self.client.sai_thrift_get_counter_stats(lsp_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("lsp packets = %d " %(counters_results[0]))
            sys_logging("lsp bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            attr_value = sai_thrift_attribute_value_t(oid=lsp_counter_id)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
            assert (status == SAI_STATUS_SUCCESS)

            mpls2 = sai_thrift_inseg_entry_t(label2)
            attr_value = sai_thrift_attribute_value_t(oid=pw_counter_id)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)
            assert (status == SAI_STATUS_SUCCESS)

            self.ctc_send_packet(1, str(pkt3))
            self.ctc_verify_packets(pkt4, [2])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(pw_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("pw packets = %d " %(counters_results[0]))
            sys_logging("pw bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 122)

            counters_results = self.client.sai_thrift_get_counter_stats(lsp_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("lsp packets = %d " %(counters_results[0]))
            sys_logging("lsp bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 122)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
            assert (status == SAI_STATUS_SUCCESS)

            mpls2 = sai_thrift_inseg_entry_t(label2)
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)
            assert (status == SAI_STATUS_SUCCESS)

            self.ctc_send_packet(1, str(pkt3))
            self.ctc_verify_packets(pkt4, [2])

            attrs = self.client.sai_thrift_get_counter_attribute(lsp_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_counter_attribute(pw_counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(pw_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("pw packets = %d " %(counters_results[0]))
            sys_logging("pw bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            counters_results = self.client.sai_thrift_get_counter_stats(lsp_counter_id,cnt_ids,len(cnt_ids))
            sys_logging("lsp packets = %d " %(counters_results[0]))
            sys_logging("lsp bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

            status = sai_thrift_remove_counter(self.client, pw_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_remove_counter(self.client, lsp_counter_id)
            assert (status == SAI_STATUS_SUCCESS)

class scenario_06_routes_share_stats(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.11.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '10.10.11.0'
        ip_mask = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:66'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                     eth_src=router_mac,
                                     ip_dst=ip_addr1_subnet,
                                     ip_src='192.168.0.1',
                                     ip_id=105,
                                     ip_ttl=63,
                                     pktlen=120)

        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                 eth_src='00:22:22:22:22:22',
                                 ip_dst=ip_addr2_subnet,
                                 ip_src='192.168.0.1',
                                 ip_id=105,
                                 ip_ttl=64,
                                 pktlen=120)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                     eth_src=router_mac,
                                     ip_dst=ip_addr2_subnet,
                                     ip_src='192.168.0.1',
                                     ip_id=105,
                                     ip_ttl=63,
                                     pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets(exp_pkt2, [1])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)

            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
            sys_logging("route remove status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets(exp_pkt1, [0])

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(exp_pkt2, 1, default_time_out)

            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)

            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
            sys_logging("route create status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets(exp_pkt2, [1])

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 3)
            assert (counters_results[1] == 372)

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, nhop2)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class scenario_07_ecmp_group_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client, SAI_NEXT_HOP_GROUP_TYPE_ECMP, counter_id)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)

        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet======")
            port1_pkt_cnt = 0
            port2_pkt_cnt = 0
            src_ip = int(socket.inet_aton('192.168.0.1').encode('hex'),16)
            max_itrs = 4
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip+i)[2:].zfill(8).decode('hex'))
                print src_ip_addr
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:00:11:11:11:11',
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=64)

                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=63)

                self.ctc_send_packet( 2, str(pkt))
                #self.ctc_verify_packet( (exp_pkt6_1), 6)
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt1], [0, 1])
                if rcv_idx == 0:
                    port1_pkt_cnt = port1_pkt_cnt+1
                elif rcv_idx == 1:
                    port2_pkt_cnt = port2_pkt_cnt+1

                cnt_ids=[]
                cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
                cnt_ids.append(SAI_COUNTER_STAT_BYTES)
                counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
                sys_logging("packets = %d " %(counters_results[0]))
                sys_logging("bytes = %d " %(counters_results[1]))
                assert (counters_results[0] == (port1_pkt_cnt+port2_pkt_cnt))
                assert (counters_results[1] == ((port1_pkt_cnt+port2_pkt_cnt)*104))

            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            sys_logging("port 2 receive packet conut is %d" %port2_pkt_cnt)

            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            port1_pkt_cnt = 0
            port2_pkt_cnt = 0
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip+i)[2:].zfill(8).decode('hex'))
                print src_ip_addr
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:00:11:11:11:11',
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=64)

                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=63)

                self.ctc_send_packet( 2, str(pkt))
                #self.ctc_verify_packet( (exp_pkt6_1), 6)
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt1], [0, 1])
                if rcv_idx == 0:
                    port1_pkt_cnt = port1_pkt_cnt+1
                elif rcv_idx == 1:
                    port2_pkt_cnt = port2_pkt_cnt+1

            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            sys_logging("port 2 receive packet conut is %d" %port2_pkt_cnt)

            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == (port1_pkt_cnt+port2_pkt_cnt))
            assert (counters_results[1] == ((port1_pkt_cnt+port2_pkt_cnt)*104))

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
