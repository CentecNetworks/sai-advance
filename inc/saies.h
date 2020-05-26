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
 * @file    saies.h
 *
 * @brief   This module defines SAI Ethernet Segment
 */

#if !defined (__SAIES_H_)
#define __SAIES_H_

#include <saitypes.h>

/**
 * @defgroup SAIES SAI - Ethernet Segment specific API definitions
 *
 * @{
 */
 
/**
 * @brief Defines Ethernet Segment attributes
 */
typedef enum _sai_es_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_ES_ATTR_START,

    /**
     * @brief ESI Label
     *
     * @type sai_uint32_t
     * @flags MANDATORY_ON_CREATE | CREATE_ONLY
     * @default 0
     */
    SAI_ES_ATTR_ESI_LABEL = SAI_ES_ATTR_START,
    
    /**
     * @brief End of attributes
     */
    SAI_ES_ATTR_END,

    /** Custom range base value */
    SAI_ES_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /** End of custom range base */
    SAI_ES_ATTR_CUSTOM_RANGE_END

} sai_es_attr_t;


/**
 * @brief Create ethernet segment item
 *
 * @param[out] ethernet segment item id
 * @param[in] switch_id Switch Id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_es_fn)(
        _Out_ sai_object_id_t *es_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);
        
/**
 * @brief Remove ethernet segment item
 *
 * @param[in] es_id ethernet segment item id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_es_fn)(
        _In_ sai_object_id_t es_id);
        
/**
 * @brief Set ethernet segment item attribute
 *
 * @param[in] es_id ethernet segment item id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_es_attribute_fn)(
        _In_ sai_object_id_t es_id,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get ethernet segment item attributes
 *
 * @param[in] es_id ethernet segment item id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_es_attribute_fn)(
        _In_ sai_object_id_t es_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);
        
/**
 * @brief Ethernet Segment methods table retrieved with sai_api_query()
 */
typedef struct _sai_es_api_t
{
    sai_create_es_fn                     create_es;
    sai_remove_es_fn                     remove_es;
    sai_set_es_attribute_fn              set_es_attribute;
    sai_get_es_attribute_fn              get_es_attribute;
} sai_es_api_t;

/**
 * @}
 */
#endif /** __SAIES_H_ */
