/**
 @file ctc_sai_scheduler.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
This module defines SAI Scheduler.
\b
\p
 The Scheduler Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_scheduler                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_scheduler                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  set_scheduler_attribute                              |    CTC8096,CTC7148,CTC7132     |
\t  |  get_scheduler_attribute                              |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Scheduler attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_SCHEDULER_ATTR_SCHEDULING_TYPE                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_METER_TYPE                        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE          |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Scheduler type supported by centec devices:
\p
\b
\t  |   SCHEDULER TYPE                                      |       SUPPORT CHIPS LIST       |
\t  |  SAI_SCHEDULING_TYPE_STRICT                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULING_TYPE_WRR                              |              -                 |
\t  |  SAI_SCHEDULING_TYPE_DWRR                             |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_SCHEDULER_H
#define _CTC_SAI_SCHEDULER_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

typedef struct  ctc_sai_scheduler_db_s
{
        uint8 sch_type;                 //refer to sai_scheduling_type_t
        uint8 weight;
        uint32 min_rate;                //cir
        uint32 min_burst_rate;          //cbs
        uint32 max_rate;                //pir
        uint32 max_burst_rate;          //pbs
        uint16 ref_cnt;
}ctc_sai_scheduler_db_t;


sai_status_t
ctc_sai_scheduler_api_init();

sai_status_t
ctc_sai_scheduler_db_init(uint8 lchip);

sai_status_t
ctc_sai_scheduler_port_set_scheduler(sai_object_id_t port_id, const sai_attribute_t *attr);

sai_status_t
ctc_sai_scheduler_queue_set_scheduler(sai_object_id_t queue_id, const sai_attribute_t *attr);

sai_status_t
ctc_sai_scheduler_group_set_scheduler(sai_object_id_t sch_group_id, const sai_attribute_t *attr);

void
ctc_sai_scheduler_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif

