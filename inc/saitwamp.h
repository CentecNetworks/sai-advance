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
 * @file    saitwamp.h
 *
 * @brief   This module defines SAI TWAMP interface
 */

#if !defined (__SAITWAMP_H_)
#define __SAITWAMP_H_

#include <saitypes.h>

/**
 * @defgroup SAITWAMP SAI - TWAMP specific public APIs and data structures
 *
 */

/**
 * @brief SAI TWAMP session state
 */
typedef enum _sai_twamp_session_state_t
{
    /** Session State Active  */
    SAI_TWAMP_SESSION_STATE_ACTIVE = 0,

    /** Session State Inactive */
    SAI_TWAMP_SESSION_STATE_INACTIVE

} sai_twamp_session_state_t;

/**
 * @brief SAI TWAMP session authen mode,
 *        there are three modes: unauthenticated, authenticated, and encrypted.
 */
typedef enum _sai_twamp_session_auth_mode_t
{
    /** Session session unauthenticated mode */
    SAI_TWAMP_SESSION_MODE_AUTHENTICATED = 0,

    /** Session session authenticated mode */
    SAI_TWAMP_SESSION_MODE_UNAUTHENTICATED,

    /** Session session encrypted mode */
    SAI_TWAMP_SESSION_MODE_ENCRYPTED

} sai_twamp_session_auth_mode_t;

/**
 * @brief SAI TWAMP direction
 */
typedef enum _sai_twamp_session_direction_t
{
    /** Session enable ingress port  */
    SAI_TWAMP_SESSION_INGRESS = 0,

    /** Session enable egress port  */
    SAI_TWAMP_SESSION_EGRESS

} sai_twamp_session_direction_t;

/**
 * @brief SAI TWAMP role
 */
typedef enum _sai_twamp_session_role_t
{
    /** Session enable ingress port  */
    SAI_TWAMP_SESSION_SENDER = 0,

    /** Session enable egress port  */
    SAI_TWAMP_SESSION_REFLECTOR

} sai_twamp_session_role_t;


/**
 * @brief SAI type of twamp encapsulation for TWAMP

   0                   1                   2                   3
   0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sequence Number                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                          Timestamp                            |
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Error Estimate        |           MBZ                 |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                          Receive Timestamp                    |
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                        Sender Sequence Number                 |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                      Sender Timestamp                         |
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |      Sender Error Estimate    |           MBZ                 |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Sender TTL   |                                               |
   +-+-+-+-+-+-+-+-+                                               +
   |                                                               |
   .                                                               .
   .                         Packet Padding                        .
   .                                                               .
   |                                                               |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+



   Note that all timestamps have the same format as OWAMP [RFC4656] as
   follows:

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                   Integer part of seconds                     |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                 Fractional part of seconds                    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+


 */
typedef enum _sai_twamp_mode_type_t
{
    /**
     * @brief reflector will record session stats when enabling twamp full moode 
     */
    SAI_TWAMP_MODE_TWAMP_FULL,

    /**
     * @brief reflector not record session stats when enabling twamp light moode 
     */
    SAI_TWAMP_MODE_TWAMP_LIGHT

} sai_twamp_mode_type_t;


/**
 * @brief SAI TWAMP type of encapsulation for TWAMP
 */
typedef enum _sai_twamp_encapsulation_type_t
{
    /**
     * @brief IP Encapsulation, L2 header | IP(v4/v6) header | UDP header | Original TWAMP test packet
     */
    SAI_TWAMP_ENCAPSULATION_TYPE_IP,

    /**
     * @brief L3 VPN Encapsulation, L2 header | MPLS Label List | IP(v4/v6) header | UDP header | Original TWAMP test packet
     */
    SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN

} sai_twamp_encapsulation_type_t;

/**
 * @brief SAI attributes for TWAMP session
 */
