/**
 @file ctc_sai_buffer.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
 This module defines SAI Buffer.
\b
\p
 The Scheduler Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                          |       SUPPORT CHIPS LIST       |
\t  |  create_buffer_pool                            |              -                 |
\t  |  remove_buffer_pool                            |              -                 |
\t  |  set_buffer_pool_attribute                     |              -                 |
\t  |  get_buffer_pool_attribute                     |              -                 |
\t  |  get_buffer_pool_stats                         |              -                 |
\t  |  get_buffer_pool_stats_ext                     |              -                 |
\t  |  clear_buffer_pool_stats                       |              -                 |
\t  |  create_ingress_priority_group                 |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_ingress_priority_group                 |    CTC8096,CTC7148,CTC7132     |
\t  |  set_ingress_priority_group_attribute          |    CTC8096,CTC7148,CTC7132     |
\t  |  get_ingress_priority_group_attribute          |    CTC8096,CTC7148,CTC7132     |
\t  |  get_ingress_priority_group_stats              |              -                 |
\t  |  get_ingress_priority_group_stats_ext          |              -                 |
\t  |  clear_ingress_priority_group_stats            |              -                 |
\t  |  create_buffer_profile                         |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_buffer_profile                         |    CTC8096,CTC7148,CTC7132     |
\t  |  set_buffer_profile_attribute                  |    CTC8096,CTC7148,CTC7132     |
\t  |  get_buffer_profile_attribute                  |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Buffer Pool attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_BUFFER_POOL_ATTR_SHARED_SIZE                     |              -                 |
\t  |  SAI_BUFFER_POOL_ATTR_TYPE                            |              -                 |
\t  |  SAI_BUFFER_POOL_ATTR_SIZE                            |              -                 |
\t  |  SAI_BUFFER_POOL_ATTR_THRESHOLD_MODE                  |              -                 |
\t  |  SAI_BUFFER_POOL_ATTR_XOFF_SIZE                       |              -                 |
\t  |  SAI_BUFFER_POOL_ATTR_WRED_PROFILE_ID                 |              -                 |
\b
\p
 The Buffer Pool Threshold Mode supported by centec devices:
\p
\b
\t  |   MODE                                                |   SUPPORT CHIPS LIST   |
\t  |  SAI_BUFFER_POOL_THRESHOLD_MODE_STATIC                |           -            |
\t  |  SAI_BUFFER_POOL_THRESHOLD_MODE_DYNAMIC               |           -            |
\b
\p
 The Buffer Pool Type supported by centec devices:
\p
\b
\t  |   POOL TYPE                                           |   SUPPORT CHIPS LIST   |
\t  |  SAI_BUFFER_POOL_TYPE_INGRESS                         |           -            |
\t  |  SAI_BUFFER_POOL_TYPE_EGRESS                          |           -            |
\b
\p
 The Buffer Pool Stats supported by centec devices:
\p
\b
\t  |   POOL Stats                                          |   SUPPORT CHIPS LIST   |
\t  |  SAI_BUFFER_POOL_STAT_CURR_OCCUPANCY_BYTES            |           -            |
\t  |  SAI_BUFFER_POOL_STAT_WATERMARK_BYTES                 |           -            |
\t  |  SAI_BUFFER_POOL_STAT_DROPPED_PACKETS                 |           -            |
\t  |  SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_PACKETS      |           -            |
\t  |  SAI_BUFFER_POOL_STAT_GREEN_WRED_DROPPED_BYTES        |           -            |
\t  |  SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_PACKETS     |           -            |
\t  |  SAI_BUFFER_POOL_STAT_YELLOW_WRED_DROPPED_BYTES       |           -            |
\t  |  SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_PACKETS        |           -            |
\t  |  SAI_BUFFER_POOL_STAT_RED_WRED_DROPPED_BYTES          |           -            |
\t  |  SAI_BUFFER_POOL_STAT_WRED_DROPPED_PACKETS            |           -            |
\t  |  SAI_BUFFER_POOL_STAT_WRED_DROPPED_BYTES              |           -            |
\t  |  SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_PACKETS   |           -            |
\t  |  SAI_BUFFER_POOL_STAT_GREEN_WRED_ECN_MARKED_BYTES     |           -            |
\t  |  SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_PACKETS  |           -            |
\t  |  SAI_BUFFER_POOL_STAT_YELLOW_WRED_ECN_MARKED_BYTES    |           -            |
\t  |  SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_PACKETS     |           -            |
\t  |  SAI_BUFFER_POOL_STAT_RED_WRED_ECN_MARKED_BYTES       |           -            |
\t  |  SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_PACKETS         |           -            |
\t  |  SAI_BUFFER_POOL_STAT_WRED_ECN_MARKED_BYTES           |           -            |
\b
\p
 The Buffer Profile attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_BUFFER_PROFILE_ATTR_POOL_ID                      |              -                 |
\t  |  SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE         |              -                 |
\t  |  SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_BUFFER_PROFILE_ATTR_XOFF_TH                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_BUFFER_PROFILE_ATTR_XON_TH                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH                |              -                 |
\b
\p
 The Buffer Profile Threshold Mode supported by centec devices:
\p
\b
\t  |   MODE                                                |   SUPPORT CHIPS LIST   |
\t  |  SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC             |           -            |
\t  |  SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC            |           -            |
\b
\p
 The Ingress Priority Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX                |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Ingress Priority Group stats supported by centec devices:
\p
\b
\t  |    Ingress Priority Group Stats                                   |   SUPPORT CHIPS LIST   |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_PACKETS                          |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_BYTES                            |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_CURR_OCCUPANCY_BYTES             |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_WATERMARK_BYTES                  |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_CURR_OCCUPANCY_BYTES      |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_SHARED_WATERMARK_BYTES           |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_CURR_OCCUPANCY_BYTES   |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_XOFF_ROOM_WATERMARK_BYTES        |           -            |
\t  |  SAI_INGRESS_PRIORITY_GROUP_STAT_DROPPED_PACKETS                  |           -            |
\b
*/

#ifndef _CTC_SAI_BUFFER_H
#define _CTC_SAI_BUFFER_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"



sai_status_t
ctc_sai_buffer_api_init();

sai_status_t
ctc_sai_buffer_db_init(uint8 lchip);

sai_status_t
ctc_sai_buffer_queue_set_profile(sai_object_id_t queue_id, const sai_attribute_t* attr);

sai_status_t
ctc_sai_buffer_ingress_pg_set_profile(sai_object_id_t ingress_pg_id, const sai_attribute_t* attr);

sai_status_t
ctc_sai_buffer_port_get_ingress_pg_num(sai_object_id_t port_id, sai_attribute_t* attr);

sai_status_t
ctc_sai_buffer_port_get_ingress_pg_list(sai_object_id_t port_id, sai_attribute_t* attr);


void
ctc_sai_buffer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif



