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
Thrift SAI interface y1731 tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb


oam_port_tx_smac = '00:00:00:22:00:00'
default_port_mac = '00:00:00:00:00:00'


@group('y1731')

class afunc_01_MegCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        warmboot(self.client)
        
        try:
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("set meg_type = 0x%x" %meg_type)
                    sys_logging("get meg_type = 0x%x" %a.value.s32)
                    if meg_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("set meg_name = %s" %meg_name)
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("set level = 0x%x" %level)
                    sys_logging("get level = 0x%x" %a.value.u8)
                    if level != a.value.u8:
                        raise NotImplementedError()
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
class afunc_02_EthMepCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        warmboot(self.client)
        
        try:
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_VLAN_ID:
                    sys_logging("set vlan = 0x%x" %vlan)
                    sys_logging("get vlan = 0x%x" %a.value.u32)
                    if vlan != a.value.u32:
                        raise NotImplementedError()            
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
        
class afunc_03_EthRmepCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        remote_mep_id2 = 12
        mac2 = '00:22:22:22:22:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        warmboot(self.client)
        
        try:
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 2 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id2)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id2 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac2)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac2 != a.value.mac:
                        raise NotImplementedError()
                        
            #self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
class afunc_04_EthOamDownMepRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        remote_mep_id2 = 12
        mac2 = '00:22:22:22:22:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 0, str(pkt))
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            
class afunc_05_EthOamUpMepRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        remote_mep_id2 = 12
        mac2 = '00:22:22:22:22:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 1, str(pkt))
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
                        
            #self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_06_TPOamLspTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_lsp_label
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, nhop_lsp_pe1_to_p, nogal=0)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        
        sys_logging("compose tp y1731 oam packet")
        
        srcmac = '00:22:33:44:55:66'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        ach_header = hexstr_to_ascii('10008902')
        
        mpls_inner_pkt = ach_header + str(ccm_hdr)
                                  
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 0, str(pkt))
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_07_TPOamPwTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 200)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, nhop_pw_pe1_to_pe2, nogal=1)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        
        sys_logging("compose tp y1731 oam packet")
        
        srcmac = '00:22:33:44:55:66'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        ach_header = hexstr_to_ascii('10008902')
        
        mpls_inner_pkt = ach_header + str(ccm_hdr)
                                  
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':1,'s':1}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        #cpu tx dm pkt
        dm_type = 'DMM'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0,
                                   rxtsf=0,
                                   txtsb=0,
                                   rxtsb=0)
                                   
        tx_dmm_pkt = ach_header + str(dm_hdr)
                                   
        
        warmboot(self.client)
        
        try:
            #oam pdu rx
            self.ctc_send_packet( 0, str(pkt))

            #dm cpu tx
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=8)
            
            #pdb.set_trace()
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            flush_all_fdb(self.client)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_08_VplsOamFidTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_RAW, SAI_TUNNEL_MPLS_PW_MODE_RAW, True, True, 0, 0)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, oamEn=1)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, oamEn=1)
        #pdb.set_trace()
        mac_action = SAI_PACKET_ACTION_FORWARD
        ### upstream fdb
        #mac_host_remote = '01:80:C2:00:00:33'
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPLS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id = bridge_id, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)

        sys_logging("get meg info")
        attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)

        for a in attrs.attr_list:
            if a.id == SAI_Y1731_SESSION_ATTR_VLAN_ID:
                sys_logging("set vlan = 0x%x" %vlan)
                sys_logging("get vlan = 0x%x" %a.value.u32)
                if vlan != a.value.u32:
                    raise NotImplementedError()
                       
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        #pdb.set_trace()
        
        sys_logging("compose tp y1731 oam packet")
        
        srcmac = '00:22:33:44:55:66'
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
        
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 1, str(pkt))
            #pdb.set_trace()
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                                               
            self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            flush_all_fdb(self.client)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_09_VplsOamVlanTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 20)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, oamEn=0)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, oamEn=0)
        #pdb.set_trace()
        mac_action = SAI_PACKET_ACTION_FORWARD
        ### upstream fdb
        #mac_host_remote = '01:80:C2:00:00:33'
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, dm_en=1, port_id=port1, bridge_id = None, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        #pdb.set_trace()
        
        sys_logging("compose tp y1731 oam packet")
        
        
        ##### ccm packet ####
        srcmac = '00:22:33:44:55:66'
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
        
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                            
                            
        ##### lbm packet ####
        lbm_hdr = simple_lbm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period)
                                   
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=lbm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        lbm_pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)

        ##### lbr packet ####
        lbr_hdr = simple_lbr_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period)
                                   
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=lbr_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        lbr_pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                            
        ##### dm packet ####
        dm_type = 'DMM'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0x1234,
                                   rxtsf=0,
                                   txtsb=0,
                                   rxtsb=0)
                                   
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=dm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        dm_pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                            
        dm_type = 'DMR'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0x1234,
                                   rxtsf=0x4567,
                                   txtsb=0x3344,
                                   rxtsb=0)
                                   
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=dm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        dmr_pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        #cpu tx dmm
        dm_type = 'DMM'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0,
                                   rxtsf=0,
                                   txtsb=0,
                                   rxtsb=0)
                                   
        tx_dmm_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=True,
                                vlan_vid=vlan,
                                eth_type=0x8902,
                                inner_frame=dm_hdr)
        
        warmboot(self.client)
        
        try:
            #rx oam pdu
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_send_packet( 1, str(dmr_pkt))
            #pdb.set_trace()
            
            #dm cpu tx
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=22)
            #pdb.set_trace()
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            
class afunc_10_VpwsOamFidTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_RAW, SAI_TUNNEL_MPLS_PW_MODE_RAW, True, True, 0, 0)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, admin_state=False, oamEn=1)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, admin_state=False, oamEn=1)
        #pdb.set_trace()
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=pw2_tunnel_bport_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=uni_port_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
        
        #mac_action = SAI_PACKET_ACTION_FORWARD
        #### upstream fdb
        ##mac_host_remote = '01:80:C2:00:00:33'
        #mac_host_remote = '00:88:88:88:01:01'
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        #
        #### downstream fdb
        #mac_host_local = '00:77:77:77:01:01'
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPWS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id = bridge_id, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        #pdb.set_trace()
        
        sys_logging("compose tp y1731 oam packet")
        
        srcmac = '00:22:33:44:55:66'
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
        
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        
        warmboot(self.client)
        
        try:
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt))
            
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            
                        
            #self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            #sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            
