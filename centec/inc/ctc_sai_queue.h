/**
 @file ctc_sai_queue.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0


\p
This module defines SAI Queue.
\b
\p
 The Queue Module APIs supported by centec devices:
\p
\b
\t  |   API                                                |       SUPPORT CHIPS LIST       |
\t  |  create_queue                                        |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_queue                                        |    CTC8096,CTC7148,CTC7132     |
\t  |  set_queue_attribute                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  get_queue_attribute                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  get_queue_stats                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  get_queue_stats_ext                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_queue_stats                                   |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Queue attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_QUEUE_ATTR_TYPE                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_PORT                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_INDEX                                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_WRED_PROFILE_ID                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_BUFFER_PROFILE_ID                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_ATTR_PAUSE_STATUS                         |              -                 |
\t  |  SAI_QUEUE_ATTR_ENABLE_PFC_DLDR                      |              -                 |
\b
\p
 The Queue Stats supported by centec devices:
\p
\b
\t  |   STATS TYPE                                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_QUEUE_STAT_PACKETS                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_STAT_BYTES                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_STAT_DROPPED_PACKETS                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_STAT_DROPPED_BYTES                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QUEUE_STAT_GREEN_PACKETS                         |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_BYTES                           |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_DROPPED_PACKETS                 |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_DROPPED_BYTES                   |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_PACKETS                        |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_BYTES                          |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_DROPPED_PACKETS                |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_DROPPED_BYTES                  |              -                 |
\t  |  SAI_QUEUE_STAT_RED_PACKETS                           |              -                 |
\t  |  SAI_QUEUE_STAT_RED_BYTES                             |              -                 |
\t  |  SAI_QUEUE_STAT_RED_DROPPED_PACKETS                   |              -                 |
\t  |  SAI_QUEUE_STAT_RED_DROPPED_BYTES                     |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_WRED_DROPPED_PACKETS            |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_WRED_DROPPED_BYTES              |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_PACKETS           |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_WRED_DROPPED_BYTES             |              -                 |
\t  |  SAI_QUEUE_STAT_RED_WRED_DROPPED_PACKETS              |              -                 |
\t  |  SAI_QUEUE_STAT_RED_WRED_DROPPED_BYTES                |              -                 |
\t  |  SAI_QUEUE_STAT_WRED_DROPPED_PACKETS                  |              -                 |
\t  |  SAI_QUEUE_STAT_WRED_DROPPED_BYTES                    |              -                 |
\t  |  SAI_QUEUE_STAT_CURR_OCCUPANCY_BYTES                  |              -                 |
\t  |  SAI_QUEUE_STAT_WATERMARK_BYTES                       |              -                 |
\t  |  SAI_QUEUE_STAT_SHARED_CURR_OCCUPANCY_BYTES           |              -                 |
\t  |  SAI_QUEUE_STAT_SHARED_WATERMARK_BYTES                |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_PACKETS         |              -                 |
\t  |  SAI_QUEUE_STAT_GREEN_WRED_ECN_MARKED_BYTES           |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_PACKETS        |              -                 |
\t  |  SAI_QUEUE_STAT_YELLOW_WRED_ECN_MARKED_BYTES          |              -                 |
\t  |  SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_PACKETS           |              -                 |
\t  |  SAI_QUEUE_STAT_RED_WRED_ECN_MARKED_BYTES             |              -                 |
\t  |  SAI_QUEUE_STAT_WRED_ECN_MARKED_PACKETS               |              -                 |
\t  |  SAI_QUEUE_STAT_WRED_ECN_MARKED_BYTES                 |              -                 |
\b
*/

#ifndef _CTC_SAI_QUEUE_H
#define _CTC_SAI_QUEUE_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"


#define CTC_QOS_BASIC_Q_NUM 8

//GG:4 D2:1
#define CTC_QOS_16Q_MCAST_Q_NUM ((ctcs_get_chip_type(lchip) == CTC_CHIP_GOLDENGATE) ? 4 : 1)

typedef struct ctc_sai_queue_db_s
{
    sai_object_id_t sch_grp;
    uint32  wred_id;
    uint32  buf_id;
    uint32  sch_id;
}ctc_sai_queue_db_t;


typedef enum ctc_sai_queue_set_type_e
{
    CTC_SAI_Q_SET_TYPE_WRED = 0,
    CTC_SAI_Q_SET_TYPE_BUFFER = 1,
    CTC_SAI_Q_SET_TYPE_MAX
}ctc_sai_queue_set_type_t;

typedef struct  ctc_sai_queue_traverse_param_s
{
   uint8 lchip;
   ctc_sai_queue_set_type_t set_type;
   uint32* cmp_value;
   void* p_value;
}ctc_sai_queue_traverse_param_t;


extern sai_status_t
ctc_sai_queue_api_init();

extern sai_status_t
ctc_sai_queue_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_queue_traverse_set(ctc_sai_queue_traverse_param_t* p_param);

extern sai_status_t
ctc_sai_queue_port_get_queue_num(sai_object_id_t port_id, uint32* queue_num);

extern sai_status_t
ctc_sai_queue_port_get_queue_list(sai_object_id_t port_id, sai_attribute_t* attr);

extern void
ctc_sai_queue_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif /*_CTC_SAI_QUEUE_H*/



