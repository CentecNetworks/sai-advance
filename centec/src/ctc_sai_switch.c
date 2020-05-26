#include "ctc_sai_switch.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_app_cfg.h"
#include "ctc_init.h"
#include "ctc_sai_port.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_route.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_hostif.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_stp.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_wred.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_ld_hash.h"
#include "ctc_sai_udf.h"
#include "ctc_sai_mcast.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_warmboot.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_hostif.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_samplepacket.h"
#include "ctc_sai_tunnel.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_isolation_group.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_debug_counter.h"
#include "ctc_sai_nat.h"
#include "ctc_sai_bfd.h"
#include "ctc_sai_twamp.h"
#include "ctc_sai_npm.h"
#include "ctc_sai_y1731.h"
#include "ctc_sai_ptp.h"
#include "ctc_sai_es.h"
#include "ctc_sai_synce.h"

static sai_switch_profile_id_t   g_profile_id;

extern sai_service_method_table_t g_ctc_services;
extern int32 ctc_master_cli(int32 ctc_shell_mode);
extern int32 ctc_cli_read(int32 ctc_shell_mode);
#ifndef SAI_SHELL_COMPAT
extern int32 ctc_cli_start(int32 ctc_shell_mode);
#endif
extern void  ctc_vty_close();
extern int32 ctc_app_cli_init(void);
extern sai_status_t ctc_sai_neighbor_update_arp(uint8 lchip, const sai_fdb_entry_t* fdb_entry, uint8 is_remove, uint8 is_flush);
extern int32 _ctc_sai_hostif_packet_receive_from_sdk(ctc_pkt_rx_t* p_pkt_rx);
extern dal_op_t g_dal_op;

int32
ctc_sai_switch_fdb_aging_process(uint8 gchip, void* p_data)
{
    uint8 lchip = 0;
    uint32 i = 0;
    uint32 index = 0;
    uint32  event_count = 0;
    ctc_aging_fifo_info_t* p_fifo = (ctc_aging_fifo_info_t*)p_data;
    ctc_aging_info_entry_t* p_entry = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_fdb_event_notification_data_t* fdb_events = NULL;
    ctc_l2_addr_t l2_addr;
    void* data = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    ctc_app_index_get_lchip_id(gchip, &lchip);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    fdb_events = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_fdb_event_notification_data_t)*p_fifo->fifo_idx_num);
    if (NULL == fdb_events)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(fdb_events, 0, sizeof(sai_fdb_event_notification_data_t)*p_fifo->fifo_idx_num);

    CTC_SAI_DB_LOCK(lchip);

    /*Using Dma*/
    for (i = 0; i < p_fifo->fifo_idx_num; i++)
    {
        p_entry = &(p_fifo->aging_entry[i]);
        if (p_entry->aging_type == CTC_AGING_TYPE_MAC)
        {
            fdb_events[index].event_type = SAI_FDB_EVENT_AGED;
            sal_memcpy(&fdb_events[index].fdb_entry.mac_address, p_entry->mac, sizeof(sai_mac_t));
            fdb_events[index].fdb_entry.bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, p_entry->fid);
            data = ctc_sai_db_get_object_property(lchip, fdb_events[index].fdb_entry.bv_id);
            if (NULL == data)
            {
                fdb_events[index].fdb_entry.bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1D, 0, p_entry->fid);
            }
            fdb_events[index].fdb_entry.switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
            fdb_events[index].attr = NULL;
            fdb_events[index].attr_count = 0;
            event_count ++;
        }
        if (!CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN))
        {
            sal_memset(&l2_addr, 0, sizeof(l2_addr));
            l2_addr.fid = p_entry->fid;
            sal_memcpy(l2_addr.mac, p_entry->mac, sizeof(mac_addr_t));
            ctcs_l2_remove_fdb(lchip, &l2_addr);
        }
        ctc_sai_neighbor_update_arp(lchip, (const sai_fdb_entry_t*)(&(fdb_events[index].fdb_entry)), 1, 0);
    }

    if (p_switch_master->fdb_event_cb)
    {
        p_switch_master->fdb_event_cb(event_count, fdb_events);
    }

    CTC_SAI_DB_UNLOCK(lchip);

    mem_free(fdb_events);

    return CTC_E_NONE;
}

int32
ctc_sai_switch_fdb_learning_process(uint8 gchip, void* p_data)
{
    uint8 lchip = 0;
    uint32 index = 0;
    uint32  event_count = 0;
    sai_fdb_event_notification_data_t* fdb_events = NULL;
    sai_attribute_t* attr_listtmp = NULL;
    sai_attribute_t* attr_list = NULL;
    sai_object_id_t port_oid = SAI_NULL_OBJECT_ID;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_learning_cache_t* p_cache = (ctc_learning_cache_t*)p_data;
    ctc_l2_addr_t l2_addr;
    uint32 nhp_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);
    ctc_app_index_get_lchip_id(gchip, &lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset(&l2_addr, 0, sizeof(l2_addr));

    fdb_events = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_fdb_event_notification_data_t)*p_cache->entry_num);
    if (NULL == fdb_events)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    attr_list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_attribute_t)*FDB_NOTIF_ATTRIBS_NUM*p_cache->entry_num);
    if (NULL == attr_list)
    {
        mem_free(fdb_events);
        return SAI_STATUS_NO_MEMORY;
    }
    attr_listtmp = attr_list;

    CTC_SAI_DB_LOCK(lchip);

    for (index = 0; index < p_cache->entry_num; index++)
    {
        /* pizzabox */
        l2_addr.flag = 0;
        l2_addr.fid = p_cache->learning_entry[index].fid;

        /*Using learning fifo*/
        if (!p_cache->sync_mode)
        {
            l2_addr.mac[0] = (p_cache->learning_entry[index].mac_sa_32to47 & 0xff00) >> 8;
            l2_addr.mac[1] = (p_cache->learning_entry[index].mac_sa_32to47 & 0xff);
            l2_addr.mac[2] = (p_cache->learning_entry[index].mac_sa_0to31 & 0xff000000) >> 24;
            l2_addr.mac[3] = (p_cache->learning_entry[index].mac_sa_0to31 & 0xff0000) >> 16;
            l2_addr.mac[4] = (p_cache->learning_entry[index].mac_sa_0to31 & 0xff00) >> 8;
            l2_addr.mac[5] = (p_cache->learning_entry[index].mac_sa_0to31 & 0xff);
        }
        else
        {
            /*Using Dma*/
            l2_addr.mac[0] = p_cache->learning_entry[index].mac[0];
            l2_addr.mac[1] = p_cache->learning_entry[index].mac[1];
            l2_addr.mac[2] = p_cache->learning_entry[index].mac[2];
            l2_addr.mac[3] = p_cache->learning_entry[index].mac[3];
            l2_addr.mac[4] = p_cache->learning_entry[index].mac[4];
            l2_addr.mac[5] = p_cache->learning_entry[index].mac[5];
        }

        if (p_cache->learning_entry[index].is_logic_port)
        {
            port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_SUB_PORT, 0, p_cache->learning_entry[index].logic_port);
            if (NULL == ctc_sai_db_get_object_property(lchip, port_oid))
            {
                port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_TUNNEL, 0, p_cache->learning_entry[index].logic_port);
            }
            fdb_events[index].fdb_entry.bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1D, 0, l2_addr.fid);
            if (!CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN))
            {
                l2_addr.gport = p_cache->learning_entry[index].logic_port;
                ctcs_l2_get_nhid_by_logic_port(lchip, p_cache->learning_entry[index].logic_port, &nhp_id);
                ctcs_l2_add_fdb_with_nexthop(lchip, &l2_addr, nhp_id);
            }
        }
        else
        {
            port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, SAI_BRIDGE_PORT_TYPE_PORT, 0, p_cache->learning_entry[index].global_src_port);
            fdb_events[index].fdb_entry.bv_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, l2_addr.fid);
            if (!CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN))
            {
                l2_addr.gport = p_cache->learning_entry[index].global_src_port;
                ctcs_l2_add_fdb(lchip, &l2_addr);
            }
        }

        fdb_events[index].event_type = SAI_FDB_EVENT_LEARNED;
        sal_memcpy(&fdb_events[index].fdb_entry.mac_address, l2_addr.mac, sizeof(sai_mac_t));

        fdb_events[index].fdb_entry.switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        fdb_events[index].attr       = attr_listtmp;
        fdb_events[index].attr_count = FDB_NOTIF_ATTRIBS_NUM;

        attr_listtmp->id        = SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID;
        attr_listtmp->value.oid = port_oid;
        attr_listtmp++;

        attr_listtmp->id        = SAI_FDB_ENTRY_ATTR_TYPE;
        attr_listtmp->value.s32 = SAI_FDB_ENTRY_TYPE_DYNAMIC;
        attr_listtmp++;

        attr_listtmp->id        = SAI_FDB_ENTRY_ATTR_PACKET_ACTION;
        attr_listtmp->value.s32 = SAI_PACKET_ACTION_FORWARD;
        attr_listtmp++;
        event_count ++;
        ctc_sai_neighbor_update_arp(lchip, (const sai_fdb_entry_t*)(&(fdb_events[index].fdb_entry)), 0, 0);
    }

    if (p_switch_master->fdb_event_cb)
    {
        p_switch_master->fdb_event_cb(event_count, fdb_events);
    }

    CTC_SAI_DB_UNLOCK(lchip);

    mem_free(attr_list);
    mem_free(fdb_events);

    return 0;
}

void _ctc_sai_sdk_shell_thread(void* param)
{
    #ifndef SAI_SHELL_COMPAT
    ctc_cli_start(0);
    #endif
}

int32
ctc_sai_switch_port_link_isr(uint8 gchip, void* p_data)
{
    ctc_port_link_status_t* p_link = NULL;
    uint16 gport = 0;
    uint8 lchip = 0;
    bool is_link = FALSE;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_port_oper_status_notification_t port_state_event;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    ctc_app_index_get_lchip_id(gchip, &lchip);

    p_link = (ctc_port_link_status_t*)p_data;
    gport = p_link->gport;

    sal_memset(&port_state_event, 0, sizeof(sai_port_oper_status_notification_t));

    ctcs_port_get_mac_link_up(lchip, gport, &is_link);
    CTC_SAI_DB_LOCK(lchip);
    if (is_link)
    {
        CTC_SAI_LOG_NOTICE(SAI_API_SWITCH, "gport 0x%04X Link Up, Port is enabled! \n", gport);
        port_state_event.port_state = SAI_PORT_OPER_STATUS_UP;
        ctcs_port_set_port_en(lchip, gport, 1);
    }
    else
    {
        ctc_object_id_t ctc_bridge_port_id ={0};
        sai_object_id_t bridge_port_id;
        sai_attribute_t attr_list;
        sai_object_id_t        switch_id;
        CTC_SAI_LOG_NOTICE(SAI_API_SWITCH, "gport 0x%04X Link Down, Port is disabled, please do port enable when linkup again! \n", gport);
        port_state_event.port_state = SAI_PORT_OPER_STATUS_DOWN;
        ctcs_port_set_port_en(lchip, gport, 0);
        /*flush fdb by port*/
        switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        ctc_bridge_port_id.lchip = lchip;
        ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
        ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
        ctc_bridge_port_id.value = gport;
        ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, &bridge_port_id);
        attr_list.id = SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID;
        attr_list.value.oid = bridge_port_id;
        ctc_sai_fdb_flush_fdb(switch_id, 1, &attr_list);
    }

    port_state_event.port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, gport);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_switch_master->lport_link_status[CTC_MAP_GPORT_TO_LPORT(gport)] = is_link;
    if (p_switch_master->port_state_change_cb)
    {
        p_switch_master->port_state_change_cb(1, &port_state_event);
    }
    CTC_SAI_DB_UNLOCK(lchip);

    return CTC_E_NONE;
}

int32
ctc_sai_switch_oam_event_process(uint8 gchip, void* p_data)
{
    uint8 lchip = 0;
    uint32 bfd_event_count = 0, y1731_event_count = 0;
    uint16 mep_num = 0;
    ctc_oam_event_t* p_event = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_bfd_session_state_notification_t* bfd_events = NULL;
    sai_y1731_session_event_notification_t* y1731_events = NULL;
    ctc_oam_event_entry_t* mep_info = NULL;
    uint32 mep_defect_bitmap_temp   = 0;
    sai_object_id_t bfd_session_id = 0, y1731_oid = 0;
    sai_bfd_session_state_t session_state;
    int32 y1731_event_list[5] = {0};
    uint32 bitmap_num = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    ctc_app_index_get_lchip_id(gchip, &lchip);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_event = (ctc_oam_event_t*)p_data;

    /*bfd events */
    bfd_events = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_bfd_session_state_notification_t)*p_event->valid_entry_num);
    if (NULL == bfd_events)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(bfd_events, 0, sizeof(sai_bfd_session_state_notification_t)*p_event->valid_entry_num);

    /*y1731 events */
    y1731_events = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_y1731_session_event_notification_t)*p_event->valid_entry_num);
    if (NULL == y1731_events)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(y1731_events, 0, sizeof(sai_y1731_session_event_notification_t)*p_event->valid_entry_num);


    for (mep_num = 0; mep_num < p_event->valid_entry_num; mep_num++)
    {
        mep_info = &p_event->oam_event_entry[mep_num];

        if(!p_event->oam_event_entry[mep_num].is_remote)
        {
            mep_defect_bitmap_temp = ((mep_info->event_bmp & CTC_OAM_DEFECT_UNEXPECTED_LEVEL)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_MISMERGE)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_UNEXPECTED_MEP)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_RDI_TX)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_DOWN)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_INIT)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_UP)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_MIS_CONNECT)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_CSF)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_SF));
        }
        else
        {
            mep_defect_bitmap_temp = ((mep_info->event_bmp & CTC_OAM_DEFECT_DLOC)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_RX_FIRST_PKT)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_UNEXPECTED_PERIOD)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_MAC_STATUS_CHANGE)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_SRC_MAC_MISMATCH)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_RDI_RX)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_CSF)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_DOWN)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_INIT)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_UP)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_EVENT_BFD_MIS_CONNECT)
                                      | (mep_info->event_bmp & CTC_OAM_DEFECT_SF));
        }


        //for bfd
        if((p_event->oam_event_entry[mep_num].mep_type >= CTC_OAM_MEP_TYPE_IP_BFD) &&
            (p_event->oam_event_entry[mep_num].mep_type <= CTC_OAM_MEP_TYPE_MICRO_BFD))
        {
            //local mep
            if(!p_event->oam_event_entry[mep_num].is_remote) {

                ctc_sai_bfd_traverse_get_session_by_mepindex(lchip, p_event->oam_event_entry[mep_num].lmep_index, 0, &bfd_session_id);
            }
            else  //remote mep
            {
                ctc_sai_bfd_traverse_get_session_by_mepindex(lchip, p_event->oam_event_entry[mep_num].rmep_index, 1, &bfd_session_id);
            }

            if( SAI_NULL_OBJECT_ID == bfd_session_id)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "bfd event bfd sessin id is NULL!!");
                goto out;
            }

            if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_BFD_DOWN))
            {
                session_state = SAI_BFD_SESSION_STATE_DOWN;
            }
            else if(CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_BFD_INIT))
            {
                session_state = SAI_BFD_SESSION_STATE_INIT;
            }
            else if(CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_BFD_UP))
            {
                session_state = SAI_BFD_SESSION_STATE_UP;
            }
            else
            {
                continue;
            }

            bfd_events[bfd_event_count].bfd_session_id = bfd_session_id;
            bfd_events[bfd_event_count].session_state = session_state;

            CTC_SAI_LOG_INFO(SAI_API_SWITCH, "bfd event bfd_session_id %d, state: %d!\n", bfd_session_id, session_state);

            bfd_event_count++;
        }
        else if((p_event->oam_event_entry[mep_num].mep_type >= CTC_OAM_MEP_TYPE_ETH_Y1731) && 
            (p_event->oam_event_entry[mep_num].mep_type <= CTC_OAM_MEP_TYPE_MPLS_TP_Y1731))
        {
            //local mep
            if(!p_event->oam_event_entry[mep_num].is_remote) {
                
                ctc_sai_y1731_traverse_get_oid_by_mepindex(lchip, p_event->oam_event_entry[mep_num].lmep_index, 0, &y1731_oid);                                
            }            
            else  //remote mep
            {
                ctc_sai_y1731_traverse_get_oid_by_mepindex(lchip, p_event->oam_event_entry[mep_num].rmep_index, 1, &y1731_oid);
            }
                
            if( SAI_NULL_OBJECT_ID == y1731_oid)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "y1731 event oid is NULL!!");
                goto out;
            }

            //local mep
            if(!p_event->oam_event_entry[mep_num].is_remote) 
            {
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_UNEXPECTED_LEVEL))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_LEVEL;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_MISMERGE))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_MISMERGE;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_UNEXPECTED_MEP))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_MEP;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_RDI_TX))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_TX;
                    bitmap_num++;
                }
            }
            else  //remote mep
            {
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_DLOC))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_DLOC;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_UNEXPECTED_PERIOD))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_PERIOD;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_SRC_MAC_MISMATCH))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_SRC_MAC_MISMATCH;
                    bitmap_num++;
                }
                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_RDI_RX))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_RX;
                    bitmap_num++;
                }

                if (CTC_FLAG_ISSET(mep_defect_bitmap_temp, CTC_OAM_DEFECT_EVENT_RX_FIRST_PKT))
                {
                    y1731_event_list[bitmap_num] = SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_CONNECTION_ESTABLISHED;
                    bitmap_num++;
                }
            }

            y1731_events[y1731_event_count].y1731_oid = y1731_oid;
            y1731_events[y1731_event_count].session_event_list.count = bitmap_num;
            y1731_events[y1731_event_count].session_event_list.list = y1731_event_list;

            CTC_SAI_LOG_INFO(SAI_API_SWITCH, "y1731 event y1731_oid %d, event bitmap: %d!\n", y1731_oid, mep_defect_bitmap_temp);
            
            y1731_event_count++;
        }
    }


    if ((p_switch_master->bfd_event_cb) && bfd_event_count)
    {
        p_switch_master->bfd_event_cb(bfd_event_count, bfd_events);
    }

    if ((p_switch_master->y1731_event_cb) && y1731_event_count)
    {
        p_switch_master->y1731_event_cb(y1731_event_count, y1731_events);
    }

out:
    mem_free(bfd_events);
    mem_free(y1731_events);

    return CTC_E_NONE;
}

sai_status_t
ctc_sai_switch_get_global_panel_ports(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 gchip = 0;
    uint32 num = 0;
    ctc_global_panel_ports_t local_panel_ports;
    sai_object_id_t ports[CTC_MAX_PHY_PORT];

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
    sal_memset(ports, 0, sizeof(ports));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS:
            attr->value.u32 = local_panel_ports.count;
            break;
        case SAI_SWITCH_ATTR_PORT_LIST:
            for (num = 0; num < local_panel_ports.count; num ++)
            {
                ports[num] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]));
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t),ports,local_panel_ports.count, &attr->value.objlist));
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_switch_get_global_capability(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);
    
    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_MAX_PORT_NUM];
            break;
        case SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_MAX_VRFID];
            break;
        case SAI_SWITCH_ATTR_FDB_TABLE_SIZE:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_MAC_ENTRY_NUM];
            break;
        case SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_HOST_ROUTE_ENTRY_NUM];
            break;
        case SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_LPM_ROUTE_ENTRY_NUM];
            break;
        case SAI_SWITCH_ATTR_LAG_MEMBERS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_LINKAGG_MEMBER_NUM];
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_LAGS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_LINKAGG_GROUP_NUM];
            break;
        case SAI_SWITCH_ATTR_ECMP_MEMBERS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_ECMP_MEMBER_NUM];
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_ECMP_GROUP_NUM];
            break;
        case SAI_SWITCH_ATTR_MAX_BFD_SESSION:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_OAM_SESSION_NUM];
            break;
        case SAI_SWITCH_ATTR_MAX_Y1731_SESSION:
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_OAM_SESSION_NUM];
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_switch_get_global_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint8 gchip = 0;
    uint32 value = 0;
    mac_addr_t mac;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);
    
    chip_type = ctcs_get_chip_type(lchip);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_PORT_MAX_MTU:
            attr->value.u32 = CTC_MAX_MTU_SIZE;
            break;
        case SAI_SWITCH_ATTR_CPU_PORT:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip), attr_idx);
            if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN))
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_CPU, 0, p_switch_master->cpu_eth_port);
            }
            else
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_CPU, 0, CTC_GPORT_RCPU(gchip));
            }
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES:
            attr->value.u32 = 8;
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES:
            if (p_switch_master->port_queues == CTC_QOS_PORT_QUEUE_NUM_8)
            {
                attr->value.u32 = 8;
            }
            else
            {
                attr->value.u32 = 4;
            }
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_QUEUES:
            attr->value.u32 = p_switch_master->port_queues;
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES:
            attr->value.u32 = CTC_SAI_SWITCH_ATTR_NUMBER_OF_QUEUES;
            break;
        case SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES:
            attr->value.u32 = CTC_SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUE;
            break;
        case SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED:
            attr->value.booldata = true;
            break;
        case SAI_SWITCH_ATTR_OPER_STATUS:
            attr->value.s32 = SAI_SWITCH_OPER_STATUS_UP;
            break;
        case SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
            attr->value.s32 = p_switch_master->fdb_miss_action[0];
            break;
        case SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
            if(CTC_CHIP_GOLDENGATE == chip_type)
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            }
            attr->value.s32 = p_switch_master->fdb_miss_action[2];
            break;
        case SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
            attr->value.s32 = p_switch_master->fdb_miss_action[1];
            break;
        /*meta data range*/
        case SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;
            attr->value.u32range.max = CTC_SAI_META_DATA_FDB_DST_MAX;
            break;
        case SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;           
            attr->value.u32range.max = CTC_SAI_META_DATA_ROUTE_DST_MAX;
            break;
        case SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;              
            attr->value.u32range.max = CTC_SAI_META_DATA_NEIGHBOR_DST_MAX;
            break;
        case SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;               
            attr->value.u32range.max = CTC_SAI_META_DATA_PORT_MAX;
            break;
        case SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;             
            attr->value.u32range.max = CTC_SAI_META_DATA_VLAN_MAX;
            break;
        case SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE:
            attr->value.u32range.min = 0;             
            attr->value.u32range.max = CTC_SAI_META_DATA_ACL_MAX;
            break;

        /*default vlan/stp instance/vrf/1Qbridge*/
        case SAI_SWITCH_ATTR_DEFAULT_VLAN_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, 1);
            break;
        case SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, lchip, 0, 0, 0);
            break;
        case SAI_SWITCH_ATTR_MAX_STP_INSTANCE:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_global_ctl_get(lchip,CTC_GLOBAL_CHIP_CAPABILITY,capability), attr_idx);
            attr->value.u32 = capability[CTC_GLOBAL_CAPABILITY_STP_INSTANCE_NUM];
            break;
        case SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, 0);
            break;
        case SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE, lchip, SAI_BRIDGE_TYPE_1Q, 0, p_switch_master->default_bridge_id);
            break;
        case SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE:
            if(CTC_CHIP_GOLDENGATE == chip_type)
            {
                attr->value.u64 = 9000;
            }
            else if (CTC_CHIP_DUET2 == chip_type)
            {
                attr->value.u64 = 4300;
            }
            else if (CTC_CHIP_TSINGMA == chip_type)
            {
                /*TODO, check share buffer type */
                attr->value.u64 = 9000;
            }
            break;
        case SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP:
            attr->value.oid = p_switch_master->default_trap_grp_id;
            break;
        case SAI_SWITCH_ATTR_RESTART_WARM:
            attr->value.booldata = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_WARMBOOT_EN)? true : false;
            break;
        case SAI_SWITCH_ATTR_CRC_CHECK_ENABLE:
            attr->value.booldata = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_CHECK_EN)? true : false;
            break;
        case SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE:
            attr->value.booldata = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_OVERWRITE_EN)? true : false;
            break;        
        case SAI_SWITCH_ATTR_RESTART_TYPE:
            attr->value.s32 = SAI_SWITCH_RESTART_TYPE_PLANNED;
            break;
        case SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL:
            attr->value.u32 = CTC_SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL;
            break;
        case SAI_SWITCH_ATTR_NV_STORAGE_SIZE:
            attr->value.u64 = CTC_SAI_SWITCH_ATTR_NV_STORAGE_SIZE;
            break;
        case SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY:
            attr->value.s32 = SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG_AND_SG;
            break;
        case SAI_SWITCH_ATTR_SWITCHING_MODE:
            if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CUT_THROUGH_EN))
            {
                attr->value.s32 = SAI_SWITCH_SWITCHING_MODE_CUT_THROUGH;
            }
            else
            {
                attr->value.s32 = SAI_SWITCH_SWITCHING_MODE_STORE_AND_FORWARD;
            }
            break;
        case SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE:
        case SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE:
            attr->value.booldata = false;
            break;
        case SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
            sal_memset(mac, 0, sizeof(mac_addr_t));
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_l3if_get_router_mac(lchip, mac), attr_idx);
            sal_memcpy(attr->value.mac,mac,sizeof(sai_mac_t));
            break;
        case SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES:
            {
                ctc_security_learn_limit_t  limit;

                sal_memset(&limit,0,sizeof(limit));

                limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_SYSTEM;
                
                CTC_SAI_ATTR_ERROR_RETURN(ctcs_mac_security_get_learn_limit(lchip, &limit), attr_idx);

                if (0xFFFFFFFF == limit.limit_num)
                {
                    attr->value.u32 = 0;
                }
                else
                {
                    attr->value.u32 = limit.limit_num;
                }
            }
            break;
        case SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
            {
                ctc_npm_global_cfg_t  npm_glb_config;

                sal_memset(&npm_glb_config, 0, sizeof(ctc_npm_global_cfg_t));
                CTC_SAI_ATTR_ERROR_RETURN(ctcs_npm_get_global_config(lchip, &npm_glb_config), attr_idx);
                if (CTC_NPM_SESSION_MODE_8 == npm_glb_config.session_mode)
                {
                    attr->value.u32 = 8;
                }
                if (CTC_NPM_SESSION_MODE_6 == npm_glb_config.session_mode)
                {
                    attr->value.u32 = 6;
                }
                if (CTC_NPM_SESSION_MODE_4 == npm_glb_config.session_mode)
                {
                    attr->value.u32 = 4;
                }
            }
            break;
        case SAI_SWITCH_ATTR_FDB_AGING_TIME:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_aging_get_property(lchip, CTC_AGING_TBL_MAC,CTC_AGING_PROP_AGING_SCAN_EN, &value), attr_idx);
            if (value)
            {
                CTC_SAI_ATTR_ERROR_RETURN(ctcs_aging_get_property(lchip, CTC_AGING_TBL_MAC,CTC_AGING_PROP_INTERVAL,&value), attr_idx);
                attr->value.u32 = value;
            }
            else
            {
                attr->value.u32 = 0;
            }
            break;
        case SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL:
            attr->value.u32 = CTC_SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL;
            break;
        case SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE:
            attr->value.booldata = (g_ctc_sai_master.p_shell_thread)?TRUE:FALSE;
            break;
        case SAI_SWITCH_ATTR_SWITCH_PROFILE_ID:
            attr->value.u32 = g_profile_id;
            break;
        case SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO:
            if ((0 == p_switch_master->pci_dev.busNo) && (0 == p_switch_master->pci_dev.devNo)
                && (0 == p_switch_master->pci_dev.funNo))
            {
                attr->value.s8list.count = 0;
            }
            else
            {
                int8 pci_no[4]={0};
                pci_no[0] = lchip;
                pci_no[1] = p_switch_master->pci_dev.busNo;
                pci_no[2] = p_switch_master->pci_dev.devNo;
                pci_no[3] = p_switch_master->pci_dev.funNo;
                CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(int8), pci_no, 4, &attr->value.s8list));
            }
            break;
        case SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
        case SAI_SWITCH_ATTR_INIT_SWITCH:
            attr->value.booldata = TRUE;
            break;
        case SAI_SWITCH_ATTR_FAST_API_ENABLE:
            attr->value.booldata = FALSE;
            break;
        case SAI_SWITCH_ATTR_MIRROR_TC:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_SEGMENTROUTE_MAX_SID_DEPTH:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_SEGMENTROUTE_TLV_TYPE:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_TPID_OUTER_VLAN:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_parser_get_tpid(lchip, CTC_PARSER_L2_TPID_SVLAN_TPID_0, &attr->value.u16), attr_idx);
            break;
        case SAI_SWITCH_ATTR_TPID_INNER_VLAN:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_parser_get_tpid(lchip, CTC_PARSER_L2_TPID_CVLAN_TPID, &attr->value.u16), attr_idx);
            break;
        case SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL:
            attr->value.booldata = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL)?1:0;
            break;
        case SAI_SWITCH_ATTR_PRE_SHUTDOWN:
            attr->value.booldata = CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_PRE_SHUTDOWN)?1:0;
            break;
        case SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS:
            attr->value.u8 = 1;
            break;
        case SAI_SWITCH_ATTR_TEMP_LIST:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_get_chip_sensor(lchip, CTC_CHIP_SENSOR_TEMP, &value), attr_idx);
            CTC_SAI_ATTR_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(int32), &value, 1, &attr->value.s32list), attr_idx);
            break;
        case SAI_SWITCH_ATTR_AVERAGE_TEMP:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_get_chip_sensor(lchip, CTC_CHIP_SENSOR_TEMP, &value), attr_idx);
            attr->value.s32 = value;
            break;
        case SAI_SWITCH_ATTR_MAX_TEMP:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_get_chip_sensor(lchip, CTC_CHIP_SENSOR_TEMP, &value), attr_idx);
            attr->value.s32 = value;
            break;            
        case SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT:
            CTC_SAI_ATTR_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_VXLAN_UDP_DEST_PORT, &value), attr_idx);
            attr->value.u16 = (uint16)value;
            break;
        case SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC:
            sal_memcpy(attr->value.mac, p_switch_master->vxlan_default_router_mac, sizeof(sai_mac_t));
            break;
        case SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE:
            attr->value.s32list.count = 1;
            attr->value.s32list.list[0] = SAI_BFD_SESSION_OFFLOAD_TYPE_FULL;
            break;
        case SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE:
            attr->value.s32list.count = 1;
            attr->value.s32list.list[0] = SAI_BFD_SESSION_OFFLOAD_TYPE_FULL;
            break;
        case SAI_SWITCH_ATTR_MIN_BFD_RX:
            attr->value.u32 = SAI_SUPPORTED_MIN_BFD_RX_INTERVAL;
            break;
        case SAI_SWITCH_ATTR_MIN_BFD_TX:
            attr->value.u32 = SAI_SUPPORTED_MIN_BFD_TX_INTERVAL;
            break;
        case SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE:
            attr->value.s32list.count = 1;
            attr->value.s32list.list[0] = SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_PARTIAL;
            break;
        case SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE:
            attr->value.s32list.count = 2;
            attr->value.s32list.list[0] = SAI_STATS_MODE_READ;            
            attr->value.s32list.list[1] = SAI_STATS_MODE_READ_AND_CLEAR;            
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status =  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;;
}

sai_status_t
ctc_sai_switch_set_global_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint32 value = 0;
    mac_addr_t mac;
    sai_object_id_t vr_obj_id = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 gchip = 0;
    uint32 gport = 0;
    uint32 num = 0;
    ctc_global_panel_ports_t local_panel_ports ;
    
    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);
    
    chip_type = ctcs_get_chip_type(lchip);

    ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);
    ctcs_get_gchip_id(lchip, &gchip);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_SWITCHING_MODE:
            /* cut through and store forward only support in create switch*/
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE:
        case SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
            sal_memset(mac, 0, sizeof(mac_addr_t));
            sal_memcpy(mac,attr->value.mac,sizeof(sai_mac_t));
            CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_router_mac(lchip, mac));
            vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, 0);
            p_vr_info = ctc_sai_db_get_object_property(lchip, vr_obj_id);
            sal_memcpy(p_vr_info->src_mac, attr->value.mac, sizeof(sai_mac_t));
            break;
        case SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES:
            {
                ctc_security_learn_limit_t  limit;

                limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_SYSTEM;
                
                if (attr->value.u32 == 0)
                {
                    limit.limit_num = 0xFFFFFFFF;
                }
                else
                {
                    limit.limit_num = attr->value.u32;  
                } 
                
                limit.limit_action = CTC_MACLIMIT_ACTION_FWD;

                CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &limit));
            }
            break;
        case SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
            {
                ctc_npm_global_cfg_t  npm_glb_config;

                sal_memset(&npm_glb_config, 0, sizeof(ctc_npm_global_cfg_t));
                
                if (4 == attr->value.u32)
                {
                    npm_glb_config.session_mode = CTC_NPM_SESSION_MODE_4;
                }
                else if (6 == attr->value.u32)
                {
                    npm_glb_config.session_mode = CTC_NPM_SESSION_MODE_6;
                }
                else if (8 == attr->value.u32)
                {
                    npm_glb_config.session_mode = CTC_NPM_SESSION_MODE_8;
                }

                CTC_SAI_CTC_ERROR_RETURN(ctcs_npm_set_global_config(lchip, &npm_glb_config));
            }
            break;
        case SAI_SWITCH_ATTR_FDB_AGING_TIME:
            value = attr->value.u32;
            if (0 == value)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_aging_set_property(lchip, CTC_AGING_TBL_MAC,CTC_AGING_PROP_AGING_SCAN_EN, FALSE));
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_aging_set_property(lchip, CTC_AGING_TBL_MAC,CTC_AGING_PROP_INTERVAL, value));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_aging_set_property(lchip, CTC_AGING_TBL_MAC,CTC_AGING_PROP_AGING_SCAN_EN, TRUE));
            }
            break;
        case SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
            p_switch_master->fdb_miss_action[0] = attr->value.s32;
            ctc_sai_vlan_traverse_set_unkown_pkt_action(lchip, (void*)p_switch_master, 0);
            break;
        case SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
            p_switch_master->fdb_miss_action[1] = attr->value.s32;
            ctc_sai_vlan_traverse_set_unkown_pkt_action(lchip, (void*)p_switch_master, 1);
            break;
        case SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
            if (chip_type == CTC_CHIP_GOLDENGATE)
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            p_switch_master->fdb_miss_action[2] = attr->value.s32;
            ctc_sai_vlan_traverse_set_unkown_pkt_action(lchip, (void*)p_switch_master, 2);
            break;
        case SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE:
            if (attr->value.booldata)
            {
                if (NULL == g_ctc_sai_master.p_shell_thread)
                {
                    ctc_cli_read(0);
                    CTC_SAI_CTC_ERROR_RETURN(sal_task_create(&(g_ctc_sai_master.p_shell_thread), "sdk_shell",
                          SAL_DEF_TASK_STACK_SIZE, SAL_TASK_PRIO_DEF, _ctc_sai_sdk_shell_thread, (void*)NULL));
               }
            }
            else
            {
                sal_task_destroy(g_ctc_sai_master.p_shell_thread);
                g_ctc_sai_master.p_shell_thread = NULL;
            }
            break;
        case SAI_SWITCH_ATTR_FAST_API_ENABLE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_SWITCH_ATTR_MIRROR_TC:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_SWITCH_ATTR_TPID_OUTER_VLAN:
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_tpid(lchip, CTC_PARSER_L2_TPID_SVLAN_TPID_0, attr->value.u16));
            break;
        case SAI_SWITCH_ATTR_TPID_INNER_VLAN:
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_tpid(lchip, CTC_PARSER_L2_TPID_CVLAN_TPID, attr->value.u16));
            break;
        case SAI_SWITCH_ATTR_CRC_CHECK_ENABLE:
            for (num = 0; num < local_panel_ports.count; num++)
            {
                gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_CHK_CRC_EN, attr->value.booldata));
            }
            if (attr->value.booldata)
            {
                CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_CHECK_EN);
            }
            else
            {
                CTC_UNSET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_CHECK_EN);
            }            
            break;
        case SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE:
            for (num = 0; num < local_panel_ports.count; num++)
            {
                gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_STRIP_CRC_EN, attr->value.booldata));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_APPEND_CRC_EN, attr->value.booldata));                
            }
            if (attr->value.booldata)
            {
                CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_OVERWRITE_EN);
            }
            else
            {
                CTC_UNSET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CRC_OVERWRITE_EN);
            }               
            break;
        case SAI_SWITCH_ATTR_RESTART_WARM:
            if (attr->value.booldata)
            {
                CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_WARMBOOT_EN);
            }
            else
            {
                CTC_UNSET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_WARMBOOT_EN);
            }
            break;
        case SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL:
            if (attr->value.booldata)
            {
                CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL);
            }
            else
            {
                CTC_UNSET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL);
            }
            break;
        case SAI_SWITCH_ATTR_PRE_SHUTDOWN:
            if (attr->value.booldata)
            {
                CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_PRE_SHUTDOWN);
            }
            else
            {
                CTC_UNSET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_PRE_SHUTDOWN);
            }
            break;
        case SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT:
            value = (uint32)attr->value.u16;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_VXLAN_UDP_DEST_PORT, &value));
            break;
        case SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC:
            sal_memset(mac, 0, sizeof(mac_addr_t));
            sal_memcpy(p_switch_master->vxlan_default_router_mac,attr->value.mac,sizeof(sai_mac_t));
            // TBD update for related nexthop 
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_switch_get_hash_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_parser_global_cfg_t cfg;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);

    sal_memset(&cfg,0,sizeof(ctc_parser_global_cfg_t));
    
    CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_get_global_cfg(lchip, &cfg));

    switch(attr->id)
    {
        /*read-only*/
        case SAI_SWITCH_ATTR_ECMP_HASH: /* sub type: 0 */
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, CTC_SAI_HASH_USAGE_ECMP,0,0);
            break;
        case SAI_SWITCH_ATTR_LAG_HASH:  /* sub type: 1 */
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, CTC_SAI_HASH_USAGE_LINKAGG,0,0);
            break;
        /*ecmp*/
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM:
            if(CTC_PARSER_GEN_HASH_TYPE_XOR == cfg.ecmp_hash_type)
            {
                attr->value.s32 = SAI_HASH_ALGORITHM_XOR;
            }
            else if(CTC_PARSER_GEN_HASH_TYPE_CRC == cfg.ecmp_hash_type)
            {
                attr->value.s32 = SAI_HASH_ALGORITHM_CRC;
            }
            else
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            }
            break;
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED:
            attr->value.u32 = 0xFFFF;
            break;
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH:
            attr->value.booldata = cfg.symmetric_hash_en?true:false;
            break;
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV4:
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4:
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV6:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
        /*linkagg*/
        case SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM:
            if(CTC_PARSER_GEN_HASH_TYPE_XOR == cfg.linkagg_hash_type)
            {
                attr->value.s32 = SAI_HASH_ALGORITHM_XOR;
            }
            else if(CTC_PARSER_GEN_HASH_TYPE_CRC == cfg.linkagg_hash_type)
            {
                attr->value.s32 = SAI_HASH_ALGORITHM_CRC;
            }
            else
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            }
            break;
        case SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED:
            attr->value.u32 = 0xFFFF;
            break;
        case SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH:
            attr->value.booldata = cfg.symmetric_hash_en?true:false;
            break;
        case SAI_SWITCH_ATTR_LAG_HASH_IPV4:
        case SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4:
        case SAI_SWITCH_ATTR_LAG_HASH_IPV6:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
ctc_sai_switch_set_hash_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_parser_global_cfg_t cfg;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);

    sal_memset(&cfg,0,sizeof(ctc_parser_global_cfg_t));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_get_global_cfg(lchip, &cfg));

    switch(attr->id)
    {
        /*ecmp*/
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM:
            if(SAI_HASH_ALGORITHM_XOR == attr->value.s32)
            {
                cfg.ecmp_hash_type = CTC_PARSER_GEN_HASH_TYPE_XOR;
            }
            else if(SAI_HASH_ALGORITHM_CRC == attr->value.s32)
            {
                cfg.ecmp_hash_type = CTC_PARSER_GEN_HASH_TYPE_CRC;
            }
            else
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &cfg));
            break;
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED:
#if 0 /* deleted by taocy for SONIC. syncd will shutdown switch if sai return error. 20191227*/
            /*sdk only support fix 0xFFFF*/
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
#endif
            // TODO:  taocy, set hash seed to sdk
            break;
        case SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH:
            cfg.symmetric_hash_en = attr->value.booldata?1:0;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &cfg));
            break;
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV4:
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4:
        case SAI_SWITCH_ATTR_ECMP_HASH_IPV6:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        /*linkagg*/
        case SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM:
            if(SAI_HASH_ALGORITHM_XOR == attr->value.s32)
            {
                cfg.linkagg_hash_type = CTC_PARSER_GEN_HASH_TYPE_XOR;
            }
            else if(SAI_HASH_ALGORITHM_CRC == attr->value.s32)
            {
                cfg.linkagg_hash_type = CTC_PARSER_GEN_HASH_TYPE_CRC;
            }
            else
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &cfg));
            break;
        case SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED:
