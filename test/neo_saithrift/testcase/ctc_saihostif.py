# saihostif.${name_test}
#
# ARPTest
# DHCPTest
# LLDPTest
# BGPTest
# LACPTest
# SNMPTest
# SSHTest
# IP2METest
# TTLErrorTest
#ptf --test-dir PTF_TEST_CASES saihostif.DHCPTest  --qlen=10000 --platform nn -t "server='10.3.147.47';test_port=3;port_map_file='default_interface_to_front_map.ini';verbose=True;" --device-socket 0-3@tcp://127.0.0.1:10900 --device-socket 1-3@tcp://10.3.147.47:10900

import ptf
from ptf.base_tests import BaseTest
from ptf import config
import ptf.testutils as testutils
from ptf.testutils import *
from ptf.dataplane import match_exp_pkt
import datetime
import subprocess
from switch import *
import sai_base_test

import switch_sai.switch_sai_rpc as switch_sai_rpc
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time

import pprint
from saihostif import *

      
class ARPRequestNoPolicyTest(NoPolicyTest):
    def __init__(self):
        #pdb.set_trace()
        NoPolicyTest.__init__(self)

    def runTest(self):
        self.run_suite()

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        pdb.set_trace()
        self.setup_test_port_rif(self.test_port_ind)

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=0)
        self.trap_groups.append(trap_group)

        trap1 = sai_thrift_create_hostif_trap(client=self.client,
                                              trap_type=SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST,
                                              packet_action=SAI_PACKET_ACTION_TRAP,
                                              trap_group=trap_group)
        self.traps.append(trap1)
        return

    def contruct_packet(self):
        src_mac = self.src_mac_uc
        src_ip = self.myip
        dst_ip = self.peerip

        packet = simple_arp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                   eth_src=src_mac,
                                   arp_op=1,
                                   ip_snd=src_ip,
                                   ip_tgt=dst_ip,
                                   hw_snd=src_mac,
                                   hw_tgt='ff:ff:ff:ff:ff:ff')

        return packet

class ARPResponseNoPolicyTest(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)

    def runTest(self):
        self.run_suite()

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        self.setup_test_port_rif(self.test_port_ind)

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=100)
        self.trap_groups.append(trap_group)

        trap1 = sai_thrift_create_hostif_trap(client=self.client,
                                              trap_type=SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE,
                                              packet_action=SAI_PACKET_ACTION_TRAP,
                                              trap_group=trap_group)
        self.traps.append(trap1)
        return

    def contruct_packet(self):
        src_mac = self.src_mac_uc
        src_ip = self.myip
        dst_ip = self.peerip

        packet = simple_arp_packet(eth_dst=router_mac,
                                   eth_src=src_mac,
                                   arp_op=2,
                                   ip_snd=src_ip,
                                   ip_tgt=dst_ip,
                                   hw_snd=src_mac,
                                   hw_tgt=router_mac)

        return packet

class BGPV6Test(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)
        return

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        self.create_ipv6_routes()

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=100)
        self.trap_groups.append(trap_group)

        trap = sai_thrift_create_hostif_trap(client=self.client,
                                             trap_type=SAI_HOSTIF_TRAP_TYPE_BGPV6,
                                             packet_action=SAI_PACKET_ACTION_TRAP,
                                             trap_group=trap_group)
        self.traps.append(trap)

    def runTest(self):
        self.run_suite()

    def contruct_packet(self):
        dst_ip = self.peeripv6ip
        packet = simple_tcpv6_packet(eth_dst=router_mac,
                                   ipv6_dst=dst_ip,
                                   tcp_dport=179)
        return packet

