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

@group('y1731')

class func_01_MegCreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
                #if a.id == SAI_Y1731_MEG_ATTR_NAME:
                #    sys_logging("set meg_name = %s" %meg_name)
                #    sys_logging("get meg_name = %s" %a.value.chardata)
                #    if meg_name != a.value.chardata:
                #        raise NotImplementedError()
                if a.id == SAI_Y1731_MEG_ATTR_LEVEL:
                    sys_logging("set level = 0x%x" %level)
                    sys_logging("get level = 0x%x" %a.value.u8)
                    if level != a.value.u8:
                        raise NotImplementedError()
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
class func_02_EthMepCreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
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
                        
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
        
class func_03_EthRmepCreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
class func_04_EthOamDownMepRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
            
class func_05_EthOamUpMepRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
class func_06_TPOamLspTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
class func_07_TPOamPwTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
class func_08_VplsOamFidTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
            sai_thrift_remove_bridge_sub_port(self.client, uni_port_oid, port1)            
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
            
class func_09_VplsOamVlanTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
            sai_thrift_remove_bridge_sub_port(self.client, uni_port_oid, port1)            
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
            
            
class func_10_VpwsOamFidTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
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
                    #if 1 != a.value.booldata:
                    #    raise NotImplementedError()
                        
            
                        
            #self.ctc_show_packet(1)
            
        finally:
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            #sai_thrift_delete_fdb(self.client, bridge_id, mac_host_local, uni_port_oid)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac_host_remote, pw2_tunnel_bport_oid)
            
            sai_thrift_remove_bridge_sub_port(self.client, uni_port_oid, port1)            
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
            
            
class func_11_EthOamDownMepLMTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
            
class func_12_EthOamDownMepCpuTxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
class func_13_VplsOamFidCpuTxTest(sai_base_test.ThriftInterfaceDataPlane):
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
            
            sai_thrift_remove_bridge_sub_port(self.client, uni_port_oid, port1)            
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
            
class func_14_EthOamDownMepDualLMStatsTest(sai_base_test.ThriftInterfaceDataPlane):
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