typedef enum _sai_twamp_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_TWAMP_SESSION_ATTR_START,

    /**
     * @brief TWAMP Session type DEMAND/ASYNCHRONOUS
     *
     * @type sai_twamp_session_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TYPE = SAI_TWAMP_SESSION_ATTR_START,

    /**
     * @brief TWAMP Port, RX DIR with ingress port, TX DIR with egress port,  when SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID is false
     *         and depend on SAI_TWAMP_SESSION_ATTR_DIRECTION.
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_TWAMP_SESSION_ATTR_PORT,

    /**
     * @brief TWAMP session direction of sender or receiver.
     *
     * @type sai_twamp_session_role_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_TWAMP_SESSION_ATTR_SESSION_ROLE,

    /**
     * @brief UDP Source port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT,

    /**
     * @brief UDP Dest port
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT,

    /**
     * @brief Local source IP address
     *
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_SRC_IP,

    /**
     * @brief Remote Dest IP address
     *
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_DST_IP,

    //SAI_TWAMP_SESSION_ATTR_IPHDR_VERSION,

    /**
     * @brief DSCP of Traffic Class
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_TWAMP_SESSION_ATTR_TC,

    /**
     * @brief VPN VRFID (L3 MPLS VPN), when enabling hardware lookup (SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID) with Dest IP. 
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTE,

    /**
     * @brief Encapsulation type
     *
     * @type sai_twamp_encapsulation_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE,

    /**
     * @brief To enable TWAMP session transmit pakcet
     *
     * @type booldata
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,

    /**
     * @brief Hardware lookup valid
     *
     * @type bool
     * @flags CREATE_ONLY
     * @default true
     */
    SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID,

    /**
     * @brief payload padding length
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     */
    SAI_TWAMP_SESSION_ATTR_PADDING_LENGTH,

    /**
     * @brief TWAMP Session state
     *
     * @type sai_twamp_session_state_t
     * @flags READ_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_STATE,

    /**
     * @brief TWAMP Session mode: unauthenticated, authenticated, and encrypted.
     *
     * @type sai_twamp_session_auth_mode_t
     * @flags READ_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_AUTH_MODE,

    /**
     * @brief TWAMP Session nexthop ID for generating TWAMP test packet
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID,

    /**
     * @brief TWAMP test packet tx period, configuring by TWAMP sender period of Tx 
     *         Note: if tx period equal 0, sender will contine to gen packet, duration configured by SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION.
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD,

    /**
     * @brief TWAMP test packet tx rate per Kbps, configuring by TWAMP sender bandwith of Tx port 
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TX_RATE,

    /**
     * @brief TWAMP test packet tx count, configuring by TWAMP send packet count of Tx 
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT,

    /**
     * @brief TWAMP test packet tx duration per mirco second, timneout of the tx pakcet generation
     *
     * @type sai_uint64_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION,

    /**
     * @brief twamp mode of twamp: ligit mode and full mode
     *
     * @type sai_twamp_mode_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_TWAMP_SESSION_ATTR_MODE,

    /**
     * @brief End of attributes
     */
    SAI_TWAMP_SESSION_ATTR_END,

    /** Custom range base value */
    SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_TWAMP_SESSION_ATTR_CUSTOM_RANGE_END

} sai_twamp_session_attr_t;

/**
 * @brief TWAMP Session counter IDs in sai_get_twamp_session_stats() call
 */
