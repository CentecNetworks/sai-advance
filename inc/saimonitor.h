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
 * @file    saimonitor.h
 *
 * @brief   This module defines SAI MONITOR 
 */

#if !defined (__SAIMONITOR_H_)
#define __SAIMONITOR_H_

#include <saitypes.h>


/**
* @brief Attribute Id in create_monitor_buffer() and;
* set_monitor_buffer_attribute();
* remove_monitor_buffer();
* get_monitor_buffer_attribute();
*/
typedef enum _sai_monitor_buffer_monitor_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_START = 0x00000000,

    /**
     * @brief  define the min threshold of microburst based on port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE |CREATE_ONLY
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT = SAI_MONITOR_BUFFER_MONITOR_ATTR_START,

    /**
     * @brief  define the min threshold of microburst based on port(unit is byte)  
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN,   

    /**
     * @brief define the max threshold of microburst based on port(unit is byte)  
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
      */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX,

     /**
     * @brief enable the ingress monitor  based on port, set the periodical monitor time. when a cycle ends and the notification is trigged. 
     * The system can get the byte number of messages 
     *
     * @type bool
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE,

     /**
     * @brief enable the egress monitor  based on port ,set the periodical monitor time. when a cycle ends and the notification is trigged. 
     * The system can get the byte number of messages 
     *
     * @type bool
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE,
    
    /**
     * @brief record max unicast buffer cnt(unit is byte), and when set the attr,the value can only be 0, indicate clearing watermark 
     *
     * @type  sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK,

    /**
     * @brief record max multicast buffer cnt(unit is byte) , and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type  sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK,

    /**
     * @brief record max total buffer cnt(unit is byte) , and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type  sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK,
    
    /**
     * @brief record max total buffer cnt(unit is byte)  , and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type  sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK,

    /**
     * @brief End of attributes
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_END,

    /** Custom range base value */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_CUSTOM_RANGE_END

}sai_monitor_buffer_monitor_attr_t;

/**
* @brief Attribute Id in create_monito_latency() and;
* set_monitor_latency_attribute();
* remove_monitor_latency();
* get_monitor_latency_attribute();
*/
typedef enum _sai_monitor_latency_monitor_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_START = 0x00000000,

    /**
     * @brief  define the min threshold of microburst based on port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE |CREATE_ONLY
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT = SAI_MONITOR_LATENCY_MONITOR_ATTR_START,
    /**
     * @brief latency moitor event enable 
     *
     * @type  bool
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE,

    /**
     * @brief  log the packet to cpu when the count of latency range over the threshold, per port per level control, 
     * there are 8 elements required in the array
     *
     * @type  sai_bool_list_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT,

    /**
     * @brief enable the latency monitor,set the periodical monitor time. when a cycle ends and the notification is trigged. 
     * The system can get the byte number of messages 
     *
     * @type bool
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE,

    /**
     * @brief per level control, if one packet latency in the level, the packet will be discarded
     * there are 8 elements required in the array
     *
     * @type   sai_bool_list_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD,

    /**
     * @brief record max time latency of each port(unit is ns) , and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type  sai_uint32_t
     * @flags CREATE_AND_SET
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK,
    
    /**
     * @brief End of attributes
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_END,

    /** Custom range base value */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_CUSTOM_RANGE_END
    
} sai_monitor_latency_monitor_attr_t;


/**
@brief  Support 8 latency threshold levels
*/
#define SAI_MONITOR_LATENCY_THRD_LEVEL 8 
#define SAI_MONITOR_MICROBURST_THRD_LEVEL 8 

/**
@brief  monitor event state
*/
typedef enum _sai_monitor_event_state_e
{
    SAI_MONITOR_EVENT_STATE_CLEAR,   /* monitor event clear */
    SAI_MONITOR_EVENT_STATE_OCCUR    /* monitor event occur */

} sai_monitor_event_state_e;

/*! This typedef defines the bool datatype which takes the values 
true and false.*/
typedef enum {False = 0, True = 1} Mon_boolean;

/**
@brief  micro burst event
*/
typedef struct sai_monitor_mburst_stats_s
{
    /*buffer monitor micro burst  messager*/
    sai_object_id_t buffer_monitor_microburst_port;
    uint32_t buffer_monitor_microburst_threshold_cnt[SAI_MONITOR_MICROBURST_THRD_LEVEL];
    
} sai_monitor_mburst_stats_t;

/**
@brief  buffer monitor event
*/
struct sai_monitor_buffer_event_s
{
    /*buffer monitor event messager*/
    sai_object_id_t buffer_monitor_event_port;
    uint32_t buffer_monitor_event_total_cnt;
    uint32_t buffer_monitor_event_port_unicast_cnt;
    uint32_t buffer_monitor_event_port_multicast_cnt;
    uint8_t buffer_monitor_event_state;
};
typedef struct sai_monitor_buffer_event_s sai_monitor_buffer_event_t;

/**
 * @brief buffer_monitor_stats_direction
 */
typedef enum _sai_buffer_monitor_stats_direction_t
{
    SAI_MONITOR_INGRESS,
    SAI_MONITOR_EGRESS,
    
} sai_buffer_monitor_stats_direction_t;

/**
@brief  buffer monitor stats
*/
struct sai_monitor_buffer_stats_s
{
    /*buffer monitor stats messager*/
    sai_object_id_t buffer_monitor_stats_port;
    /*sai_buffer_monitor_stats_direction_t*/
    uint32_t buffer_monitor_stats_direction;
    uint32_t buffer_monitor_stats_port_cnt;
};
typedef struct sai_monitor_buffer_stats_s sai_monitor_buffer_stats_t;

/**
@brief  buffer latency event
*/
struct sai_monitor_latency_event_s
{
    /*latency monitor event messager*/
    sai_object_id_t latency_monitor_event_port;
    uint64_t latency_monitor_event_latency; 
    uint8_t  latency_monitor_event_level;
    uint8_t  latency_monitor_event_state;
    uint32_t  latency_monitor_event_source_port;
};
typedef struct sai_monitor_latency_event_s sai_monitor_latency_event_t;

/**
@brief  buffer monitor stats
*/
struct sai_monitor_latency_stats_s
{
    /*latency monitor stats messager*/
    sai_object_id_t latency_monitor_stats_port;
    uint32_t latency_monitor_stats_level_cnt[SAI_MONITOR_LATENCY_THRD_LEVEL];
};
typedef struct sai_monitor_latency_stats_s sai_monitor_latency_stats_t;

/**
 * @brief buffer_monitor_message_type
 */
typedef enum _sai_buffer_monitor_message_type_t
{
   
    SAI_MONITOR_BUFFER_EVENT_MESSAGE,
    SAI_MONITOR_BUFFER_STATS_MESSAGE,
    SAI_MONITOR_MICORBURST_STATS_MESSAGE,
    
} sai_buffer_monitor_message_type_t;

/**
 * @brief buffer_monitor_message_type
 */
typedef enum _sai_buffer_monitor_based_on_type_t
{
    SAI_MONITOR_BUFFER_BASED_ON_PORT,
    SAI_MONITOR_BUFFER_BASED_ON_TOTAL,
    
} sai_buffer_monitor_based_on_type_t;

/**
@brief  buffer monitor notification data
*/
typedef struct _sai_monitor_buffer_notification_data_t
{
    /**
     * @brief buffer monitor id.
     *
     * @objects 
     */
    sai_object_id_t monitor_buffer_id;
    /*sai_buffer_monitor_message_type_t*/
    uint32_t buffer_monitor_message_type;
    /*sai_buffer_monitor_based_on_type_t*/
    uint32_t buffer_monitor_based_on_type;
    
    union
    {
        /*buffer event information*/
        sai_monitor_buffer_event_t buffer_event;   
        /*buffer stats information*/
        sai_monitor_buffer_stats_t  buffer_stats; 
        /*microburst stats information*/
        sai_monitor_mburst_stats_t  microburst_stats;    
    }  u;
    
} sai_monitor_buffer_notification_data_t;

