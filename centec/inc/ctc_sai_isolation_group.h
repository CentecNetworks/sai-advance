/**
 @file ctc_sai_isolation_group.h

 @author  Copyright (C) 2019 Centec Networks Inc.  All rights reserved.

 @date 2019-04-22

 @version v2.0

\p
This module defines SAI Isolation Group.
\b
\p
 The Isolation Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                               |       SUPPORT CHIPS LIST       |
\t  |  create_isolation_group                             |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_isolation_group                             |    CTC8096,CTC7148,CTC7132     |
\t  |  set_isolation_group_attribute                      |    CTC8096,CTC7148,CTC7132     |
\t  |  get_isolation_group_attribute                      |    CTC8096,CTC7148,CTC7132     |
\t  |  create_isolation_group_member                      |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_isolation_group_member                      |    CTC8096,CTC7148,CTC7132     |
\t  |  set_isolation_group_member_attribute               |    CTC8096,CTC7148,CTC7132     |
\t  |  get_isolation_group_member_attribute               |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Isolation Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                         |       SUPPORT CHIPS LIST       |
\t  |  SAI_ISOLATION_GROUP_ATTR_TYPE                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST     |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Isolation Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                         |       SUPPORT CHIPS LIST       |
\t  |  SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT   |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_ISOLATION_GROUP_H
#define _CTC_SAI_ISOLATION_GROUP_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef struct ctc_sai_isolation_group_member_s
{
    ctc_slistnode_t    head;                /* keep head top!! */
    uint32 ist_grp_mem_id;
    sai_object_id_t port_id;
    sai_object_id_t ist_grp_id;
}ctc_sai_isolation_group_member_t;

typedef struct ctc_sai_isolation_group_s
{
    uint32        ist_grp_id;
    uint32        ist_type;
    ctc_slist_t*   port_list;    /* port use the isolation group member list*/
}ctc_sai_isolation_group_t;

extern sai_status_t
ctc_sai_isolation_group_api_init();

extern sai_status_t
ctc_sai_isolation_group_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_isolation_group_db_deinit(uint8 lchip);

extern void
ctc_sai_isolation_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif  /*_CTC_SAI_ISOLATION_GROUP_H*/

