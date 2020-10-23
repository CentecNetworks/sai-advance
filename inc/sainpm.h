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
 * @brief SAI NPM type of encapsulation
 */
typedef enum _sai_npm_encapsulation_type_t
{

    /* L2 scene encap */

    /** NPM used as Ether encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN = 0,
    
    /** NPM used as L2VPN encapsulation, based on port and vlan */
    SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS,

    /** NPM used as L2VPN encapsulation, based on VPWS tunnel */
    SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS,


    /* L3 scene encap */

    /** NPM used as Native IP encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_RAW_IP,

    /** NPM used as MPLS L3VPN encapsulation */
    SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN,

} sai_npm_encapsulation_type_t;




/**
 * @brief SAI NPM session role 
 */
typedef enum _sai_npm_session_role_t
{
    /** send packet devices  */
    SAI_NPM_SESSION_SENDER = 0,

    /** reflector packet devices  */
    SAI_NPM_SESSION_REFLECTOR

} sai_npm_session_role_t;



/**
 * @brief SAI NPM session packet tx mode
 */
typedef enum _sai_npm_pkt_tx_mode_t
{
    /** continunos send npm test packet */
    SAI_NPM_TX_MODE_CONTINUOUS = 0,

    /** only send npm test packet with assign numbers */
    SAI_NPM_TX_MODE_PACKET_NUM,

    /** send npm test packet with period interval */
    SAI_NPM_TX_MODE_PERIOD

} sai_npm_pkt_tx_mode_t;






/**
 * @brief SAI attributes for NPM session
 */
 
typedef enum _sai_npm_session_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_NPM_SESSION_ATTR_START,


    /**
     * @brief NPM session role of sender or receiver.
     * @type sai_npm_session_role_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SESSION_ROLE = SAI_NPM_SESSION_ATTR_START,
    

    /**
     * @brief npm test packet Encapsulation type
     * @type sai_npm_encapsulation_type_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE,


    /**
     * @brief npm test port
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY 
     * @objects SAI_OBJECT_TYPE_PORT for L3 scene encap or SAI_OBJECT_TYPE_BRIDGE_PORT for L2 scene encap
     */     
    SAI_NPM_SESSION_ATTR_NPM_TEST_PORT,

    /**
     * @brief npm packet receive port
     * @type sai_object_list_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY 
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT,


    /**
     * @brief npm test packet src mac address
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly for L2 scene encap
     */
    SAI_NPM_SESSION_ATTR_SRC_MAC,
    
    /**
     * @brief npm test packet dst mac address
     * @type sai_mac_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @validonly for L2 scene encap
     */
    SAI_NPM_SESSION_ATTR_DST_MAC,
    

    /**
     * @brief npm test packet outer vlan id
     * @type sai_uint16_t
     * @flags CREATE_ONLY
     * @validonly for L2 scene encap    
     */
    SAI_NPM_SESSION_ATTR_OUTER_VLANID,

    /**
     * @brief npm test packet inner vlan id
     * @type sai_uint16_t
     * @flags CREATE_ONLY
     * @validonly for L2 scene encap
     */
    SAI_NPM_SESSION_ATTR_INNER_VLANID,
    
    /**
     * @brief npm test packet src ip address
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_SRC_IP,

    /**
     * @brief npm test packet dst ip address
     * @type sai_ip4_t or sai_ip6_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */
    SAI_NPM_SESSION_ATTR_DST_IP,


    /**
     * @brief npm test packet UDP src port
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */    
    SAI_NPM_SESSION_ATTR_UDP_SRC_PORT,

    /**
     * @brief npm test packet UDP dst port
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     */ 
    SAI_NPM_SESSION_ATTR_UDP_DST_PORT,


    /**
     * @brief npm test packet ip header ttl 
     * @type sai_uint8_t
     * @flags CREATE_ONLY
     * @default 255   
     */
    SAI_NPM_SESSION_ATTR_TTL,

    /**
     * @brief npm test packet traffic class
     * @type sai_uint8_t
     * @flags CREATE_ONLY
     * @default 0   
     */
    SAI_NPM_SESSION_ATTR_TC,
    
    /**
     * @brief to enable transmit npm test pakcet
     * @type booldata
     * @flags CREATE_AND_SET
     * @default false
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER     
     */
    SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT,
    

    /**
     * @brief VPN VRFID
     * @type sai_object_id_t
     * @flags CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_VIRTUAL_ROUTER
     * @default 0
     * @validonly SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID == true and L3 scene encap
     */
    SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER,

    
    /**
     * @brief Hardware lookup valid
     * @type booldata
     * @flags CREATE_ONLY
     * @default true
     */    
    SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID,


    /**
     * @brief NPM test packet length
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER     
     */
    SAI_NPM_SESSION_ATTR_PACKET_LENGTH,
    

    /**
     * @brief NPM test packet tx rate per Kbps
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER      
     */    
    SAI_NPM_SESSION_ATTR_TX_RATE,


    /**
     * @brief NPM packet tx mode 
     * @type sai_npm_pkt_tx_mode_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER  
     */
    SAI_NPM_SESSION_ATTR_PKT_TX_MODE,


    /**
     * @brief NPM test packet tx period,
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER and SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_TX_MODE_PERIOD        
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD,


    /**
     * @brief NPM test packet tx pkt cnt
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER and SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_TX_MODE_PACKET_NUM        
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_CNT,


    /**
     * @brief NPM test packet tx pkt duration
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER and SAI_NPM_SESSION_ATTR_PKT_TX_MODE == SAI_NPM_TX_MODE_CONTINUOUS        
     */
    SAI_NPM_SESSION_ATTR_TX_PKT_DURATION,

    /**
     * @brief NPM test packet offset to insert timestamp
     * @type sai_uint32_t
     * @flags CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER   
     * @default from octet 4 after L4 (UDP/TCP), timestamp will occupy 8 octets
     */
    SAI_NPM_SESSION_ATTR_TIMESTAMP_OFFSET,

    /**
     * @brief NPM test packet offset to insert sequence number
     * @type sai_uint32_t
     * @flags CREATE_ONLY
     * @condition SAI_NPM_SESSION_ATTR_SESSION_ROLE == SAI_NPM_SESSION_SENDER   
     * @default from octet 0 after L4 (UDP/TCP), sequence number will occupy 4 octets
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
    SAI_NPM_SESSION_STATS_DROP_PACKETS,

    /** Packet max latency */
    SAI_NPM_SESSION_STATS_MAX_LATENCY,

    /** Packet min latency */
    SAI_NPM_SESSION_STATS_MIN_LATENCY,

    /** Packet avg latency */
    SAI_NPM_SESSION_STATS_AVG_LATENCY,

    /** Packet max jitter */
    SAI_NPM_SESSION_STATS_MAX_JITTER,

    /** Packet min jitter */
    SAI_NPM_SESSION_STATS_MIN_JITTER,

    /** Packet avg jitter */
    SAI_NPM_SESSION_STATS_AVG_JITTER,    

    /** Max rx ir */
    SAI_NPM_SESSION_STATS_MAX_IR,  

    /** MIN rx ir */
    SAI_NPM_SESSION_STATS_MIN_IR, 

} sai_npm_session_stats_t;




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
