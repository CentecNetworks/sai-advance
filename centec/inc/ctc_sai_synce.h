
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
\e  |  create_synce;                                            |    CTC7132,CTC8180     |
\e  |  remove_synce;                                            |    CTC7132,CTC8180     |
\e  |  set_synce_attribute;                                     |    CTC7132,CTC8180     |
\e  |  get_synce_attribute;                                     |    CTC7132,CTC8180     |
\p
 The synce attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\e  |  SAI_SYNCE_ATTR_CLOCK_ID                                  |    CTC7132,CTC8180     |
\e  |  SAI_SYNCE_ATTR_RECOVERED_PORT                            |    CTC7132,CTC8180     |
\e  |  SAI_SYNCE_ATTR_CLOCK_DIVIDER                             |    CTC7132,CTC8180     |
\e  |  SAI_SYNCE_ATTR_CLOCK_OUTPUT_ENABLE                       |    CTC7132,CTC8180     |
\e  |  SAI_SYNCE_ATTR_LINK_DETECT_ENABLE                        |    CTC7132,CTC8180     |
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

extern sai_status_t
ctc_sai_synce_db_init(uint8 lchip);



#endif /*_CTC_SAI_SYNCE_H*/
