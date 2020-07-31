/**
 * Copyright (c) 2020 Centec Open Technologies, Inc.
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
 *    Centec would like to thank the following companies for their review and
 *    assistance with these files:
 *
 * @file    sainpm.h
 *
 * @brief   This module defines SAI NPM interface
 */

#if !defined (__SAINPM_H_)
#define __SAINPM_H_

#include <saitypes.h>

/**
 * @defgroup SAINPM SAI - NPM specific public APIs and data structures
 *
 */

/**
 * @brief SAI NPM direction of RFC2544 and RFC1564
 */
typedef enum _sai_npm_session_direction_t
{
    /** Session enable ingress port  */
    SAI_NPM_SESSION_INGRESS = 0,

    /** Session enable egress port  */
    SAI_NPM_SESSION_EGRESS

} sai_npm_session_direction_t;

/**
 * @brief SAI NPM role of RFC2544 and RFC1564
 */
typedef enum _sai_npm_session_role_t
{
    /** Session enable ingress port  */
    SAI_NPM_SESSION_SENDER = 0,

    /** Session enable egress port  */
    SAI_NPM_SESSION_REFLECTOR

} sai_npm_session_role_t;

typedef enum _sai_npm_session_color_mode_t
{
    /** Session enable color-aware mode  */
    SAI_NPM_SESSION_COLOR_AWARE = 0,

    /** Session enable color-blind mode  */
    SAI_NPM_SESSION_COLOR_BLIND

} sai_npm_session_color_mode_t;


typedef enum sai_npm_pkt_tx_mode_e
{
    SAI_NPM_TX_MODE_CONTINUOUS = 0,

    SAI_NPM_TX_MODE_PACKET_NUM,

    SAI_NPM_TX_MODE_PERIOD

} sai_npm_pkt_tx_mode_t;


/**
 * @brief SAI NPM type of encapsulation for NPM
 */
typedef enum _sai_npm_encapsulation_type_t
{
    /**
     * @brief IP Encapsulation, L2 header | IP(v4/v6) header | UDP header | Original TWAMP test packet
     */
    SAI_NPM_ENCAPSULATION_TYPE_IP = 0,

    /**
     * @brief L3 VPN Encapsulation, L2 header | MPLS Label List | IP(v4/v6) header | UDP header | Original TWAMP test packet
     */
    SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI,

    /**
     * @brief L3 VPN Encapsulation, L2 header | MPLS Label List | IP(v4/v6) header | UDP header | Original TWAMP test packet
     */
    SAI_NPM_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI,
    

} sai_npm_encapsulation_type_t;

/**
 * @brief SAI attributes for NPM session of RFC2544 and RFC1564
 */
typedef enum _sai_npm_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_NPM_SESSION_ATTR_START,

    /**
     * @brief NPM Port, RX DIR with ingress port, TX DIR with egress port,  when SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID is false
     *         and depend on SAI_NPM_SESSION_ATTR_DIRECTION.
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_NPM_PORT = SAI_NPM_SESSION_ATTR_START,

    /**
     * @brief receive port of NPM sender and reflector, including NNI of L3 MPLS VPN and ingress port of RAW IP, for acl match this inport to npm engine.
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_RECEIVE_PORT,

    /**
     * @brief NPM  RFC 1564 color mode, refer to sai_npm_session_color_mode_t
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_COLOR_MODE,

    /**
     * @brief NPM session direction of sender or receiver.
     *
     * @type sai_npm_session_role_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_NPM_SESSION_ATTR_SESSION_ROLE,

    /**
     * @brief UDP Source port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,

    /**
     * @brief UDP Dest port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_UDP_DST_PORT,

    /**
     * @brief Local source IP address
     *
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SRC_IP,

    /**
     * @brief Remote Dest IP address
     *
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_DST_IP,

    /**
     * @brief DSCP of Traffic Class
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_NPM_SESSION_ATTR_TC,

    /**
     * @brief IP header TTL
     *
     * @type sai_uint8_t
     * @flags CREATE_ONLY
     * @default 255
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER     
     */
    SAI_NPM_SESSION_ATTR_TTL,
	
    /**
     * @brief VPN VRFID (L3 MPLS VPN), when enabling hardware lookup (SAI_NPM_SESSION_ATTR_INWARD_VALID) with Dest IP. 
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,

    /**
     * @brief Encapsulation type
     *
     * @type sai_npm_encapsulation_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,

    /**
     * @brief To enable NPM session transmit pakcet
     *
     * @type booldata
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,

    /**
     * @brief hardware lookup valid
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default true
     */
    SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,

    /**
     * @brief npm rfc 2544/1564 packet length, including 64, 128, 512, 1024, 1280, 1518 Byte 
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER     
     */
    SAI_NPM_SESSION_ATTR_PACKET_LENGTH,
	
    /**
     * @brief npm packet tx mode of npm: CONTINUOUS, PACKET_NUM, PERIOD
     *
     * @type sai_npm_pkt_tx_mode_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_PKT_TX_MODE,

    /**
     * @brief NPM test packet tx period, configuring by NPM sender period of Tx 
     *         Note: if tx period equal 0, sender will contine to gen packet, duration configured by SAI_NPM_SESSION_ATTR_TX_PKT_DURATION.
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,

    /**
     * @brief NPM test packet tx rate per Kbps, configuring by NPM sender bandwith of Tx port 
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_RATE,

    /**
     * @brief NPM test packet tx count, configuring by NPM send packet count of Tx 
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_CNT,

    /**
     * @brief NPM test packet tx duration per mirco second, timneout of the tx pakcet generation
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,

    /**
     * @brief End of attributes
     */
    SAI_NPM_SESSION_ATTR_END,

    /** Custom range base value */
    SAI_NPM_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_NPM_SESSION_ATTR_CUSTOM_RANGE_END

} sai_npm_session_attr_t;

