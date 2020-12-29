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
 * @file    sainpm.h
 *
 * @brief   This module defines SAI Network Performance Measurement interface
 */

#if !defined (__SAINPM_H_)
#define __SAINPM_H_

#include <saitypes.h>

/**
 * @defgroup SAINPM SAI - Network Performance Measurement specific public APIs and data structures
 *
 * @{
 */

/**
 * @brief SAI Network Performance Measurement type of encapsulation
 */
typedef enum _sai_npm_encapsulation_type_t
{
    /** L2 scene encap */

    /** Network Performance Measurement used as Ether encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN = 0,

    /** Network Performance Measurement used as L2 Virtual Private Network encapsulation, based on port and vlan */
    SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS,

    /** Network Performance Measurement used as L2 Virtual Private Network encapsulation, based on Virtual Private Wire Service tunnel */
    SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS,

    /** L3 scene encap */

    /** Network Performance Measurement used as Native IP encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_RAW_IP,

    /** Network Performance Measurement used as MPLS L3 Virtual Private Network encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN,

} sai_npm_encapsulation_type_t;

/**
 * @brief SAI Network Performance Measurement session role
 */
typedef enum _sai_npm_session_role_t
{
    /** Send packet devices */
    SAI_NPM_SESSION_ROLE_SENDER = 0,

    /** Reflector packet devices */
    SAI_NPM_SESSION_ROLE_REFLECTOR

} sai_npm_session_role_t;

/**
 * @brief SAI Network Performance Measurement session packet tx mode
 */
typedef enum _sai_npm_pkt_tx_mode_t
{
    /** Continuous send Network Performance Measurement test packet */
    SAI_NPM_PKT_TX_MODE_CONTINUOUS = 0,

    /** Only send Network Performance Measurement test packet with assign numbers */
    SAI_NPM_PKT_TX_MODE_PACKET_NUM,

    /** Send Network Performance Measurement test packet with period interval */
    SAI_NPM_PKT_TX_MODE_PERIOD

} sai_npm_pkt_tx_mode_t;

/**
 * @brief SAI attributes for Network Performance Measurement session
 */
typedef enum _sai_npm_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_NPM_SESSION_ATTR_START,

    /**
     * @brief Network Performance Measurement session role of sender or receiver.
     *
     * @type sai_npm_session_role_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SESSION_ROLE = SAI_NPM_SESSION_ATTR_START,

    /**
     * @brief Network Performance Measurement test packet Encapsulation type
     *
     * @type sai_npm_encapsulation_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,

    /**
     * @brief Network Performance Measurement test port
     * objects SAI_OBJECT_TYPE_PORT for L3 scene encap or SAI_OBJECT_TYPE_BRIDGE_PORT for L2 scene encap
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_NPM_TEST_PORT,

    /**
     * @brief Network Performance Measurement packet receive port
     *
     * @type sai_object_list_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT,

    /**
     * @brief Network Performance Measurement test packet src MAC address
     *
     * for L2 scene encap
     *
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SRC_MAC,

    /**
     * @brief Network Performance Measurement test packet dst MAC address
     *
     * valid only for L2 scene encap
     *
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_DST_MAC,

    /**
     * @brief Network Performance Measurement test packet outer vlan id
     *
     * valid only for L2 scene encap
     *
     * @type sai_uint16_t
     * @flags CREATE_ONLY
     * @isvlan true
     * @default 0
     */
    SAI_NPM_SESSION_ATTR_OUTER_VLANID,

    /**
     * @brief Network Performance Measurement test packet inner vlan id
     *
     * valid only for L2 scene encap
     *
     * @type sai_uint16_t
     * @flags CREATE_ONLY
     * @isvlan true
     * @default 0
     */
    SAI_NPM_SESSION_ATTR_INNER_VLANID,

    /**
     * @brief Network Performance Measurement test packet source IP address
     *
     * @type sai_ip4_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SRC_IP,

    /**
     * @brief Network Performance Measurement test packet destination IP address
     *
     * @type sai_ip4_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_DST_IP,

    /**
     * @brief Network Performance Measurement test packet UDP src port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,

    /**
     * @brief Network Performance Measurement test packet UDP dst port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_UDP_DST_PORT,

    /**
     * @brief Network Performance Measurement test packet IP header TTL
     *
     * @type sai_uint8_t
     * @flags CREATE_ONLY
     * @default 255
     */
    SAI_NPM_SESSION_ATTR_TTL,

    /**
     * @brief Network Performance Measurement test packet traffic class
     *
     * @type sai_uint8_t
     * @flags CREATE_ONLY
     * @default 0
     */
    SAI_NPM_SESSION_ATTR_TC,

    /**
     * @brief To enable transmit Network Performance Measurement test packet
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     * @validonly SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,

    /**
     * @brief Virtual Private Network VRF ID
     * valid when SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID == true and L3 scene encap
     *
     * @type sai_object_id_t
     * @flags CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_VIRTUAL_ROUTER
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,

    /**
     * @brief Hardware lookup valid
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default true
     */
    SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,

    /**
     * @brief Network Performance Measurement test packet length
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_PACKET_LENGTH,

    /**
     * @brief Network Performance Measurement test packet tx rate per K-bit per second
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_TX_RATE,

    /**
     * @brief Network Performance Measurement packet tx mode
     *
     * @type sai_int32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_PKT_TX_MODE,

    /**
     * @brief Network Performance Measurement test packet tx period,
     * Valid when SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_PKT_TX_MODE_PERIOD
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,

    /**
     * @brief Network Performance Measurement test packet tx packet count
     * Valid when SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_PKT_TX_MODE_PACKET_NUM
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_CNT,

    /**
     * @brief Network Performance Measurement test packet tx pkt duration
     * Valid when SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_PKT_TX_MODE_CONTINUOUS
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,

    /**
     * @brief Network Performance Measurement test packet offset to insert timestamp
     *
     * default from octet 4 after L4 (UDP/TCP), timestamp will occupy 8 octets
     *
     * @type sai_uint32_t
     * @flags CREATE_ONLY
     * @default 4
     * @validonly SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET,

    /**
     * @brief Network Performance Measurement test packet offset to insert sequence number
     * default from octet 0 after L4 (UDP/TCP), sequence number will occupy 4 octets
     *
     * @type sai_uint32_t
     * @flags CREATE_ONLY
     * @default 0
     * @validonly SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_ROLE_SENDER
     */
    SAI_NPM_SESSION_ATTR_SEQUENCE_NUMBER_OFFSET,

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
 * @brief Network Performance Measurement Session counter IDs in sai_get_npm_session_stats() call
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
    SAI_NPM_SESSION_STATS_DROP_PACKETS,

    /** Packet max latency */
    SAI_NPM_SESSION_STATS_MAX_LATENCY,

    /** Packet min latency */
    SAI_NPM_SESSION_STATS_MIN_LATENCY,

    /** Packet avg latency */
    SAI_NPM_SESSION_STATS_AVG_LATENCY,

    /** Packet max jitters */
    SAI_NPM_SESSION_STATS_MAX_JITTER,

    /** Packet min jitters */
    SAI_NPM_SESSION_STATS_MIN_JITTER,

    /** Packet avg jitters */
    SAI_NPM_SESSION_STATS_AVG_JITTER,

    /** Max rx information rate */
    SAI_NPM_SESSION_STATS_MAX_IR,

    /** MIN rx information rate */
    SAI_NPM_SESSION_STATS_MIN_IR,

} sai_npm_session_stats_t;