/**
 * @brief latency_monitor_message_type
 */
typedef enum _sai_latency_monitor_message_type_t
{
   
    SAI_MONITOR_LATENCY_EVENT_MESSAGE,
    SAI_MONITOR_LATENCY_STATS_MESSAGE,
    
} sai_latency_monitor_message_type_t;

/**
@brief  latency monitor notification data
*/
typedef struct _sai_monitor_latency_notification_data_t
{
    /**
     * @brief latency monitor id.
     *
     * @objects 
     */
    sai_object_id_t monitor_latency_id;
    uint32_t latency_monitor_message_type;

    union
    {
        /*latency event information*/
        sai_monitor_latency_event_t latency_event;  
        /* latency stats information*/
        sai_monitor_latency_stats_t latency_stats;   
    }  u;

} sai_monitor_latency_notification_data_t;


/**
 * @brief MONITOR BUFFER notifications
 *
 * @count data[count]
 *
 * @param[in] count Number of notifications
 * @param[in] data Pointer to monitor buffer notification data array
 */
typedef void (*sai_monitor_buffer_notification_fn)(
        _In_ uint32_t count,
        _In_ const sai_monitor_buffer_notification_data_t *data);


/**
 * @brief create buffer monitor 
 *
 * @param[out]monitor_buffer_id buffer monitor id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_monitor_buffer_fn)(
        _Out_ sai_object_id_t *monitor_buffer_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief remove buffer monitor
 *
 * @param[in] monitor_buffer_id buffer monitor id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_monitor_buffer_fn)(
        _In_ sai_object_id_t monitor_buffer_id);


/**
 * @brief set monitor attribute
 *
 * @param[in] monitor_buffer_id buffer monitor id
 * @param[in] attr attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_monitor_buffer_attribute_fn)(
        _In_ sai_object_id_t monitor_buffer_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief get monitor attribute
 *
 * @param[in] monitor_buffer_id buffer monitor id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_monitor_buffer_attribute_fn)(
        _In_ sai_object_id_t monitor_buffer_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);


/**
 * @brief MONITOR LATENCY notifications
 *
 * @count data[count]
 *
 * @param[in] count Number of notifications
 * @param[in] data Pointer to latency monitor notification data array
 */
typedef void (*sai_monitor_latency_notification_fn)(
        _In_ uint32_t count,
        _In_ const sai_monitor_latency_notification_data_t *data);


/**
 * @brief create latency monitor
 *
 * @param[out]monitor_latency_id latency monitor id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_monitor_latency_fn)(
        _Out_ sai_object_id_t *monitor_latency_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief remove monitor
 *
 * @param[in] monitor_latency_id latency monitor id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_monitor_latency_fn)(
        _In_ sai_object_id_t monitor_latency_id);


/**
 * @brief set monitor attribute
 *
 * @param[in] monitor_latency_id latency monitor id
 * @param[in] attr attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_monitor_latency_attribute_fn)(
        _In_ sai_object_id_t monitor_latency_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief get monitor attribute
 *
 * @param[in] monitor_latency_id latency monitor id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_monitor_latency_attribute_fn)(
        _In_ sai_object_id_t monitor_latency_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief MONITOR API
 */
typedef struct _sai_monitor_api_t
{ 
    sai_create_monitor_buffer_fn                 create_monitor_buffer;
    sai_remove_monitor_buffer_fn               remove_monitor_buffer;
    sai_set_monitor_buffer_attribute_fn        set_monitor_buffer_attribute;
    sai_get_monitor_buffer_attribute_fn        get_monitor_buffer_attribute;

    sai_create_monitor_latency_fn                 create_monitor_latency;
    sai_remove_monitor_latency_fn               remove_monitor_latency;
    sai_set_monitor_latency_attribute_fn        set_monitor_latency_attribute;
    sai_get_monitor_latency_attribute_fn        get_monitor_latency_attribute;

} sai_monitor_api_t;

/**
 * @}
 */
#endif /** __SAIMONITOR_H_ */
