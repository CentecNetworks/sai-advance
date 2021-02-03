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
\t  |   API                                                 |           SUPPORT CHIPS LIST           |
\t  |  create_scheduler_group                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_scheduler_group                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_scheduler_group_attribute                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_scheduler_group_attribute                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Scheduler Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |           SUPPORT CHIPS LIST           |
\t  |  SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_PORT_ID                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_LEVEL                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\e  |  SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID                  |            CTC7132,CTC8180             |
\b
*/

#ifndef _CTC_SAI_SCHEDULER_GROUP_H
#define _CTC_SAI_SCHEDULER_GROUP_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"


#define CTC_SAI_MAX_SCHED_LEVELS 2
#define CTC_SAI_MAX_SCHED_LEVELS_TMM 5
#define CTC_SAI_SCHED_MAX_GRP_NUM 8
#define CTC_SAI_SCHED_ETS_GRP_NUM 3
#define CTC_SAI_SCHED_SERVICE_GRP_NUM 64
#define CTC_SAI_SCHED_PORT_GRP_NUM 4

//service L0,L1,L2,L3,L4 support 64(1 per port),128, 256, 384, 1216 sch group
#define CTC_SAI_SCHED_PORT_GRP_NUM_TMM 12 //8 level5 basic group + 4 level1 service group
#define CTC_SAI_SCHED_GRP_LEVEL1_MAX_CHILD_NUM_TMM 255  //uint8,sdk max child number is 512 128*4
#define CTC_SAI_SCHED_GRP_LEVEL2_MAX_CHILD_NUM_TMM 255  //uint8,sdk max child number is 1024 256*4
#define CTC_SAI_SCHED_GRP_LEVEL3_MAX_CHILD_NUM_TMM 255  //uint8,sdk max child number is 1536 384*4
#define CTC_SAI_SCHED_GRP_LEVEL4_MAX_CHILD_NUM_TMM 255  //uint8,sdk max child number is 7525 944*8



#define CTC_SAI_PORT_SCHED_GROUP_NUM 4


typedef struct  ctc_sai_sched_group_child_id_s
{
   ctc_slistnode_t node;
   sai_object_id_t child_id;
}ctc_sai_sched_group_child_id_t;

typedef struct  ctc_sai_sched_group_db_s
{
    ctc_slist_t *child_list_head;
    uint32 child_cnt;
    uint8  child_type;//oid type
    sai_object_id_t parent_id;
    sai_object_id_t sched_id;
    uint8 max_childs;
    uint16 service_id;
    uint32  ctc_sche_group;
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

sai_status_t
ctc_sai_scheduler_group_set_ctc_group_parent_and_class(uint8 lchip, uint32 ctc_sche_group, sai_object_id_t parent_oid);

sai_status_t
ctc_sai_scheduler_group_set_ctc_weight_and_shaping(uint8 lchip, uint8 level,uint16 group_index, uint32 ctc_sche_group, sai_object_id_t scheduler_oid, bool is_set);

uint16
ctc_sai_scheduler_group_get_group_index_base(uint8 lchip, uint16 service_id);

void
ctc_sai_scheduler_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif


