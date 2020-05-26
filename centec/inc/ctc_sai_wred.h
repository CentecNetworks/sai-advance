/**
 @file ctc_sai_wred.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
This module defines SAI Wred.
\b
\p
 The Wred Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_wred                                          |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_wred                                          |    CTC8096,CTC7148,CTC7132     |
\t  |  set_wred_attribute                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  get_wred_attribute                                   |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Wred attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_WRED_ATTR_GREEN_ENABLE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_GREEN_MIN_THRESHOLD                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_GREEN_MAX_THRESHOLD                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_GREEN_DROP_PROBABILITY                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_YELLOW_ENABLE                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_RED_ENABLE                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_RED_MIN_THRESHOLD                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_RED_MAX_THRESHOLD                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_RED_DROP_PROBABILITY                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_WRED_ATTR_WEIGHT                                 |              -                 |
\t  |  SAI_WRED_ATTR_ECN_MARK_MODE                          |              -                 |
\t  |  SAI_WRED_ATTR_ECN_GREEN_MIN_THRESHOLD                |              -                 |
\t  |  SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD                |              -                 |
\t  |  SAI_WRED_ATTR_ECN_GREEN_MARK_PROBABILITY             |              -                 |
\t  |  SAI_WRED_ATTR_ECN_YELLOW_MIN_THRESHOLD               |              -                 |
\t  |  SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD               |              -                 |
\t  |  SAI_WRED_ATTR_ECN_YELLOW_MARK_PROBABILITY            |              -                 |
\t  |  SAI_WRED_ATTR_ECN_RED_MIN_THRESHOLD                  |              -                 |
\t  |  SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD                  |              -                 |
\t  |  SAI_WRED_ATTR_ECN_RED_MARK_PROBABILITY               |              -                 |
\t  |  SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MIN_THRESHOLD        |              -                 |
\t  |  SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MAX_THRESHOLD        |              -                 |
\t  |  SAI_WRED_ATTR_ECN_COLOR_UNAWARE_MARK_PROBABILITY     |              -                 |
\b
*/

#ifndef _CTC_SAI_WRED_H
#define _CTC_SAI_WRED_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"


typedef struct ctc_sai_wred_db_s
{
    uint8    color_en[3];
    uint16   min_th[3];         //refer to sai_packet_color_t
    uint16   max_th[3];         //refer to sai_packet_color_t
    uint16   drop_prob[3];      //refer to sai_packet_color_t
    uint16   used_cnt;
}ctc_sai_wred_db_t;


extern sai_status_t
ctc_sai_wred_api_init();

extern sai_status_t
ctc_sai_wred_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_wred_queue_set_wred(sai_object_id_t queue_id, uint32 wred_id, uint32 old_wred_id, bool enable);

extern void
ctc_sai_wred_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif /*_CTC_SAI_WRED_H*/




