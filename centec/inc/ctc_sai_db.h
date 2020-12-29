/**
 @file ctc_sai_db.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

   This file is used to save /query db.
*/

#ifndef _CTC_SAI_DB_H
#define _CTC_SAI_DB_H

#include <sys/epoll.h>
#include "sal.h"
#include "dal.h"
#include "ctcs_api.h"
#include "ctc_hash.h"
#include "ctc_vector.h"
#include "ctc_opf.h"
#include "ctc_app_index.h"
#include "ctc_sai_warmboot.h"

#include "ctc_sai.h"
#include "ctc_sai_oid.h"

/*include other module header files*/
#define CTC_SAI_MAX_CHIP_NUM   32

#define CTC_SAI_META_DATA_FDB_DST_MAX   (CTC_MAX_ACL_CID - 2) /* for sdk, 0 is invalid, need mapping from sai*/
#define CTC_SAI_META_DATA_ROUTE_DST_MAX   (CTC_MAX_ACL_CID - 2) /* for sdk, 0 is invalid, need mapping from sai*/
#define CTC_SAI_META_DATA_NEIGHBOR_DST_MAX   0
#define CTC_SAI_META_DATA_PORT_MAX   (255 - 1)   /* for sdk, 0 is invalid, need mapping from sai*/
#define CTC_SAI_META_DATA_VLAN_MAX   (255 - 1)  /* for sdk, 0 is invalid, need mapping from sai*/
#define CTC_SAI_META_DATA_ACL_MAX (0x3FFF - 1) /* for sdk, 0 is invalid, need mapping from sai*/
#define CTC_SAI_META_DATA_SAI_TO_CTC(meta_date) (meta_date + 1)
#define CTC_SAI_META_DATA_CTC_TO_SAI(meta_date) (meta_date? (meta_date - 1) : 0)


#define CTC_SAI_DB_LOCK(lchip) ctc_sai_db_lock(lchip)
#define CTC_SAI_DB_UNLOCK(lchip) ctc_sai_db_unlock(lchip)

typedef struct ctc_sai_master_s
{
    uint8 cli_init;
    sal_task_t* p_shell_thread;
}ctc_sai_master_t;
extern ctc_sai_master_t g_ctc_sai_master;

typedef enum ctc_sai_db_id_type_e
{
    CTC_SAI_DB_ID_TYPE_COMMON = CTC_OPF_CUSTOM_ID_START,
    CTC_SAI_DB_ID_TYPE_VLAN,
    CTC_SAI_DB_ID_TYPE_VSI,
    CTC_SAI_DB_ID_TYPE_VPWS,
    CTC_SAI_DB_ID_TYPE_LOGIC_PORT,
    CTC_SAI_DB_ID_TYPE_VRF,
    CTC_SAI_DB_ID_TYPE_L3IF,
    CTC_SAI_DB_ID_TYPE_ARP,
    CTC_SAI_DB_ID_TYPE_NEXTHOP,
    CTC_SAI_DB_ID_TYPE_TUNNEL_ID,
    CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER,
    CTC_SAI_DB_ID_TYPE_APS,
    CTC_SAI_DB_ID_TYPE_POLICER,
    CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP,
    CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP,
    CTC_SAI_DB_ID_TYPE_RPF_GROUP,
    CTC_SAI_DB_ID_TYPE_LAG,
    CTC_SAI_DB_ID_TYPE_STP,
    /* SAI ACL */
    CTC_SAI_DB_ID_TYPE_ACL_GROUP_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_TABLE_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_ENTRY_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_GROUP_MEMBER_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_PORT_RANGE_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_VLAN_RANGE_INDEX,
    CTC_SAI_DB_ID_TYPE_ACL_COUNTER_INDEX,
    /* SDK ACL OR SCL */
    CTC_SAI_DB_ID_TYPE_SDK_SCL_GROUP_ID,
    CTC_SAI_DB_ID_TYPE_SDK_SCL_ENTRY_ID,
    CTC_SAI_DB_ID_TYPE_SDK_ACL_GROUP_ID,
    CTC_SAI_DB_ID_TYPE_SDK_ACL_ENTRY_ID,
    /* MAX FRAME SIZE INDEX*/
    CTC_SAI_DB_ID_TYPE_MAX_FRAME_SIZE,
    /* ISOLATION GROUP ID*/
    CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP,
    CTC_SAI_DB_ID_TYPE_VIF,
    CTC_SAI_DB_ID_TYPE_COUNTER,
    CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER,
    CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_IN_INDEX,
    CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_OUT_INDEX,
    CTC_SAI_DB_ID_TYPE_BFD,
    CTC_SAI_DB_ID_TYPE_TWAMP,
    CTC_SAI_DB_ID_TYPE_NPM,
    CTC_SAI_DB_ID_TYPE_ES,
    CTC_SAI_DB_ID_TYPE_Y1731_MEG,
    CTC_SAI_DB_ID_TYPE_Y1731_SESSION,
    CTC_SAI_DB_ID_TYPE_Y1731_REMOTE_MEP,
    CTC_SAI_DB_ID_TYPE_PTP,
    CTC_SAI_DB_ID_TYPE_SYNCE,
    CTC_SAI_DB_ID_TYPE_UDF_GROUP,
    CTC_SAI_DB_ID_TYPE_UDF_ENTRY,
    CTC_SAI_DB_ID_TYPE_UDF_MATCH,
    CTC_SAI_DB_ID_TYPE_WRED,

    CTC_SAI_DB_ID_TYPE_MAX,
}ctc_sai_db_id_type_t;

/* NOTES START: need set block array in ctc_sai_db_init() when add new type*/
typedef enum ctc_sai_db_entry_type_e
{
    CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR = 0,
    CTC_SAI_DB_ENTRY_TYPE_ROUTE,
    CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC,
    CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC,
    CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB,
    CTC_SAI_DB_ENTRY_TYPE_ACL, /* used for keeping the relationship between acl hardware entry(group) id and sdk entry(group) id */
    CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, /* used for keeping the relationship between bind point and bounded oid (group or table)*/
    CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS,  /* used for keeping the relationship between bind point and bounded oid (group or table)*/
    CTC_SAI_DB_ENTRY_TYPE_MPLS,
    CTC_SAI_DB_ENTRY_TYPE_NAT,
    CTC_SAI_DB_ENTRY_TYPE_MAX,
}ctc_sai_db_entry_type_t;

typedef enum ctc_sai_db_vector_type_e
{
    CTC_SAI_DB_VECTOR_TYPE_MIRROR = 0,
    CTC_SAI_DB_VECTOR_TYPE_MAX,
}ctc_sai_db_vector_type_t;
/* NOTES END*/

#define CTC_SAI_DB_MIRROR_SESSION_NUM 4
typedef enum ctc_sai_db_mirror_type_e
{
    CTC_SAI_DB_MIRROR_IGS_PORT = 0,
    CTC_SAI_DB_MIRROR_EGS_PORT,
    CTC_SAI_DB_MIRROR_IGS_ACL0,
    CTC_SAI_DB_MIRROR_IGS_ACL1,
    CTC_SAI_DB_MIRROR_IGS_ACL2,
    CTC_SAI_DB_MIRROR_IGS_ACL3,
    CTC_SAI_DB_MIRROR_IGS_ACL4,
    CTC_SAI_DB_MIRROR_IGS_ACL5,
    CTC_SAI_DB_MIRROR_IGS_ACL6,
    CTC_SAI_DB_MIRROR_IGS_ACL7,
    CTC_SAI_DB_MIRROR_EGS_ACL0,
    CTC_SAI_DB_MIRROR_EGS_ACL1,
    CTC_SAI_DB_MIRROR_EGS_ACL2,
    CTC_SAI_DB_MIRROR_MAX,
}ctc_sai_db_mirror_type_t;

#define _____OBJECT_DB______
typedef struct  ctc_sai_oid_property_s
{
    /*key*/
    sai_object_id_t oid;
    uint32 calc_key_len[0];
    /*data*/
    void* data;
}ctc_sai_oid_property_t;


#define _____NEIGHBOR_KEY______
typedef struct  ctc_sai_neighbor_key_s
{
    /*key*/
    uint16 l3if_id;
    uint8 sai_rif_type;
    uint8 ip_ver;
    union {
        sai_ip4_t ip4;
        sai_ip6_t ip6;
    }addr;
}ctc_sai_neighbor_key_t;

#define _____ROUTE_KEY______
typedef struct  ctc_sai_route_key_s
{
    /*key*/
    uint16 vrf_id;
    uint8 mask_len;
    uint8 ip_ver;
    union {
        sai_ip4_t ip4;
        sai_ip6_t ip6;
    }addr;
}ctc_sai_route_key_t;

