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
 * @brief Attribute Id in create_monitor_buffer_monitor() and;
 * set_monitor_buffer_monitor_attribute();
 * remove_monitor_buffer_monitor();
 * get_monitor_buffer_monitor_attribute();
 */
typedef enum _sai_monitor_buffer_monitor_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_START = 0x00000000,

    /**
     * @brief Define the min threshold of microburst based on port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE |CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT = SAI_MONITOR_BUFFER_MONITOR_ATTR_START,

    /**
     * @brief Define the min threshold of microburst based on port(unit is byte)
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD,

    /**
     * @brief Define the max threshold of microburst based on port(unit is byte)
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD,

    /**
     * @brief Enable the ingress monitor  based on port, set the periodical monitor time. when a cycle ends and the notification is triggered.
     * The system can get the byte number of messages
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE,

    /**
     * @brief Enable the egress monitor  based on port, set the periodical monitor time. when a cycle ends and the notification is triggered.
     * The system can get the byte number of messages
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE,

    /**
     * @brief Record max unicast buffer count(unit is byte), and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK,

    /**
     * @brief Record max multicast buffer count(unit is byte), and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK,

    /**
     * @brief Record max total buffer count(unit is byte), and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK,

    /**
     * @brief Record max total buffer count(unit is byte), and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
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

} sai_monitor_buffer_monitor_attr_t;

/**
 * @brief Attribute Id in create_monitor_latency_monitor() and;
 * set_monitor_latency_monitor_attribute();
 * remove_monitor_latency_monitor();
 * get_monitor_latency_monitor_attribute();
 */
typedef enum _sai_monitor_latency_monitor_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_START = 0x00000000,

    /**
     * @brief Define the min threshold of microburst based on port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE |CREATE_ONLY
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT = SAI_MONITOR_LATENCY_MONITOR_ATTR_START,

    /**
     * @brief Latency monitor over max threshold inform enable
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE,

    /**
     * @brief Log the packet to CPU when the count of latency range over the threshold, per port per level control,
     * there are 8 elements required in the array
     *
     * @type sai_bool_list_t
     * @flags CREATE_AND_SET
     * @default empty
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT,

    /**
     * @brief Enable the latency monitor,set the periodical monitor time. when a cycle ends and the notification is triggered.
     * The system can get the byte number of messages
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE,

    /**
     * @brief Per level control, if one packet latency in the level, the packet will be discarded
     * there are 8 elements required in the array
     *
     * @type sai_bool_list_t
     * @flags CREATE_AND_SET
     * @default empty
     */
    SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD,

    /**
     * @brief Record max time latency of each port(unit is Nanosecond), and when set the attr,the value can only be 0, indicate clearing watermark
     *
     * @type sai_uint32_t
     * @flags CREATE_AND_SET
     * @default 0
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
 * @brief Support 8 latency threshold levels
 */
#define SAI_MONITOR_LATENCY_THRD_LEVEL 8
#define SAI_MONITOR_MICROBURST_THRD_LEVEL 8

/**
 * @brief Monitor event state
 */
typedef enum _sai_monitor_event_state_t
{
    /** Monitor event clear */
    SAI_MONITOR_EVENT_STATE_CLEAR,

    /** Monitor event occur */
    SAI_MONITOR_EVENT_STATE_OCCUR

} sai_monitor_event_state_t;

/**
 * @brief Micro burst event
 */
typedef struct _sai_monitor_mburst_stats_t
{
    /** Buffer monitor micro burst message */
    sai_object_id_t buffer_monitor_microburst_port;
    sai_uint32_t buffer_monitor_microburst_threshold_cnt[8];

} sai_monitor_mburst_stats_t;

/**
 * @brief Buffer monitor event
 */
typedef struct _sai_monitor_buffer_event_t
{
    /** Buffer monitor event message */
    sai_object_id_t buffer_monitor_event_port;
    sai_uint32_t buffer_monitor_event_total_cnt;
    sai_uint32_t buffer_monitor_event_port_unicast_cnt;
    sai_uint32_t buffer_monitor_event_port_multicast_cnt;
    sai_uint8_t buffer_monitor_event_state;
} sai_monitor_buffer_event_t;

/**
 * @brief Buffer_monitor_stats_direction
 */
typedef enum _sai_buffer_monitor_stats_direction_t
{
    SAI_BUFFER_MONITOR_STATS_DIRECTION_INGRESS,
    SAI_BUFFER_MONITOR_STATS_DIRECTION_EGRESS,

} sai_buffer_monitor_stats_direction_t;

/**
 * @brief Buffer monitor stats
 */
typedef struct _sai_monitor_buffer_stats_t
{
    /** Buffer monitor stats message */
    sai_object_id_t buffer_monitor_stats_port;

    /** Direction */
    sai_uint32_t buffer_monitor_stats_direction;

    sai_uint32_t buffer_monitor_stats_port_cnt;
} sai_monitor_buffer_stats_t;

/**
 * @brief Buffer latency event
 */
typedef struct _sai_monitor_latency_event_t
{
    /** Latency monitor event message */
    sai_object_id_t latency_monitor_event_port;
    sai_uint64_t latency_monitor_event_latency;
    sai_uint8_t  latency_monitor_event_level;
    sai_uint8_t  latency_monitor_event_state;
    sai_uint32_t  latency_monitor_event_source_port;
} sai_monitor_latency_event_t;

/**
 * @brief Buffer monitor stats
 */
typedef struct _sai_monitor_latency_stats_t
{
    /** Latency monitor stats message */
    sai_object_id_t latency_monitor_stats_port;
    sai_uint32_t latency_monitor_stats_level_cnt[8];
} sai_monitor_latency_stats_t;

/**
 * @brief Buffer_monitor_message_type
 */
typedef enum _sai_buffer_monitor_message_type_t
{
    SAI_BUFFER_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE,
    SAI_BUFFER_MONITOR_MESSAGE_TYPE_STATS_MESSAGE,
    SAI_BUFFER_MONITOR_MESSAGE_TYPE_MICORBURST_STATS_MESSAGE,

} sai_buffer_monitor_message_type_t;

/**
 * @brief Buffer_monitor_message_type
 */
typedef enum _sai_buffer_monitor_based_on_type_t
{
    SAI_BUFFER_MONITOR_BASED_ON_TYPE_PORT,
    SAI_BUFFER_MONITOR_BASED_ON_TYPE_TOTAL,

} sai_buffer_monitor_based_on_type_t;

/**
 * @extraparam sai_buffer_monitor_message_type_t buffer_monitor_message_type
 */
typedef union _sai_monitor_buffer_data_t
{
    /**
     * @brief Buffer event
     *
     * @validonly buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE
     */
    sai_monitor_buffer_event_t buffer_event;

    /**
     * @brief Buffer stats
     *
     * @validonly buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_STATS_MESSAGE
     */
    sai_monitor_buffer_stats_t buffer_stats;

    /**
     * @brief Micro burst stats
     *
     * @validonly buffer_monitor_message_type == SAI_BUFFER_MONITOR_MESSAGE_TYPE_MICORBURST_STATS_MESSAGE
     */
    sai_monitor_mburst_stats_t microburst_stats;
} sai_monitor_buffer_data_t;

/**
 * @brief Buffer monitor notification data
 */
typedef struct _sai_monitor_buffer_notification_data_t
{
    /**
     * @brief Buffer monitor id.
     *
     * @objects SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR
     */
    sai_object_id_t monitor_buffer_monitor_id;

    /** Message type */
    sai_buffer_monitor_message_type_t buffer_monitor_message_type;

    /** Based on type */
    sai_buffer_monitor_based_on_type_t buffer_monitor_based_on_type;

    /**
     * @brief Buffer monitor data.
     *
     * @passparam buffer_monitor_message_type
     */
    sai_monitor_buffer_data_t u;

} sai_monitor_buffer_notification_data_t;

/**
 * @brief Latency_monitor_message_type
 */