typedef enum _sai_twamp_session_stats_t
{
    /** Rx packet stat count */
    SAI_TWAMP_SESSION_STATS_RX_PACKETS,

    /** Rx byte stat count */
    SAI_TWAMP_SESSION_STATS_RX_BYTE,

    /** Tx packet stat count */
    SAI_TWAMP_SESSION_STATS_TX_PACKETS,

    /** Tx byte stat count */
    SAI_TWAMP_SESSION_STATS_TX_BYTE,

    /** Packet Drop stat count */
    SAI_TWAMP_SESSION_STATS_DROP_PACKETS,

    /** Packet max latency */
    SAI_TWAMP_SESSION_STATS_MAX_LATENCY,

    /** Packet min latency */
    SAI_TWAMP_SESSION_STATS_MIN_LATENCY,

    /** Packet avg latency */
    SAI_TWAMP_SESSION_STATS_AVG_LATENCY,

    /** Packet max jitter */
    SAI_TWAMP_SESSION_STATS_MAX_JITTER,

    /** Packet min jitter */
    SAI_TWAMP_SESSION_STATS_MIN_JITTER,

    /** Packet avg jitter */
    SAI_TWAMP_SESSION_STATS_AVG_JITTER,

    /** Session first timestamp */
    SAI_TWAMP_SESSION_STATS_FIRST_TS,

    /** Session last timestamp */
    SAI_TWAMP_SESSION_STATS_LAST_TS,

    /** Session duration timestamp */
    SAI_TWAMP_SESSION_STATS_DURATION_TS

} sai_twamp_session_stats_t;

/**
 * @brief Defines the operational status of the TWAMP session
 */
typedef struct sai_twamp_session_status_notification_s
{
    /** TWAMP Session id */
    sai_object_id_t twamp_session_id;

    /** TWAMP session state */
    sai_twamp_session_stats_t session_stats;

} sai_twamp_session_status_notification_t;


/**
 * @brief Create TWAMP session.
 *
 * @param[out] twamp_session_id TWAMP session id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Value of attributes
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_create_twamp_session_fn)(
        _Out_ sai_object_id_t *twamp_session_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove TWAMP session.
 *
 * @param[in] twamp_session_id TWAMP session id
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_remove_twamp_session_fn)(
        _In_ sai_object_id_t twamp_session_id);

/**
 * @brief Set TWAMP session attributes.
 *
 * @param[in] twamp_session_id TWAMP session id
 * @param[in] attr Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_set_twamp_session_attribute_fn)(
        _In_ sai_object_id_t twamp_session_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get TWAMP session attributes.
 *
 * @param[in] twamp_session_id TWAMP session id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Value of attribute
 *
 * @return #SAI_STATUS_SUCCESS if operation is successful otherwise a different
 * error code is returned.
 */
typedef sai_status_t (*sai_get_twamp_session_attribute_fn)(
        _In_ sai_object_id_t twamp_session_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief Get TWAMP session statistics counters. Deprecated for backward compatibility.
 *
 * @param[in] twamp_session_id TWAMP session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_twamp_session_stats_fn)(
        _In_ sai_object_id_t twamp_session_id,
        _In_ uint32_t stats_count,
        _Inout_ sai_attribute_t *stats_list);

/**
 * @brief Clear TWAMP session statistics counters.
 *
 * @param[in] twamp_session_id TWAMP session id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_clear_twamp_session_stats_fn)(
        _In_ sai_object_id_t twamp_session_id,
        _In_ uint32_t stats_count,
        _In_ const sai_attribute_t *stats_list);

/**
 * @brief TWAMP session status change notification
 *
 * Passed as a parameter into sai_initialize_switch()
 *
 * @param[in] threshold of notifications
 * @param[in] data Array of TWAMP session status
 */
typedef void (*sai_twamp_session_status_change_notification_fn)(
        _In_ uint32_t threshold,
        _In_ const sai_twamp_session_status_notification_t *data);

/**
 * @brief TWAMP method table retrieved with sai_api_query()
 */
typedef struct _sai_twamp_api_t
{
    sai_create_twamp_session_fn            create_twamp_session;
    sai_remove_twamp_session_fn            remove_twamp_session;
    sai_set_twamp_session_attribute_fn     set_twamp_session_attribute;
    sai_get_twamp_session_attribute_fn     get_twamp_session_attribute;
    sai_get_twamp_session_stats_fn         get_twamp_session_stats;
    sai_clear_twamp_session_stats_fn       clear_twamp_session_stats;

} sai_twamp_api_t;

/**
 * @}
 */
#endif /** __SAITWAMP_H_ */