class afunc_11_EthOamDownMepLMTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        remote_mep_id2 = 12
        mac2 = '00:22:22:22:22:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)

        data_dstmac = '00:66:66:66:66:66'
        data_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=data_dstmac,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.1.1.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        ## lm packet ##
        lm_type = 'LMM'
        lm_hdr = simple_lm_packet(lm_type,
                                   mel=level,
                                   rdi=0,
                                   txfcf=10,
                                   rxfcf=0,
                                   txfcb=0)
                                   
        lmm_pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=lm_hdr)
                                
        lm_type = 'LMR'
        lmr_hdr = simple_lm_packet(lm_type,
                                   mel=level,
                                   rdi=0,
                                   txfcf=10,
                                   rxfcf=20,
                                   txfcb=30)
                                   
        lmr_pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=lmr_hdr)
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 0, str(data_pkt), count=5)
            self.ctc_send_packet( 1, str(data_pkt), count=3)
            #pdb.set_trace()
            
            #self.ctc_send_packet( 0, str(lmm_pkt))
            self.ctc_send_packet( 0, str(lmr_pkt))
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            #self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            
class afunc_12_EthOamDownMepCpuTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        remote_mep_id2 = 12
        mac2 = '00:22:22:22:22:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)

        data_dstmac = '00:66:66:66:66:66'
        data_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=data_dstmac,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.1.1.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        ## lm packet ##
        lm_type = 'LMM'
        lm_hdr = simple_lm_packet(lm_type,
                                   mel=level,
                                   rdi=0,
                                   txfcf=0,
                                   rxfcf=0,
                                   txfcb=0)
                                   
        lmm_pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=lm_hdr)
                                
        lm_type = 'LMR'
        lmr_hdr = simple_lm_packet(lm_type,
                                   mel=level,
                                   rdi=0,
                                   txfcf=10,
                                   rxfcf=20,
                                   txfcb=30)
                                   
        lmr_pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=lmr_hdr)
                                
        dm_type = 'DMM'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0,
                                   rxtsf=0,
                                   txtsb=0,
                                   rxtsb=0)
                                   
        dmm_pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=dm_hdr)
                                
        
        warmboot(self.client)
        
        try:
            #data traffic for lm stats
            #self.ctc_send_packet( 0, str(data_pkt), count=5)
            #self.ctc_send_packet( 1, str(data_pkt), count=3)
            #pdb.set_trace()
            
            #oam pdu rx to cpu
            #self.ctc_send_packet( 0, str(lmm_pkt))
            #self.ctc_send_packet( 0, str(lmr_pkt))
            
            #oam pdu tx from cpu
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            
            #sai_thrift_send_hostif_packet(self.client, mep_id, str(lmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id)
            
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=22)
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_13_VplsOamFidCpuTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data configuration ######
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
        
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_RAW, SAI_TUNNEL_MPLS_PW_MODE_RAW, True, True, 0, 0)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD

        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id=tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, oamEn=1)

        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id_pw2, bridge_id=bridge_id, oamEn=1)

        mac_action = SAI_PACKET_ACTION_FORWARD
        ### upstream fdb
        #mac_host_remote = '01:80:C2:00:00:33'
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #pdb.set_trace()
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPLS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id = bridge_id, vlan_id=vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        sys_logging("compose tp y1731 oam packet")
        
        srcmac = '00:22:33:44:55:66'
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
        
        mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=False,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
        
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                            
                            
        dm_type = 'DMM'
        dm_hdr = simple_dm_packet(dm_type,
                                   mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   txtsf=0,
                                   rxtsf=0,
                                   txtsb=0,
                                   rxtsb=0)
                                   
        tx_dmm_pkt = simple_eth_packet(pktlen=97,
                                eth_dst=oam_dmac1,
                                eth_src=innersrcmac,
                                dl_vlan_enable=True,
                                vlan_vid=vlan,
                                eth_type=0x8902,
                                inner_frame=dm_hdr)
                                   
        
        warmboot(self.client)
        
        try:
            #ccm rx
            #self.ctc_send_packet( 1, str(pkt))
            
            #dm cpu tx
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=22)            
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                #if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                #    sys_logging("set mac = %s" %mac1)
                #    sys_logging("get mac = %s" %a.value.mac)
                #    if mac1 != a.value.mac:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