/**
 * @brief NPM Session counter IDs in sai_get_npm_session_stats() call
 */
typedef enum _sai_npm_session_stats_t
{
    /** Rx packet stat count */
    SAI_NPM_SESSION_STATS_RX_PACKETS,

    /** Rx byte stat count */
    SAI_NPM_SESSION_STATS_RX_BYTE,

    /** Tx packet stat count */
    SAI_NPM_SESSION_STATS_TX_PACKETS,

    /** Tx byte stat count */
    SAI_NPM_SESSION_STATS_TX_BYTE,

    /** Packet Drop stat count */
    SAI_NPM_SESSION_STATS_DROP_PACKETS

} sai_npm_session_stats_t;

/**
 * @brief Defines the operational status of the NPM session
 */
typedef struct sai_npm_session_status_notification_s
{
    /** NPM Session id */
    sai_object_id_t npm_session_id;

    /** NPM session state */
    sai_npm_session_stats_t session_stats;

} sai_npm_session_status_notification_t;


/**
 * @brief Create NPM session.
 *
 * @param[out] npm_session_id NPM session id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_npm_session_fn)(
        _Out_ sai_object_id_t *npm_session_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove NPM session.
 *
 * @param[in] npm_session_id NPM session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_npm_session_fn)(
        _In_ sai_object_id_t npm_session_id);

/**
 * @brief Set NPM session attributes.
 *
 * @param[in] npm_session_id NPM session id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_npm_session_attribute_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get NPM session attributes.
 *
 * @param[in] npm_session_id NPM session id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_npm_session_attribute_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief Get NPM session statistics counters. Deprecated for backward compatibility.
 *
 * @param[in] npm_session_id NPM session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return SAI_STATUS_SUCCESS on success, failure status code on error
 */

typedef sai_status_t (*sai_get_npm_session_stats_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters);

/**
 * @brief Clear NPM session statistics counters.
 *
 * @param[in] twamp_session_id NPM session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_clear_npm_session_stats_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t stats_count,
        _In_ const sai_stat_id_t *counter_ids);

/**
 * @brief NPM method table retrieved with sai_api_query()
 */
typedef struct _sai_npm_api_t
{
    sai_create_npm_session_fn            create_npm_session;
    sai_remove_npm_session_fn            remove_npm_session;
    sai_set_npm_session_attribute_fn     set_npm_session_attribute;
    sai_get_npm_session_attribute_fn     get_npm_session_attribute;
    sai_get_npm_session_stats_fn         get_npm_session_stats;
    sai_clear_npm_session_stats_fn       clear_npm_session_stats;

} sai_npm_api_t;

/**
 * @}
 */
#endif /** __SAINPM_H_ */
