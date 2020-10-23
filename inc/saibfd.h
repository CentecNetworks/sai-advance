/**
 * Copyright (c) 2014 Microsoft Open Technologies, Inc.
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
 * @file    saibfd.h
 *
 * @brief   This module defines SAI BFD interface
 */

#if !defined (__SAIBFD_H_)
#define __SAIBFD_H_

#include <saitypes.h>

#define SAI_BFD_CV_SIZE 32
/**
 * @defgroup SAIBFD SAI - BFD specific public APIs and data structures
 *
 * @{
 */

/**
 * @brief SAI session type of BFD
 */
typedef enum _sai_bfd_session_type_t
{
    /** Demand Active Mode */
    SAI_BFD_SESSION_TYPE_DEMAND_ACTIVE = 0,

    /** Demand Passive Mode */
    SAI_BFD_SESSION_TYPE_DEMAND_PASSIVE,

    /** Asynchronous Active Mode */
    SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE,

    /** Asynchronous Passive Mode */
    SAI_BFD_SESSION_TYPE_ASYNC_PASSIVE,

} sai_bfd_session_type_t;

/**
 * @brief SAI offload type of BFD session
 */
typedef enum _sai_bfd_session_offload_type_t
{
    /** No Offload: No offload supported */
    SAI_BFD_SESSION_OFFLOAD_TYPE_NONE = 0,

    /** Full Offload: both session establishment and sustenance */
    SAI_BFD_SESSION_OFFLOAD_TYPE_FULL,

    /** Sustenance Offload: Session Sustenance only. */
    SAI_BFD_SESSION_OFFLOAD_TYPE_SUSTENANCE,

} sai_bfd_session_offload_type_t;

/**
 * @brief SAI type of encapsulation for BFD
 */
typedef enum _sai_bfd_encapsulation_type_t
{
    /**
     * @brief IP in IP Encapsulation | L2 Ethernet header | IP header | Inner IP header | Original BFD packet
     */
    SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP,

    /**
     * @brief L3 GRE Tunnel Encapsulation | L2 Ethernet header | IP header | GRE header | Original BFD packet
     */
    SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL,

    /**
     * @brief MPLS Encapsulation | L2 Ethernet header | MPLS header (| ACH header) (| IP header | UDP header) | Original BFD packet
     */
    SAI_BFD_ENCAPSULATION_TYPE_MPLS,

    /**
     * @brief No Encapsulation
     */
    SAI_BFD_ENCAPSULATION_TYPE_NONE,

} sai_bfd_encapsulation_type_t;
    
/**
 * @brief SAI type of MPLS encapsulated BFD
 */
typedef enum _sai_bfd_mpls_type_t
{
    /** Normal mpls BFD, include LSP/PW */
    SAI_BFD_MPLS_TYPE_NORMAL,
    
    /** MPLS TP BFD */
    SAI_BFD_MPLS_TYPE_TP,
    
} sai_bfd_mpls_type_t;

/**
 * @brief SAI BFD session state
 */
typedef enum _sai_bfd_session_state_t
{
    /** BFD Session is in Admin down */
    SAI_BFD_SESSION_STATE_ADMIN_DOWN,

    /** BFD Session is Down */
    SAI_BFD_SESSION_STATE_DOWN,

    /** BFD Session is in Initialization */
    SAI_BFD_SESSION_STATE_INIT,

    /** BFD Session is Up */
    SAI_BFD_SESSION_STATE_UP,

} sai_bfd_session_state_t;

/**
 * @brief Defines the operational status of the BFD session
 */
typedef struct _sai_bfd_session_state_notification_t
{
    /**
     * @brief BFD Session id
     *
     * @objects SAI_OBJECT_TYPE_BFD_SESSION
     */
    sai_object_id_t bfd_session_id;

    /** BFD session state */
    sai_bfd_session_state_t session_state;

} sai_bfd_session_state_notification_t;

/**
 * @brief Defines the ACH channel type of BFD encapsulation
 */