#if 0 /* deleted by taocy for SONIC. syncd will shutdown switch if sai return error. 20191227*/
            /*sdk only support fix 0xFFFF*/
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
#endif
            // TODO:  taocy, set hash seed to sdk
            break;
        case SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH:
            cfg.symmetric_hash_en = attr->value.booldata?1:0;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &cfg));
            break;
        case SAI_SWITCH_ATTR_LAG_HASH_IPV4:
        case SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4:
        case SAI_SWITCH_ATTR_LAG_HASH_IPV6:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_switch_get_qos_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint32 value = 0;
    ctc_sai_switch_master_t* p_switch = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);

    p_switch = ctc_sai_get_switch_property(lchip);
    
    if (NULL == p_switch)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        /*qos read-only*/
        case SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES:
        case SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS:
        case SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL:
        case SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;

        case SAI_SWITCH_ATTR_QOS_DEFAULT_TC:
            attr->value.u8 = p_switch->default_tc;
            break;
        case SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
            value = p_switch->qos_domain_dot1p[0].tc.dot1p_to_tc_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
            value = p_switch->qos_domain_dot1p[0].color.dot1p_to_color_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
            value = p_switch->qos_domain_dscp[0].tc.dscp_to_tc_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
            value = p_switch->qos_domain_dscp[0].color.dscp_to_color_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP:
            value = p_switch->tc_to_queue_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
            value = p_switch->qos_domain_dot1p[0].tc_color.tc_color_to_dot1p_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
            value = p_switch->qos_domain_dscp[0].tc_color.tc_color_to_dscp_map_id;
            if (value)
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, value);
            }
            else
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY:
        case SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION:
        case SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE:
        case SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL:
        case SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE:
        case SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_switch_set_qos_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 value = 0;
    ctc_sai_switch_master_t* p_switch = NULL;
    bool enable = FALSE;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, attr->value.oid, &ctc_object_id);

    p_switch = ctc_sai_get_switch_property(lchip);
    
    if (NULL == p_switch)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_QOS_DEFAULT_TC:
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_default_tc(lchip, attr->value.u8));
            p_switch->default_tc = attr->value.u8;
            break;
        case SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dot1p[0].tc.dot1p_to_tc_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dot1p[0].tc.dot1p_to_tc_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dot1p[0].tc.dot1p_to_tc_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[DOT1P_TO_TC_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dot1p[0].tc.dot1p_to_tc_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, enable));
            break;
        case SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dot1p[0].color.dot1p_to_color_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dot1p[0].color.dot1p_to_color_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dot1p[0].color.dot1p_to_color_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[DOT1P_TO_COLOR_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dot1p[0].color.dot1p_to_color_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, enable));
            break;
        case SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dscp[0].tc.dscp_to_tc_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dscp[0].tc.dscp_to_tc_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dscp[0].tc.dscp_to_tc_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[DSCP_TO_TC_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dscp[0].tc.dscp_to_tc_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_DSCP_TO_TC, enable));
            break;
        case SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dscp[0].color.dscp_to_color_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dscp[0].color.dscp_to_color_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dscp[0].color.dscp_to_color_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[DSCP_TO_COLOR_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dscp[0].color.dscp_to_color_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, enable));
            break;
        case SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->tc_to_queue_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_TC_TO_QUEUE, enable));
            p_switch->tc_to_queue_map_id = enable ? value : 0;
            break;
        case SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dot1p[0].tc_color.tc_color_to_dot1p_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dot1p[0].tc_color.tc_color_to_dot1p_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dot1p[0].tc_color.tc_color_to_dot1p_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[TC_AND_COLOR_TO_DOT1P_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dot1p[0].tc_color.tc_color_to_dot1p_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, enable));
            break;
        case SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                value = p_switch->qos_domain_dscp[0].tc_color.tc_color_to_dscp_map_id;
            }
            else
            {
                enable = TRUE;
                value = ctc_object_id.value;
                if (ctc_object_id.value == p_switch->qos_domain_dscp[0].tc_color.tc_color_to_dscp_map_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
                else if (p_switch->qos_domain_dscp[0].tc_color.tc_color_to_dscp_map_id)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_SWITCH,"[TC_AND_COLOR_TO_DSCP_MAP] Already exsit! map_id:%d",
                                        p_switch->qos_domain_dscp[0].tc_color.tc_color_to_dscp_map_id);
                    return SAI_STATUS_FAILURE;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, value, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, enable));
            break;
        case SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY:
        case SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION:
        case SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE:
        case SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL:
        case SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE:
        case SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_switch_get_callback_event(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    
    p_switch_master = ctc_sai_get_switch_property(lchip);
    
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY:
            attr->value.ptr = p_switch_master->switch_state_change_cb;
            break;
        case SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY:
            attr->value.ptr = p_switch_master->switch_shutdown_request_cb;
            break;
        case SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY:
            attr->value.ptr = p_switch_master->fdb_event_cb;
            break;
        case SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY:
            attr->value.ptr = p_switch_master->port_state_change_cb;
            break;
        case SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY:
            attr->value.ptr = p_switch_master->packet_event_cb;
            break;
        case SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY:
            attr->value.ptr = p_switch_master->bfd_event_cb;
            break;
        case SAI_SWITCH_ATTR_TWAMP_STATUS_CHANGE_NOTIFY:
            attr->value.ptr = p_switch_master->twamp_state_cb;
            break;
        case SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY:
            attr->value.ptr = p_switch_master->y1731_event_cb;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_switch_set_callback_event(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY:
            p_switch_master->switch_state_change_cb = (sai_switch_state_change_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY:
            p_switch_master->switch_shutdown_request_cb = (sai_switch_shutdown_request_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY:
            p_switch_master->fdb_event_cb = (sai_fdb_event_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY:
            p_switch_master->port_state_change_cb = (sai_port_state_change_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY:
            p_switch_master->packet_event_cb = (sai_packet_event_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY:
            p_switch_master->bfd_event_cb = (sai_bfd_session_state_change_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_TWAMP_STATUS_CHANGE_NOTIFY:
            p_switch_master->twamp_state_cb = (sai_twamp_session_status_change_notification_fn)attr->value.ptr;
            break;
        case SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY:
            p_switch_master->y1731_event_cb = (sai_y1731_session_state_change_notification_fn)attr->value.ptr;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

sai_status_t
ctc_sai_switch_get_available_info(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint32 count = 0;
    sai_acl_resource_list_t acl_resource;
    ctc_sai_switch_master_t *p_switch_master = NULL;
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    sal_memset(&acl_resource, 0, sizeof(sai_acl_resource_list_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" get switch attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY:
            attr->value.u32 = p_switch_master->route_cnt[SAI_IP_ADDR_FAMILY_IPV4];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY:
            attr->value.u32 = p_switch_master->route_cnt[SAI_IP_ADDR_FAMILY_IPV6];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY:
            attr->value.u32 = p_switch_master->nexthop_cnt[SAI_IP_ADDR_FAMILY_IPV4];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY:
            attr->value.u32 = p_switch_master->nexthop_cnt[SAI_IP_ADDR_FAMILY_IPV6];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY:
            attr->value.u32 = p_switch_master->neighbor_cnt[SAI_IP_ADDR_FAMILY_IPV4];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY:
            attr->value.u32 = p_switch_master->neighbor_cnt[SAI_IP_ADDR_FAMILY_IPV6];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY:
            ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_NEXT_HOP_GROUP, &count);
            attr->value.u32 = count;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY:
            ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, &count);
            attr->value.u32 = count;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY:
            {
                attr->value.u32 = ctc_sai_fdb_get_fdb_count(lchip);
                break;
            }
        case SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY:
            ctc_sai_db_entry_property_get_cnt(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, &count);
            attr->value.u32 = count;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY:
            ctc_sai_db_entry_property_get_cnt(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, &count);
            attr->value.u32 = count;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY:
            attr->value.u32 = p_switch_master->nat_cnt[CTC_SAI_CNT_DNAT];
            break;
        case SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY:
            attr->value.u32 = p_switch_master->nat_cnt[CTC_SAI_CNT_SNAT];
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION:
            ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_BFD_SESSION, &count);
            attr->value.u32 = count;
            break;
        case SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION:
            ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_Y1731_SESSION, &count);
            attr->value.u32 = count;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_switch_get_acl_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t *p_bounded_oid = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);

    switch (attr->id)
    {
        /*read-only*/
        /*Acl table/group/entry priority*/
        case SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY:
            attr->value.u32 = 1;
            break;
        case SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY:
            attr->value.u32 = 32767;
            break;
        case SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY : /* acl entry priority take up 16 bit */
            attr->value.u32 = 1;
            break;
        case SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY:
            attr->value.u32 = 65535;
            break;
        case SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY:
        case SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
        /*acl trap id*/
        case SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE:
            attr->value.u32range.min = 78;
            attr->value.u32range.max = 128;
            break;
        case SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT:
            attr->value.u32 = 19; /* count the number of SAI ACL action supported by CTC SDK (both ingress and egress) */
            break;
        case SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT:
            attr->value.u32 = 12 + 64 * 8;
            break;
        case SAI_SWITCH_ATTR_ACL_CAPABILITY:
            attr->value.aclcapability.is_action_list_mandatory = false;
            attr->value.aclcapability.action_list.count = 19;
            attr->value.aclcapability.action_list.list[0] = SAI_ACL_ACTION_TYPE_REDIRECT;
            attr->value.aclcapability.action_list.list[1] = SAI_ACL_ACTION_TYPE_PACKET_ACTION;
            attr->value.aclcapability.action_list.list[2] = SAI_ACL_ACTION_TYPE_COUNTER;
            attr->value.aclcapability.action_list.list[3] = SAI_ACL_ACTION_TYPE_MIRROR_INGRESS;
            attr->value.aclcapability.action_list.list[4] = SAI_ACL_ACTION_TYPE_SET_POLICER;
            attr->value.aclcapability.action_list.list[5] = SAI_ACL_ACTION_TYPE_SET_TC;
            attr->value.aclcapability.action_list.list[6] = SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR;
            attr->value.aclcapability.action_list.list[7] = SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID;
            attr->value.aclcapability.action_list.list[8] = SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI;
            attr->value.aclcapability.action_list.list[9] = SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID;
            attr->value.aclcapability.action_list.list[10] = SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI;
            attr->value.aclcapability.action_list.list[11] = SAI_ACL_ACTION_TYPE_SET_DSCP;
            attr->value.aclcapability.action_list.list[12] = SAI_ACL_ACTION_TYPE_SET_ECN;
            attr->value.aclcapability.action_list.list[13] = SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE;
            attr->value.aclcapability.action_list.list[14] = SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA;
            attr->value.aclcapability.action_list.list[15] = SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID;
            attr->value.aclcapability.action_list.list[16] = SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN;
            attr->value.aclcapability.action_list.list[17] = SAI_ACL_ACTION_TYPE_MIRROR_EGRESS;
            attr->value.aclcapability.action_list.list[18] = SAI_ACL_ACTION_TYPE_EGRESS_SAMPLEPACKET_ENABLE;
            break;
        case SAI_SWITCH_ATTR_INGRESS_ACL:
            p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND, (void*)(&key->key.object_id));
            attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
            break;
        case SAI_SWITCH_ATTR_EGRESS_ACL:
            return SAI_STATUS_NOT_SUPPORTED;
            break;

        /*read-only*/
        case SAI_SWITCH_ATTR_ACL_STAGE_INGRESS:
            attr->value.aclcapability.is_action_list_mandatory = false;
            attr->value.aclcapability.action_list.count = 17;
            attr->value.aclcapability.action_list.list[0] = SAI_ACL_ACTION_TYPE_REDIRECT;
            attr->value.aclcapability.action_list.list[1] = SAI_ACL_ACTION_TYPE_PACKET_ACTION;
            attr->value.aclcapability.action_list.list[2] = SAI_ACL_ACTION_TYPE_COUNTER;
            attr->value.aclcapability.action_list.list[3] = SAI_ACL_ACTION_TYPE_MIRROR_INGRESS;
            attr->value.aclcapability.action_list.list[4] = SAI_ACL_ACTION_TYPE_SET_POLICER;
            attr->value.aclcapability.action_list.list[5] = SAI_ACL_ACTION_TYPE_SET_TC;
            attr->value.aclcapability.action_list.list[6] = SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR;
            attr->value.aclcapability.action_list.list[7] = SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID;
            attr->value.aclcapability.action_list.list[8] = SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI;
            attr->value.aclcapability.action_list.list[9] = SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID;
            attr->value.aclcapability.action_list.list[10] = SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI;
            attr->value.aclcapability.action_list.list[11] = SAI_ACL_ACTION_TYPE_SET_DSCP;
            attr->value.aclcapability.action_list.list[12] = SAI_ACL_ACTION_TYPE_SET_ECN;
            attr->value.aclcapability.action_list.list[13] = SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE;
            attr->value.aclcapability.action_list.list[14] = SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA;
            attr->value.aclcapability.action_list.list[15] = SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID;
            attr->value.aclcapability.action_list.list[16] = SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN;
            break;
        case SAI_SWITCH_ATTR_ACL_STAGE_EGRESS:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_switch_set_acl_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_INFO(SAI_API_SWITCH, "object id %"PRIx64" set switch attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SWITCH_ATTR_INGRESS_ACL:
            CTC_SAI_ERROR_RETURN(ctc_sai_acl_bind_point_set(key, attr));
            break;
        case SAI_SWITCH_ATTR_EGRESS_ACL:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "switch attribute %d not implemented\n", attr->id);
            return  SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_switch_create_db(uint8 lchip)
{
    CTC_SAI_ERROR_RETURN(ctc_sai_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_switch_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_port_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_fdb_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_stp_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_vlan_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_virtual_router_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_route_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_next_hop_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_next_hop_group_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_hostif_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_mirror_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_lag_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_policer_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_wred_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_queue_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_ld_hash_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_udf_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_mcast_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_samplepacket_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_group_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_buffer_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_mpls_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_tunnel_db_init(lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_acl_db_init(lchip));
    CTC_SAI_ERROR_RETURN((ctc_sai_isolation_group_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_counter_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_debug_counter_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_nat_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_bfd_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_twamp_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_npm_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_y1731_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_ptp_db_init(lchip)));
    CTC_SAI_ERROR_RETURN((ctc_sai_es_db_init(lchip)));
        return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_switch_destroy_db(uint8 lchip)
{
    ctc_sai_isolation_group_db_deinit(lchip);
    ctc_sai_tunnel_db_deinit(lchip);
    ctc_sai_samplepacket_db_deinit(lchip);
    ctc_sai_hostif_db_deinit(lchip);
    ctc_sai_port_db_deinit(lchip);
    ctc_sai_neighbor_db_deinit(lchip);
    ctc_sai_ld_hash_db_deinit(lchip);
    ctc_sai_mirror_db_deinit(lchip);
    ctc_sai_qos_map_db_deinit(lchip);
    ctc_sai_mcast_db_deinit(lchip);
    ctc_sai_acl_db_deinit(lchip);
    ctc_sai_bfd_db_deinit(lchip);
    ctc_sai_y1731_db_deinit(lchip);

    /*Last Operation*/
    ctc_sai_db_deinit(lchip);

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
ctc_sai_swith_isr_init(uint8 lchip)
{
    /* 1. register event callback */
    ctcs_interrupt_register_event_cb(lchip, CTC_EVENT_L2_SW_LEARNING,    ctc_sai_switch_fdb_learning_process);
    ctcs_interrupt_register_event_cb(lchip, CTC_EVENT_L2_SW_AGING,       ctc_sai_switch_fdb_aging_process);
    ctcs_interrupt_register_event_cb(lchip, CTC_EVENT_PORT_LINK_CHANGE,  ctc_sai_switch_port_link_isr);
    ctcs_interrupt_register_event_cb(lchip, CTC_EVENT_OAM_STATUS_UPDATE, ctc_sai_switch_oam_event_process);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_switch_init_switch(uint8 lchip, dal_pci_dev_t* p_pci_dev, sai_object_id_t switch_id)
{
    sai_status_t     status = SAI_STATUS_SUCCESS;
    const char                 *profile_char;
    uint8                     boot_type     = 0;
    uint8 chip_type = 0;
    uint32 linkagg_num = 0;
    const char*                       init_cfg_file = NULL;
    const char*                       datapath_cfg_file = NULL;
    sai_service_method_table_t* p_api_services=NULL;
    ctc_init_cfg_t* init_config = NULL;
    dal_op_t dal_cfg;
    ctc_pkt_global_cfg_t pkt_cfg;
    ctc_linkagg_global_cfg_t lag_cfg;
    ctc_nh_global_cfg_t    nh_global_cfg;
    ctc_port_global_cfg_t port_cfg;
    ctc_oam_global_t  oam_global;
    ctc_l2_fdb_global_cfg_t l2_fdb_global_cfg;
    ctc_mpls_init_t* mpls_cfg = NULL;
    ctc_intr_global_cfg_t intr_cfg;
    ctc_dma_global_cfg_t* dma_cfg = NULL;
    ctc_bpe_global_cfg_t bpe_cfg;
    ctc_chip_global_cfg_t   chip_cfg;
    ctc_datapath_global_cfg_t* datapath_cfg = NULL;
    ctc_qos_global_cfg_t*      qos_cfg  =NULL;
    ctc_ipuc_global_cfg_t      ipuc_cfg;
    ctc_stats_global_cfg_t stats_cfg;
    ctc_stacking_glb_cfg_t*      stacking_cfg  =NULL;
    ctc_ftm_key_info_t* ftm_key_info = NULL;
    ctc_ftm_tbl_info_t* ftm_tbl_info = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_overlay_tunnel_global_cfg_t* p_overlay_cfg = NULL;
    ctc_acl_global_cfg_t* p_acl_cfg = NULL;
    ctc_acl_league_t league;

    uint8 reloading = 0;
    char* boot_type_str[] = {"ColdBoot", "WarmBoot"};
    sal_time_t tv;
    char* p_time_str = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    ftm_key_info = (ctc_ftm_key_info_t*)sal_malloc(sizeof(ctc_ftm_key_info_t)*CTC_FTM_KEY_TYPE_MAX*3);
    ftm_tbl_info = (ctc_ftm_tbl_info_t*)sal_malloc(sizeof(ctc_ftm_tbl_info_t)*CTC_FTM_TBL_TYPE_MAX);
    init_config = (ctc_init_cfg_t*)sal_malloc( sizeof(ctc_init_cfg_t));
    mpls_cfg = (ctc_mpls_init_t*)sal_malloc( sizeof(ctc_mpls_init_t));
    datapath_cfg = (ctc_datapath_global_cfg_t*)sal_malloc(sizeof(ctc_datapath_global_cfg_t));
    dma_cfg = (ctc_dma_global_cfg_t*)sal_malloc(sizeof(ctc_dma_global_cfg_t));
    qos_cfg = (ctc_qos_global_cfg_t*)sal_malloc(sizeof(ctc_qos_global_cfg_t));
    stacking_cfg = (ctc_stacking_glb_cfg_t*)sal_malloc(sizeof(ctc_stacking_glb_cfg_t));
    p_overlay_cfg = (ctc_overlay_tunnel_global_cfg_t*)sal_malloc(sizeof(ctc_overlay_tunnel_global_cfg_t));
    p_acl_cfg = (ctc_acl_global_cfg_t*)sal_malloc(sizeof(ctc_acl_global_cfg_t));

    if ((NULL == ftm_key_info) || (NULL == ftm_tbl_info) || (NULL == init_config)
        || (NULL == mpls_cfg) || (NULL == datapath_cfg) || (NULL == dma_cfg) || (NULL == qos_cfg) || (NULL == stacking_cfg) || (NULL == p_overlay_cfg) || (NULL == p_acl_cfg))
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(init_config, 0, sizeof(ctc_init_cfg_t));
    sal_memset(&dal_cfg, 0, sizeof(dal_op_t));
    sal_memset(&pkt_cfg, 0, sizeof(ctc_pkt_global_cfg_t));
    sal_memset(&lag_cfg, 0, sizeof(ctc_linkagg_global_cfg_t));
    sal_memset(&nh_global_cfg,0,sizeof(ctc_nh_global_cfg_t));
    sal_memset(&oam_global,0,sizeof(ctc_oam_global_t));
    sal_memset(&l2_fdb_global_cfg,0,sizeof(ctc_l2_fdb_global_cfg_t));
    sal_memset(mpls_cfg,0,sizeof(ctc_mpls_init_t));
    sal_memset(&intr_cfg,0,sizeof(ctc_intr_global_cfg_t));
    sal_memset(dma_cfg,0,sizeof(ctc_dma_global_cfg_t));
    sal_memset(ftm_key_info, 0, 3*CTC_FTM_KEY_TYPE_MAX * sizeof(ctc_ftm_key_info_t));
    sal_memset(ftm_tbl_info, 0, CTC_FTM_TBL_TYPE_MAX * sizeof(ctc_ftm_tbl_info_t));
    sal_memset(&bpe_cfg,0,sizeof(ctc_bpe_global_cfg_t));
    sal_memset(&chip_cfg,0,sizeof(ctc_chip_global_cfg_t));
    sal_memset(datapath_cfg,0,sizeof(ctc_datapath_global_cfg_t));
    sal_memset(qos_cfg,0,sizeof(ctc_qos_global_cfg_t));
    sal_memset(&ipuc_cfg,0,sizeof(ctc_ipuc_global_cfg_t));
    sal_memset(&stats_cfg,0,sizeof(ctc_stats_global_cfg_t));
    sal_memset(stacking_cfg,0,sizeof(ctc_stacking_glb_cfg_t));
    sal_memset(&port_cfg,0,sizeof(ctc_port_global_cfg_t));
    sal_memset(p_overlay_cfg, 0, sizeof(ctc_overlay_tunnel_global_cfg_t));
    sal_memset(p_acl_cfg, 0, sizeof(ctc_acl_global_cfg_t));

    /* Config module init parameter, if set init_config.p_MODULE_cfg = NULL, using SDK default configration */
    init_config->dal_cfg = &dal_cfg;
    init_config->p_pkt_cfg = &pkt_cfg;
    init_config->p_nh_cfg    = &nh_global_cfg;
    init_config->p_oam_cfg   = &oam_global;
    init_config->p_l2_fdb_cfg= &l2_fdb_global_cfg;
    init_config->p_mpls_cfg  = mpls_cfg;
    init_config->p_intr_cfg  = &intr_cfg;
    init_config->p_dma_cfg = dma_cfg;
    init_config->ftm_info.key_info = ftm_key_info;
    init_config->ftm_info.tbl_info = ftm_tbl_info;
    init_config->p_bpe_cfg = &bpe_cfg;
    init_config->p_chip_cfg = &chip_cfg;
    init_config->p_datapath_cfg = datapath_cfg;
    init_config->p_qos_cfg = qos_cfg;
    init_config->p_ipuc_cfg = &ipuc_cfg;
    init_config->p_stats_cfg = &stats_cfg;
    init_config->p_stacking_cfg = stacking_cfg;
    init_config->p_linkagg_cfg = &lag_cfg;
    init_config->p_port_cfg = &port_cfg;
    init_config->p_overlay_cfg = p_overlay_cfg;
    init_config->p_acl_cfg = p_acl_cfg;

    sal_memcpy(&dal_cfg, &g_dal_op, sizeof(dal_op_t));
    dal_cfg.lchip = lchip;
    sal_memcpy(&dal_cfg.pci_dev, p_pci_dev, sizeof(dal_pci_dev_t));
    ctc_sai_get_services_fn(&p_api_services);

    init_cfg_file = p_api_services->profile_get_value(g_profile_id, SAI_KEY_INIT_CONFIG_FILE);
    datapath_cfg_file = p_api_services->profile_get_value(g_profile_id, SAI_KEY_HW_PORT_PROFILE_ID_CONFIG_FILE);

    /* get config info */
    status = ctc_app_get_config(lchip, (char*)init_cfg_file, (char*)datapath_cfg_file, init_config);
    if (status != 0)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "ctc_app_get_config failed:%s@%d \n",  __FUNCTION__, __LINE__);
        return SAI_STATUS_INVALID_PARAMETER;
    }

    init_config->p_pkt_cfg->rx_cb = _ctc_sai_hostif_packet_receive_from_sdk;
    init_config->p_stats_cfg->stats_mode = CTC_STATS_MODE_DEFINE;
    init_config->p_port_cfg->use_isolation_id = 1;
    
    profile_char = p_api_services->profile_get_value(g_profile_id, SAI_KEY_FDB_TABLE_SIZE);
    if (NULL != profile_char)
    {
        init_config->ftm_info.misc_info.profile_specs[CTC_FTM_SPEC_MAC]  = (uint32)sal_atoi(profile_char);
    }

    profile_char = p_api_services->profile_get_value(g_profile_id, SAI_KEY_L3_ROUTE_TABLE_SIZE);
    if (NULL != profile_char)
    {
        init_config->ftm_info.misc_info.profile_specs[CTC_FTM_SPEC_IPUC_LPM]  = (uint32)sal_atoi(profile_char);
    }

    profile_char = p_api_services->profile_get_value(g_profile_id, SAI_KEY_L3_NEIGHBOR_TABLE_SIZE);
    if (NULL != profile_char)
    {
        init_config->ftm_info.misc_info.profile_specs[CTC_FTM_SPEC_IPUC_HOST]  = (uint32)sal_atoi(profile_char);
    }

    profile_char = p_api_services->profile_get_value(g_profile_id, SAI_KEY_NUM_LAG_MEMBERS);
    /*default mode is  CTC_LINKAGG_MODE_FLEX*/
    init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_FLEX;
    if (NULL != profile_char)
    {
        linkagg_num  = (uint32)sal_atoi(profile_char);
        if (linkagg_num == 4)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_4;
        }
        else if (linkagg_num == 8)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_8;
        }
        else if (linkagg_num == 16)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_16;
        }
        else if (linkagg_num == 32)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_32;
        }
        else if (linkagg_num == 56)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_56;
        }
        else if (linkagg_num == 64)
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_64;
        }
        else
        {
            init_config->p_linkagg_cfg->linkagg_mode = CTC_LINKAGG_MODE_FLEX;
        }
    }

    profile_char = p_api_services->profile_get_value(g_profile_id, SAI_KEY_BOOT_TYPE);
    if (NULL != profile_char)
    {
        boot_type = (uint8)sal_atoi(profile_char);
    }
    else
    {
        boot_type = 0;
    }

    switch (boot_type)
    {
            /* cold boot */
        case 0:
            reloading = 0;
            break;
        case 1:
            reloading = 1;
            break;
            /* default */
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Boot type %d not recognized, must be 0 (cold) or 1 (warm) or 2 (fast)\n", boot_type);
            return SAI_STATUS_INVALID_PARAMETER;
    }

    //p_overlay_cfg->vxlan_mode = CTC_OVERLAY_TUNNEL_DECAP_BY_IPDA_VNI;
    p_overlay_cfg->vxlan_mode = 0;
    p_overlay_cfg->vni_mapping_mode = 0;

    //ECMP number of members per group Default is 64
    //nh_global_cfg.max_ecmp = 64;

    sal_time(&tv);
    p_time_str = sal_ctime(&tv);
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "Create Swtich, %s, Start time %s", boot_type_str[boot_type], p_time_str);

    ctc_sai_warmboot_init(lchip, reloading);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_sdk_init(lchip, init_config), status, roll_back_0);
    sal_memset(&league, 0, sizeof(ctc_acl_league_t));

    league.dir = CTC_INGRESS;
    league.auto_move_en = 0;
    league.acl_priority = 5;
    league.lkup_level_bitmap = 0x60;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_acl_set_league_mode(lchip, &league), status, roll_back_1);

    chip_type = ctcs_get_chip_type(lchip);
    if(CTC_CHIP_GOLDENGATE != chip_type)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_diag_init(lchip, NULL), status, roll_back_1);
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_swith_isr_init(lchip), status, roll_back_2);
    if (!reloading)
    {
        if (FALSE == g_ctc_sai_master.cli_init)
        {
            ctc_master_cli(1);
            g_ctc_sai_master.cli_init = TRUE;
        }
    }
    ctc_wb_deinit(lchip);
    CTC_SAI_CTC_ERROR_GOTO(ctc_sai_warmboot_init(lchip, reloading), status, roll_back_2);   /*because ctcs_sdk_init call ctc_wb_init_done*/
    CTC_SAI_CTC_ERROR_GOTO(ctc_sai_switch_create_db(lchip), status, roll_back_2);
    CTC_SAI_CTC_ERROR_GOTO(ctc_sai_warmboot_init_done(lchip, reloading), status, roll_back_3);

    sal_time(&tv);
    p_time_str = sal_ctime(&tv);
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "Create Swtich, %s, End time %s", boot_type_str[boot_type], p_time_str);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "get switch oid property error lchip %d!\n", lchip);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto roll_back_3;
    }

    if (init_config->p_chip_cfg->cpu_port_en)
    {
        CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN);
        p_switch_master->cpu_eth_port = init_config->p_chip_cfg->cpu_port;
    }

    p_switch_master->port_queues = init_config->p_qos_cfg->queue_num_per_network_port;
    
    if (init_config->p_chip_cfg->cut_through_en)
    {
        CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CUT_THROUGH_EN);
    }

    if (init_config->p_l2_fdb_cfg->hw_learn_en)
    {
        CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN);
    }

    goto roll_back_0;

