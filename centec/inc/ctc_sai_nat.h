/**
 @file ctc_sai_nat.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI Route.
\b
\p
 The NAT Module APIs supported by centec devices:
\p
\b
\t  |   API                                  |       SUPPORT CHIPS LIST       |
\t  |  create_nat_entry                     |           CTC7132              |
\t  |  remove_nat_entry                     |           CTC7132              |
\t  |  set_nat_entry_attribute              |           CTC7132              |
\t  |  get_nat_entry_attribute              |           CTC7132              |
\t  |  create_nat_entries                   |           CTC7132              |
\t  |  remove_nat_entries                   |           CTC7132              |
\t  |  set_nat_entries_attribute            |           CTC7132              |
\t  |  get_nat_entries_attribute            |           CTC7132              |
\t  |  create_nat_zone_counter              |              -                 |
\t  |  remove_nat_zone_counter              |              -                 |
\t  |  set_nat_zone_counter_attribute       |              -                 |
\t  |  get_nat_zone_counter_attribute       |              -                 |


\b
\p
 The NAT attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                            |       SUPPORT CHIPS LIST       |
\t  |  SAI_NAT_ENTRY_ATTR_NAT_TYPE           |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_SRC_IP             |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_SRC_IP_MASK        |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_VR_ID              |               -                |
\t  |  SAI_NAT_ENTRY_ATTR_DST_IP             |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_DST_IP_MASK        |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_L4_SRC_PORT        |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_L4_DST_PORT        |            CTC7132             |
\t  |  SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT|               -                |
\t  |  SAI_NAT_ENTRY_ATTR_PACKET_COUNT       |               -                |
\t  |  SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT  |               -                |
\t  |  SAI_NAT_ENTRY_ATTR_BYTE_COUNT         |               -                |
\t  |  SAI_NAT_ENTRY_ATTR_HIT_BIT_COR        |               -                |
\t  |  SAI_NAT_ENTRY_ATTR_HIT_BIT            |            CTC7132             |
\e  |  SAI_NAT_ENTRY_ATTR_CUSTOM_DNAT_REROUTE|            CTC7132             |
\b

*/


#ifndef _CTC_SAI_NAT_H
#define _CTC_SAI_NAT_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

#define CTC_SAI_CNT_DNAT 0 
#define CTC_SAI_CNT_SNAT 1

typedef struct ctc_sai_nat_s
{
    sai_nat_type_t nat_type; 
    uint32 nh_id;
    bool dnat_reroute;
    ip_addr_t new_ipsa;
    uint16    new_l4_src_port; 
} ctc_sai_nat_t;

#endif /*_CTC_SAI_NAT_H*/

extern sai_status_t
ctc_sai_nat_api_init();

extern sai_status_t
ctc_sai_nat_db_init(uint8 lchip);

extern void 
ctc_sai_nat_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);


