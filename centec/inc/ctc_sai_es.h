/**
 @file ctc_sai_es.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2020-04-09

 @version v1.0

\p
This module defines SAI Ethernet Segment.
\b
\p
 The Ethernet Segment Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |       SUPPORT CHIPS LIST       |
\e  |  create_es                                                |        CTC7132,CTC8180         |
\e  |  remove_es                                                |        CTC7132,CTC8180         |
\e  |  get_es_attribute                                         |        CTC7132,CTC8180         |
\b
\p
 The Ethernet Segment attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\e  |  SAI_ES_ATTR_ESI_LABEL                                    |        CTC7132,CTC8180         |
\b
*/

#ifndef _CTC_SAI_ES_H
#define _CTC_SAI_ES_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef struct ctc_sai_es_s
{
    uint32        local_es_id;
    uint32        esi_label;
    int32         ref_cnt;
}ctc_sai_es_t;


extern sai_status_t
ctc_sai_es_api_init();

extern sai_status_t
ctc_sai_es_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_es_db_deinit(uint8 lchip);

extern void
ctc_sai_es_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif  /*_CTC_SAI_ES_H*/

