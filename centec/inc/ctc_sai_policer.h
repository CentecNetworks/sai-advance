/**
 @file ctc_sai_policer.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
 This module defines SAI Policer.
\b
\p
 The Policer Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_policer                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_policer                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  set_policer_attribute                                |    CTC8096,CTC7148,CTC7132     |
\t  |  get_policer_attribute                                |    CTC8096,CTC7148,CTC7132     |
\t  |  get_policer_stats                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  get_policer_stats_ext                                |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_policer_stats                                  |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Policer attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_POLICER_ATTR_METER_TYPE                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_MODE                                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_COLOR_SOURCE                        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_CBS                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_CIR                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_PBS                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_PIR                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_GREEN_PACKET_ACTION                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_YELLOW_PACKET_ACTION                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_RED_PACKET_ACTION                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_ATTR_ENABLE_COUNTER_PACKET_ACTION_LIST   |              -                 |
\b
\p
 The Policer Stats supported by centec devices:
\p
\b
\t  |   STATS TYPE                                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_POLICER_STAT_PACKETS                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_ATTR_BYTES                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_GREEN_PACKETS                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_GREEN_BYTES                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_YELLOW_PACKETS                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_YELLOW_BYTES                        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_RED_PACKETS                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_POLICER_STAT_RED_BYTES                           |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_POLICER_H
#define _CTC_SAI_POLICER_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

#define CTC_SAI_POLICER_APPLY_DEFAULT 0xFFFFFFFF

enum ctc_sai_stmctl_type_e
{
    CTC_SAI_STMCTL_TYPE_FLOOD,
    CTC_SAI_STMCTL_TYPE_BCAST,
    CTC_SAI_STMCTL_TYPE_MCAST,
    CTC_SAI_STMCTL_TYPE_MAX
};
typedef enum ctc_sai_stmctl_type_e ctc_sai_stmctl_type_t;

typedef struct ctc_sai_policer_db_s
{
    uint8 meter_type;         /*SAI_POLICER_ATTR_METER_TYPE*/
    uint8 mode;               /*sai_policer_mode_t*/
    uint8 color_source;
    uint8 action[3]; /*refer to sai_packet_color_t*/
    uint32 cbs;
    uint32 cir;
    uint32 pbs;
    uint32 pir;
    union
    {
        uint32 port_id;  /*CTC_QOS_POLICER_TYPE_PORT*/
        uint32 entry_id; /*CTC_QOS_POLICER_TYPE_FLOW*/
    }id;
    uint8  type; /*refer to ctc_qos_policer_type_t*/
}ctc_sai_policer_db_t;


extern sai_status_t
ctc_sai_policer_api_init();

extern sai_status_t
ctc_sai_policer_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_policer_port_set_policer(uint8 lchip, uint32 gport, uint32 policer_id, bool enable);

extern sai_status_t
ctc_sai_policer_acl_set_policer(uint8 lchip, uint32 entry_id, uint32 policer_id, bool enable);

extern sai_status_t
ctc_sai_policer_port_set_stmctl(uint8 lchip, uint32 gport, uint32 policer_id, ctc_sai_stmctl_type_t stm_type, bool enable);

extern sai_status_t
ctc_sai_policer_set_copp_policer(uint8 lchip, uint32 policer_id, bool enable);

extern sai_status_t
ctc_sai_policer_revert_policer(uint8 lchip, uint32 policer_id);

extern void
ctc_sai_policer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_POLICER_H*/