typedef enum _sai_bfd_ach_channel_type_t
{
    /** BFD ACH channel type without IP/UDP achType = 0x0007 */
    SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW,

    /** BFD ACH channel type with IPv4/UDP achType = 0x0021 */
    SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4,

    /** BFD ACH channel type with IPv6/UDP achType = 0x0057 */
    SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6,
    
    /** BFD ACH channel type TP CC achType = 0x0022, CV achType = 0x0023 */
    SAI_BFD_ACH_CHANNEL_TYPE_TP,    

} sai_bfd_ach_channel_type_t;

/**
 * @brief SAI attributes for BFD session
 */
typedef enum _sai_bfd_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_BFD_SESSION_ATTR_START,

    /**
     * @brief BFD Session type DEMAND/ASYNCHRONOUS
     *
     * @type sai_bfd_session_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_TYPE = SAI_BFD_SESSION_ATTR_START,

    /**
     * @brief Hardware lookup valid
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default true
     */
    SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID,

    /**
     * @brief Virtual Router
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_VIRTUAL_ROUTER
     * @condition SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID == true
     */
    SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER,

    /**
     * @brief Destination Port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     * @condition SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID == false
     */
    SAI_BFD_SESSION_ATTR_PORT,

    /**
     * @brief Local discriminator
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,

    /**
     * @brief Remote discriminator
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,

    /**
     * @brief UDP Source port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,

    /**
     * @brief Class-of-Service (Traffic Class)
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_BFD_SESSION_ATTR_TC,

    /**
     * @brief L2 header TPID.
     *
     * @type sai_uint16_t
     * @flags CREATE_AND_SET
     * @isvlan false
     * @default 0x8100
     * @validonly SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID == true
     */
    SAI_BFD_SESSION_ATTR_VLAN_TPID,

    /**
     * @brief L2 header VLAN Id.
     *
     * @type sai_uint16_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @isvlan true
     * @condition SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID == true
     */
    SAI_BFD_SESSION_ATTR_VLAN_ID,

    /**
     * @brief L2 header packet priority (3 bits).
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     * @validonly SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID == true
     */
    SAI_BFD_SESSION_ATTR_VLAN_PRI,

    /**
     * @brief L2 header Vlan CFI (1 bit).
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     * @validonly SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID == true
     */
    SAI_BFD_SESSION_ATTR_VLAN_CFI,

    /**
     * @brief Vlan header valid
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default false
     */
    SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID,

    /**
     * @brief Encapsulation type
     *
     * @type sai_bfd_encapsulation_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,

    /**
     * @brief IP header version
     *
     * @type sai_uint8_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_BFD_SESSION_ATTR_IPHDR_VERSION,

    /**
     * @brief IP header TOS
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_BFD_SESSION_ATTR_TOS,

    /**
     * @brief IP header TTL
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 255
     */
    SAI_BFD_SESSION_ATTR_TTL,

    /**
     * @brief Source IP
     *
     * @type sai_ip_address_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,

    /**
     * @brief Destination IP
     *
     * @type sai_ip_address_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,

    /**
     * @brief Tunnel IP header TOS
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP
     */
    SAI_BFD_SESSION_ATTR_TUNNEL_TOS,

    /**
     * @brief Tunnel IP header TTL
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 255
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP
     */
    SAI_BFD_SESSION_ATTR_TUNNEL_TTL,

    /**
     * @brief Tunnel source IP
     *
     * @type sai_ip_address_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP
     */
    SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS,

    /**
     * @brief Tunnel destination IP
     *
     * @type sai_ip_address_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP
     */
    SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS,

    /**
     * @brief L2 source MAC address
     *
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @condition SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID == false
     */
    SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS,

    /**
     * @brief L2 destination MAC address
     *
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @condition SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID == false
     */
    SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS,

    /**
     * @brief To enable echo function on BFD session
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_BFD_SESSION_ATTR_ECHO_ENABLE,

    /**
     * @brief Multi hop BFD session
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default false
     */
    SAI_BFD_SESSION_ATTR_MULTIHOP,

    /**
     * @brief Control Plane Independent
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default false
     */
    SAI_BFD_SESSION_ATTR_CBIT,

    /**
     * @brief Minimum Transmit interval in microseconds
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_BFD_SESSION_ATTR_MIN_TX,

    /**
     * @brief Minimum Receive interval in microseconds
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_BFD_SESSION_ATTR_MIN_RX,

    /**
     * @brief Detect time Multiplier
     *
     * @type sai_uint8_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_BFD_SESSION_ATTR_MULTIPLIER,

    /**
     * @brief Minimum Remote Transmit interval in microseconds
     *
     * @type sai_uint32_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX,

    /**
     * @brief Minimum Remote Receive interval in microseconds
     *
     * @type sai_uint32_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX,

    /**
     * @brief BFD Session state
     * could be set to admin down
     *
     * @type sai_bfd_session_state_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_STATE,

    /**
     * @brief Offload type
     *
     * @type sai_bfd_session_offload_type_t
     * @flags CREATE_ONLY
     * @default SAI_BFD_SESSION_OFFLOAD_TYPE_NONE
     */
    SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE,

    /**
     * @brief Negotiated Transmit interval in microseconds
     *
     * @type sai_uint32_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_NEGOTIATED_TX,

    /**
     * @brief Negotiated Receive interval in microseconds
     *
     * @type sai_uint32_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_NEGOTIATED_RX,

    /**
     * @brief Local Diagnostic code field as specified by RFC
     *
     * @type sai_uint8_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_LOCAL_DIAG,

    /**
     * @brief Remote Diagnostic code field
     *
     * @type sai_uint8_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_DIAG,

    /**
     * @brief Remote time Multiplier
     *
     * @type sai_uint8_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER,
    
    /**
     * @brief End of attributes
     */
    SAI_BFD_SESSION_ATTR_END,

    /** Custom range base value */
    SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /**
     * @brief BFD Session remote state
     *
     * @type sai_bfd_session_state_t
     * @flags READ_ONLY
     */
    SAI_BFD_SESSION_ATTR_REMOTE_STATE = SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_START,
    
    /**
     * @brief MPLS encapsulated BFD type
     *
     * @type sai_bfd_mpls_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     */
    SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE,
    
    /**
     * @brief BFD ACH valid
     *
     * @type bool
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     */
    SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID,
    
    /**
     * @brief BFD ACH channel type
     *
     * @type sai_bfd_ach_channel_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS && SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID == true
     */
    SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE,
    
    /**
     * @brief MPLS label bind to BFD session
     * @type sai_label_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     */
    SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL,
    
    /**
     * @brief transmit MPLS label ttl
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     */
    SAI_BFD_SESSION_ATTR_MPLS_TTL,
    
    /**
     * @brief transmit MPLS label exp
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     */
    SAI_BFD_SESSION_ATTR_MPLS_EXP,
    
    /**
     * @brief TP BFD CV enable
     * @type bool
     * @flags CREATE_AND_SET
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
        && SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE == SAI_BFD_MPLS_TYPE_TP
     */
    SAI_BFD_SESSION_ATTR_TP_CV_ENABLE,
    
    /**
     * @brief TP BFD CV Source MEP-ID char[SAI_BFD_CV_SIZE]
     * @type char
     * @flags CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     *  && SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE == SAI_BFD_MPLS_TYPE_TP 
     *  && SAI_BFD_SESSION_ATTR_TP_CV_ENABLE == TRUE
     */
    SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID,
    
    /**
     * @brief TP BFD section OAM router interface id
     *
     * @type sai_object_id_t
     * @flags CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_ROUTER_INTERFACE
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     *  && SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE == SAI_BFD_MPLS_TYPE_TP 
     */
    SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,

    /**
     * @brief TP BFD without gal, by default, bfd for lsp with gal, bfd for pw without gal
     *
     * @type bool
     * @flags CREATE_ONLY
     * @validonly SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE == SAI_BFD_ENCAPSULATION_TYPE_MPLS
     *  && SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE == SAI_BFD_MPLS_TYPE_TP 
     */
    SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL,

    /**
     * @brief The next hop id
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP, SAI_OBJECT_TYPE_NEXT_HOP_GROUP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_BFD_SESSION_ATTR_NEXT_HOP_ID,

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
    SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,

    /**
     * @brief indicate the path bfd session monitored is protecting path or working path
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @validonly SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID != SAI_NULL_OBJECT_ID
     * @default 0
     */
    SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,

    /**
     * @brief indicate the bfd session hw protection is enabled or not
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @validonly SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID != SAI_NULL_OBJECT_ID
     * @default 0
     */
    SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN,

    /** End of custom range base */
    SAI_BFD_SESSION_ATTR_CUSTOM_RANGE_END

} sai_bfd_session_attr_t;