#define _____MCAST_IP_KEY______
typedef struct  ctc_sai_mcast_ip_key_s
{
    /*key*/
    uint16 vrf_id;
    uint8 src_mask_len;
    uint8  ip_ver:1;
    uint8  is_l2mc:1;
    uint8  is_pending:1;
    uint8  is_bridge:1;
    uint8  rsv:4;
    union {
        sai_ip4_t ip4;
        sai_ip6_t ip6;
    }src;
    union {
        sai_ip4_t ip4;
        sai_ip6_t ip6;
    }dst;
}ctc_sai_mcast_ip_key_t;

#define _____MCAST_FDB_KEY______
typedef struct  ctc_sai_mcast_fdb_key_s
{
    /*key*/
    mac_addr_t mac;
    uint16  fid;
    uint16  is_pending:1;
    uint16  is_bridge:1;
    uint16  rsv:14;
}ctc_sai_mcast_fdb_key_t;

#define _____MPLS_KEY______
typedef struct  ctc_sai_mpls_key_s
{
    /*key*/
    uint32  label;
}ctc_sai_mpls_key_t;

#define _____NAT_KEY______
typedef struct  ctc_sai_nat_key_s
{
    /*key*/
    uint16 vrf_id;
    uint8 ip_ver;
    sai_ip4_t src_ip;
    sai_ip4_t dst_ip;
    uint8 proto;
    uint16 l4_src_port;
    uint16 l4_dst_port;
    uint32 nat_type;
}ctc_sai_nat_key_t;


#define _____ENTRY_DB______
typedef struct  ctc_sai_entry_property_s
{
    /*key*/
    ctc_sai_db_entry_type_t entry_type;
    union
    {
        ctc_sai_neighbor_key_t neighbor;
        ctc_sai_route_key_t route;
        ctc_sai_mcast_ip_key_t mcast_ip;
        ctc_sai_mcast_fdb_key_t mcast_fdb;
        ctc_sai_mpls_key_t mpls;
        ctc_sai_nat_key_t nat;
        uint64 hardware_id;    /* used for keeping the relationship between hardware entry(group) id and sdk entry(group) id */
        sai_object_id_t oid;   /* used for keeping the relationship between bind point oid and bounded oid */
    }key;
    uint32 calc_key_len[0];
    /*data*/
    void* data;
}ctc_sai_entry_property_t;

#define _____VECTOR_DB______
typedef struct  ctc_sai_vector_property_s
{
    /*key*/
    uint32 index;
    uint32 calc_key_len[0];
    /*data*/
    void* data;
}ctc_sai_vector_property_t;

#define _____QOS_DOMAIN______

#define QOS_MAP_DOMAIN_NUM_DOT1P   8
#define QOS_MAP_DOMAIN_NUM_DSCP   16
#define QOS_MAP_DOMAIN_NUM_EXP   16

typedef struct ctc_sai_qos_domain_map_id_s
{
    union
    {
        uint32 dot1p_to_tc_map_id;
        uint32 dscp_to_tc_map_id;
        uint32 exp_to_tc_map_id;
    }tc;
    union
    {
        uint32 dot1p_to_color_map_id;
        uint32 dscp_to_color_map_id;
        uint32 exp_to_color_map_id;
    }color;
    union
    {
        uint32 tc_color_to_dot1p_map_id;
        uint32 tc_color_to_dscp_map_id;
        uint32 tc_color_to_exp_map_id;
    }tc_color;
    uint16 ref_cnt_tc;
    uint16 ref_cnt_color;
    uint16 ref_cnt_tc_color;
}ctc_sai_qos_domain_map_id_t;

#define _____SWITCH_DB_____

typedef enum ctc_sai_switch_flag_e
{
    CTC_SAI_SWITCH_FLAG_CPU_ETH_EN              = 1U<<0,
    CTC_SAI_SWITCH_FLAG_CUT_THROUGH_EN          = 1U<<1,
    CTC_SAI_SWITCH_FLAG_CRC_CHECK_EN            = 1U<<2,
    CTC_SAI_SWITCH_FLAG_HW_LEARNING_EN          = 1U<<3,
    CTC_SAI_SWITCH_FLAG_WARMBOOT_EN             = 1U<<4,
    CTC_SAI_SWITCH_FLAG_UNINIT_DATA_PLANE_ON_REMOVAL  = 1U<<5,
    CTC_SAI_SWITCH_FLAG_PRE_SHUTDOWN            = 1U<<6,
    CTC_SAI_SWITCH_FLAG_CRC_OVERWRITE_EN        = 1u<<7,
    CTC_SAI_DB_FLAG_MAX
}ctc_sai_switch_flag_t;

