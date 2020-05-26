/**
 @file ctc_sai_scheduler_group.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
This module defines SAI Scheduler Group.
\b
\p
 The Scheduler Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_scheduler_group                               |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_scheduler_group                               |    CTC8096,CTC7148,CTC7132     |
\t  |  set_scheduler_group_attribute                        |    CTC8096,CTC7148,CTC7132     |
\t  |  get_scheduler_group_attribute                        |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Scheduler Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_PORT_ID                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_LEVEL                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE                 |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_SCHEDULER_GROUP_H
#define _CTC_SAI_SCHEDULER_GROUP_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"


#define CTC_SAI_MAX_SCHED_LEVELS 3
#define CTC_SAI_SCHED_MAX_GRP_NUM 8
//#define CTC_SAI_SCHED_ETS_GRP_NUM 2
#define CTC_SAI_SCHED_PORT_GRP_NUM 4

#define CTC_SAI_PORT_SCHED_GROUP_NUM 4

typedef struct  ctc_sai_sched_group_db_s
{
    sai_object_id_t child_list[CTC_SAI_SCHED_MAX_GRP_NUM];
    uint32 child_cnt;
    uint8  child_type;//oid type
    sai_object_id_t parent_id;
    sai_object_id_t sched_id;
    uint8 max_childs;
}ctc_sai_sched_group_db_t;

sai_status_t
ctc_sai_scheduler_group_api_init();

sai_status_t
ctc_sai_scheduler_group_db_init(uint8 lchip);

sai_status_t
ctc_sai_scheduler_group_port_get_sched_group_list(sai_object_id_t port_id, sai_attribute_t *attr);

sai_status_t
ctc_sai_scheduler_group_port_get_sched_group_num(sai_object_id_t port_id, sai_attribute_t *attr);

sai_status_t
ctc_sai_scheduler_group_queue_set_scheduler(sai_object_id_t queue_id, const sai_attribute_t *attr);

void
ctc_sai_scheduler_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif


