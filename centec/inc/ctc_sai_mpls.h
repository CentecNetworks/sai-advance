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
\t  |  SAI_INSEG_ENTRY_ATTR_PSC_TYPE                        |            CTC7132             |
\t  |  SAI_INSEG_ENTRY_ATTR_QOS_TC                          |            CTC7132             |
\t  |  SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP              |            CTC7132             |
\t  |  SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP           |            CTC7132             |
\t  |  SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE                    |            CTC7132             |
\t  |  SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE                    |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID                 |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP                     |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE             |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE               |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD         |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_COUNTER_ID                      |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_POLICER_ID                      |            CTC7132             |
\e  |  SAI_INSEG_ENTRY_ATTR_SERVICE_ID                      |            CTC7132             |
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
    uint8 pop;
    sai_packet_action_t action;
    sai_object_id_t nexthop_oid;
    sai_object_id_t decap_tunnel_oid;
    sai_object_id_t frr_nhp_grp_oid;
    sai_object_id_t counter_oid;
    uint8 frr_configured_role;
    bool frr_rx_discard;
    bool is_es;
    uint8 pop_ttl_mode;
    uint8 pop_qos_mode;
    uint8 psc_type;
    uint8 qos_tc;
    uint8 exp_to_tc_map_id;
    uint8 exp_to_color_map_id;
    uint8 qos_domain_id;
    uint32 policer_id;
    uint16 service_id;  //only for insegment with tunnel(pw label)

}ctc_sai_mpls_t;

typedef enum _sai_mpls_db_op_t
{
    SAI_MPLS_DB_OP_ADD,
    SAI_MPLS_DB_OP_DEL,

    SAI_MPLS_DB_OP_END
} sai_mpls_db_op_t;


extern sai_status_t
ctc_sai_mpls_api_init();
extern sai_status_t
ctc_sai_mpls_db_init(uint8 lchip);
extern void
ctc_sai_mpls_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_mpls_db_op(uint8 lchip, uint8 db_op, const sai_inseg_entry_t *inseg_entry, ctc_sai_mpls_t** mpls_property);

#endif /*_CTC_SAI_MPLS_H*/