/**
 * @brief BFD Session counter IDs in sai_get_bfd_session_stats() call
 */
typedef enum _sai_bfd_session_stat_t
{
    /** Ingress packet stat count */
    SAI_BFD_SESSION_STAT_IN_PACKETS,

    /** Egress packet stat count */
    SAI_BFD_SESSION_STAT_OUT_PACKETS,

    /** Packet Drop stat count */
    SAI_BFD_SESSION_STAT_DROP_PACKETS

} sai_bfd_session_stat_t;

/**
 * @brief Create BFD session.
 *
 * @param[out] bfd_session_id BFD session id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_bfd_session_fn)(
        _Out_ sai_object_id_t *bfd_session_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove BFD session.
 *
 * @param[in] bfd_session_id BFD session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_bfd_session_fn)(
        _In_ sai_object_id_t bfd_session_id);

/**
 * @brief Set BFD session attributes.
 *
 * @param[in] bfd_session_id BFD session id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_bfd_session_attribute_fn)(
        _In_ sai_object_id_t bfd_session_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get BFD session attributes.
 *
 * @param[in] bfd_session_id BFD session id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_bfd_session_attribute_fn)(
        _In_ sai_object_id_t bfd_session_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief Get BFD session statistics counters. Deprecated for backward compatibility.
 *
 * @param[in] bfd_session_id BFD session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_bfd_session_stats_fn)(
        _In_ sai_object_id_t bfd_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters);

/**
 * @brief Get BFD session statistics counters extended.
 *
 * @param[in] bfd_session_id BFD session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[in] mode Statistics mode
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_bfd_session_stats_ext_fn)(
        _In_ sai_object_id_t bfd_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters);

/**
 * @brief Clear BFD session statistics counters.
 *
 * @param[in] bfd_session_id BFD session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_clear_bfd_session_stats_fn)(
        _In_ sai_object_id_t bfd_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids);

/**
 * @brief BFD session state change notification
 *
 * Passed as a parameter into sai_initialize_switch()
 *
 * @count data[count]
 *
 * @param[in] count Number of notifications
 * @param[in] data Array of BFD session state
 */
typedef void (*sai_bfd_session_state_change_notification_fn)(
        _In_ uint32_t count,
        _In_ const sai_bfd_session_state_notification_t *data);

/**
 * @brief BFD method table retrieved with sai_api_query()
 */
typedef struct _sai_bfd_api_t
{
    sai_create_bfd_session_fn            create_bfd_session;
    sai_remove_bfd_session_fn            remove_bfd_session;
    sai_set_bfd_session_attribute_fn     set_bfd_session_attribute;
    sai_get_bfd_session_attribute_fn     get_bfd_session_attribute;
    sai_get_bfd_session_stats_fn         get_bfd_session_stats;
    sai_get_bfd_session_stats_ext_fn     get_bfd_session_stats_ext;
    sai_clear_bfd_session_stats_fn       clear_bfd_session_stats;

} sai_bfd_api_t;

/**
 * @}
 */
#endif /** __SAIBFD_H_ */