class MTUErrorTest(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)

        port1 = port_list[self.test_port_ind]
        port2 = port_list[self.test_port_ind+1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        self.src_ip = '192.168.0.1'
        self.ip_addr1 = '10.10.10.1'


        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)
        self.trap_groups.append(trap_group)

        trap = sai_thrift_create_hostif_trap(client=self.client,
                                             trap_type=SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
                                             packet_action=SAI_PACKET_ACTION_TRAP,
                                             trap_group=trap_group)
        self.traps.append(trap)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        self.v_routers.append(vr_id)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        self.rifs.append(rif_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        self.rifs.append(rif_id2)
        
        attr_value = sai_thrift_attribute_value_t(u32=600)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_MTU, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, self.ip_addr1, dmac1)
        neighbor_data=[addr_family, rif_id1, self.ip_addr1, dmac1]
        self.neighbors.append(neighbor_data)

        nhop1 = sai_thrift_create_nhop(self.client, addr_family, self.ip_addr1, rif_id1)
        self.next_hops.append(nhop1)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
        route_data=[vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1]
        self.routes.append(route_data)
        return

    def runTest(self):
        self.run_suite()

    def contruct_packet(self):

        packet = simple_tcp_packet(pktlen=1000,
                                   eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ip_dst=self.ip_addr1,
                                   ip_src=self.src_ip,
                                   ip_id=105,
                                   ip_ttl=255)
        return packet

class OSPFTest(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)
        return

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        self.create_routes()

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)
        self.trap_groups.append(trap_group)

        trap = sai_thrift_create_hostif_trap(client=self.client,
                                             trap_type=SAI_HOSTIF_TRAP_TYPE_OSPF,
                                             packet_action=SAI_PACKET_ACTION_TRAP,
                                             trap_group=trap_group)
        self.traps.append(trap)

    def runTest(self):
        self.run_suite()

    def contruct_packet(self):
        dst_ip = self.peerip
        packet = simple_ip_packet(eth_dst=router_mac,
                                   ip_dst=dst_ip,
                                   ip_proto=89)
        return packet

class DHCPV6Test(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        self.setup_test_port_rif(self.test_port_ind)

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=100)
        self.trap_groups.append(trap_group)

        trap = sai_thrift_create_hostif_trap(client=self.client,
                                             trap_type=SAI_HOSTIF_TRAP_TYPE_DHCPV6,
                                             packet_action=SAI_PACKET_ACTION_TRAP,
                                             trap_group=trap_group)
        self.traps.append(trap)
        return

    def runTest(self):
        self.run_suite()

    def contruct_packet(self):
        src_mac = self.src_mac_uc
        packet = simple_udpv6_packet(pktlen=100,
                                   eth_dst='ff:ff:ff:ff:ff:ff',
                                   eth_src=src_mac,
                                   dl_vlan_enable=False,
                                   vlan_vid=0,
                                   vlan_pcp=0,
                                   ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                   ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                   udp_sport=547,
                                   udp_dport=546,
                                   with_udp_chksum=True)

        return packet
        
class VRRPTest(NoPolicyTest):
    def __init__(self):
        NoPolicyTest.__init__(self)
        return

    def setUp(self):
        ControlPlaneBaseTest.setUp(self)
        self.create_routes()

        trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)
        self.trap_groups.append(trap_group)

        trap = sai_thrift_create_hostif_trap(client=self.client,
                                             trap_type=SAI_HOSTIF_TRAP_TYPE_VRRP,
                                             packet_action=SAI_PACKET_ACTION_TRAP,
                                             trap_group=trap_group)
        self.traps.append(trap)

    def runTest(self):
        self.run_suite()

    def contruct_packet(self):
        dst_ip = self.peerip
        packet = simple_ip_packet(eth_dst=router_mac,
                                   ip_dst=self.peerip,
                                   ip_ttl=255,
                                   ip_proto=112)
        return packet

        

class StressTest(sai_base_test.ThriftInterfaceDataPlane):
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
        self.traps=[]
        self.trap_groups=[]
        
        warmboot(self.client)
        try:
            trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=100)
            self.trap_groups.append(trap_group)
            SAI_HOSTIF_TRAP_TYPE_TTL_ERROR,
            SAI_HOSTIF_TRAP_TYPE_BGP,
            SAI_HOSTIF_TRAP_TYPE_LACP,
            SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST,
            SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE,
            SAI_HOSTIF_TRAP_TYPE_LLDP,
            SAI_HOSTIF_TRAP_TYPE_DHCP,
            SAI_HOSTIF_TRAP_TYPE_SNMP,
            SAI_HOSTIF_TRAP_TYPE_SSH,
            SAI_HOSTIF_TRAP_TYPE_IP2ME,
            SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY,
            SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE,
            SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT,
            SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT,
            SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT,
            SAI_HOSTIF_TRAP_TYPE_BGPV6,
            SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR,
            trap1 = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_TTL_ERROR,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            self.traps.append(trap1)
            trap2 = sai_thrift_create_hostif_trap(client=self.client,
                                         trap_type=SAI_HOSTIF_TRAP_TYPE_BGP,
                                         packet_action=SAI_PACKET_ACTION_TRAP,
                                         trap_group=trap_group)
            self.traps.append(trap2)
            trap3 = sai_thrift_create_hostif_trap(client=self.client,
                                        trap_type=SAI_HOSTIF_TRAP_TYPE_LACP,
                                        packet_action=SAI_PACKET_ACTION_TRAP,
                                        trap_group=trap_group)
            self.traps.append(trap3)
            trap4 = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            self.traps.append(trap4)
            trap5 = sai_thrift_create_hostif_trap(client=self.client,
                                         trap_type=SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE,
                                         packet_action=SAI_PACKET_ACTION_TRAP,
                                         trap_group=trap_group)
            self.traps.append(trap5)
            trap6 = sai_thrift_create_hostif_trap(client=self.client,
                                        trap_type=SAI_HOSTIF_TRAP_TYPE_LLDP,
                                        packet_action=SAI_PACKET_ACTION_TRAP,
                                        trap_group=trap_group)
            self.traps.append(trap6)
            trap7 = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_DHCP,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            self.traps.append(trap7)
            trap8 = sai_thrift_create_hostif_trap(client=self.client,
                                         trap_type=SAI_HOSTIF_TRAP_TYPE_SNMP,
                                         packet_action=SAI_PACKET_ACTION_TRAP,
                                         trap_group=trap_group)
            self.traps.append(trap8)
            trap9 = sai_thrift_create_hostif_trap(client=self.client,
                                        trap_type=SAI_HOSTIF_TRAP_TYPE_SSH,
                                        packet_action=SAI_PACKET_ACTION_TRAP,
                                        trap_group=trap_group)
            self.traps.append(trap9)
            trap10 = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_IP2ME,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            self.traps.append(trap10)
            trap11 = sai_thrift_create_hostif_trap(client=self.client,
                                         trap_type=SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY,
                                         packet_action=SAI_PACKET_ACTION_TRAP,
                                         trap_group=trap_group)
            self.traps.append(trap11)

            trap12 = sai_thrift_create_hostif_trap(client=self.client,
                                        trap_type=SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE,
                                        packet_action=SAI_PACKET_ACTION_TRAP,
                                        trap_group=trap_group)
            self.traps.append(trap12)
            trap13 = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            self.traps.append(trap13)
            trap14 = sai_thrift_create_hostif_trap(client=self.client,
                                         trap_type=SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT,
                                         packet_action=SAI_PACKET_ACTION_TRAP,
                                         trap_group=trap_group)
            self.traps.append(trap14)
            trap15 = sai_thrift_create_hostif_trap(client=self.client,
                                        trap_type=SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT,
                                        packet_action=SAI_PACKET_ACTION_TRAP,
                                        trap_group=trap_group)
            self.traps.append(trap15)
        finally:
            for trap in self.traps:
                sai_thrift_remove_hostif_trap(self.client, trap)

            for trap_group in self.trap_groups:
                sai_thrift_remove_hostif_trap_group(self.client, trap_group)

class HostIfAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
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
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        warmboot(self.client)
        try:
            hostif_id = sai_thrift_create_hostif(self.client, SAI_HOSTIF_TYPE_NETDEV, port1, "ETH_Cec1")
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_HOSTIF_ATTR_OPER_STATUS, value=attr_value)
            self.client.sai_thrift_set_hostif_attribute(hostif_id, attr)
            attrs = self.client.sai_thrift_get_hostif_attribute(hostif_id)
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_ATTR_TYPE:
                    print "hostif attr type %d" %a.value.s32
                    if SAI_HOSTIF_TYPE_NETDEV != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_ATTR_OBJ_ID:
                    print "hostif port id 0x%lx" %a.value.oid
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_ATTR_NAME:
                    print "hostif name %s" %a.value.chardata
                if a.id == SAI_HOSTIF_ATTR_OPER_STATUS:
                    print "hostif oper status %d" %a.value.booldata
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_hostif(hostif_id)

class HostIfTableEntryAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
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
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        warmboot(self.client)
        try:
            trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)

            trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_LLDP,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            attr_list=[]

            atr_value=sai_thrift_attribute_value_t(s32=SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT)
            atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE,
                                       value=atr_value)
            attr_list.append(atr)

            atr_value=sai_thrift_attribute_value_t(oid=port1)
            atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID,
                                       value=atr_value)
            attr_list.append(atr)

            atr_value=sai_thrift_attribute_value_t(oid=trap_id)
            atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID,
                                       value=atr_value)
            attr_list.append(atr)

            atr_value=sai_thrift_attribute_value_t(s32=SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB)
            atr=sai_thrift_attribute_t(id=SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE,
                                       value=atr_value)
            attr_list.append(atr)

            hostif_tab_entry_id = self.client.sai_thrift_create_hostif_table_entry(attr_list)
            attrs = self.client.sai_thrift_get_hostif_table_entry_attribute(hostif_tab_entry_id)
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE:
                    print "hostif table entry type %d" %a.value.s32
                    if SAI_HOSTIF_TABLE_ENTRY_TYPE_PORT != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID:
                    print "hostif table entry port id 0x%lx" %a.value.oid
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID:
                    print "hostif table entry trap id 0x%lx" %a.value.oid
                    if trap_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE:
                    print "hostif table entry channel type %d" %a.value.s32
                    if SAI_HOSTIF_TABLE_ENTRY_CHANNEL_TYPE_CB != a.value.s32:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_hostif_table_entry(hostif_tab_entry_id)
            self.client.sai_thrift_remove_hostif_trap(trap_id)
            self.client.sai_thrift_remove_hostif_trap_group(trap_group)

class HostIfTrapGroupAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
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
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        warmboot(self.client)
        try:
            trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)
            attrs = self.client.sai_thrift_get_hostif_trap_group_attribute(trap_group)
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE:
                    print "hostif trap group admin state %d" %a.value.booldata
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE:
                    print "hostif trap group queue %d" %a.value.u32
                    if 4 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER:
                    print "hostif trap group policer id 0x%lx" %a.value.oid
                    if 0 != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_hostif_trap_group(trap_group)
            
class HostIfTrapAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        HostIf trap attribute test. Verify All supported hostif trap attribute. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        warmboot(self.client)
        try:
            trap_group = sai_thrift_create_hostif_trap_group(self.client, queue_id=4)

            trap_id = sai_thrift_create_hostif_trap(client=self.client,
                                                 trap_type=SAI_HOSTIF_TRAP_TYPE_LLDP,
                                                 packet_action=SAI_PACKET_ACTION_TRAP,
                                                 trap_group=trap_group)
            attrs = self.client.sai_thrift_get_hostif_trap_attribute(trap_id)
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE:
                    print "hostif trap type %d" %a.value.s32
                    if SAI_HOSTIF_TRAP_TYPE_LLDP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION:
                    print "hostif trap action %d" %a.value.s32
                    if SAI_PACKET_ACTION_TRAP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY:
                    print "hostif trap priority id 0x%lx" %a.value.u32
                    if 1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP:
                    print "hostif trap group 0x%lx" %a.value.oid
                    if trap_group != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_hostif_trap(trap_id)
            self.client.sai_thrift_remove_hostif_trap_group(trap_group)
            