typedef enum _sai_latency_monitor_message_type_t
{
    SAI_LATENCY_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE,
    SAI_LATENCY_MONITOR_MESSAGE_TYPE_STATS_MESSAGE,

} sai_latency_monitor_message_type_t;

/**
 * @extraparam sai_latency_monitor_message_type_t latency_monitor_message_type
 */
typedef union _sai_monitor_latency_data_t
{
    /**
     * @brief Latency event
     *
     * @validonly latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_EVENT_MESSAGE
     */
    sai_monitor_latency_event_t latency_event;

    /**
     * @brief Latency stats
     *
     * @validonly latency_monitor_message_type == SAI_LATENCY_MONITOR_MESSAGE_TYPE_STATS_MESSAGE
     */
    sai_monitor_latency_stats_t latency_stats;
} sai_monitor_latency_data_t;

/**
 * @brief Latency monitor notification data
 */
typedef struct _sai_monitor_latency_notification_data_t
{
    /**
     * @brief Latency monitor id.
     *
     * @objects SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR
     */
    sai_object_id_t monitor_latency_monitor_id;

    sai_latency_monitor_message_type_t latency_monitor_message_type;

    /**
     * @brief Latency monitor data.
     *
     * @passparam latency_monitor_message_type
     */
    sai_monitor_latency_data_t u;

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
 * @brief Create buffer monitor
 *
 * @param[out] monitor_buffer_monitor_id Buffer monitor id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_monitor_buffer_monitor_fn)(
        _Out_ sai_object_id_t *monitor_buffer_monitor_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove buffer monitor
 *
 * @param[in] monitor_buffer_monitor_id Buffer monitor id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_monitor_buffer_monitor_fn)(
        _In_ sai_object_id_t monitor_buffer_monitor_id);

/**
 * @brief Set monitor attribute
 *
 * @param[in] monitor_buffer_monitor_id Buffer monitor id
 * @param[in] attr Attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_monitor_buffer_monitor_attribute_fn)(
        _In_ sai_object_id_t monitor_buffer_monitor_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get monitor attribute
 *
 * @param[in] monitor_buffer_monitor_id Buffer monitor id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_monitor_buffer_monitor_attribute_fn)(
        _In_ sai_object_id_t monitor_buffer_monitor_id,
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
 * @brief Create latency monitor
 *
 * @param[out] monitor_latency_monitor_id Latency monitor id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_monitor_latency_monitor_fn)(
        _Out_ sai_object_id_t *monitor_latency_monitor_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove monitor
 *
 * @param[in] monitor_latency_monitor_id Latency monitor id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_monitor_latency_monitor_fn)(
        _In_ sai_object_id_t monitor_latency_monitor_id);

/**
 * @brief Set monitor attribute
 *
 * @param[in] monitor_latency_monitor_id Latency monitor id
 * @param[in] attr Attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_monitor_latency_monitor_attribute_fn)(
        _In_ sai_object_id_t monitor_latency_monitor_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get monitor attribute
 *
 * @param[in] monitor_latency_monitor_id Latency monitor id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_monitor_latency_monitor_attribute_fn)(
        _In_ sai_object_id_t monitor_latency_monitor_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief MONITOR API
 */
typedef struct _sai_monitor_api_t
{
    sai_create_monitor_buffer_monitor_fn               create_monitor_buffer_monitor;
    sai_remove_monitor_buffer_monitor_fn               remove_monitor_buffer_monitor;
    sai_set_monitor_buffer_monitor_attribute_fn        set_monitor_buffer_monitor_attribute;
    sai_get_monitor_buffer_monitor_attribute_fn        get_monitor_buffer_monitor_attribute;
    sai_create_monitor_latency_monitor_fn              create_monitor_latency_monitor;
    sai_remove_monitor_latency_monitor_fn              remove_monitor_latency_monitor;
    sai_set_monitor_latency_monitor_attribute_fn       set_monitor_latency_monitor_attribute;
    sai_get_monitor_latency_monitor_attribute_fn       get_monitor_latency_monitor_attribute;

} sai_monitor_api_t;

/**
 * @}
 */
#endif /** __SAIMONITOR_H_ */
