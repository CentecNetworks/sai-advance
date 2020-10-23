/**
 * Copyright (c) 2020 CentecNetworks, Inc.
 *
 *    Licensed under the Apache License, Version 2.0 (the "License"); you may
 *    not use this file except in compliance with the License. You may obtain
 *    a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 *    THIS CODE IS PROVIDED ON AN *AS IS* BASIS, WITHOUT WARRANTIES OR
 *    CONDITIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT
 *    LIMITATION ANY IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS
 *    FOR A PARTICULAR PURPOSE, MERCHANTABILITY OR NON-INFRINGEMENT.
 *
 *    See the Apache Version 2.0 License for specific language governing
 *    permissions and limitations under the License.
 *
 *
 * @file    saiy1731.h
 *
 * @brief   This module defines SAI Y.1731 interface
 */

#if !defined (__SAIY1731_H_)
#define __SAIY1731_H_

#include <saitypes.h>

#define SAI_Y1731_MEG_NAME_SIZE 16
/**
 * @defgroup SAIY1731 SAI - Y.1731 specific public APIs and data structures
 *
 * @{
 */


/**
 * @brief SAI session type of Y.1731
 */
typedef enum _sai_y1731_meg_type_t
{
    /** Y.1731 used as Ether encapsulation */
    SAI_Y1731_MEG_TYPE_ETHER_VLAN = 0,

    /** Y.1731 used as L2VPN encapsulation, based on AC port vlan */
    SAI_Y1731_MEG_TYPE_L2VPN_VLAN,
    
    /** Y.1731 used as L2VPN encapsulation, based on VSI */
    SAI_Y1731_MEG_TYPE_L2VPN_VPLS,

    /** Y.1731 used as L2VPN encapsulation, based on VPWS tunnel */
    SAI_Y1731_MEG_TYPE_L2VPN_VPWS,

    /** Y.1731 used as MPLS-TP based */
    SAI_Y1731_MEG_TYPE_MPLS_TP,

} sai_y1731_meg_type_t;

/**
 * @brief SAI attributes for Y.1731 MEG
 */
typedef enum _sai_y1731_meg_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_Y1731_MEG_ATTR_START,

    /**
     * @brief Y1731 MEG type
     *
     * @type sai_y1731_meg_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_MEG_ATTR_TYPE = SAI_Y1731_MEG_ATTR_START,
    
    /**
     * @brief Y1731 MEG Name char[SAI_Y1731_MEG_NAME_SIZE]
     *
     * @type char
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_MEG_ATTR_NAME,
    
    /**
     * @brief Y1731 MEG Level
     *
     * @type sai_uint8_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or 
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS
     */
    SAI_Y1731_MEG_ATTR_LEVEL,
    
    /**
     * @brief End of attributes
     */
    SAI_Y1731_MEG_ATTR_END,

    /** Custom range base value */
    SAI_Y1731_MEG_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_Y1731_MEG_ATTR_CUSTOM_RANGE_END
    
} sai_y1731_meg_attr_t;


/**
 * @brief SAI attributes for Y.1731 Remote Mep
 */
typedef enum _sai_y1731_remote_mep_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_Y1731_REMOTE_MEP_ATTR_START,

    /**
     * @brief Y1731 session id which Remote MEP bind to
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID = SAI_Y1731_REMOTE_MEP_ATTR_START,
    
    /**
     * @brief Y1731 remote mep id
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID,
    
    /**
     * @brief Y1731 remote mep mac address
     * @only use in SAI_Y1731_MEG_TYPE_ETHER_VLAN
     *
     * @type sai_mac_t
     * @flags CREATE_AND_SET
     */
    SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS,

    /**
     * @brief Y1731 remote mep is enabled
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default TRUE
     */
    SAI_Y1731_REMOTE_MEP_ATTR_ENABLE,

    /**
     * @brief Y1731 receive the correct ccm from remote mep
     * @indicate the connection to remote mep has been established
     *
     * @type bool
     * @flags READ_ONLY
     */
    SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED,

    /**
     * @brief The hw protection next hop group id
     *  set to SAI_OBJECT_TYPE_NEXT_HOP_GROUP, only for SAI_NEXT_HOP_GROUP_TYPE_PROTECTION
     *  used for hardware protection switch
     *  set to SAI_NULL_OBJECT_ID to disable hw protection
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP_GROUP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,

    /**
     * @brief indicate the path y1731 rmep monitored is protecting path or working path
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @validonly SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID != SAI_NULL_OBJECT_ID
     * @default 0
     */
    SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,

    /**
     * @brief indicate the y1731 rmep session hw protection is enabled or not
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @validonly SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID != SAI_NULL_OBJECT_ID
     * @default 0
     */
    SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN,
    
    /**
     * @brief End of attributes
     */
    SAI_Y1731_REMOTE_MEP_ATTR_END,

    /** Custom range base value */
    SAI_Y1731_REMOTE_MEP_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_Y1731_REMOTE_MEP_ATTR_CUSTOM_RANGE_END
    
} sai_y1731_remote_mep_attr_t;

/**
 * @brief SAI session direction of Y.1731
 */
typedef enum _sai_y1731_session_direction_t
{
    /** Y.1731 Down/Outward Mep */
    SAI_Y1731_SESSION_DIR_DOWNMEP = 0,

    /** Y.1731 Up/Inward Mep */
    SAI_Y1731_SESSION_DIR_UPMEP,

    /** Y.1731 Node mep */
    SAI_Y1731_SESSION_DIR_NODEMEP

} sai_y1731_session_direction_t;

/**
 * @brief SAI session ccm period of Y.1731
 */
typedef enum _sai_y1731_session_ccm_period_t
{
    /** Invalid Ccm interval*/
    SAI_Y1731_SESSION_CCM_PERIOD_0 = 0,
    
    /** Ccm interval 3.3 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_1,

    /** Ccm interval 10 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_2,
    
    /** Ccm interval 100 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_3,
    
    /** Ccm interval 1 s */
    SAI_Y1731_SESSION_CCM_PERIOD_4,
    
    /** Ccm interval 10 s */
    SAI_Y1731_SESSION_CCM_PERIOD_5,
    
    /** Ccm interval 1 min */
    SAI_Y1731_SESSION_CCM_PERIOD_6,
    
    /** Ccm interval 10 min */
    SAI_Y1731_SESSION_CCM_PERIOD_7

} sai_y1731_session_ccm_period_t;

/**
 * @brief SAI offload type of BFD session
 */
typedef enum _sai_y1731_session_performance_monitor_offload_type_t
{

    /** No Offload: No offload supported, all do in CPU */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE = 0,

    /** Full Offload: Both transmit & receive supported in ASIC
    *   Performance caculation supported in ASIC
    *   Provide processed data to CPU
    */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL,

    /** Partial Offload: necessary specific process supported offload in ASIC
    *   like LM stats counting, dm timestamp edit
    */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_PARTIAL,

} sai_y1731_session_performance_monitor_offload_type_t;

/**
 * @brief SAI session lm type of Y.1731
 */
typedef enum _sai_y1731_session_lm_type_t
{
    /** Single ended LM type */
    SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED = 0,
    
    /** Dual ended LM type */
    SAI_Y1731_SESSION_LM_TYPE_DUAL_ENDED
    
} sai_y1731_session_lm_type_t;

/**
 * @brief SAI attributes for Y.1731 session
 */
