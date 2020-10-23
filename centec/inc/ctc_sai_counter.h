/**
 @file ctc_sai_counter.h

 @author  Copyright (C) 2019 Centec Networks Inc.  All rights reserved.

 @date 2019-12-10

 @version v2.0

\p
 This module defines SAI Hostif.
\b
\p
 The Hostif Module APIs supported by centec devices:
\p
\b
\t  |   API                                          |       SUPPORT CHIPS LIST       |
\t  |  create_counter                                |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_counter                                |    CTC8096,CTC7148,CTC7132     |
\t  |  set_counter_attribute                         |    CTC8096,CTC7148,CTC7132     |
\t  |  get_counter_attribute                         |    CTC8096,CTC7148,CTC7132     |
\t  |  get_counter_stats                             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_counter_stats_ext                         |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_counter_stats                           |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Counter attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_COUNTER_ATTR_TYPE                                |    CTC8096,CTC7148,CTC7132     |
\b
*/



#ifndef _CTC_SAI_COUNTER_H
#define _CTC_SAI_COUNTER_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef enum ctc_sai_counter_type_s
{
    CTC_SAI_COUNTER_TYPE_ROUTE = 0,
    CTC_SAI_COUNTER_TYPE_NEXTHOP,
    CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW,
    CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP,
    CTC_SAI_COUNTER_TYPE_ECMP,
    CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW,
    CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP,
    CTC_SAI_COUNTER_TYPE_TUNNEL_IGS,
    CTC_SAI_COUNTER_TYPE_TUNNEL_EGS,
    CTC_SAI_COUNTER_TYPE_HOSTIF,
    CTC_SAI_COUNTER_TYPE_MAX,

} ctc_sai_counter_type_t;

typedef struct ctc_sai_hostif_trap_queue_s
{
    uint16 queue_id;
    uint16 cpu_reason;
} ctc_sai_hostif_trap_queue_t;

typedef struct ctc_sai_counter_s
{
    sai_counter_type_t counter_type;
    ctc_sai_counter_type_t ctc_sai_counter_type;

    uint64 packet_count;
    uint64 byte_count;

    uint8  is_trap_stats;
    uint32 ref_cnt;
    union
    {
        uint32 stats_id;
        ctc_sai_hostif_trap_queue_t hostif_queue;
    }statsinfo;
} ctc_sai_counter_t;

extern sai_status_t
ctc_sai_counter_api_init();

extern sai_status_t
ctc_sai_counter_db_init(uint8 lchip);

extern void
ctc_sai_counter_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_counter_id_hostif_trap_create(sai_object_id_t counter_id, ctc_sai_counter_type_t ctc_sai_counter_type, uint16 cpu_reason, uint16 queue_id);

extern sai_status_t
ctc_sai_counter_id_hostif_trap_remove(sai_object_id_t counter_id, ctc_sai_counter_type_t ctc_sai_counter_type);

extern sai_status_t
ctc_sai_counter_id_create(sai_object_id_t counter_id, ctc_sai_counter_type_t ctc_sai_counter_type, uint32* stats_id);

extern sai_status_t
ctc_sai_counter_id_remove(sai_object_id_t counter_id, ctc_sai_counter_type_t ctc_sai_counter_type);

extern sai_status_t
ctc_sai_counter_init_resource(uint8 lchip);

#endif
