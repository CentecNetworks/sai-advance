/**
 @file ctc_sai_virtual_router.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI Virtual Router.
\b
\p
 The Virtual Router Module APIs supported by centec devices:
\p
\b
\t  |   API                                               |           SUPPORT CHIPS LIST           |
\t  |  create_virtual_router                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_virtual_router                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_virtual_router_attribute                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_virtual_router_attribute                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Virtual Router attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                   |           SUPPORT CHIPS LIST           |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION         |                  -                     |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION   |                  -                     |
\t  |  SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION   |                  -                     |
\b
*/

#ifndef _CTC_SAI_VIRTUAL_ROUTER_H
#define _CTC_SAI_VIRTUAL_ROUTER_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef struct  ctc_sai_virtual_router_s
{
   sai_mac_t src_mac;
   uint8 v4_state;
   uint8 v6_state;
}ctc_sai_virtual_router_t;


extern sai_status_t
ctc_sai_virtual_router_api_init();

extern sai_status_t
ctc_sai_virtual_router_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_virtual_router_get_vr_info(sai_object_id_t virtual_router_id, uint8* v4_state, uint8* v6_state,  sai_mac_t src_mac);

extern void
ctc_sai_virtual_router_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);


#endif /*_CTC_SAI_VIRTUAL_ROUTER_H*/

