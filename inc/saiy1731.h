/**
 * Copyright (c) 2020 Microsoft Open Technologies, Inc.
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
 *    Microsoft would like to thank the following companies for their review and
 *    assistance with these files: Intel Corporation, Mellanox Technologies Ltd,
 *    Dell Products, L.P., Facebook, Inc., Marvell International Ltd.
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

    /** Y.1731 used as L2 Virtual Private Network encapsulation, based on AC port vlan */
    SAI_Y1731_MEG_TYPE_L2VPN_VLAN,

    /** Y.1731 used as L2 Virtual Private Network encapsulation, based on Virtual Switch Instance */
    SAI_Y1731_MEG_TYPE_L2VPN_VPLS,

    /** Y.1731 used as L2 Virtual Private Network encapsulation, based on Virtual Private Wire Service tunnel */
    SAI_Y1731_MEG_TYPE_L2VPN_VPWS,

    /** Y.1731 used as MPLS Transport based */
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
     * @condition SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS
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
 * @brief SAI attributes for Y.1731 Remote Maintenance End Point
 */
typedef enum _sai_y1731_remote_mep_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_Y1731_REMOTE_MEP_ATTR_START,

    /**
     * @brief Y1731 session id which Remote Maintenance End Point bind to
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_Y1731_SESSION
     */
    SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID = SAI_Y1731_REMOTE_MEP_ATTR_START,

    /**
     * @brief Y1731 remote Maintenance End Point id
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID,

    /**
     * @brief Y1731 remote Maintenance End Point MAC address
     * only use in SAI_Y1731_MEG_TYPE_ETHER_VLAN
     *
     * @type sai_mac_t
     * @flags CREATE_AND_SET
     * @default vendor
     */
    SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS,

    /**
     * @brief Y1731 remote Maintenance End Point is enabled
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default true
     */
    SAI_Y1731_REMOTE_MEP_ATTR_ENABLE,

    /**
     * @brief Y1731 receive the correct Continuity Check Message from remote Maintenance End Point
     * indicate the connection to remote Maintenance End Point has been established
     *
     * @type bool
     * @flags READ_ONLY
     */
    SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED,

    /**
     * @brief The HW protection next hop group id
     * only for SAI_NEXT_HOP_GROUP_TYPE_PROTECTION
     * used for hardware protection switch
     * set to SAI_NULL_OBJECT_ID to disable
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP_GROUP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,

    /**
     * @brief Indicate the path y1731 remote Maintenance End Point monitored is protecting path or working path
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,

    /**
     * @brief Indicate the y1731 remote Maintenance End Point session HW protection is enabled or not
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
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
    /** Y.1731 Down/Outward Maintenance End Point */
    SAI_Y1731_SESSION_DIRECTION_DOWNMEP = 0,

    /** Y.1731 Up/Inward Maintenance End Point */
    SAI_Y1731_SESSION_DIRECTION_UPMEP,

    /** Y.1731 Node Maintenance End Point */
    SAI_Y1731_SESSION_DIRECTION_NODEMEP

} sai_y1731_session_direction_t;

/**
 * @brief SAI session Continuity Check Message period of Y.1731
 */
typedef enum _sai_y1731_session_ccm_period_t
{
    /** Invalid Continuity Check Message interval */
    SAI_Y1731_SESSION_CCM_PERIOD_0 = 0,

    /** Continuity Check Message interval 3.3 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_1,

    /** Continuity Check Message interval 10 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_2,

    /** Continuity Check Message interval 100 ms */
    SAI_Y1731_SESSION_CCM_PERIOD_3,

    /** Continuity Check Message interval 1 s */
    SAI_Y1731_SESSION_CCM_PERIOD_4,

    /** Continuity Check Message interval 10 s */
    SAI_Y1731_SESSION_CCM_PERIOD_5,

    /** Continuity Check Message interval 1 min */
    SAI_Y1731_SESSION_CCM_PERIOD_6,

    /** Continuity Check Message interval 10 min */
    SAI_Y1731_SESSION_CCM_PERIOD_7

} sai_y1731_session_ccm_period_t;

/**
 * @brief SAI offload type of BFD session
 */
typedef enum _sai_y1731_session_perf_monitor_offload_type_t
{
    /** No Offload: No offload supported, all do in CPU */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_NONE = 0,

    /**
     * @brief Full Offload: Both transmit & receive supported in ASIC
     * Performance calculation supported in ASIC
     * Provide processed data to CPU
     */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_FULL,

    /**
     * @brief Partial Offload: necessary specific process supported offload in ASIC
     * like Loss Measurement stats counting, Delay Measurement timestamp edit
     */
    SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_PARTIAL,

} sai_y1731_session_perf_monitor_offload_type_t;

/**
 * @brief SAI session Loss Measurement type of Y.1731
 */
typedef enum _sai_y1731_session_lm_type_t
{
    /** Single ended Loss Measurement type */
    SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED = 0,

    /** Dual ended Loss Measurement type */
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
     * @objects SAI_OBJECT_TYPE_Y1731_MEG
     */
    SAI_Y1731_SESSION_ATTR_MEG = SAI_Y1731_SESSION_ATTR_START,

    /**
     * @brief Y1731 session direction type
     *
     * @type sai_int32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_SESSION_ATTR_DIR,

    /**
     * @brief Y1731 session vlan id
     *
     * valid when SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN, if set SAI_Y1731_SESSION_ATTR_VLAN_ID
     * to 0, indicate it is a Y.1731 Ether link OAM, and meg level should be set to 0
     *
     * condition SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPWS
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_SESSION_ATTR_VLAN_ID,

    /**
     * @brief Y1731 session bridge id for L2 Virtual Private Network
     *
     * condition SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPWS
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_BRIDGE
     */
    SAI_Y1731_SESSION_ATTR_BRIDGE_ID,

    /**
     * @brief Y1731 session Associated Port or LAG object id
     *
     * condition SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_ETHER_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VLAN or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPLS or SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_L2VPN_VPWS
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_Y1731_SESSION_ATTR_PORT_ID,

    /**
     * @brief Y1731 session MPLS label for Transport Y.1731
     *
     * validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL,

    /**
     * @brief Y1731 session local Maintenance End Point id
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
     * @default true
     */
    SAI_Y1731_SESSION_ATTR_ENABLE,

    /**
     * @brief Y1731 session Continuity Check Message period 3.3ms/10ms/100ms/1s/10s/1min/10min
     *
     * @type sai_y1731_session_ccm_period_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_Y1731_SESSION_ATTR_CCM_PERIOD,

    /**
     * @brief Y1731 session Continuity Check Message transmit enable
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default true
     */
    SAI_Y1731_SESSION_ATTR_CCM_ENABLE,

    /**
     * @brief Remote Maintenance End Point list
     *
     * @type sai_object_list_t
     * @flags READ_ONLY
     * @objects SAI_OBJECT_TYPE_Y1731_REMOTE_MEP
     */
    SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST,

    /**
     * @brief Y1731 session Loss Measurement stats offload type
     *
     * @type sai_int32_t
     * @flags CREATE_ONLY
     * @default 0
     */
    SAI_Y1731_SESSION_ATTR_LM_OFFLOAD_TYPE,

    /**
     * @brief Y1731 session Loss Measurement stats enable
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_LM_ENABLE,

    /**
     * @brief Y1731 session Loss Measurement stats type dual/single
     *
     * @type sai_y1731_session_lm_type_t
     * @flags CREATE_AND_SET
     * @default SAI_Y1731_SESSION_LM_TYPE_SINGLE_ENDED
     */
    SAI_Y1731_SESSION_ATTR_LM_TYPE,

    /**
     * @brief Y1731 session Delay Measurement offload type
     *
     * @type sai_int32_t
     * @flags CREATE_ONLY
     * @default 0
     */
    SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE,

    /**
     * @brief Y1731 session Delay Measurement enable
     * enable delay measurement on Maintenance End Point
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_DM_ENABLE,

    /**
     * @brief Y1731 session local Remote Defect Indicator set
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_LOCAL_RDI,

    /**
     * @brief Transport Y1731 section OAM router interface id
     * validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     *
     * @type sai_object_id_t
     * @flags CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_ROUTER_INTERFACE
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,

    /**
     * @brief Transport Y.1731 without gal, by default, for Label Switched Path with gal, for Pseudo wire without gal
     * validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default false
     */
    SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL,

    /**
     * @brief Transmit Transport Y.1731 MPLS label TTL
     * validonly SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_Y1731_SESSION_ATTR_TTL,

    /**
     * @brief Transmit Transport Y.1731 MPLS label exp or Vlan Cos
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_Y1731_SESSION_ATTR_EXP_OR_COS,

    /**
     * @brief The next hop id
     * valid when SAI_Y1731_MEG_ATTR_TYPE == SAI_Y1731_MEG_TYPE_MPLS_TP
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
 * @brief Y1731 Session Loss Measurement stats IDs in sai_get_y1731_session_stats_fn() call
 * Used in Dual-ended Loss Measurement with Continuity Check Message
 */
typedef enum _sai_y1731_session_stat_t
{
    /** Counter in last received Continuity Check Message */
    SAI_Y1731_SESSION_STAT_TX_FCF,

    /** Counter in last received Continuity Check Message */
    SAI_Y1731_SESSION_STAT_RX_FCB,

    /** Counter in last received Continuity Check Message */
    SAI_Y1731_SESSION_STAT_TX_FCB,

    /** Counter for in-profile data frames received from the peer Maintenance End Point in local stats when receive last Continuity Check Message */
    SAI_Y1731_SESSION_STAT_RX_FCL

} sai_y1731_session_stat_t;

/**
 * @brief SAI notification event type of Y1731 session
 */
typedef enum _sai_y1731_session_notify_event_type_t
{
    /** Y1731 event Maintenance Entity Group mismatch Continuity Check Message defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_MISMERGE = 0,

    /** Y1731 event level cross connect Continuity Check Message defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_LEVEL,

    /** Y1731 event Unexpected Maintenance End Point defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_MEP,

    /** Y1731 event Unexpected period defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_PERIOD,

    /** Y1731 event Loss of Continuity defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_UNEXPECTED_DLOC,

    /** Y1731 event Remote Maintenance End Point MAC not match defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_SRC_MAC_MISMATCH,

    /** Y1731 event Remote Defect Indicator rx defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_RX,

    /** Y1731 event Remote Defect Indicator tx defect */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_RDI_TX,

    /** Y1731 event connection established */
    SAI_Y1731_SESSION_NOTIFY_EVENT_TYPE_CONNECTION_ESTABLISHED,

} sai_y1731_session_notify_event_type_t;

/**
 * @brief Defines the operational status of the Y1731 session
 */
typedef struct _sai_y1731_session_event_notification_t
{
    /**
     * @brief Y.1731 Session object id or Remote Maintenance End Point object id
     * event could occur on Y.1731 session Local Maintenance End Point or Remote Maintenance End Point
     *
     * @objects SAI_OBJECT_TYPE_Y1731_SESSION, SAI_OBJECT_TYPE_Y1731_REMOTE_MEP
     */
    sai_object_id_t y1731_oid;

    /** Y1731 session event list sai_y1731_session_notify_event_type_t */
    sai_s32_list_t session_event_list;

} sai_y1731_session_event_notification_t;

/**
 * @brief Create Y.1731 MEG.
 *
 * @param[out] y1731_meg_id Y1731 MEG id
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
 * @param[in] y1731_meg_id Y1731 MEG id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_meg_fn)(
        _In_ sai_object_id_t y1731_meg_id);

/**
 * @brief Set Y.1731 MEG attributes.
 *
 * @param[in] y1731_meg_id Y1731 MEG id
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
 * @param[in] y1731_meg_id Y1731 MEG id
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
 * @param[out] y1731_session_id Y1731 session id
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
 * @param[in] y1731_session_id Y1731 session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_session_fn)(
        _In_ sai_object_id_t y1731_session_id);

/**
 * @brief Set Y.1731 session attributes.
 *
 * @param[in] y1731_session_id Y1731 session id
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
 * @param[in] y1731_session_id Y1731 session id
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
 * @brief Create Y.1731 remote Maintenance End Point.
 *
 * @param[out] y1731_remote_mep_id Y1731 remote Maintenance End Point object id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_y1731_remote_mep_fn)(
        _Out_ sai_object_id_t *y1731_remote_mep_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove Y.1731 remote Maintenance End Point.
 *
 * @param[in] y1731_remote_mep_id Y1731 remote Maintenance End Point object id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_y1731_remote_mep_fn)(
        _In_ sai_object_id_t y1731_remote_mep_id);

/**
 * @brief Set Y.1731 remote Maintenance End Point attributes.
 *
 * @param[in] y1731_remote_mep_id Y1731 remote Maintenance End Point object id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_y1731_remote_mep_attribute_fn)(
        _In_ sai_object_id_t y1731_remote_mep_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Y.1731 session attributes.
 *
 * @param[in] y1731_remote_mep_id Y1731 remote Maintenance End Point object id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_y1731_remote_mep_attribute_fn)(
        _In_ sai_object_id_t y1731_remote_mep_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief Get Y.1731 session statistics lm_stats. Deprecated for backward compatibility.
 *
 * @param[in] y1731_session_id Y1731 session id
 * @param[in] number_of_counters Number of lm_stats in the array
 * @param[in] counter_ids Specifies the array of Loss Measurement stats ids
 * @param[out] counters Array of resulting Loss Measurement stats values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_y1731_session_stats_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters);

/**
 * @brief Get Y.1731 session statistics counters extended.
 *
 * @param[in] y1731_session_id Y1731 session id
 * @param[in] number_of_counters Number of lm_stats in the array
 * @param[in] counter_ids Specifies the array of Loss Measurement stats ids
 * @param[in] mode Statistics mode
 * @param[out] counters Array of resulting Loss Measurement stats values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_y1731_session_stats_ext_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters);

/**
 * @brief Clear Y.1731 session statistics counters.
 *
 * @param[in] y1731_session_id Y1731 session id
 * @param[in] number_of_counters Number of lm_stats in the array
 * @param[in] counter_ids Specifies the array of Loss Measurement stats ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_clear_y1731_session_stats_fn)(
        _In_ sai_object_id_t y1731_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids);

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

    sai_get_y1731_session_stats_fn         get_y1731_session_stats;
    sai_get_y1731_session_stats_ext_fn     get_y1731_session_stats_ext;
    sai_clear_y1731_session_stats_fn       clear_y1731_session_stats;

} sai_y1731_api_t;

/**
 * @}
 */
#endif /** __SAIY1731_H_ */