roll_back_3:
    ctc_sai_db_deinit(lchip);
roll_back_2:
    if(CTC_CHIP_GOLDENGATE != chip_type)
    {
        ctcs_diag_deinit(lchip);
    }
roll_back_1:
    ctcs_sdk_deinit(lchip);

roll_back_0:
    if (ftm_key_info)
    {
        sal_free(ftm_key_info);
    }

    if (ftm_tbl_info)
    {
        sal_free(ftm_tbl_info);
    }

    if (mpls_cfg)
    {
        sal_free(mpls_cfg);
    }

    if (datapath_cfg)
    {
        sal_free(datapath_cfg);
    }

    if(dma_cfg)
    {
        sal_free(dma_cfg);
    }
    if(qos_cfg)
    {
        sal_free(qos_cfg);
    }

    if(stacking_cfg)
    {
        sal_free(stacking_cfg);
    }

    if(p_overlay_cfg)
    {
        sal_free(p_overlay_cfg);
    }
    
    if(p_acl_cfg)
    {
        sal_free(p_acl_cfg);
    }

    if(init_config)
    {
        sal_free(init_config);
    }

    return status;
}


static sai_status_t
ctc_sai_switch_deinit_switch(sai_object_id_t switch_id)
{
    ctc_sai_switch_master_t* p_switch_info = NULL;
    uint8 lchip = 0;
    char* boot_type_str[] = {"ColdBoot", "WarmBoot"};
    uint8 wb_flag = 0, stop_dataplane = 0;
    sal_time_t tv;
    char* p_time_str = NULL;
    ctc_global_panel_ports_t local_panel_ports;
    uint16 count = 0;
    uint8 lchip_num = 0;
    uint8 gchip = 0;
    uint32 gport = 0;

    sal_memset(&local_panel_ports, 0 ,sizeof(local_panel_ports));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    ctcs_get_gchip_id(lchip, &gchip);

    p_switch_info = ctc_sai_get_switch_property(lchip);

    if (NULL == p_switch_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    wb_flag = CTC_FLAG_ISSET(p_switch_info->flag, CTC_SAI_SWITCH_FLAG_WARMBOOT_EN) ? 1 : 0;
    stop_dataplane = CTC_FLAG_ISSET(p_switch_info->flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL)?1:0;
    
    if(stop_dataplane)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));
        for(count = 0; count < local_panel_ports.count; count++)
        {   
            gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[count]);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_mac_en(lchip, gport, 0));
            if (1 == SDK_WORK_PLATFORM)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_port_en(lchip, gport, 0));
            }
        }

    }
    
    sal_time(&tv);
    p_time_str = sal_ctime(&tv);
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "Remove Swtich, %s, Start time %s", boot_type_str[wb_flag], p_time_str);

    if (wb_flag)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_warmboot_sync(lchip));
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_switch_destroy_db(lchip));
    ctcs_get_local_chip_num(lchip, &lchip_num);
    if (1 == lchip_num)
    {
        ctc_wb_deinit(lchip);
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_sdk_deinit(lchip));

    sal_time(&tv);
    p_time_str = sal_ctime(&tv);
    CTC_SAI_LOG_CRITICAL(SAI_API_SWITCH, "Remove Swtich, %s, End time %s", boot_type_str[wb_flag], p_time_str);

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Create switch
 *
 *   SDK initialization/connect to SDK. After the call the capability attributes should be
 *   ready for retrieval via sai_get_switch_attribute(). Same Switch Object id should be
 *   given for create/connect for each NPU.
 *
 * @param[out] switch_id The Switch Object ID
 * @param[in] attr_count number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_switch_create_switch(sai_object_id_t* switch_id,
                                        uint32_t attr_count,
                                        const sai_attribute_t* attr_list)
{
    uint8 lchip = 0;
    uint32 index = 0;
    uint32 loop_i = 0;
    sai_status_t     status = 0;
    const sai_attribute_value_t *attr_val       = NULL;
    ctc_object_id_t             ctc_sai_switch_id;
    sai_status_t                sai_status={0};
    uint32                      attr_idx;
    dal_pci_dev_t pci_dev;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_object_key_t key;
    sai_attribute_t  attr;

    CTC_SAI_PTR_VALID_CHECK(switch_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    sal_memset(&ctc_sai_switch_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&pci_dev, 0, sizeof(dal_pci_dev_t));
    sal_memset(&attr, 0, sizeof(sai_attribute_t));

    
    ctc_sai_switch_id.type = SAI_OBJECT_TYPE_SWITCH;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_INIT_SWITCH, &attr_val, &attr_idx);
    
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Missing mandatory SAI_SWITCH_ATTR_INIT_SWITCH attr\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    // TBD SAI_SWITCH_ATTR_INIT_SWITCH
    
    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        index = attr_val->s8list.count;
        if ((1 == index) || (4 == index))
        {
            ctc_sai_switch_id.lchip = attr_val->s8list.list[0];
            ctc_sai_switch_id.value = attr_val->s8list.list[0];
            if (index > 1)
            {
                pci_dev.busNo = attr_val->s8list.list[1];
                pci_dev.devNo = attr_val->s8list.list[2];
                pci_dev.funNo = attr_val->s8list.list[3];
            }
        }
    }
    else
    {
        ctc_sai_switch_id.lchip = 0;
        ctc_sai_switch_id.value = 0;
    }

    lchip = ctc_sai_switch_id.lchip;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_SWITCH, &ctc_sai_switch_id, switch_id));

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_SWITCH_PROFILE_ID, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        g_profile_id = attr_val->u32;
    }
    else
    {
        g_profile_id = 0;
    }

    sai_status = ctc_sai_switch_init_switch(lchip, &pci_dev, *switch_id);
    
    if (CTC_SAI_ERROR(sai_status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "init ctcs_sdk_init failed lchip %d!\n", lchip);
        return SAI_STATUS_UNINITIALIZED;
    }

    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch global info, invalid lchip %d!\n", lchip);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_switch_master->profile_id = g_profile_id;
    
    sal_memcpy(&(p_switch_master->pci_dev), &pci_dev, sizeof(dal_pci_dev_t));

    sai_status = ctc_sai_find_attrib_in_list(attr_count,
                                     attr_list,
                                     SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY,
                                     &attr_val,
                                     &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->switch_state_change_cb = (sai_switch_state_change_notification_fn)attr_val->ptr;
    }


    sai_status = ctc_sai_find_attrib_in_list(attr_count,
                                     attr_list,
                                     SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY,
                                     &attr_val,
                                     &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->switch_shutdown_request_cb = (sai_switch_shutdown_request_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->fdb_event_cb = (sai_fdb_event_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count,
                                     attr_list,
                                     SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY,
                                     &attr_val,
                                     &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->port_state_change_cb = (sai_port_state_change_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->bfd_event_cb = (sai_bfd_session_state_change_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_TWAMP_STATUS_CHANGE_NOTIFY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->twamp_state_cb = (sai_twamp_session_status_change_notification_fn)attr_val->ptr;
    }

    
    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->y1731_event_cb = (sai_y1731_session_state_change_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        p_switch_master->packet_event_cb = (sai_packet_event_notification_fn)attr_val->ptr;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(sai_status))
    {
        mac_addr_t mac;
        sal_memset(mac, 0, sizeof(mac_addr_t));
        sal_memcpy(mac, attr_val->mac,sizeof(sai_mac_t));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_router_mac(lchip, mac));
    }

    sal_memset(&key, 0, sizeof(key));
    key.key.object_id = *switch_id;
    while (loop_i <= SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION)
    {
        sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, loop_i, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(sai_status))
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr_list[attr_idx]));
        }
        loop_i++;
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL, &attr_val, &attr_idx);
    if(!CTC_SAI_ERROR(sai_status))
    {
        CTC_SET_FLAG(p_switch_master->flag, attr_val->booldata ? CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL : 0);
    }
    else
    {
        CTC_SET_FLAG(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL);
    }
    sai_status = ctc_sai_find_attrib_in_list(attr_count,attr_list, SAI_SWITCH_ATTR_PRE_SHUTDOWN, &attr_val, &attr_idx);
    if(!CTC_SAI_ERROR(sai_status))
    {
        CTC_SET_FLAG(p_switch_master->flag, attr_val->booldata ? CTC_SAI_SWITCH_FLAG_PRE_SHUTDOWN : 0);
    }

    sal_memset(&key, 0, sizeof(key));
    key.key.object_id = *switch_id;
    sai_status = ctc_sai_find_attrib_in_list(attr_count,attr_list, SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT, &attr_val, &attr_idx);
    if(!CTC_SAI_ERROR(sai_status))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr_list[attr_idx]));
    }

    sai_status = ctc_sai_find_attrib_in_list(attr_count,attr_list, SAI_SWITCH_ATTR_CRC_CHECK_ENABLE, &attr_val, &attr_idx);
    if(!CTC_SAI_ERROR(sai_status))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr_list[attr_idx]));
    }
    else
    {
        attr.id = SAI_SWITCH_ATTR_CRC_CHECK_ENABLE;
        attr.value.booldata = true;
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr));
    }        

    sai_status = ctc_sai_find_attrib_in_list(attr_count,attr_list, SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE, &attr_val, &attr_idx);
    if(!CTC_SAI_ERROR(sai_status))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr_list[attr_idx]));
    }
    else
    {
        attr.id = SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE;
        attr.value.booldata = true;
        CTC_SAI_ERROR_RETURN(ctc_sai_switch_set_global_property(&key, &attr));
    }         

    return status;
}