typedef enum _sai_y1731_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_Y1731_SESSION_ATTR_START,

    /**
     * @brief Y1731 session MEG OID
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_SESSION_ATTR_MEG = SAI_Y1731_SESSION_ATTR_START,
    
    /**
     * @brief Y1731 session direction type
     *
     * @type sai_y1731_session_direction_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_SESSION_ATTR_DIR,
    
    /**
     * @brief Y1731 session vlan id
     * 
     * when SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN, if set SAI_Y1731_SESSION_ATTR_VLAN_ID
     * to 0, indicate it is a Y.1731 Ether linkOam, and meg level should be set to 0
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or 
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS or
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPWS
     */
    SAI_Y1731_SESSION_ATTR_VLAN_ID,
    
    /**
     * @brief Y1731 session bridge id for L2VPN
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS 
     */
    SAI_Y1731_SESSION_ATTR_BRIDGE_ID,
    
    /**
     * @brief Y1731 session Associated Port or LAG object id
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or 
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or
     *      SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS
     */
    SAI_Y1731_SESSION_ATTR_PORT_ID,
    
    /**
     * @brief Y1731 session mpls label for TP Y.1731
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP 
     */
    SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL,
    
    /**
     * @brief Y1731 session local mep id
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID,

    /**
     * @brief Y1731 session is enabled
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default TRUE
     */
    SAI_Y1731_SESSION_ATTR_ENABLE,
    
    /**
     * @brief Y1731 session ccm period 3.3ms/10ms/100ms/1s/10s/1min/10min
     *
     * @type sai_y1731_session_ccm_period_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_Y1731_SESSION_ATTR_CCM_PERIOD,
    
    /**
     * @brief Y1731 session ccm transmit enable
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default true
     */
    SAI_Y1731_SESSION_ATTR_CCM_ENABLE,    
    
    /**
     * @brief Remote MEP list
     *
     * @type sai_object_list_t
     * @flags READ_ONLY
     * @objects SAI_OBJECT_TYPE_Y1731_REMOTE_MEP
     */
    SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST,

    /**
     * @brief Y1731 session LM stats offload type
     *
     * @type sai_y1731_session_performance_monitor_offload_type_t
     * @flags CREATE_ONLY
     * @default SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE
     */
    SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE,    
    
    /**
     * @brief Y1731 session LM stats enable
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_LM_ENABLE,
    
    /**
     * @brief Y1731 session LM stats type dual/single
     *
     * @type sai_y1731_session_lm_type_t
     * @flags CREATE_AND_SET
     * @default SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED
     */
    SAI_Y1731_SESSION_ATTR_LM_TYPE,

    /**
     * @brief Y1731 session DM offload type
     *
     * @type sai_y1731_session_performance_monitor_offload_type_t
     * @flags CREATE_ONLY
     * @default SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE
     */
    SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE,
    
    /**
     * @brief Y1731 session DM enable
     * @enable delay measurement on mep
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_DM_ENABLE,
    
    /**
     * @brief Y1731 session local RDI set
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_LOCAL_RDI,
    
    /**
     * @brief TP Y1731 section OAM router interface id
     *
     * @type sai_object_id_t
     * @flags CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_ROUTER_INTERFACE
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     * @default NULL_OBJECT
     */
    SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,
    
    /**
     * @brief TP Y.1731 without gal, by default, TP Y.1731 for lsp with gal, TP Y.1731 for pw without gal
     *
     * @type bool
     * @flags CREATE_ONLY
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP     
     *  
     */
    SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL,
    
    /**
     * @brief transmit TP Y.1731 MPLS label ttl
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     * @default 0, use Nexthop MPLS encapsulation ttl
     */
    SAI_Y1731_SESSION_ATTR_TTL,
    
    /**
     * @brief transmit TP Y.1731 MPLS label exp or Vlan Cos
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0, use Nexthop MPLS encapsulation exp
     */
    SAI_Y1731_SESSION_ATTR_EXP_OR_COS,
    
    /**
     * @brief The next hop id
     * @used when SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP, SAI_OBJECT_TYPE_NEXT_HOP_GROUP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID,   
    
    /**
     * @brief End of attributes
     */
    SAI_Y1731_SESSION_ATTR_END,

    /** Custom range base value */
    SAI_Y1731_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_Y1731_SESSION_ATTR_CUSTOM_RANGE_END
    
} sai_y1731_session_attr_t;

/**
 * @brief Y1731 Session LM stats IDs in sai_get_y1731_session_lm_stats_fn() call
 * @Used in Dual-ended LM with CCM
 */
typedef enum _sai_y1731_lm_stat_id_t
{
    /** TxFcf in last received CCM */
    SAI_Y1731_SESSION_LM_STAT_TX_FCF,

    /** RxFcb in last received CCM */
    SAI_Y1731_SESSION_LM_STAT_RX_FCB,

    /** TxFcb in last received CCM */
    SAI_Y1731_SESSION_LM_STAT_TX_FCB,
    
    /** RxFcl in local stats when receive last CCM */
    SAI_Y1731_SESSION_LM_STAT_RX_FCL

} sai_lm_stat_id_t;


/**
 * @brief SAI notification event type of Y1731 session
 */
typedef enum _sai_y1731_session_notify_event_type_t
{

    /** Y1731 event mismerge ccm defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_MISMERGE = 0,
    
    /** Y1731 event level cross connect ccm defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_LEVEL,
    
    /** Y1731 event Unexpected MEP defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_MEP,
    
    /** Y1731 event Unexpected period defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_PERIOD,
    
    /** Y1731 event LOC defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_DLOC,
    
    /** Y1731 event Remote mep mac not match defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_SRC_MAC_MISMATCH,
    
    /** Y1731 event RDI rx defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_RX,
    
    /** Y1731 event RDI tx defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_TX,

    /** Y1731 event connection established */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_CONNECTION_ESTABLISHED,

} sai_y1731_session_notify_event_type_t;

/**
 * @brief Defines the operational status of the Y1731 session
 */
typedef struct _sai_y1731_session_event_notification_t
{
    /** Y.1731 Session oid or Remote mep oid 
    * event could occur on Y.1731 session Local Mep or Remote Mep
    * object could be SAI_OBJECT_TYPE_Y1731_SESSION or SAI_OBJECT_TYPE_Y1731_REMOTE_MEP
    */
    sai_object_id_t y1731_oid;

    /** Y1731 session event list sai_y1731_session_notify_event_type_t */
    sai_s32_list_t session_event_list;

} sai_y1731_session_event_notification_t;


