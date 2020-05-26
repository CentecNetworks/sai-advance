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
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_qos_map                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_qos_map                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  set_qos_map_attribute                                |    CTC8096,CTC7148,CTC7132     |
\t  |  get_qos_map_attribute                                |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Qosmap attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_QOS_MAP_ATTR_TYPE                                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST                   |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Qosmap type supported by centec devices:
\p
\b
\t  |   MAP TYPE                                            |       SUPPORT CHIPS LIST       |
\t  |  SAI_QOS_MAP_TYPE_DOT1P_TO_TC                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_DSCP_TO_TC                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_DSCP_TO_COLOR                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_TC_TO_QUEUE                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_QOS_MAP_TYPE_TC_TO_PRIORITY_GROUP                |              -                 |
\t  |  SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_PRIORITY_GROUP      |              -                 |
\t  |  SAI_QOS_MAP_TYPE_PFC_PRIORITY_TO_QUEUE               |              -                 |
\b
*/

#ifndef _CTC_SAI_QOSMAP_H
#define _CTC_SAI_QOSMAP_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"


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
ctc_sai_qos_map_switch_set_default_tc(uint8 lchip, uint8 tc);

extern void
ctc_sai_qos_map_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif /*_CTC_SAI_QOSMAP_H*/




