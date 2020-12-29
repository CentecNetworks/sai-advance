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
 * @file    saimpls.h
 *
 * @brief   This module defines SAI MPLS interface
 */

#if !defined (__SAIMPLS_H_)
#define __SAIMPLS_H_

#include <saitypes.h>

/**
 * @defgroup SAIMPLS SAI - MPLS specific API definitions
 *
 * @{
 */
typedef enum _sai_inseg_entry_psc_type_t
{
    /**
     * @brief EXP of MPLS label infers both TC and COLOR
     */
    SAI_INSEG_ENTRY_PSC_TYPE_ELSP,

    /**
     * @brief MPLS label infers TC and EXP of MPLS label infers COLOR
     */
    SAI_INSEG_ENTRY_PSC_TYPE_LLSP,

    /**
     * @brief Do not use MPLS label infers TC and COLOR
     */
    SAI_INSEG_ENTRY_PSC_TYPE_NONE

} sai_inseg_entry_psc_type_t;

typedef enum _sai_inseg_entry_pop_ttl_mode_t
{
    /**
     * @brief Uniform mode
     *
     * TTL of inner header is computed based on TTL of outer header on pop.
     */
    SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM,

    /**
     * @brief Pipe mode
     *
     * TTL of inner header is left unchanged on pop.
     */
    SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE
} sai_inseg_entry_pop_ttl_mode_t;

typedef enum _sai_inseg_entry_pop_qos_mode_t
{
    /**
     * @brief Uniform mode
     *
     * DSCP or EXP of inner header is computed based on TC AND COLOR of outer header on pop.
     */
    SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM,

    /**
     * @brief Uniform mode
     *
     * DSCP or EXP of inner header is left unchanged on pop.
     */
    SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE
} sai_inseg_entry_pop_qos_mode_t;

/**
 * @brief MPLS in-segment configured role
 */
typedef enum _sai_inseg_entry_configured_role_t
{
    /** MPLS in-segment is primary */
    SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY,

    /** MPLS in-segment is standby */
    SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY,

} sai_inseg_entry_configured_role_t;

/**
 * @brief MPLS in-segment observed role
 */
typedef enum _sai_inseg_entry_frr_observed_role_t
{
    /** MPLS in-segment is active */
    SAI_INSEG_ENTRY_FRR_OBSERVED_ROLE_ACTIVE,

    /** MPLS in-segment is inactive */
    SAI_INSEG_ENTRY_FRR_OBSERVED_ROLE_INACTIVE,

} sai_inseg_entry_frr_observed_role_t;

/**
 * @brief Attribute Id for SAI in segment
 *
 * @flags Contains flags
 */
