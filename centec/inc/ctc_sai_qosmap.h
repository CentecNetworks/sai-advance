/**
 @file ctc_sai_qosmap.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-01

 @version v2.0

\p
This module defines SAI Qosmap.
\b
\p
 The Qosmap Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |           SUPPORT CHIPS LIST           |
\t  |  create_qos_map                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_qos_map                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_qos_map_attribute                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_qos_map_attribute                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Qosmap attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |           SUPPORT CHIPS LIST           |
\t  |  SAI_QOS_MAP_ATTR_TYPE                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Qosmap type supported by centec devices:
\p
\b
\t  |   MAP TYPE                                            |           SUPPORT CHIPS LIST           |
\t  |  SAI_QOS_MAP_TYPE_DOT1P_TO_TC                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_DSCP_TO_TC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_DSCP_TO_COLOR                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_TC_TO_QUEUE                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_QOS_MAP_TYPE_TC_TO_PRIORITY_GROUP                |                   -                    |
\t  |  SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_PRIORITY_GROUP      |                   -                    |
\t  |  SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_QUEUE               |                   -                    |
\t  |  SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC                      |            CTC7132,CTC8180             |
\t  |  SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR                   |            CTC7132,CTC8180             |
\t  |  SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP            |            CTC7132,CTC8180             |
\b
*/

#ifndef _CTC_SAI_QOSMAP_H
#define _CTC_SAI_QOSMAP_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

//domain = 0, used for switch
#define QOS_MAP_DOMAIN_ID_START       1
#define QOS_MAP_SAI_TC_TO_CTC_PRI     2
#define QOS_MAP_CTC_PRI_TO_SAI_DSCP   4

typedef struct ctc_sai_qos_map_db_s
{
    sai_qos_map_type_t     map_type;
    sai_qos_map_list_t     map_list;
    uint16                 domain_bmp;  //if (map_type == SAI_QOS_MAP_TYPE_TC_TO_QUEUE), reuse it
}ctc_sai_qos_map_db_t;


extern sai_status_t
ctc_sai_qos_map_api_init();

extern sai_status_t
ctc_sai_qos_map_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_qos_map_db_deinit(uint8 lchip);

extern sai_status_t
ctc_sai_qos_map_port_set_map(sai_object_id_t port_oid, uint32 map_id, sai_qos_map_type_t map_type, bool enable);

extern sai_status_t
ctc_sai_qos_map_switch_set_map(uint8 lchip, uint32 map_id, sai_qos_map_type_t map_type, bool enable);

extern sai_status_t
ctc_sai_qos_map_mpls_inseg_set_map(const sai_inseg_entry_t* inseg_entry, uint32 pcs_type, uint8 qos_tc,
    uint32 map_id, sai_qos_map_type_t map_type, bool enable);

extern sai_status_t
ctc_sai_qos_map_mpls_nh_set_map(sai_object_id_t nh_oid, uint32 map_id, sai_qos_map_type_t map_type, bool enable, uint8* ret_domain);


//extern sai_status_t
//ctc_sai_qos_map_switch_set_default_tc(uint8 lchip, uint8 tc);

extern void
ctc_sai_qos_map_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif /*_CTC_SAI_QOSMAP_H*/




