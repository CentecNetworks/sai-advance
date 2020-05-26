/**
 @file ctc_sai_mpls.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI MPLS.
\b
\p
 The MPLS Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_inseg_entry                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_inseg_entry                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  set_inseg_entry_attribute                            |    CTC8096,CTC7148,CTC7132     |
\t  |  get_inseg_entry_attribute                            |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The MPLS attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_INSEG_ENTRY_ATTR_NUM_OF_POP                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_INSEG_ENTRY_ATTR_PACKET_ACTION                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY                   |              -                 |
\t  |  SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_INSEG_ENTRY_ATTR_TUNNEL_ID                       |    CTC8096,CTC7148,CTC7132     |
\b

*/

#ifndef _CTC_SAI_MPLS_H
#define _CTC_SAI_MPLS_H

#include "ctc_mpls.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/
typedef struct  ctc_sai_mpls_s
{
    sai_packet_action_t action;
    sai_object_id_t nexthop_oid;
    sai_object_id_t decap_tunnel_oid;
}ctc_sai_mpls_t;


extern sai_status_t
ctc_sai_mpls_api_init();
extern sai_status_t
ctc_sai_mpls_db_init(uint8 lchip);
extern void
ctc_sai_mpls_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
_ctc_sai_mpls_get_ctc_nh_id(sai_packet_action_t action, sai_object_id_t nexthop_oid, uint32* p_ctc_nh_id, ctc_mpls_ilm_t* p_ctc_mpls_ilm);
#endif /*_CTC_SAI_MPLS_H*/

