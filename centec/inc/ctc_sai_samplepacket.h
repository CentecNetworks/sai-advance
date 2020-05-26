/**
 @file ctc_sai_samplepacket.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-04-02

 @version v2.0

\p
This module defines SAI Samplepacket.
\b
\p
 The Samplepacket Module APIs supported by centec devices:
\p
\b
\t  |   API                                               |       SUPPORT CHIPS LIST       |
\t  |  create_samplepacket                                |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_samplepacket                                |    CTC8096,CTC7148,CTC7132     |
\t  |  set_samplepacket_attribute                         |    CTC8096,CTC7148,CTC7132     |
\t  |  get_samplepacket_attribute                         |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Samplepacket attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                         |       SUPPORT CHIPS LIST       |
\t  |  SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SAMPLEPACKET_ATTR_TYPE                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_SAMPLEPACKET_ATTR_MODE                         |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_SAMPLEPACKET_H
#define _CTC_SAI_SAMPLEPACKET_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef struct ctc_sai_samplepacket_bind_node_s
{
    ctc_slistnode_t    head;                /* keep head top!! */
    uint8 ctc_dir;
    uint8 is_acl;
    uint8 acl_log_id;
    uint32 gport;
    sai_object_id_t acl_entry_id;
}ctc_sai_samplepacket_bind_node_t;

typedef struct ctc_sai_samplepacket_s
{
    uint32        samplepacket_id;
    uint32        sample_rate;
    uint16        sample_type;
    uint16        sample_mode;
    ctc_slist_t*   port_list;    /* port use the samplepacket list*/

}ctc_sai_samplepacket_t;

extern sai_status_t
ctc_sai_samplepacket_api_init();

extern sai_status_t
ctc_sai_samplepacket_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_samplepacket_set_port_samplepacket(uint8 lchip, uint32 gport, const sai_attribute_t *attr, void* p_port_db);

extern sai_status_t
ctc_sai_samplepacket_set_acl_samplepacket(uint8 lchip, uint8 ctc_dir, uint8 acl_priority, sai_object_id_t acl_entry_id, sai_attribute_t* attr, uint32* p_acl_log_id, uint32* p_log_rate);

extern sai_status_t
ctc_sai_samplepacket_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_samplepacket_db_deinit(uint8 lchip);

extern void
ctc_sai_samplepacket_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif  /*_CTC_SAI_SAMPLEPACKET_H*/

