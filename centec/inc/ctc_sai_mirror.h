/**
 @file ctc_sai_mirror.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI MIRROR.
\b
\p
 The MIRROR Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_mirror_session                                |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_mirror_session                                |    CTC8096,CTC7148,CTC7132     |
\t  |  set_mirror_session_attribute                         |    CTC8096,CTC7148,CTC7132     |
\t  |  get_mirror_session_attribute                         |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The MIRROR attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_MIRROR_SESSION_ATTR_TYPE                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_MONITOR_PORT                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_TC                           |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_VLAN_TPID                    |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_VLAN_ID                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_VLAN_PRI                     |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_VLAN_CFI                     |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_ERSPAN_ENCAPSULATION_TYPE    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION                |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_TOS                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_TTL                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_CONGESTION_MODE              |              -                 |
\t  |  SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MIRROR_SESSION_ATTR_POLICER                      |              -                 |
\b

*/
#ifndef _CTC_SAI_MIRROR_H
#define _CTC_SAI_MIRROR_H

#include "ctcs_api.h"
/*don't need include other header files*/

extern sai_status_t
ctc_sai_mirror_api_init();
extern sai_status_t
ctc_sai_mirror_db_init(uint8 lchip);
extern sai_status_t
ctc_sai_mirror_set_port_mirr(uint8 lchip, uint32 gport, const sai_attribute_t *attr);
extern sai_status_t
ctc_sai_mirror_get_port_mirr(uint8 lchip, uint32 gport, sai_attribute_t *attr);
extern sai_status_t
ctc_sai_mirror_set_acl_mirr(uint8 lchip, uint8 priority, uint8* ctc_session_id, uint32* sample_rate, sai_attribute_t *attr);
extern sai_status_t
ctc_sai_mirror_get_acl_mirr(uint8 lchip, uint8 priority, uint8 ctc_session_id, sai_attribute_t *attr);
extern sai_status_t
ctc_sai_mirror_free_sess_res_index(uint8 lchip, uint8 ctc_dir, uint8 priority, uint8 session_id);
extern sai_status_t
ctc_sai_mirror_alloc_sess_res_index(uint8 lchip, uint8 ctc_dir, uint8 priority, uint8* session_id);
extern void
ctc_sai_mirror_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);
extern sai_status_t
ctc_sai_mirror_db_deinit(uint8 lchip);

#endif /*_CTC_SAI_MIRROR_H*/