/**
 * @brief Remove/disconnect Switch
 *   Release all resources associated with currently opened switch
 *
 * @param[in] switch_id The Switch id
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_switch_remove_switch(sai_object_id_t switch_id)
{
    CTC_SAI_ERROR_RETURN(ctc_sai_switch_deinit_switch(switch_id));
    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  switch_attr_fn_entries[] = {
    {SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS, ctc_sai_switch_get_global_panel_ports, NULL},
    {SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_PORT_LIST, ctc_sai_switch_get_global_panel_ports, NULL},
    {SAI_SWITCH_ATTR_PORT_MAX_MTU, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_CPU_PORT, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_FDB_TABLE_SIZE, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_LAG_MEMBERS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_LAGS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_ECMP_MEMBERS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_QUEUES, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_OPER_STATUS, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_TEMP_LIST, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MAX_TEMP, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_AVERAGE_TEMP, ctc_sai_switch_get_global_property, NULL},      
    {SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_DEFAULT_VLAN_ID, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MAX_STP_INSTANCE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_INGRESS_ACL, ctc_sai_switch_get_acl_property, ctc_sai_switch_set_acl_property},
    {SAI_SWITCH_ATTR_EGRESS_ACL, ctc_sai_switch_get_acl_property, ctc_sai_switch_set_acl_property},
    {SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES, ctc_sai_switch_get_qos_property, NULL},
    {SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS, ctc_sai_switch_get_qos_property, NULL},
    {SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL, ctc_sai_switch_get_qos_property, NULL},
    {SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP, ctc_sai_switch_get_qos_property, NULL},
    {SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY, NULL, NULL},    
    {SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ECMP_HASH, ctc_sai_switch_get_hash_property, NULL},
    {SAI_SWITCH_ATTR_LAG_HASH, ctc_sai_switch_get_hash_property, NULL},
    {SAI_SWITCH_ATTR_RESTART_WARM, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_WARM_RECOVER, NULL, NULL},    
    {SAI_SWITCH_ATTR_RESTART_TYPE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_NV_STORAGE_SIZE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_CAPABILITY, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_SWITCHING_MODE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_FDB_AGING_TIME, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_ECMP_HASH_IPV4, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_ECMP_HASH_IPV6, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_HASH_IPV4, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_LAG_HASH_IPV6, ctc_sai_switch_get_hash_property, ctc_sai_switch_set_hash_property},
    {SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_QOS_DEFAULT_TC, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_SWITCH_PROFILE_ID, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_INIT_SWITCH, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_TWAMP_STATUS_CHANGE_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_MAX_TWAMP_SESSION, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},    
    {SAI_SWITCH_ATTR_FAST_API_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_MIRROR_TC, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_ACL_STAGE_INGRESS, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_ACL_STAGE_EGRESS, ctc_sai_switch_get_acl_property, NULL},
    {SAI_SWITCH_ATTR_SEGMENTROUTE_MAX_SID_DEPTH, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_SEGMENTROUTE_TLV_TYPE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL, ctc_sai_switch_get_qos_property, ctc_sai_switch_set_qos_property},
    {SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_TPID_OUTER_VLAN, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_TPID_INNER_VLAN, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_CRC_CHECK_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_MAX_BFD_SESSION, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MIN_BFD_RX, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_MIN_BFD_TX, ctc_sai_switch_get_global_property, NULL},
    {SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE, NULL, NULL},
    {SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_MAX_MIRROR_SESSION, NULL, NULL},
    {SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION, NULL, NULL},
    {SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE, ctc_sai_switch_get_global_property, NULL},  
    {SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_TAM_OBJECT_ID, NULL, NULL},
    {SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY, NULL, NULL},
    {SAI_SWITCH_ATTR_PRE_SHUTDOWN, ctc_sai_switch_get_global_property, ctc_sai_switch_set_global_property},
    {SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID, NULL, NULL},
    {SAI_SWITCH_ATTR_NAT_ENABLE, NULL, NULL},
    {SAI_SWITCH_ATTR_Y1731_SESSION_EVENT_NOTIFY, ctc_sai_switch_get_callback_event, ctc_sai_switch_set_callback_event},
    {SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION, ctc_sai_switch_get_available_info, NULL},
    {SAI_SWITCH_ATTR_MAX_Y1731_SESSION, ctc_sai_switch_get_global_capability, NULL},
    {SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE, ctc_sai_switch_get_global_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

/**
 * @brief Set switch attribute value
 *
 * @param[in] switch_id Switch id
 * @param[in] attr Switch attribute
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t
ctc_sai_switch_set_switch_attribute(sai_object_id_t switch_id, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = switch_id };
    sai_status_t           status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = switch_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_SWITCH, switch_attr_fn_entries, attr);

    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to set switch attr:%d, status:%d\n", attr->id,status);
    }

    return status;
}

/**
 * @brief Get switch attribute value
 *
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of switch attributes
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
 static sai_status_t
 ctc_sai_switch_get_switch_attribute(sai_object_id_t switch_id, sai_uint32_t attr_count, sai_attribute_t* attr_list)
 {
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = switch_id };
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = switch_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_SWITCH, loop, switch_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }
    
out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
 }

sai_status_t ctc_sai_switch_get_switch_stats(
        sai_object_id_t switch_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        uint64_t *counters)
{
    uint8 lchip = 0;
    uint16 index = 0;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint64 cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    for (index = 0; index < number_of_counters; index ++ )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_debug_counter_get_switch_stats(lchip, counter_ids[index], 0, &cnt), status, out);
        counters[index] = cnt;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch stats ,status = %d\n", status);
    }
    return status;

}

sai_status_t ctc_sai_switch_get_switch_stats_ext (
        sai_object_id_t switch_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        sai_stats_mode_t mode,
        uint64_t *counters)
{
    uint8 lchip = 0;
    uint16 index = 0;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint64 cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    for (index = 0; index < number_of_counters; index ++ )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_debug_counter_get_switch_stats(lchip, counter_ids[index], mode, &cnt), status, out);
        counters[index] = cnt;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get switch stats ,status = %d\n", status);
    }    
    return status;

}


sai_status_t ctc_sai_switch_clear_switch_stats (
        sai_object_id_t switch_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids)
{
    uint8 lchip = 0;
    uint16 index = 0;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint64 cnt = 0;

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_LOG_ENTER(SAI_API_SWITCH);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    /* Clear on Read */
    for (index = 0; index < number_of_counters; index ++ )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_debug_counter_get_switch_stats(lchip, counter_ids[index], 1, &cnt), status, out);
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to clear switch stats ,status = %d\n", status);
    }     
    return status;

}