typedef enum _sai_inseg_entry_attr_t
{
    /**
     * @brief Start of attributes
     */
    SAI_INSEG_ENTRY_ATTR_START,

    /**
     * @brief Number of pops
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_INSEG_ENTRY_ATTR_NUM_OF_POP = SAI_INSEG_ENTRY_ATTR_START,

    /**
     * @brief Packet action
     *
     * @type sai_packet_action_t
     * @flags CREATE_AND_SET
     * @default SAI_PACKET_ACTION_FORWARD
     */
    SAI_INSEG_ENTRY_ATTR_PACKET_ACTION,

    /**
     * @brief Packet priority for trap/log actions
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     */
    SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY,

    /**
     * @brief The next hop id
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP, SAI_OBJECT_TYPE_NEXT_HOP_GROUP, SAI_OBJECT_TYPE_ROUTER_INTERFACE
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID,

    /**
     * @brief Define PSC type for a label.
     *
     * Defines how to infer both TC and COLOR
     *
     * @type sai_inseg_entry_psc_type_t
     * @flags CREATE_AND_SET
     * @default SAI_INSEG_ENTRY_PSC_TYPE_ELSP
     */
    SAI_INSEG_ENTRY_ATTR_PSC_TYPE,

    /**
     * @brief TC for a label.
     *
     * Associate TC by a label (override TC provided by QOS MAP)
     * Mainly used for L-LSP tunnels, where label infers TC and EXP infers COLOR
     *
     * @type sai_uint8_t
     * @flags CREATE_AND_SET
     * @default 0
     * @validonly SAI_INSEG_ENTRY_ATTR_PSC_TYPE == SAI_INSEG_ENTRY_PSC_TYPE_LLSP
     */
    SAI_INSEG_ENTRY_ATTR_QOS_TC,

    /**
     * @brief Enable EXP -> TC MAP on label.
     *
     * Associate TC by a QOS MAP
     * Mainly used for E-LSP tunnels, where EXP infers both TC and COLOR
     * Overrides SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_TC_MAP and SAI_PORT_ATTR_QOS_MPLS_EXP_TO_TC_MAP
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_QOS_MAP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     * @validonly SAI_INSEG_ENTRY_ATTR_PSC_TYPE == SAI_INSEG_ENTRY_PSC_TYPE_ELSP
     */
    SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP,

    /**
     * @brief Enable EXP -> COLOR MAP on label.
     *
     * Associate COLOR by a QOS MAP
     * Overrides SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP and SAI_PORT_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_QOS_MAP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP,

    /**
     * @brief Define TTL setting for PHP or POP
     *
     * @type sai_inseg_entry_pop_ttl_mode_t
     * @flags CREATE_AND_SET
     * @default SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM
     */
    SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE,

    /**
     * @brief Define QOS setting for PHP or POP
     *
     * @type sai_inseg_entry_pop_qos_mode_t
     * @flags CREATE_AND_SET
     * @default SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM
     */
    SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE,

    /**
     * @brief End of attributes
     */
    SAI_INSEG_ENTRY_ATTR_END,

    /** Custom range base value */
    SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_START = 0x10000000,

    /**
     * @brief The tunnel id
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_TUNNEL
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID,

    /**
     * @brief Fast Reroute nexthop group
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_NEXT_HOP_GROUP
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP,

    /**
     * @brief Fast Reroute configured Role in packet receiving direction
     * valid when SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP != NULL
     *
     * @type sai_inseg_entry_configured_role_t
     * @flags CREATE_AND_SET
     * @default SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY
     */
    SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE,

    /**
     * @brief Fast Reroute observed Role in packet receiving direction
     *
     * valid when SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP != NULL
     *
     * @type sai_inseg_entry_frr_observed_role_t
     * @flags READ_ONLY
     * @isresourcetype true
     */
    SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE,

    /**
     * @brief Fast Reroute observed Role inactive discard in receiving direction
     * validonly SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP != NULL
     *
     * @type bool
     * @flags CREATE_AND_SET
     * @default false
     */
    SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD,

    /**
     * @brief Attach a counter
     *
     * When it is empty, then packet hits won't be counted
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_COUNTER
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_COUNTER_ID,

    /**
     * @brief Attach/Detach policer to MPLS in-segment
     *
     * Set policer id = #SAI_NULL_OBJECT_ID to disable policer on MPLS in-segment.
     *
     * @type sai_object_id_t
     * @flags CREATE_AND_SET
     * @objects SAI_OBJECT_TYPE_POLICER
     * @allownull true
     * @default SAI_NULL_OBJECT_ID
     */
    SAI_INSEG_ENTRY_ATTR_POLICER_ID,

    /**
     * @brief Service id for MPLS in-segment entry
     *
     * used for H-QOS, set to service schedule group service id
     * set to 0 means disable H-QOS on MPLS label, usually used in PW label
     *
     * @type sai_uint16_t
     * @flags CREATE_AND_SET
     * @isvlan false
     * @default 0
     */
    SAI_INSEG_ENTRY_ATTR_SERVICE_ID,

    /** End of custom range base */
    SAI_INSEG_ENTRY_ATTR_CUSTOM_RANGE_END

} sai_inseg_entry_attr_t;

/**
 * @brief In segment entry
 */
typedef struct _sai_inseg_entry_t
{
    /**
     * @brief Switch ID
     *
     * @objects SAI_OBJECT_TYPE_SWITCH
     */
    sai_object_id_t switch_id;

    /**
     * @brief MPLS label
     */
    sai_label_id_t label;

} sai_inseg_entry_t;

/**
 * @brief Create In Segment entry
 *
 * @param[in] inseg_entry InSegment entry
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_create_inseg_entry_fn)(
        _In_ const sai_inseg_entry_t *inseg_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list);

/**
 * @brief Remove In Segment entry
 *
 * @param[in] inseg_entry InSegment entry
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_remove_inseg_entry_fn)(
        _In_ const sai_inseg_entry_t *inseg_entry);

/**
 * @brief Set In Segment attribute value
 *
 * @param[in] inseg_entry InSegment entry
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_set_inseg_entry_attribute_fn)(
        _In_ const sai_inseg_entry_t *inseg_entry,
        _In_ const sai_attribute_t *attr);

/**
 * @brief Get In Segment attribute value
 *
 * @param[in] inseg_entry InSegment entry
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
typedef sai_status_t (*sai_get_inseg_entry_attribute_fn)(
        _In_ const sai_inseg_entry_t *inseg_entry,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list);

/**
 * @brief MPLS methods table retrieved with sai_api_query()
 */
typedef struct _sai_mpls_api_t
{
    sai_create_inseg_entry_fn                      create_inseg_entry;
    sai_remove_inseg_entry_fn                      remove_inseg_entry;
    sai_set_inseg_entry_attribute_fn               set_inseg_entry_attribute;
    sai_get_inseg_entry_attribute_fn               get_inseg_entry_attribute;

} sai_mpls_api_t;

/**
 * @}
 */
#endif /** __SAIMPLS_H_ */