/**
 * @brief Create Y.1731 MEG.
 *
 * @param[out] y1731_meg_id Y.1731 MEG id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_y1731_meg_fn)(
        _Out_ sai_object_id_t *y1731_meg_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove Y.1731 MEG.
 *
 * @param[in] y1731_meg_id Y.1731 MEG id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_meg_fn)(
        _In_ sai_object_id_t y1731_meg_id);

/**
 * @brief Set Y.1731 MEG attributes.
 *
 * @param[in] y1731_meg_id Y.1731 MEG id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_y1731_meg_attribute_fn)(
        _In_ sai_object_id_t y1731_meg_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Y.1731 MEG attributes.
 *
 * @param[in] y1731_meg_id Y.1731 MEG id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_y1731_meg_attribute_fn)(
        _In_ sai_object_id_t y1731_meg_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);
        
/**
 * @brief Create Y.1731 session.
 *
 * @param[out] y1731_session_id Y.1731 session id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_y1731_session_fn)(
        _Out_ sai_object_id_t *y1731_session_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove Y.1731 session.
 *
 * @param[in] y1731_session_id Y.1731 session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_session_fn)(
        _In_ sai_object_id_t y1731_session_id);

/**
 * @brief Set Y.1731 session attributes.
 *
 * @param[in] y1731_session_id Y.1731 session id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_y1731_session_attribute_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Y.1731 session attributes.
 *
 * @param[in] y1731_session_id Y.1731 session id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_y1731_session_attribute_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief Create Y.1731 remote mep.
 *
 * @param[out] y1731_rmep_id Y.1731 remote mep oid
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_y1731_remote_mep_fn)(
        _Out_ sai_object_id_t *y1731_rmep_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove Y.1731 remote mep.
 *
 * @param[in] y1731_rmep_id Y.1731 remote mep oid
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_remote_mep_fn)(
        _In_ sai_object_id_t y1731_rmep_id);

/**
 * @brief Set Y.1731 remote mep attributes.
 *
 * @param[in] y1731_rmep_id Y.1731 remote mep oid
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_y1731_remote_mep_attribute_fn)(
        _In_ sai_object_id_t y1731_rmep_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Y.1731 session attributes.
 *
 * @param[in] y1731_rmep_id Y.1731 remote mep oid
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_y1731_remote_mep_attribute_fn)(
        _In_ sai_object_id_t y1731_rmep_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);


/**
 * @brief Get Y.1731 session statistics lm_stats. Deprecated for backward compatibility.
 *
 * @param[in] y1731_session_id Y.1731 session id
 * @param[in] number_of_stats Number of lm_stats in the array
 * @param[in] lm_stats_ids Specifies the array of lm stats ids
 * @param[out] lm_stats Array of resulting lm stats values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_y1731_session_lm_stats_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ uint32_t number_of_stats,
        _In_ const sai_stat_id_t *lm_stats_ids,
        _Out_ uint64_t *lm_stats);


/**
 * @brief Y.1731 session state change notification
 *
 * Passed as a parameter into sai_initialize_switch()
 *
 * @count data[count]
 *
 * @param[in] count Number of notifications
 * @param[in] data Array of Y.1731 session event
 */
typedef void (*sai_y1731_session_state_change_notification_fn)(
        _In_ uint32_t count,
        _In_ const sai_y1731_session_event_notification_t *data);

/**
 * @brief Y.1731 method table retrieved with sai_api_query()
 */
typedef struct _sai_y1731_api_t
{
    sai_create_y1731_meg_fn                create_y1731_meg;
    sai_remove_y1731_meg_fn                remove_y1731_meg;
    sai_set_y1731_meg_attribute_fn         set_y1731_meg_attribute;
    sai_get_y1731_meg_attribute_fn         get_y1731_meg_attribute;
    
    sai_create_y1731_session_fn            create_y1731_session;
    sai_remove_y1731_session_fn            remove_y1731_session;
    sai_set_y1731_session_attribute_fn     set_y1731_session_attribute;
    sai_get_y1731_session_attribute_fn     get_y1731_session_attribute;

    sai_create_y1731_remote_mep_fn         create_y1731_remote_mep;
    sai_remove_y1731_remote_mep_fn         remove_y1731_remote_mep;
    sai_set_y1731_remote_mep_attribute_fn  set_y1731_remote_mep_attribute;
    sai_get_y1731_remote_mep_attribute_fn  get_y1731_remote_mep_attribute;
    
    sai_get_y1731_session_lm_stats_fn        get_y1731_session_lm_stats;

} sai_y1731_api_t;

/**
 * @}
 */
#endif /** __SAIY1731_H_ */