class afunc_14_EthOamDownMepDualLMStatsTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        lm_type = SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, lm_type=lm_type, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)
        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        #remote_mep_id2 = 12
        #mac2 = '00:22:22:22:22:22'
        #rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)
        #
        #sys_logging("creat rmep id2 = %d" %rmep_id2)
        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name,
                                   txfcf=10,
                                   rxfcb=20,
                                   txfcb=21)
                                   
        pkt = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr)
                                
        ccm_hdr2 = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name,
                                   txfcf=11,
                                   rxfcb=25,
                                   txfcb=30)
                                   
        pkt2 = simple_eth_packet(pktlen=97,
                                eth_dst='01:80:C2:00:00:33',
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                eth_type=0x8902,
                                inner_frame=ccm_hdr2)

        data_dstmac = '00:66:66:66:66:66'
        data_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=data_dstmac,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.1.1.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        
        
        warmboot(self.client)
        
        try:
            self.ctc_send_packet( 0, str(data_pkt), count=6)
            self.ctc_send_packet( 1, str(data_pkt), count=3)
            
            self.ctc_send_packet( 0, str(pkt))
            
            cnt_ids=[]
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCF)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCL)
            counters_results = self.client.sai_thrift_get_y1731_session_lm_stats(mep_id,cnt_ids,len(cnt_ids))
            sys_logging("TX_FCF = %d " %(counters_results[0]))
            sys_logging("RX_FCB = %d " %(counters_results[1]))
            sys_logging("TX_FCB = %d " %(counters_results[2]))
            sys_logging("RX_FCL = %d " %(counters_results[3]))
            #assert (counters_results[0] == 1)
            #assert (counters_results[1] == 124)
            
            self.ctc_send_packet( 0, str(pkt2))
            
            cnt_ids=[]
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCF)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCL)
            counters_results = self.client.sai_thrift_get_y1731_session_lm_stats(mep_id,cnt_ids,len(cnt_ids))
            sys_logging("TX_FCF = %d " %(counters_results[0]))
            sys_logging("RX_FCB = %d " %(counters_results[1]))
            sys_logging("TX_FCB = %d " %(counters_results[2]))
            sys_logging("RX_FCL = %d " %(counters_results[3]))
            
            time.sleep(1)
            
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("set meg_id = 0x%x" %meg_id)
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("set local_mep_id = %s" %local_mep_id)
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("set ccm_period = 0x%x" %ccm_period)
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("set mep_id = 0x%x" %mep_id)
                    sys_logging("get mep_id = 0x%x" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("set remote_mep_id = %s" %remote_mep_id1)
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("set mac = %s" %mac1)
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            #self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            #self.client.sai_thrift_remove_y1731_rmep(rmep_id2)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            

class func_01_create_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = "ETHER_VLAN"
        level1 = 0

        meg_type2 = SAI_Y1731_MEG_TYPE_L2VPN_VLAN
        meg_name2 = "L2VPN_VLAN"
        level2 = 1

        meg_type3 = SAI_Y1731_MEG_TYPE_L2VPN_VPLS
        meg_name3 = "L2VPN_VPLS"
        level3 = 2

        meg_type4 = SAI_Y1731_MEG_TYPE_L2VPN_VPWS
        meg_name4 = "L2VPN_VPWS"
        level4 = 3

        meg_type5 = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name5 = "MPLS_TP"
        level5 = 7
        
        meg_id1 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, level1)
        sys_logging("creat meg id = %d" %meg_id1)
        assert( meg_id1 != SAI_NULL_OBJECT_ID)
        meg_id2 = sai_thrift_create_y1731_meg(self.client, meg_type2, meg_name2, level2)
        sys_logging("creat meg id = %d" %meg_id2)
        assert( meg_id2 != SAI_NULL_OBJECT_ID)        
        meg_id3 = sai_thrift_create_y1731_meg(self.client, meg_type3, meg_name3, level3)
        sys_logging("creat meg id = %d" %meg_id3)    
        assert( meg_id3 != SAI_NULL_OBJECT_ID)        
        meg_id4 = sai_thrift_create_y1731_meg(self.client, meg_type4, meg_name4, level4)
        sys_logging("creat meg id = %d" %meg_id4)
        assert( meg_id4 != SAI_NULL_OBJECT_ID)        
        meg_id5 = sai_thrift_create_y1731_meg(self.client, meg_type5, meg_name5, level5)
        sys_logging("creat meg id = %d" %meg_id5) 
        assert( meg_id5 != SAI_NULL_OBJECT_ID)        
        warmboot(self.client)
        
        try:
        
            sys_logging("get meg1 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type1 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name1 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level1 != a.value.u8:
                        raise NotImplementedError()

            sys_logging("get meg2 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type2 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name2 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level2 != a.value.u8:
                        raise NotImplementedError()
                        
            sys_logging("get meg3 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id3)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type3 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name3 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level3 != a.value.u8:
                        raise NotImplementedError()

            sys_logging("get meg4 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id4)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type4 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name4 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level4 != a.value.u8:
                        raise NotImplementedError()

            sys_logging("get meg5 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id5)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type5 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name5 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level5 != a.value.u8:
                        raise NotImplementedError()
                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id1)
            self.client.sai_thrift_remove_y1731_meg(meg_id2)            
            self.client.sai_thrift_remove_y1731_meg(meg_id3)
            self.client.sai_thrift_remove_y1731_meg(meg_id4)             
            self.client.sai_thrift_remove_y1731_meg(meg_id5)
           
            

class func_02_create_same_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = "ETHER_VLAN"
        level1 = 0
        
        meg_id1 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, level1)
        sys_logging("creat meg id = %d" %meg_id1)
        assert( meg_id1 != SAI_NULL_OBJECT_ID)
        
        meg_id2 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, 1)
        sys_logging("creat meg id = %d" %meg_id2)
        assert( meg_id2 == SAI_NULL_OBJECT_ID)      
        
        warmboot(self.client)
        
        try:
        
            sys_logging("get meg1 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type1 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name1 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level1 != a.value.u8:
                        raise NotImplementedError()                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id1)
            


class func_03_create_multi_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = "ETHER_VLAN1"
        level1 = 1
        
        meg_id1 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, level1)
        sys_logging("creat meg id = %d" %meg_id1)
        assert( meg_id1 != SAI_NULL_OBJECT_ID)
        
        meg_type2 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name2 = "ETHER_VLAN2"
        level2 = 1
        
        meg_id2 = sai_thrift_create_y1731_meg(self.client, meg_type2, meg_name2, level2)
        sys_logging("creat meg id = %d" %meg_id2)
        assert( meg_id2 != SAI_NULL_OBJECT_ID)     
        
        assert( meg_id1 != meg_id2 )
        
        warmboot(self.client)
        
        try:
        
            sys_logging("get meg1 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type1 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name1 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level1 != a.value.u8:
                        raise NotImplementedError()
            
            sys_logging("get meg2 info")
            attrs = self.client.sai_thrift_get_y1731_meg_attribute(meg_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)            
            for a in attrs.attr_list:
                if a.id == SAI_Y1731_MEG_ATTR_TYPE:
                    sys_logging("get meg type = 0x%x" %a.value.s32)
                    if meg_type2 != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_NAME:
                    sys_logging("get meg_name = %s" %a.value.chardata)
                    if meg_name2 != a.value.chardata:
                        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("get meg level = 0x%x" %a.value.u8)
                    if level2 != a.value.u8:
                        raise NotImplementedError()
                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id1)
            self.client.sai_thrift_remove_y1731_meg(meg_id2) 



class func_04_create_max_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = ''
        level1 = 0
        
        meg_id_list = range(684)
         
        for i in range(0,682):
            meg_name = '%d' %i
            sys_logging("meg_name = %s" %meg_name)
            meg_id_list[i] = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name, level1)
            sys_logging("creat meg id = %d" %meg_id_list[i])
            assert( meg_id_list[i] != SAI_NULL_OBJECT_ID)
                   
        warmboot(self.client)
        
        try:

            meg_name = '%d' %682
            sys_logging("meg_name = %s" %meg_name)
            meg_id_list[682] = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name, level1)
            sys_logging("creat meg id = %d" %meg_id_list[682])
            assert( meg_id_list[682] == SAI_NULL_OBJECT_ID)            
            
        finally:
        
            sys_logging("clear configuration")
            for i in range(0,682):
                meg_name = '%d' %i
                sys_logging("meg_name = %s" %meg_name)            
                self.client.sai_thrift_remove_y1731_meg(meg_id_list[i])
                sys_logging("remove meg id = %d" %meg_id_list[i])



class func_05_remove_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = "ETHER_VLAN"
        level1 = 0
        
        meg_id1 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, level1)
        sys_logging("creat meg id = %d" %meg_id1)
        assert( meg_id1 != SAI_NULL_OBJECT_ID)
                    
        warmboot(self.client)
        
        try:
        
            status = self.client.sai_thrift_remove_y1731_meg(meg_id1)
            sys_logging("remove meg status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 
                                
        finally:
        
            sys_logging("clear configuration")


class func_06_remove_not_exist_y1731_meg_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        meg_type1 = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name1 = "ETHER_VLAN"
        level1 = 0
        
        meg_id1 = sai_thrift_create_y1731_meg(self.client, meg_type1, meg_name1, level1)
        sys_logging("creat meg id = %d" %meg_id1)
        assert( meg_id1 != SAI_NULL_OBJECT_ID)
                    
        warmboot(self.client)
        
        try:
        
            status = self.client.sai_thrift_remove_y1731_meg(meg_id1)
            sys_logging("remove meg status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 

            status = self.client.sai_thrift_remove_y1731_meg(meg_id1)
            sys_logging("remove meg status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
            
        finally:
        
            sys_logging("clear configuration")



class func_07_create_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id)
        
        warmboot(self.client)
        
        try:
            sys_logging("get mep info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DIR:
                    sys_logging("get dir = 0x%x" %a.value.s32)
                    if dir != a.value.s32:
                        raise NotImplementedError() 
                        
                if a.id == SAI_Y1731_SESSION_ATTR_VLAN_ID:
                    sys_logging("get vlan = 0x%x" %a.value.u32)
                    if vlan != a.value.u32:
                        raise NotImplementedError()  
                        
                if a.id == SAI_Y1731_SESSION_ATTR_BRIDGE_ID:
                    sys_logging("get bridge id  = 0x%x" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()  
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError() 
                        
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_CCM_ENABLE:
                    sys_logging("get ccm enable = 0x%x" %a.value.booldata)
                    if ccm_en != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE:
                    sys_logging("get lm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_ENABLE:
                    sys_logging("get lm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_TYPE:
                    sys_logging("get lm type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE:
                    sys_logging("get dm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_ENABLE:
                    sys_logging("get dm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos  = 0x%x" %a.value.u8)
                    if 1 != a.value.u8:
                        raise NotImplementedError()
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class func_08_create_same_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id1 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id1)
        assert ( mep_id1 != SAI_NULL_OBJECT_ID)

        mep_id2 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id2)
        assert ( mep_id2 == SAI_NULL_OBJECT_ID)

        mep_id3 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, 11, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id3)
        assert ( mep_id3 == SAI_NULL_OBJECT_ID)
        
        warmboot(self.client)
        
        try:
            sys_logging("get mep1 info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_Y1731_SESSION_ATTR_MEG:
                    sys_logging("get meg_id = 0x%x" %a.value.oid)
                    if meg_id != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DIR:
                    sys_logging("get dir = 0x%x" %a.value.s32)
                    if dir != a.value.s32:
                        raise NotImplementedError() 
                        
                if a.id == SAI_Y1731_SESSION_ATTR_VLAN_ID:
                    sys_logging("get vlan = 0x%x" %a.value.u32)
                    if vlan != a.value.u32:
                        raise NotImplementedError()  
                        
                if a.id == SAI_Y1731_SESSION_ATTR_BRIDGE_ID:
                    sys_logging("get bridge id  = 0x%x" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()  
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError() 
                        
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("get local_mep_id = %s" %a.value.u32)
                    if local_mep_id != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if ccm_period != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_CCM_ENABLE:
                    sys_logging("get ccm enable = 0x%x" %a.value.booldata)
                    if ccm_en != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE:
                    sys_logging("get lm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_ENABLE:
                    sys_logging("get lm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_TYPE:
                    sys_logging("get lm type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE:
                    sys_logging("get dm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_ENABLE:
                    sys_logging("get dm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos  = 0x%x" %a.value.u8)
                    if 1 != a.value.u8:
                        raise NotImplementedError()
          
            self.ctc_show_packet(0)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id1)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            

class func_09_create_multi_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id1 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id1)
        assert ( mep_id1 != SAI_NULL_OBJECT_ID)

        mep_id2 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port2, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id2)
        assert ( mep_id2 != SAI_NULL_OBJECT_ID)

        assert (mep_id1 != mep_id2)
        
        warmboot(self.client)
        
        try:
        
            sys_logging("get mep1 info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError() 
                        
            sys_logging("get mep2 info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if port2 != a.value.oid:
                        raise NotImplementedError() 

                        
            self.ctc_show_packet(0)
            self.ctc_show_packet(1)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id2)            
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            

#stress case can not test on uml           
'''
class func_10_create_max_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1

        
        mep_id_list = range(4096)
         
        for i in range(2,2050):    
            vlan = i      
            sys_logging(" vlan_id = %d" %vlan)            
            mep_id_list[i] = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
            sys_logging("creat mep id = %d" %mep_id_list[i])
            assert ( mep_id_list[i] != SAI_NULL_OBJECT_ID)
        
        warmboot(self.client)
        
        try:
            
            vlan = 2050      
            sys_logging(" vlan_id = %d" %vlan)            
            mep_id_list[2050] = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=2050)        
            sys_logging("creat mep id = %d" %mep_id_list[2050])
            assert ( mep_id_list[2050] == SAI_NULL_OBJECT_ID)        

            
        finally:
        
            sys_logging("clear configuration")
            for i in range(2,2050): 
                self.client.sai_thrift_remove_y1731_session(mep_id_list[i])
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
'''            
            
class func_11_remove_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                  
            sys_logging("remove mep session")                        
            status = self.client.sai_thrift_remove_y1731_session(mep_id)  
            sys_logging("remove mep session status = %d" %status)            
            assert (status != SAI_STATUS_SUCCESS)
            
            status = self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            sys_logging("remove rmep status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("remove mep session")                        
            status = self.client.sai_thrift_remove_y1731_session(mep_id)  
            sys_logging("remove mep session status = %d" %status)            
            assert (status == SAI_STATUS_SUCCESS)            
            
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            
 
class func_12_remove_not_exist_y1731_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
               
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)

        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id1 = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id1)
        assert ( mep_id1 != SAI_NULL_OBJECT_ID)
        
        warmboot(self.client)
        
        try:
        
            sys_logging("get mep1 info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
                                   
            sys_logging("remove mep1 session")                        
            status = self.client.sai_thrift_remove_y1731_session(mep_id1)  
            sys_logging("remove mep1 session status = %d" %status)            
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("remove mep1 session")                        
            status = self.client.sai_thrift_remove_y1731_session(mep_id1)  
            sys_logging("remove mep1 session status = %d" %status)            
            assert (status != SAI_STATUS_SUCCESS)
            
        finally:
        
            sys_logging("clear configuration")        
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

'''
class func_13_create_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("get mep_id = %d" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                        
            mac2 = '00:11:11:11:11:22'
            attr_value = sai_thrift_attribute_value_t(mac=mac2)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
            sys_logging("set rmep attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("get mep_id = %d" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac2 != a.value.mac:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
'''


class func_14_create_same_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            remote_mep_id1 = 11
            mac1 = '00:11:11:11:11:11'
            rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
            sys_logging("creat rmep id2 = %d" %rmep_id2)
            assert ( rmep_id2 == SAI_NULL_OBJECT_ID )
        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("get mep_id = %d" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                                                          
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)


            


class func_15_create_multi_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        assert ( rmep_id1 != SAI_NULL_OBJECT_ID )
        
        remote_mep_id2 = 12
        mac2 = '00:11:11:11:11:22'
        rmep_id2 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id2, mac2)        
        sys_logging("creat rmep id2 = %d" %rmep_id2)
        assert ( rmep_id2 != SAI_NULL_OBJECT_ID )

        assert ( rmep_id2 != rmep_id1 )

        rmep_list = [rmep_id1,rmep_id2]
        
        warmboot(self.client)
        
        try:

            sys_logging("get mep info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST:                    
                    sys_logging("get mep_id rmep list = ")
                    sys_logging("SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST count = %d ###" %a.value.objlist.count)
                    if 2 != a.value.objlist.count:
                        raise NotImplementedError()
                    for b in a.value.objlist.object_id_list:
                        sys_logging("rmep_id is  = %d" %b)
                        assert (b in rmep_list) 
        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("get mep_id = %d" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id1 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac1 != a.value.mac:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

            sys_logging("get rmep 2 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id2)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID:
                    sys_logging("get mep_id = %d" %a.value.oid)
                    if mep_id != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID:
                    sys_logging("get remote_mep_id = %s" %a.value.u32)
                    if remote_mep_id2 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS:
                    sys_logging("get mac = %s" %a.value.mac)
                    if mac2 != a.value.mac:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_rmep(rmep_id2)            
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)



class func_16_create_max_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("create meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("create mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        
        rmep_list = range(4106)         
        for i in range(11,4104):  
            remote_mep_id1 = i  
            sys_logging(" remote_mep_id1 = %d" %remote_mep_id1)            
            rmep_list[i] = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
            sys_logging("create rmep id1 = %d" %rmep_list[i])
            assert ( rmep_list[i] != SAI_NULL_OBJECT_ID )
        
        warmboot(self.client)
        
        try:
        
            remote_mep_id1 = 4105  
            sys_logging(" remote_mep_id1 = %d" %remote_mep_id1)            
            rmep_list[4105] = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
            sys_logging("create rmep id1 = %d" %rmep_list[4105])
            assert ( rmep_list[4105] == SAI_NULL_OBJECT_ID )
            
        finally:
        
            sys_logging("clear configuration")
            for i in range(11,4104):  
                remote_mep_id1 = i  
                sys_logging(" remote_mep_id1 = %d" %remote_mep_id1)                
                self.client.sai_thrift_remove_y1731_rmep(rmep_list[i])
                sys_logging("remove rmep id1 = %d" %rmep_list[i])
                
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            



class func_17_remove_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            sys_logging("remove rmep status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status != SAI_STATUS_SUCCESS)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)



class func_18_remove_not_exist_y1731_rmep_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        oam_dmac1 = '01:80:C2:00:00:33'
        
        vlan = 10
        sys_logging("### Step1. Create Vlan, mcast FDB ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        grp_attr_list = []
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=oam_dmac1, bv_id=vlan_oid1)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
        
        sys_logging("### Step2. Set Port Oam Enable ###")
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            sys_logging("remove rmep status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            sys_logging("remove rmep status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            

            
class func_19_EthOam_DownMep_Dual_LMStats_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        vlan = 10        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr) 
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 0
        lm_type = SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, lm_type=lm_type, port_id=port1, vlan_id = vlan)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        data_dstmac = '00:66:66:66:66:66'
        data_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=data_dstmac,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.1.1.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                                
        warmboot(self.client)
        
        try:
        
            self.ctc_send_packet( 0, str(data_pkt), count=2)
            self.ctc_send_packet( 1, str(data_pkt), count=3)

            sys_logging(" step1 cpu tx ccm")
            
            oam_multicast_dmac = '01:80:C2:00:00:34'
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name,
                                        txfcf=0,
                                        rxfcb=0,
                                        txfcb=0)
                                        
            tx_ccm_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,                                    
                                    inner_frame=ccm_hdr)
            
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_ccm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id)                                    
            
            time.sleep(1)
            
            ccm_hdr1 = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name,
                                        txfcf=3,
                                        rxfcb=0,
                                        txfcb=0)
                                        
            tx_ccm_pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    vlan_pcp=0,                                    
                                    inner_frame=ccm_hdr1)            
            
            self.ctc_show_packet(0,None,str(tx_ccm_pkt1),1)


            sys_logging(" step2 receive ccm")

            ccm_hdr2 = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name,
                                        txfcf=5,
                                        rxfcb=6,
                                        txfcb=7)
                                        
            tx_ccm_pkt2 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_port_tx_smac,
                                    eth_src=mac1,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    vlan_pcp=0,                                    
                                    inner_frame=ccm_hdr2)            
            

            self.client.sai_thrift_clear_cpu_packet_info() 
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(tx_ccm_pkt2))
            time.sleep(1)
            '''
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()
            '''
                    
            cnt_ids=[]
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCF)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_TX_FCB)
            cnt_ids.append(SAI_Y1731_SESSION_LM_STAT_RX_FCL)
            
            counters_results = self.client.sai_thrift_get_y1731_session_lm_stats(mep_id,cnt_ids,len(cnt_ids))
            
            sys_logging("TX_FCF = %d " %(counters_results[0]))
            sys_logging("RX_FCB = %d " %(counters_results[1]))
            sys_logging("TX_FCB = %d " %(counters_results[2]))
            sys_logging("RX_FCL = %d " %(counters_results[3]))
            assert ( counters_results[0] == 5 )
            assert ( counters_results[1] == 6 )
            assert ( counters_results[2] == 7 )
            assert ( counters_results[3] == 2 )            

                       
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)            

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)            

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 

            
class scenario_01_eth_down_mep_ccm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
            
            oam_multicast_dmac = '01:80:C2:00:00:34'
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))
            
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get vlan cos = 0x%x" %a.value.u8)
                    if 1 != a.value.u8:
                        raise NotImplementedError()
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                        
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===
            # sdk cli show
            # show oam mep y1731 eth-oam port 0 vlan 10 md-level 4
            # rmep, 1stPkt

            attr_value = sai_thrift_attribute_value_t(u8=7)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get vlan cos = 0x%x" %a.value.u8)
                    if 7 != a.value.u8:
                        raise NotImplementedError()

            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=7,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))
          
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_01_eth_down_mep_ccm_test_for_lag(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        lag_oid = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        #lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)        

        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        is_lag = 1        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)

                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr) 
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        attrs = self.client.sai_thrift_get_port_attribute(port2)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
                
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=lag_oid, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("create rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if lag_oid != a.value.oid:
                        raise NotImplementedError() 

                        
            oam_multicast_dmac = '01:80:C2:00:00:34'
            oam_port_tx_smac_lag = '00:00:00:22:00:40'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac_lag,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))
                      
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                        
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===
            # sdk cli show
            # show oam mep y1731 eth-oam port 0 vlan 10 md-level 4
            # rmep, 1stPkt

          
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            #sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)  
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_02_eth_up_mep_ccm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
           
            oam_multicast_dmac = '01:80:C2:00:00:34'
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(1,None,str(pkt1))

            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                        
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(1, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===
            # sdk cli show
            # show oam mep y1731 eth-oam port 0 vlan 10 md-level 4
            # rmep, 1stPkt
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 





class scenario_03_eth_down_mep_lb_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
           
            sys_logging("### Step4. receive lbm ###")

            oam_multicast_dmac = '01:80:C2:00:00:34'
            
            
            lbm_hdr = simple_lbm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbm_hdr)

            lbr_hdr = simple_lbr_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt2 = simple_eth_packet(pktlen=97,
                                    eth_dst=mac1,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbr_hdr)
                                    
                                    
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt2, [0]) 

            sys_logging("### Step5. receive lbr ###")

            lbr_hdr = simple_lbr_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt3 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_port_tx_smac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbr_hdr)
                                    
                                    
            self.client.sai_thrift_clear_cpu_packet_info()              
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(pkt3))
            time.sleep(1)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

            
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)


            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 






class scenario_04_eth_down_mep_lt_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 0
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
           
            self.client.sai_thrift_clear_cpu_packet_info()
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError()
                
            oam_multicast_dmac = '01:80:C2:00:00:3c'
            

            
            ltm_hdr = simple_ltm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ltm_hdr)
                                    

            ltr_hdr = simple_ltr_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt2 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ltr_hdr)
                                    
            self.client.sai_thrift_clear_cpu_packet_info()              
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(pkt1))
            time.sleep(1)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 



            self.client.sai_thrift_clear_cpu_packet_info()              
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(pkt2))
            time.sleep(1)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 



class scenario_05_eth_rdi_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                           
            sys_logging("get session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            # rdi is 0
            oam_multicast_dmac = '01:80:C2:00:00:34'
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))

            
            wrong_oam_macda = '01:80:C2:00:00:33'
            wrong_level = 3
            # ccm with wrong level    
            ccm_hdr = simple_ccm_packet(mel=wrong_level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=wrong_oam_macda,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            # report low ccm error defect
            # event id: 1 and 7
            # sdk cli show
            # show oam mep y1731 eth-oam port 0 vlan 10 md-level 4
            # lmep, TxRDI
            
            sys_logging("get session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            # rdi is 1
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=1,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))

            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_RDI, value=attr_value)
            self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set local rdi " )            
            
            sys_logging("get session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            # rdi is 0
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_show_packet(0,None,str(pkt1))


            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_RDI, value=attr_value)
            self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set local rdi " )            
            
            sys_logging("get session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_RDI:
                    sys_logging("get local rdi = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            # rdi is 1
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=1,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    vlan_pcp=1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 



class scenario_06_eth_link_oam_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 0
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=0, bridge_id=None)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            oam_multicast_dmac = '01:80:C2:00:00:30'
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name)

                                        
            pkt1 = simple_eth_packet(pktlen=93,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=False,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            self.ctc_show_packet(0,None,str(pkt1))


            sys_logging("get mep info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_Y1731_SESSION_ATTR_VLAN_ID:
                    sys_logging("get vlan = 0x%x" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()  
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                        
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=93,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=mac1,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===
            # sdk cli show
            # show oam mep y1731 eth-oam port 0 vlan 10 md-level 4
            # rmep, 1stPkt
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 




class scenario_07_eth_down_mep_lm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr) 
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
            if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
                
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 0
        lm_type = SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, lm_type=lm_type, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)

        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)

        data_dstmac = '00:66:66:66:66:66'
        data_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=data_dstmac,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.1.1.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        warmboot(self.client)
        
        try:

            self.ctc_send_packet( 0, str(data_pkt), count=2)
            self.ctc_send_packet( 1, str(data_pkt), count=3)
            

            # Single LM
            
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                    
                if a.id == SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE:
                    sys_logging("get lm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_ENABLE:
                    sys_logging("get lm enable = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_TYPE:
                    sys_logging("get lm type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED != a.value.s32:
                        raise NotImplementedError()


            sys_logging("### Step1. TX Y1731_LMM ###")

            lm_type = 'LMM'
            lm_hdr = simple_lm_packet(lm_type,
                                       mel=level,
                                       rdi=0,
                                       txfcf=0,
                                       rxfcf=0,
                                       txfcb=0)
                                       
            lmm_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lm_hdr)           

            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_LM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(lmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id,)                                    


            lm_hdr = simple_lm_packet(lm_type,
                                       mel=level,
                                       rdi=0,
                                       txfcf=3,
                                       rxfcf=0,
                                       txfcb=0)
                                       
            lmm_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lm_hdr) 

            
            self.ctc_show_packet(0,None,str(lmm_pkt),1)


            sys_logging("### Step2. RX Y1731_LMM ###")

            lm_type = 'LMR'
            lmr_hdr = simple_lm_packet(lm_type,
                                       mel=level,
                                       rdi=0,
                                       txfcf=3,
                                       rxfcf=2,
                                       txfcb=3)
                                       
            lmr_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=mac1,
                                    eth_src=oam_port_tx_smac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lmr_hdr)


            self.ctc_send_packet(0, str(lmm_pkt))
            self.ctc_verify_packets(lmr_pkt, [0])


            sys_logging("### Step3. RX Y1731_LMR ###")

            self.client.sai_thrift_clear_cpu_packet_info()

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 

            self.ctc_send_packet(0, str(lmr_pkt))

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = 0x%x" %a.value.u64)
                    if 2 != a.value.u64:
                        raise NotImplementedError()                

            self.client.sai_thrift_clear_cpu_packet_info()

            
            # Dual LM

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
                             
            attr_value = sai_thrift_attribute_value_t(s32=SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)            

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)  
                 
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_ENABLE:
                    sys_logging("get ccm enable = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE:
                    sys_logging("get lm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_ENABLE:
                    sys_logging("get lm enable = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_LM_TYPE:
                    sys_logging("get lm type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get vlan cos = 0x%x" %a.value.u8)
                    if 0 != a.value.u8:
                        raise NotImplementedError()
                    

            sys_logging("### Step1. TX Y1731_CCM ###")

            oam_multicast_dmac = '01:80:C2:00:00:34'
            

            ccm_hdr1 = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name,
                                        txfcf=3,
                                        rxfcb=0,
                                        txfcb=0)
                                        
            tx_ccm_pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_multicast_dmac,
                                    eth_src=oam_port_tx_smac,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    vlan_pcp=0,                                    
                                    inner_frame=ccm_hdr1)            
            
            self.ctc_show_packet(0,None,str(tx_ccm_pkt1))


            sys_logging("### Step2. RX Y1731_CCM ###")
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name,
                                        txfcf=0,
                                        rxfcb=0,
                                        txfcb=0)
                                        
            pkt = simple_eth_packet(pktlen=93,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,                                    
                                    inner_frame=ccm_hdr)

            ccm_hdr1 = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=local_mep_id,
                                        megid=meg_name,
                                        txfcf=3,
                                        rxfcb=2,
                                        txfcb=0)
                                        

            pkt1 = simple_eth_packet(pktlen=93,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=oam_port_tx_smac,
                                    eth_type=0x8902,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,                                    
                                    inner_frame=ccm_hdr1)
                                    
            self.ctc_send_packet(0, str(pkt))            
            self.ctc_verify_packets(pkt1, [0]) 
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_08_eth_down_mep_dm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)
                
        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 0
        lm_type = SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, lm_en=1, lm_type=lm_type, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)

        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                       
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                    
                if a.id == SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE:
                    sys_logging("get dm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_ENABLE:
                    sys_logging("get dm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:

                if a.id == SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE:
                    sys_logging("get dm offload type = 0x%x" %a.value.s32)
                    if SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_DM_ENABLE:
                    sys_logging("get dm enable = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()



            sys_logging("### Step4. TX Y1731_1DM ###")

            oam_dmac1 = '01:80:C2:00:00:34'            
            dm_type = '1DM'
            dm_hdr = simple_dm_packet(dm_type,
                                       mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       txtsf=0x445678,
                                       rxtsf=0,
                                       txtsb=0,
                                       rxtsb=0)
                                       
            tx_dmm_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    eth_type=0x8902,
                                    inner_frame=dm_hdr)

            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=22)                                    

            self.ctc_show_packet(0,None,str(tx_dmm_pkt),1)

            sys_logging("### Step5. RX Y1731_1DM ###")

            self.client.sai_thrift_clear_cpu_packet_info()

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 

            self.ctc_send_packet(0, str(tx_dmm_pkt))

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = 0x%x" %a.value.oid)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = 0x%x" %a.value.u64)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                
                if a.id == SAI_HOSTIF_PACKET_ATTR_TIMESTAMP:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_sec)
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_nsec)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()

            sys_logging("### Step6. TX Y1731_DMM ###")
            
            oam_dmac1 = '01:80:C2:00:00:34'            
            dm_type = 'DMM'
            dm_hdr = simple_dm_packet(dm_type,
                                       mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       txtsf=0x445678,
                                       rxtsf=0,
                                       txtsb=0,
                                       rxtsb=0)
                                       
            tx_dmm_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    eth_type=0x8902,
                                    inner_frame=dm_hdr)
            
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_OAM_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, mep_id, str(tx_dmm_pkt), oam_tx_type, host_if_tx_type, oam_session=mep_id, dm_offset=22)                                    
            
            self.ctc_show_packet(0,None,str(tx_dmm_pkt),1)

            sys_logging("### Step7. RX Y1731_DMM ###")

            oam_mac = '00:00:00:22:00:00'
            
            dm_type = 'DMR'
            dm_hdr = simple_dm_packet(dm_type,
                                       mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       txtsf=0x445678,
                                       rxtsf=0x345678,
                                       txtsb=0x445678,
                                       rxtsb=0)
                                       
            rx_dmr_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=mac1,
                                    eth_src=oam_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan,
                                    eth_type=0x8902,
                                    inner_frame=dm_hdr)

            self.ctc_send_packet(0, str(tx_dmm_pkt))
            self.ctc_verify_packets(rx_dmr_pkt, [0]) 

            

            sys_logging("### Step8. RX Y1731_DMR ###")


            self.client.sai_thrift_clear_cpu_packet_info()
            
            self.ctc_send_packet(0, str(rx_dmr_pkt))
        
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = 0x%x" %a.value.oid)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = 0x%x" %a.value.u64)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                
                if a.id == SAI_HOSTIF_PACKET_ATTR_TIMESTAMP:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_sec)
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_nsec)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                    
            self.client.sai_thrift_clear_cpu_packet_info()

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_09_vpls_vlan_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data forward configuration ######
        
        vlan = 10        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
                
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("1d bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
                      
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 10)
        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 100
        pop_nums = 1
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, oamEn=0)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, oamEn=0)

        mac_action = SAI_PACKET_ACTION_FORWARD
        
        ### upstream fdb
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id=None, vlan_id=vlan)      
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)      
        sys_logging("creat rmep id1 = %d" %rmep_id1)
      
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
            
            srcmac = '00:22:33:44:55:66'
            
            oam_dmac1 = '01:80:C2:00:00:33'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
            
            mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=innersrcmac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=srcmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

            self.ctc_send_packet( 1, str(pkt))

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                        
            self.ctc_show_packet(1)
            
            attr_value = sai_thrift_attribute_value_t(u32=13)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(s32=2)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_PERIOD, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(u8=5)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("get local mep_id = 0x%x" %a.value.u32)
                    if 13 != a.value.u32:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if 2 != a.value.s32:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos  = 0x%x" %a.value.u8)
                    if 5 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_CCM_ENABLE:
                    sys_logging("get ccm enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            self.ctc_show_packet(1)
                       
                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 




class scenario_10_vpls_vsi_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        
        ##### data forward configuration ######
        
        vlan = 10        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     
                
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("1d bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
                      
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 10)
        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 100
        pop_nums = 1
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, oamEn=1)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, oamEn=1)

        mac_action = SAI_PACKET_ACTION_FORWARD
        
        ### upstream fdb
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPLS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id=bridge_id, vlan_id=vlan)      
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)      
        sys_logging("creat rmep id1 = %d" %rmep_id1)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_ENABLE, value=attr_value)
        status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
        sys_logging("set mep session attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_ENABLE, value=attr_value)
        status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
        sys_logging("set mep session attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)
        
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
            
            srcmac = '00:22:33:44:55:66'
            
            oam_dmac1 = '01:80:C2:00:00:33'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
            
            mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=innersrcmac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=srcmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

            self.ctc_send_packet( 1, str(pkt))
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
        
            self.ctc_show_packet(1)
            
            attr_value = sai_thrift_attribute_value_t(u32=13)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(s32=2)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_CCM_PERIOD, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u8=5)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID:
                    sys_logging("get local mep_id = 0x%x" %a.value.u32)
                    if 13 != a.value.u32:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_CCM_PERIOD:
                    sys_logging("get ccm_period = 0x%x" %a.value.s32)
                    if 2 != a.value.s32:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos  = 0x%x" %a.value.u8)
                    if 5 != a.value.u8:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(1)
                       
                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_10_vpls_vsi_test_for_lag(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        ##### data forward configuration ######

        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        vlan = 10        
        
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)     

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr) 
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("1d bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
                      
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 10)
        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 100
        pop_nums = 1
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
                  
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, lag_oid, bridge_id, vlan, oamEn=1)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, oamEn=1)

        mac_action = SAI_PACKET_ACTION_FORWARD
        
        ### upstream fdb
        mac_host_remote = '00:88:88:88:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid, mac_action)
        
        ### downstream fdb
        mac_host_local = '00:77:77:77:01:01'
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac_host_local, uni_port_oid, mac_action)
        
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPLS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=lag_oid, bridge_id=bridge_id, vlan_id=vlan)      
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)      
        sys_logging("creat rmep id1 = %d" %rmep_id1)

        
        try:

            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_Y1731_SESSION_ATTR_PORT_ID:
                    sys_logging("get port id  = 0x%x" %a.value.oid)
                    if lag_oid != a.value.oid:
                        raise NotImplementedError() 
                        
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
            
            srcmac = '00:22:33:44:55:66'
            
            oam_dmac1 = '01:80:C2:00:00:33'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
            
            mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=innersrcmac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=srcmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

            self.ctc_send_packet( 2, str(pkt))
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
        
            self.ctc_show_packet(2)
                                                          
        finally:
        
            sys_logging("clear configuration")
            
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, lag_oid)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
                       
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)    

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_11_vpws_vlan_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        ##### data forward configuration ######
        
        vlan = 10        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)             
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 10)        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 100
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, admin_state=False, oamEn=0)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, admin_state=False, oamEn=0)

        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=pw2_tunnel_bport_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)        
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=uni_port_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
      
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id=None, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)       
        sys_logging("creat rmep id1 = %d" %rmep_id1)
                                           
        warmboot(self.client)
        
        try:


            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
            
            srcmac = '00:22:33:44:55:66'
            
            oam_dmac1 = '01:80:C2:00:00:33'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
            
            mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=innersrcmac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=srcmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

            self.ctc_send_packet( 1, str(pkt))

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(1)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 




class scenario_12_vpws_vsi_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        ##### data forward configuration ######
        
        vlan = 10        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        sys_logging("### Step2. Set Port Oam Enable ###")

        attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)             
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 10)        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 100
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        sys_logging("Set bridge configuration")
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan, admin_state=False, oamEn=1)
        
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, admin_state=False, oamEn=1)

        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=pw2_tunnel_bport_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)        
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=uni_port_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
      
        #### OAM configuration ####
        meg_type = SAI_Y1731_MEG_TYPE_L2VPN_VPWS
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_UPMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, bridge_id=bridge_id, vlan_id=vlan)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        innersrcmac = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, innersrcmac)       
        sys_logging("creat rmep id1 = %d" %rmep_id1)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_LM_ENABLE, value=attr_value)
        status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
        sys_logging("set mep session attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_DM_ENABLE, value=attr_value)
        status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
        sys_logging("set mep session attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)
        
        warmboot(self.client)
        
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
            
            srcmac = '00:22:33:44:55:66'
            
            oam_dmac1 = '01:80:C2:00:00:33'
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
            
            mpls_inner_pkt = simple_eth_packet(pktlen=97,
                                    eth_dst=oam_dmac1,
                                    eth_src=innersrcmac,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':10,'s':1}, {'label':0,'tc':0,'ttl':0,'s':0}]
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=srcmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

            self.ctc_send_packet(1, str(pkt))


            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(1)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            sai_thrift_remove_bridge_sub_port_2(self.client, uni_port_oid, port1)            
            self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=default_port_mac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 


class scenario_13_tp_section_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0] 

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4        
        dst_ip = '20.20.20.1'                                    
        dmac1 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        sys_logging("create neighbor1")

        dst_ip2 = '20.20.20.2'                                    
        dmac2 = '00:00:00:00:00:02'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip2, dmac2)
        sys_logging("create neighbor2")
        
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        sys_logging("create nhop to route interface")

        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id1)
        sys_logging("create nhop to route interface")
        
        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "MPLS_TP"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 2 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_tp_section_session(self.client, meg_id, rif_id1, dir, local_mep_id, ccm_period, ccm_en, nhop1)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("compose tp y1731 oam packet")
               
            ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
            ach_header = hexstr_to_ascii('10008902')
        
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                  
            mpls_label_stack = [{'label':13,'tc':0,'ttl':1,'s':1}]

            pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=dmac1,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)

            self.ctc_send_packet( 0, str(pkt))

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(0)
                    
            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID:
                    sys_logging("get rif oid = 0x%x" %a.value.oid)
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError()

                        
            attr_value = sai_thrift_attribute_value_t(oid=rif_id1)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)                        
                        
            attr_value = sai_thrift_attribute_value_t(oid=nhop2)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID:
                    sys_logging("get rif oid = 0x%x" %a.value.oid)
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()
            
                if a.id == SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if nhop2 != a.value.oid:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(0)                        

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)                                   
            self.client.sai_thrift_remove_next_hop(nhop1)  
            self.client.sai_thrift_remove_next_hop(nhop2)            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip2, dmac2)            
            self.client.sai_thrift_remove_router_interface(rif_id1)




class scenario_14_tp_lsp_ccm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
                
        ##### basic configuration ######
        
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        #### OAM configuration ####
        
        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_lsp_label
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, nhop_lsp_pe1_to_p, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        sys_logging("compose tp y1731 oam packet") 
        
        srcmac = '00:22:33:44:55:66'        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        ach_header = hexstr_to_ascii('10008902')
        
        mpls_inner_pkt = ach_header + str(ccm_hdr)
                                  
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                   
        
        warmboot(self.client)
        
        try:
        
            self.ctc_show_packet(0)

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()  
                        
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get mpls label = 0x%x" %a.value.u32)
                    if mpls_in_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            self.ctc_send_packet( 0, str(pkt))                                                                                   
            time.sleep(1)   
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()            
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)

            
            
            
class scenario_15_tp_pw_ccm_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
                
        ##### basic configuration ######

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
                
        nhp_pw2_label = 400
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 200)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        inseg_pw2_label = 300        
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        #### OAM configuration ####
        
        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = inseg_pw2_label
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, nhop_pw_pe1_to_pe2, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
        
        
        sys_logging("compose tp y1731 oam packet") 
        
        srcmac = '00:22:33:44:55:66'        
        ccm_hdr = simple_ccm_packet(mel=level,
                                   rdi=0,
                                   period=ccm_period,
                                   mepid=remote_mep_id1,
                                   megid=meg_name)
                                   
        ach_header = hexstr_to_ascii('10008902')
        
        mpls_inner_pkt = ach_header + str(ccm_hdr)
                                  
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':1,'s':1}]
        pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                                  
        warmboot(self.client)
        
        try:
        
            self.ctc_show_packet(0)

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                                    
            sys_logging("get meg info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get mpls label = 0x%x" %a.value.u32)
                    if mpls_in_label != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = %s" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_TTL:
                    sys_logging("get session ttl = 0x%x" %a.value.u8)
                    if 64 != a.value.u8:
                        raise NotImplementedError()                        

                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos = 0x%x" %a.value.u8)
                    if 0 != a.value.u8:
                        raise NotImplementedError()
                        
                        
            self.ctc_send_packet( 0, str(pkt))                                                                                   
            time.sleep(1)   
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            attr_value = sai_thrift_attribute_value_t(u8=100)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_TTL, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u8=7)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_SESSION_ATTR_EXP_OR_COS, value=attr_value)
            status = self.client.sai_thrift_set_y1731_session_attribute(mep_id, attr)
            sys_logging("set mep session attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get mep session info")
            attrs = self.client.sai_thrift_get_y1731_session_attribute(mep_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_SESSION_ATTR_TTL:
                    sys_logging("get session ttl = 0x%x" %a.value.u8)
                    if 100 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_Y1731_SESSION_ATTR_EXP_OR_COS:
                    sys_logging("get exp or cos = 0x%x" %a.value.u8)
                    if 7 != a.value.u8:
                        raise NotImplementedError()
                        
            self.ctc_show_packet(0)
            
        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)

                        
            