/**
 * @brief Create Network Performance Measurement session.
 *
 * @param[out] npm_session_id Network Performance Measurement session id
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
 * @brief Remove Network Performance Measurement session.
 *
 * @param[in] npm_session_id Network Performance Measurement session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_npm_session_fn)(
        _In_ sai_object_id_t npm_session_id);

/**
 * @brief Set Network Performance Measurement session attributes.
 *
 * @param[in] npm_session_id Network Performance Measurement session id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_npm_session_attribute_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Network Performance Measurement session attributes.
 *
 * @param[in] npm_session_id Network Performance Measurement session id
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
 * @brief Get Network Performance Measurement session statistics counters.
 *
 * @param[in] npm_session_id Network Performance Measurement session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_npm_session_stats_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters);

/**
 * @brief Get Network Performance Measurement session statistics counters extended.
 *
 * @param[in] npm_session_id Network Performance Measurement session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[in] mode Statistics mode
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_npm_session_stats_ext_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters);

/**
 * @brief Clear Network Performance Measurement session statistics counters.
 *
 * @param[in] npm_session_id Twamp_session_id Network Performance Measurement session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_clear_npm_session_stats_fn)(
        _In_ sai_object_id_t npm_session_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids);

/**
 * @brief Network Performance Measurement method table retrieved with sai_api_query()
 */
typedef struct _sai_npm_api_t
{
    sai_create_npm_session_fn            create_npm_session;
    sai_remove_npm_session_fn            remove_npm_session;
    sai_set_npm_session_attribute_fn     set_npm_session_attribute;
    sai_get_npm_session_attribute_fn     get_npm_session_attribute;
    sai_get_npm_session_stats_fn         get_npm_session_stats;
    sai_get_npm_session_stats_ext_fn     get_npm_session_stats_ext;
    sai_clear_npm_session_stats_fn       clear_npm_session_stats;

} sai_npm_api_t;

/**
 * @}
 */
#endif /** __SAINPM_H_ */
