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
 * @file    saisynce.h
 *
 * @brief   This module defines SAI Synchronous Ethernet
 */

#if !defined (__SAISYNCE_H_)
#define __SAISYNCE_H_

#include <saitypes.h>

/**
 * @brief Attribute Id in create_synce() and;
 * set_synce_attribute();
 * remove_synce();
 * get_synce_attribute();
 */
typedef enum _sai_synce_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_SYNCE_ATTR_START = 0x00000000,

    /**
     * @brief Local port ID, clock recovered from the port
     *
     * @type sai_object_id_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_PORT
     */
    SAI_SYNCE_ATTR_RECOVERED_PORT = SAI_SYNCE_ATTR_START,

    /**
     * @brief Clock divider 0~1023
     *
     * @type sai_uint16_t
     * @flags MANDATORY_ON_CREATE | CREATE_AND_SET
     * @isvlan false
     */
    SAI_SYNCE_ATTR_CLOCK_DIVIDER,

    /**
     * @brief End of attributes
     */
    SAI_SYNCE_ATTR_END,

    /** Custom range base value */
    SAI_SYNCE_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_SYNCE_ATTR_CUSTOM_RANGE_END

} sai_synce_attr_t;

/**
 * @brief Create Synchronous Ethernet
 *
 * @param[out] synce_id Synchronous Ethernet id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_synce_fn)(
        _Out_ sai_object_id_t *synce_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove Synchronous Ethernet
 *
 * @param[in] synce_id Synchronous Ethernet id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_synce_fn)(
        _In_ sai_object_id_t synce_id);

/**
 * @brief Set Synchronous Ethernet attribute
 *
 * @param[in] synce_id Synchronous Ethernet id
 * @param[in] attr Attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_synce_attribute_fn)(
        _In_ sai_object_id_t synce_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get Synchronous Ethernet attribute
 *
 * @param[in] synce_id Synchronous Ethernet id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_synce_attribute_fn)(
        _In_ sai_object_id_t synce_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief SYNC API
 */
typedef struct _sai_synce_api_t
{
    sai_create_synce_fn               create_synce;
    sai_remove_synce_fn               remove_synce;
    sai_set_synce_attribute_fn        set_synce_attribute;
    sai_get_synce_attribute_fn        get_synce_attribute;

} sai_synce_api_t;

/**
 * @}
 */
#endif /** __SAISYNCE_H_ */