class scenario_16_defect_test_dloc(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 20
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===

            time.sleep(5)


            #=== event occur, event id: 4 ===            
            #=== event occur, event id: 8 ===

                        
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            
class scenario_16_defect_test_mismerge(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 20
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===


            meg_name1 = "ETHER_VLAN1"
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name1)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 0 ===            
            #=== event occur, event id: 7 ===

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)


class scenario_16_defect_test_unexpected_level(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 20
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===


            level1 = 3
            ccm_hdr = simple_ccm_packet(mel=level1,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:33',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 1 ===            
            #=== event occur, event id: 7 ===

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)



class scenario_16_defect_test_unexpected_mep(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===

            remote_mep_id2 = 12
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id2,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 2 ===            
            #=== event occur, event id: 7 ===

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)       


class scenario_16_defect_test_unexpected_period(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===

            ccm_period1 = 2
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period1,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 3 ===            

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)  


          
class scenario_16_defect_test_src_mac_mismatch(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===

            mac2 = '00:11:11:11:11:22'
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac2,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 5 ===            
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                         
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)  




                      
class scenario_16_defect_test_rx_rdi(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
        
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

        sys_logging("### Step3. Create OAM MEP ###")
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "ETHER_VLAN"
        level = 4
                
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id=vlan)       
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac1 = '00:11:11:11:11:11'
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)
               
        warmboot(self.client)
        
        try:
                                   
            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))
            
            sys_logging("get rmep info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
            #=== event occur, event id: 8 ===

            ccm_hdr = simple_ccm_packet(mel=level,
                                        rdi=1,
                                        period=ccm_period,
                                        mepid=remote_mep_id1,
                                        megid=meg_name)
                                        
            pkt = simple_eth_packet(pktlen=97,
                                    eth_dst='01:80:C2:00:00:34',
                                    eth_src=mac1,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=ccm_hdr)
                                    
            self.ctc_send_packet(0, str(pkt))

            #=== event occur, event id: 6 ===            
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
                         
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)  
            


class scenario_17_mip_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("### Step1. Create basic Environment ###")
        
        vlan = 10                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
                
        sys_logging("### Step2. Set Port Oam Enable ###")
       
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        
        for a in attrs.attr_list:
        
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (0 == a.value.booldata)

            if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###"  %a.value.u8)
                assert (0 == a.value.u8)

            if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###"  %a.value.mac)
                assert (default_port_mac == a.value.mac)
                
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)        

        attr_value = sai_thrift_attribute_value_t(u8=16)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_MIP_ENABLE, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr) 

        port_mac = '00:11:11:11:11:11'
        attr_value = sai_thrift_attribute_value_t(mac=port_mac)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr) 
        
        attrs = self.client.sai_thrift_get_port_attribute(port1)
        
        for a in attrs.attr_list:
        
            if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                assert (1 == a.value.booldata)

            if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###"  %a.value.u8)
                assert (16 == a.value.u8)

            if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###"  %a.value.mac)
                assert (port_mac == a.value.mac)
                

        sys_logging("### Step3. Create OAM MEP ###")
        
     
        level = 4
        ccm_period = 1 

               
        warmboot(self.client)
        
        try:
                       
            macda = port_mac
            macsa = '00:00:00:00:00:01'

            # step 1 level match
            
            lbm_hdr = simple_lbm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbm_hdr)

            lbr_hdr = simple_lbr_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt2 = simple_eth_packet(pktlen=97,
                                    eth_dst=macsa,
                                    eth_src=macda,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbr_hdr)
                                    
                                    
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt2, [0]) 

                        
            # step 2 level not match

            level = 3 
            lbm_hdr = simple_lbm_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt1 = simple_eth_packet(pktlen=97,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbm_hdr)

            lbr_hdr = simple_lbr_packet(mel=level,
                                        rdi=0,
                                        period=ccm_period)
                                        
            pkt2 = simple_eth_packet(pktlen=97,
                                    eth_dst=macsa,
                                    eth_src=macda,
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    eth_type=0x8902,
                                    inner_frame=lbr_hdr)
                                    
                                    
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1]) 
            
            
        finally:
        
            sys_logging("clear configuration")

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)  

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_MIP_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(mac=oam_port_tx_smac)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)                       

            attrs = self.client.sai_thrift_get_port_attribute(port1)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %d ###"  %a.value.booldata)
                    assert (0 == a.value.booldata)

                if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###"  %a.value.u8)
                    assert (0 == a.value.u8)

                if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                    sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###"  %a.value.mac)
                    assert (oam_port_tx_smac == a.value.mac)        
                    
