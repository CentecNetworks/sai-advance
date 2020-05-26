/**
 @file ctc_sai_segmentroute.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-04-28

 @version v2.0

\p
 This module defines SAI Segmentroute.
\b
\p
 The TAM Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\t  |  create_segmentroute_sidlist                              |           -            |
\t  |  remove_segmentroute_sidlist                              |           -            |
\t  |  set_segmentroute_sidlist_attribute                       |           -            |
\t  |  get_segmentroute_sidlist_attribute                       |           -            |
\t  |  create_segmentroute_sidlists                             |           -            |
\t  |  remove_segmentroute_sidlists                             |           -            |
\b
\p
 The TAM Sidlist attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_SEGMENTROUTE_SIDLIST_ATTR_TYPE                       |           -            |
\t  |  SAI_SEGMENTROUTE_SIDLIST_ATTR_TLV_LIST                   |           -            |
\t  |  SAI_SEGMENTROUTE_SIDLIST_ATTR_SEGMENT_LIST               |           -            |
\b
*/

#ifndef _CTC_SAI_SEGMENTROUTE_H
#define _CTC_SAI_SEGMENTROUTE_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/


extern sai_status_t
ctc_sai_segmentroute_api_init();

extern sai_status_t
ctc_sai_segmentroute_db_init(uint8 lchip);

#endif /*_CTC_SAI_SEGMENTROUTE_H*/

