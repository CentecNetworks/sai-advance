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

typedef struct  ctc_sai_next_hop_grp_s
{
    sai_object_id_t w_nh_oid;/*member nexthop id*/
    sai_object_id_t p_nh_oid;/*member nexthop id*/
    sai_object_id_t w_member_oid; /*member oid id*/
    sai_object_id_t p_member_oid; /*member oid id*/
    sai_object_id_t counter_oid;
    uint16        logic_port;
    uint32 rx_label_primary;
    uint32 rx_label_standby;
    uint8 aps_nh_created;
    ctc_nh_aps_type_t aps_nh_type;
    uint32 aps_tunnel_id; /*when member is mpls tunnel, use aps tunnel id in Centec SDK */
}ctc_sai_next_hop_grp_t;

typedef struct  ctc_sai_next_hop_grp_member_s
{
    sai_object_id_t nh_grp_oid;/*group nexthop id*/
}ctc_sai_next_hop_grp_member_t;

extern sai_status_t
ctc_sai_next_hop_group_api_init();

extern sai_status_t
ctc_sai_next_hop_group_db_init(uint8 lchip);

extern void
ctc_sai_next_hop_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_NEXT_HOP_GROUP_H*/

