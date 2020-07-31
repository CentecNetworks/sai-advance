
/**
 @file ctc_sai_synce.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-06-21

 @version v2.0

\p
 This module defines SAI SynvE.
\b
\p
 The SyncE Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\t  |  create_synce;                                            |        CTC7132         |
\t  |  set_synce_attribute;                                     |        CTC7132         |
\t  |  remove_synce;                                            |        CTC7132         |
\t  |  get_synce_attribute;                                     |        CTC7132         |
\b
\p
 The synce attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_SYNCE_ATTR_CLOCK_ID                                  |        CTC7132         |
\t  |  SAI_SYNCE_ATTR_RECOVERED_PORT                            |        CTC7132         |
\t  |  SAI_SYNCE_ATTR_CLOCK_DIVIDER                             |        CTC7132         |
\t  |  SAI_SYNCE_ATTR_CLOCK_OUTPUT_ENABLE                       |        CTC7132         |
\t  |  SAI_SYNCE_ATTR_LINK_DETECT_ENABLE                        |        CTC7132         |
\b
*/

#ifndef _CTC_SAI_SYNCE_H
#define _CTC_SAI_SYNCE_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

typedef struct ctc_sai_synce_db_s
{
    uint16  recovered_clock_lport;
    
} ctc_sai_synce_db_t;

extern sai_status_t
ctc_sai_synce_api_init();


#endif /*_CTC_SAI_SYNCE_H*/
