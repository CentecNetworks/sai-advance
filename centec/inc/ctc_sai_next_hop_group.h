/**
 @file ctc_sai_next_hop_group.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
 This module defines SAI Next Hop Group.
\b
\p
 The Next Hop Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                       |       SUPPORT CHIPS LIST       |
\t  |  create_next_hop_group                      |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_next_hop_group                      |    CTC8096,CTC7148,CTC7132     |
\t  |  set_next_hop_group_attribute               |    CTC8096,CTC7148,CTC7132     |
\t  |  get_next_hop_group_attribute               |    CTC8096,CTC7148,CTC7132     |
\t  |  create_next_hop_group_member               |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_next_hop_group_member               |    CTC8096,CTC7148,CTC7132     |
\t  |  set_next_hop_group_member_attribute        |    CTC8096,CTC7148,CTC7132     |
\t  |  get_next_hop_group_member_attribute        |    CTC8096,CTC7148,CTC7132     |
\t  |  create_next_hop_group_members              |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_next_hop_group_members              |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Next Hop Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                   |       SUPPORT CHIPS LIST       |
\t  |  SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NEXT_HOP_GROUP_ATTR_TYPE                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER       |        CTC7148,CTC7132         |
\t  |  SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID           |            CTC7132             |
\b
\p
 The Next Hop Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                       |       SUPPORT CHIPS LIST       |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT            |              -                 |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE   |        CTC7148,CTC7132         |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE     |        CTC7148 ,CTC7132        |
\t  |  SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT  |              -                 |
\b

*/

#ifndef _CTC_SAI_NEXT_HOP_GROUP_H
#define _CTC_SAI_NEXT_HOP_GROUP_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/


extern sai_status_t
ctc_sai_next_hop_group_api_init();

extern sai_status_t
ctc_sai_next_hop_group_db_init(uint8 lchip);

extern void
ctc_sai_next_hop_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_NEXT_HOP_GROUP_H*/

