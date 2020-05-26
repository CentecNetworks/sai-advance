/**
 @file ctc_sai_route.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI Route.
\b
\p
 The Route Module APIs supported by centec devices:
\p
\b
\t  |   API                                  |       SUPPORT CHIPS LIST       |
\t  |  create_route_entry                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_route_entry                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_route_entry_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_route_entry_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  create_route_entries                  |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_route_entries                  |    CTC8096,CTC7148,CTC7132     |
\t  |  set_route_entries_attribute           |    CTC8096,CTC7148,CTC7132     |
\t  |  get_route_entries_attribute           |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Route attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                            |       SUPPORT CHIPS LIST       |
\t  |  SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID     |              -                 |
\t  |  SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_ROUTE_ENTRY_ATTR_META_DATA        |         CTC7148,CTC7132        |
\t  |  SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY   |            CTC7132             |
\t  |  SAI_ROUTE_ENTRY_ATTR_COUNTER_ID       |            CTC7132             |
\b

*/

#ifndef _CTC_SAI_ROUTE_H
#define _CTC_SAI_ROUTE_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef struct  ctc_sai_route_s
{
    sai_packet_action_t action;
    sai_object_id_t nh_obj_id;
    uint16 cid;
    sai_object_id_t counter_obj_id;
}ctc_sai_route_t;


extern sai_status_t
ctc_sai_route_api_init();

extern sai_status_t
ctc_sai_route_db_init(uint8 lchip);

extern void
ctc_sai_route_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_ROUTE_H*/