#define CTC_SAI_NAT_TYPE_NUM 2
#define CTC_SAI_LOCAL_PORT_NUM 512
typedef struct ctc_sai_switch_master_s{
    uint32 default_bridge_id;
    uint32 flag;
    uint32 cpu_eth_port;
    uint32 profile_id;
    uint8 port_queues;
    uint32 fdb_miss_action[3];  /* pkt_action[0]:unicast; pkt_action[1]:muticast;  pkt_action[2]:broadcast; */
    //uint8 default_tc;
    uint32 hostif_acl_grp_id;
    uint16 lport_link_status[CTC_SAI_LOCAL_PORT_NUM];
    sal_task_t *recv_task;
    sal_task_t *port_polling_task;
    sal_task_t *fiber_polling_task;
    sal_task_t *macled_polling_task;
    sal_task_t *platform_callback_task;
    int32 epoll_sock;
    struct epoll_event evl;
    uint16 default_wtd_thrd[3]; /*refer to sai_packet_color_t*/
    uint16 default_ecn_thrd[3]; /*refer to sai_packet_color_t*/
    uint32 tc_to_queue_map_id;
    ctc_sai_qos_domain_map_id_t  qos_domain_dot1p[QOS_MAP_DOMAIN_NUM_DOT1P];
    ctc_sai_qos_domain_map_id_t  qos_domain_dscp[QOS_MAP_DOMAIN_NUM_DSCP];
    ctc_sai_qos_domain_map_id_t  qos_domain_exp[QOS_MAP_DOMAIN_NUM_EXP];
    uint32 route_cnt[MAX_CTC_IP_VER];
    uint32 nexthop_cnt[MAX_CTC_IP_VER];
    uint32 neighbor_cnt[MAX_CTC_IP_VER];
    uint32 max_frame_idx_cnt[CTC_FRAME_SIZE_MAX];
    uint32 nat_cnt[CTC_SAI_NAT_TYPE_NUM];
    sai_switch_state_change_notification_fn     switch_state_change_cb;
    sai_switch_shutdown_request_notification_fn switch_shutdown_request_cb;
    sai_fdb_event_notification_fn               fdb_event_cb;
    sai_monitor_latency_notification_fn     monitor_latency_cb;
    sai_monitor_buffer_notification_fn     monitor_buffer_cb;
    sai_port_state_change_notification_fn       port_state_change_cb;
    sai_packet_event_notification_fn            packet_event_cb;
    sai_bfd_session_state_change_notification_fn        bfd_event_cb;
    sai_y1731_session_state_change_notification_fn      y1731_event_cb;
    sai_queue_pfc_deadlock_notification_fn              pfc_deadlock_cb;
    sai_signal_degrade_event_notification_fn            port_sd_cb;
    sai_packet_event_ptp_tx_notification_fn            ptp_packet_tx_event_cb;
    sai_object_id_t                             default_trap_grp_id;
    dal_pci_dev_t pci_dev;
    sai_mac_t vxlan_default_router_mac;
    uint8 pfc_dld_interval[8];
    uint32 monitor_buffer_total_thrd_min;
    uint32 monitor_buffer_total_thrd_max;
    uint32 monitor_latency_total_thrd_min;
    uint32 monitor_latency_total_thrd_max;
} ctc_sai_switch_master_t;

typedef sai_status_t (*ctc_sai_wb_sync_cb)(uint8 lchip, void* key, void* data);
typedef sai_status_t (*ctc_sai_wb_sync_cb1)(uint8 lchip);
typedef sai_status_t (*ctc_sai_wb_reload_cb)(uint8 lchip, void* key, void* data);
typedef sai_status_t (*ctc_sai_wb_reload_cb1)(uint8 lchip);
typedef struct ctc_sai_db_wb_s{
    ctc_sai_wb_sync_cb wb_sync_cb; /* for module obj,entry,vector */
    ctc_sai_wb_sync_cb1 wb_sync_cb1; /* for module global */
    ctc_sai_wb_reload_cb wb_reload_cb;/*for IDs*/
    ctc_sai_wb_reload_cb1 wb_reload_cb1;/*for pointer*/
    uint32 data_len;
    uint32 version;
} ctc_sai_db_wb_t;

