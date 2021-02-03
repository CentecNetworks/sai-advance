/**
 @file ctc_sai_lag.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
 This module defines SAI LAG.
\b
\p
 The LAG Module APIs supported by centec devices:
\p
\b
\t  |   API                                          |           SUPPORT CHIPS LIST           |
\t  |  create_lag                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_lag                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_lag_attribute                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_lag_attribute                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_lag_member                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_lag_member                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_lag_member_attribute                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_lag_member_attribute                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_lag_members                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_lag_members                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The LAG attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |           SUPPORT CHIPS LIST           |
\t  |  SAI_LAG_ATTR_PORT_LIST                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_ATTR_INGRESS_ACL                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_ATTR_EGRESS_ACL                              |                   -                    |
\t  |  SAI_LAG_ATTR_PORT_VLAN_ID                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_ATTR_DROP_UNTAGGED                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_ATTR_DROP_TAGGED                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\e  |  SAI_LAG_ATTR_MODE                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\e  |  SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM                   |            CTC7132,CTC8180             |
\b 

\p
 The LAG MEMBER attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |           SUPPORT CHIPS LIST           |
\t  |  SAI_LAG_MEMBER_ATTR_LAG_ID                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_MEMBER_ATTR_PORT_ID                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

*/

#ifndef _CTC_SAI_LAG_H
#define _CTC_SAI_LAG_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef void (*ctc_sai_lag_member_change_notification_fn)(uint8 lchip, uint32 linkagg_id, uint32 mem_port, bool change);
typedef enum ctc_sai_lag_mem_change_type_s
{
    CTC_SAI_LAG_MEM_CHANGE_TYPE_HOSTIF,
    CTC_SAI_LAG_MEM_CHANGE_TYPE_BRIDGE_PORT,
    CTC_SAI_LAG_MEM_CHANGE_TYPE_ACL,
    CTC_SAI_LAG_MEM_CHANGE_TYPE_MAX
}ctc_sai_lag_mem_change_type_t;

typedef struct ctc_sai_lag_info_s
{
    uint32 member_ports_bits[8];
    uint32 Egress_disable_ports_bits[8];
    uint32 Ingress_disable_ports_bits[8];
    uint32 lag_mode;
    uint16 vlan_id;
    uint8 vlan_priority;
    uint8 is_binding_rif;
    uint8 is_binding_sub_rif;
    uint16 binding_sub_rif_count;    
    uint8 bind_bridge_port_type_bmp; // bit 0 mean bind 1q port, bit 1 mean bind 1d port , bit 2 mean bind 1d sub port, bit 3 mean bind 1d qinq port    
    bool drop_tagged;
    bool drop_untagged;
    int32 scl0_ref_cnt;
    int32 scl1_ref_cnt;

    uint16 max_lag_member;
    ctc_sai_lag_member_change_notification_fn cb[CTC_SAI_LAG_MEM_CHANGE_TYPE_MAX];

    uint16 logic_port;  //for port type 1d bridge port
    uint16 bridge_id;   //for port type 1d bridge port
}ctc_sai_lag_info_t;


extern sai_status_t
ctc_sai_lag_api_init();
extern sai_status_t
ctc_sai_lag_db_init(uint8 lchip);
extern sai_status_t
ctc_sai_lag_binding_rif(sai_object_id_t sai_lag_id, uint8 is_binding, uint8 l3if_type);
extern sai_status_t
ctc_sai_lag_register_member_change_cb(uint8 lchip, ctc_sai_lag_mem_change_type_t type, uint32 lag_port, ctc_sai_lag_member_change_notification_fn cb);
extern sai_status_t
ctc_sai_lag_remove_member_change_cb(uint8 lchip, ctc_sai_lag_mem_change_type_t type, uint32 lag_port);
extern sai_status_t
ctc_sai_lag_notification_all_members_change(uint8 lchip, ctc_sai_lag_mem_change_type_t type, uint32 lag_port, uint32 change);
extern void
ctc_sai_lag_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_LAG_H*/