#define ________SAI_API________

const sai_switch_api_t g_ctc_sai_switch_api = {
    ctc_sai_switch_create_switch,
    ctc_sai_switch_remove_switch,
    ctc_sai_switch_set_switch_attribute,
    ctc_sai_switch_get_switch_attribute,
    ctc_sai_switch_get_switch_stats,
    ctc_sai_switch_get_switch_stats_ext,
    ctc_sai_switch_clear_switch_stats,
};
    
#define ________SAI_DUMP________

void ctc_sai_switch_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_switch_master_t* p_switch_info = NULL;
    sai_object_id_t  switch_oid_cur = 0;
    ctc_sai_switch_master_t ctc_switch_master_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    ctc_global_panel_ports_t local_panel_ports;
    uint16 loop_count = 0;
	uint8 gchip = 0;
    char src_mac[64] = {0};

	ctcs_get_gchip_id(lchip, &gchip);
    CTC_SAI_LOG_DUMP(p_file, "\n");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI SWITCH MODULE");

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_SWITCH))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Switch");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_switch_master_t");
        sal_memset(&ctc_switch_master_cur, 0, sizeof(ctc_sai_switch_master_t));
        sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
        switch_oid_cur = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        p_switch_info = ctc_sai_db_get_object_property(lchip, switch_oid_cur);
        ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);

        sal_memcpy((&ctc_switch_master_cur), p_switch_info, sizeof(ctc_sai_switch_master_t));

        p_dmp_grep = dump_grep_param;

        if ((0 != p_dmp_grep->key.key.object_id) && (switch_oid_cur != p_dmp_grep->key.key.object_id))
        {
            return;
        }
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------------STP----------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "Default bridge ID: %d\n", ctc_switch_master_cur.default_bridge_id);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "---------------------------------------------------FLAGS---------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10s %-10s %-30d\n", "CPU ETH enable: ", CTC_FLAG_ISSET(ctc_switch_master_cur.flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN)?"Y":"N", "CPU ETH port: ", ctc_switch_master_cur.cpu_eth_port);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10s\n", "Cut through enable: ", CTC_FLAG_ISSET(ctc_switch_master_cur.flag, CTC_SAI_SWITCH_FLAG_CUT_THROUGH_EN)?"Y":"N");
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10s\n", "CRC check enable: ", CTC_FLAG_ISSET(ctc_switch_master_cur.flag, CTC_SAI_SWITCH_FLAG_CRC_CHECK_EN)?"Y":"N");
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10s\n", "HW learning enable: ", CTC_FLAG_ISSET(ctc_switch_master_cur.flag, CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN)?"Y":"N");
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10s\n", "Uninit data plane on removal: ", CTC_FLAG_ISSET(ctc_switch_master_cur.flag, CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL)?"Y":"N");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------------QOS----------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "Ucast port queues: ", ctc_switch_master_cur.port_queues);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "Default tc: ", ctc_switch_master_cur.default_tc);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "Default WTD thrd(G): ", ctc_switch_master_cur.default_wtd_thrd[SAI_PACKET_COLOR_GREEN]);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "Default WTD thrd(Y): ", ctc_switch_master_cur.default_wtd_thrd[SAI_PACKET_COLOR_YELLOW]);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "Default WTD thrd(R): ", ctc_switch_master_cur.default_wtd_thrd[SAI_PACKET_COLOR_RED]);
        CTC_SAI_LOG_DUMP(p_file, "%-30s %-10d\n", "TC to queue map id: ", ctc_switch_master_cur.tc_to_queue_map_id);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------QOS_DOMAIN_DOT1P---------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Index  Dot1p_to_tc  cnt  Dot1p_to_color  cnt  Tc/color_to_dot1p  cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        for (loop_count = 0; loop_count < QOS_MAP_DOMAIN_NUM_DOT1P; loop_count++)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-7d0x%-11x0x%-3x0x%-14x0x%-3x0x%-17x0x%-3x\n", loop_count,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dot1p[loop_count].tc),
                             ctc_switch_master_cur.qos_domain_dot1p[loop_count].ref_cnt_tc,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dot1p[loop_count].color),
                             ctc_switch_master_cur.qos_domain_dot1p[loop_count].ref_cnt_color,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dot1p[loop_count].tc_color),
                             ctc_switch_master_cur.qos_domain_dot1p[loop_count].ref_cnt_tc_color);
        }
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------QOS_DOMAIN_DSCP---------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Index  Dscp_to_tc  cnt  Dscp_to_color  cnt  Tc/color_to_dscp  cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        for (loop_count = 0; loop_count < QOS_MAP_DOMAIN_NUM_DSCP; loop_count++)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-7d0x%-10x0x%-3x0x%-13x0x%-3x0x%-16x0x%-3x\n", loop_count,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dscp[loop_count].tc),
                             ctc_switch_master_cur.qos_domain_dscp[loop_count].ref_cnt_tc,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dscp[loop_count].color),
                             ctc_switch_master_cur.qos_domain_dscp[loop_count].ref_cnt_color,
                             *(uint32 *)(&ctc_switch_master_cur.qos_domain_dscp[loop_count].tc_color),
                             ctc_switch_master_cur.qos_domain_dscp[loop_count].ref_cnt_tc_color);
        }
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-------------------------------------------------ROUTE_CNT-------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv4 route cnt: ", ctc_switch_master_cur.route_cnt[CTC_IP_VER_4]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv6 route cnt: ", ctc_switch_master_cur.route_cnt[CTC_IP_VER_6]);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------------NEXTHOP_CNT------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv4 nexthop cnt: ", ctc_switch_master_cur.nexthop_cnt[CTC_IP_VER_4]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv6 nexthop cnt: ", ctc_switch_master_cur.nexthop_cnt[CTC_IP_VER_6]);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------------NEIGHBOR_CNT-----------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv4 nexthop cnt: ", ctc_switch_master_cur.neighbor_cnt[CTC_IP_VER_4]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "IPv6 nexthop cnt: ", ctc_switch_master_cur.neighbor_cnt[CTC_IP_VER_6]);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------------NAT_CNT-----------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "snat cnt: ", ctc_switch_master_cur.nat_cnt[CTC_SAI_CNT_SNAT]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "dnat nexthop cnt: ", ctc_switch_master_cur.nat_cnt[CTC_SAI_CNT_DNAT]);        
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "---------------------------------------------MAX_FRAME_INDEX_CNT-------------------------------------------------------");
        for(loop_count = 0; loop_count < CTC_FRAME_SIZE_MAX; loop_count++)
        {
            CTC_SAI_LOG_DUMP(p_file, "%s(%d):     %-10d\n", "Max frame idx cnt", loop_count, ctc_switch_master_cur.max_frame_idx_cnt[loop_count]);
        }
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------------UDF----------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "UDF group cnt: ", ctc_switch_master_cur.udf_group_cnt);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------------FDB----------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Ucast fdb miss action:  ", ctc_switch_master_cur.fdb_miss_action[0]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Mcast fdb miss action:  ", ctc_switch_master_cur.fdb_miss_action[1]);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Bcast fdb miss action:  ", ctc_switch_master_cur.fdb_miss_action[2]);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "---------------------------------------------------HOSTIF--------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Hostif acl grp id: ", ctc_switch_master_cur.hostif_acl_grp_id);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Epoll sock: ", ctc_switch_master_cur.epoll_sock);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10u\n", "Epoll event: ", ctc_switch_master_cur.evl.events);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10d\n", "Epoll fd: ", ctc_switch_master_cur.evl.data.fd);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "---------------------------------------------------OTHER---------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10"PRIx64"\n", "Default trap grp id: ", ctc_switch_master_cur.default_trap_grp_id);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10u\n", "Bus No: ", ctc_switch_master_cur.pci_dev.busNo);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10u\n", "Dev No: ", ctc_switch_master_cur.pci_dev.devNo);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10u\n", "Fun No: ", ctc_switch_master_cur.pci_dev.funNo);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-10u\n", "profile_id: ", ctc_switch_master_cur.profile_id);       
        ctc_sai_get_mac_str(ctc_switch_master_cur.vxlan_default_router_mac, src_mac);
        CTC_SAI_LOG_DUMP(p_file, "%-25s %-16s\n", "vxlan_default_router_mac: ", src_mac);

        
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "----------------------------------------------PORT_LINK_STATUS---------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Port          Status | Port          Status");
        for(loop_count = 0; loop_count<local_panel_ports.count/2; loop_count++)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-14d%-7s| %-14d%-9s\n", loop_count,
                ctc_switch_master_cur.lport_link_status[loop_count] || 1 == SDK_WORK_PLATFORM ? "up":"down",
                loop_count+((local_panel_ports.count/2)),
                ctc_switch_master_cur.lport_link_status[loop_count+((local_panel_ports.count/2))] || 1 == SDK_WORK_PLATFORM ? "up":"down");
        }
        if(local_panel_ports.count%2)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-14d%-7s|", loop_count,
                              ctc_switch_master_cur.lport_link_status[loop_count] || 1 == SDK_WORK_PLATFORM ? "up":"down");
        }




    }
}


#define ________SAI_INIT________


sai_status_t
ctc_sai_switch_db_init(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t switch_id;
    ctc_qos_drop_t  ctc_drop;
    ctc_sai_switch_master_t* p_switch_info = NULL;
    uint8 gchip = 0;

    ctcs_get_gchip_id(lchip, &gchip);
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_SWITCH;
    wb_info.data_len = sizeof(ctc_sai_switch_master_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    CTC_SAI_ERROR_RETURN(ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_SWITCH, (void*)(&wb_info)));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    p_switch_info = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_switch_master_t));
    if (NULL == p_switch_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_switch_info, 0, sizeof(ctc_sai_switch_master_t));
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, switch_id, (void*)p_switch_info), status, roll_back_0);
    p_switch_info->default_bridge_id = 1;

    /* init default wtd threshold */
    sal_memset(&ctc_drop,0,sizeof(ctc_drop));
    ctc_drop.drop.mode = CTC_QUEUE_DROP_WTD;
    ctc_drop.queue.gport = CTC_MAP_LPORT_TO_GPORT(gchip, 0);
    ctc_drop.queue.queue_id = 0;
    ctc_drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_qos_get_drop_scheme(lchip, &ctc_drop), status, roll_back_0);
    p_switch_info->default_wtd_thrd[SAI_PACKET_COLOR_GREEN] = ctc_drop.drop.max_th[2];
    p_switch_info->default_wtd_thrd[SAI_PACKET_COLOR_YELLOW] = ctc_drop.drop.max_th[1];
    p_switch_info->default_wtd_thrd[SAI_PACKET_COLOR_RED] = ctc_drop.drop.max_th[0];

    return SAI_STATUS_SUCCESS;
roll_back_0:
    mem_free(p_switch_info);
    return status;
}

sai_status_t
ctc_sai_switch_api_init()
{
    ctc_sai_register_module_api(SAI_API_SWITCH, (void*)&g_ctc_sai_switch_api);

    return SAI_STATUS_SUCCESS;
}