typedef struct  ctc_sai_db_s
{
    sal_mutex_t*  p_mutex;
    ctc_hash_t*   oid_hash[SAI_OBJECT_TYPE_MAX];
    ctc_hash_t*   entry_hash[CTC_SAI_DB_ENTRY_TYPE_MAX];
    ctc_vector_t* vector[CTC_SAI_DB_VECTOR_TYPE_MAX];
    ctc_sai_db_wb_t wb_info[CTC_SAI_WB_TYPE_VECTOR - CTC_SAI_WB_TYPE_OID + 1][SAI_OBJECT_TYPE_MAX];
} ctc_sai_db_t;

typedef struct  ctc_sai_db_traverse_param_s
{
   uint8 lchip;
   void* value0;
   void* value1;
   void* value2;
   void* value3;
   void* value4;
}ctc_sai_db_traverse_param_t;

extern sai_status_t
ctc_sai_db_entry_unmapping_key(uint8 lchip, ctc_sai_db_entry_type_t type, ctc_sai_entry_property_t* entry_property, void* key);
extern bool
ctc_sai_db_check_object_property_exist(uint8 lchip, sai_object_id_t object_id);
extern bool
ctc_sai_db_check_object_exist(sai_object_id_t object_id);
extern sai_status_t
ctc_sai_db_get_db_entry_type(sai_object_type_t object_type, ctc_sai_db_entry_type_t* type);
extern void*
ctc_sai_db_get_object_property(uint8 lchip, sai_object_id_t object_id);
extern sai_status_t
ctc_sai_db_add_object_property(uint8 lchip, sai_object_id_t object_id, void* object_property);
extern sai_status_t
ctc_sai_db_remove_object_property(uint8 lchip, sai_object_id_t object_id);
extern sai_status_t
ctc_sai_db_traverse_object_property(uint8 lchip, sai_object_type_t object_type, hash_traversal_fn fn, void* data);
extern sai_status_t
ctc_sai_db_get_object_property_count(uint8 lchip, sai_object_type_t object_type, uint32* count);
extern void*
ctc_sai_db_entry_property_get_property(uint8 lchip, ctc_sai_db_entry_type_t type, void* key);
extern void*
ctc_sai_db_entry_property_get(uint8 lchip, ctc_sai_db_entry_type_t type, void* key);
extern sai_status_t
ctc_sai_db_entry_property_add(uint8 lchip, ctc_sai_db_entry_type_t type, void* key, void* property);
extern sai_status_t
ctc_sai_db_entry_property_remove(uint8 lchip, ctc_sai_db_entry_type_t type, void* key);
extern sai_status_t
ctc_sai_db_entry_property_traverse(uint8 lchip, ctc_sai_db_entry_type_t type, hash_traversal_fn fn, void* data);
extern void*
ctc_sai_db_vector_get(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index);
extern sai_status_t
ctc_sai_db_entry_property_get_cnt(uint8 lchip, ctc_sai_db_entry_type_t type, uint32* count);
extern sai_status_t
ctc_sai_db_vector_add(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index, void* data);
extern sai_status_t
ctc_sai_db_vector_remove(uint8 lchip, ctc_sai_db_vector_type_t type, uint32 index);
extern sai_status_t
ctc_sai_db_vector_traverse(uint8 lchip, ctc_sai_db_vector_type_t type, vector_traversal_fn fn, void* data);
extern sai_status_t
ctc_sai_db_lock(uint8 lchip);
extern sai_status_t
ctc_sai_db_unlock(uint8 lchip);
extern ctc_sai_switch_master_t*
ctc_sai_get_switch_property(uint8 lchip);
extern sai_status_t
ctc_sai_db_alloc_id(uint8 lchip, ctc_sai_db_id_type_t type, uint32 *id);
extern sai_status_t
ctc_sai_db_free_id(uint8 lchip, ctc_sai_db_id_type_t type, uint32 id);
extern sai_status_t
ctc_sai_db_opf_get_count(uint8 lchip, ctc_sai_db_id_type_t type, uint32* count);
extern sai_status_t
ctc_sai_db_alloc_id_from_position(uint8 lchip, ctc_sai_db_id_type_t type, uint32 id);
extern sai_status_t
ctc_sai_db_init(uint8 lchip);
extern sai_status_t
ctc_sai_db_deinit(uint8 lchip);

#endif /*_CTC_SAI_DB_H*/

