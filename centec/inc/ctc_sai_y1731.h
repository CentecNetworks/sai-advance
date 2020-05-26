/**
 @file ctc_sai_y1731.h

 @author  Copyright (C) 2020 Centec Networks Inc.  All rights reserved.

 @date 2020-04-10

 @version v2.0

\p
 This module defines SAI Y1731.
\b
\p
 The BFD Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |   SUPPORT CHIPS LIST   |
\t  |  create_y1731_meg                                         |        CTC7132         |
\t  |  remove_y1731_meg                                         |        CTC7132         |
\t  |  set_y1731_meg_attribute                                  |        CTC7132         |
\t  |  get_y1731_meg_attribute                                  |        CTC7132         |
\t  |  create_y1731_session                                     |        CTC7132         |
\t  |  remove_y1731_session                                     |        CTC7132         |
\t  |  set_y1731_session_attribute                              |        CTC7132         |
\t  |  get_y1731_session_attribute                              |        CTC7132         |
\t  |  create_y1731_remote_mep                                  |        CTC7132         |
\t  |  remove_y1731_remote_mep                                  |        CTC7132         |
\t  |  set_y1731_remote_mep_attribute                           |        CTC7132         |
\t  |  get_y1731_remote_mep_attribute                           |        CTC7132         |
\t  |  get_y1731_session_lm_stats                               |        CTC7132         |
\b
\p
 The Y1731 MEG attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_Y1731_MEG_ATTR_TYPE                                  |        CTC7132         |
\t  |  SAI_Y1731_MEG_ATTR_NAME                                  |        CTC7132         |
\t  |  SAI_Y1731_MEG_ATTR_LEVEL                                 |        CTC7132         |
\b
\p
 The Y1731 Session attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_Y1731_SESSION_ATTR_MEG                               |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_DIR                               |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_VLAN_ID                           |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_BRIDGE_ID                         |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_PORT_ID                           |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_MPLS_IN_LABEL                     |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_LOCAL_MEP_ID                      |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_CCM_PERIOD                        |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_CCM_ENABLE                        |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_IS_P2P_MODE                       |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_REMOTE_MEP_LIST                   |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_LM_STATS_OFFLOAD_TYPE             |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_LM_STATS_ENABLE                   |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_LM_STATS_TYPE                     |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_DM_OFFLOAD_TYPE                   |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_DM_ENABLE                         |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_LOCAL_RDI                         |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_TP_ROUTER_INTERFACE_ID            |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_TP_WITHOUT_GAL                    |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_MPLS_TTL                          |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_MPLS_EXP                          |        CTC7132         |
\t  |  SAI_Y1731_SESSION_ATTR_NEXT_HOP_ID                       |        CTC7132         |
\b
\p
 The Y1731 Rmep attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |   SUPPORT CHIPS LIST   |
\t  |  SAI_Y1731_REMOTE_MEP_ATTR_Y1731_SESSION_ID               |        CTC7132         |
\t  |  SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_ID                  |        CTC7132         |
\t  |  SAI_Y1731_REMOTE_MEP_ATTR_REMOTE_MEP_MAC_ADDRESS         |        CTC7132         |
\b 
*/


#ifndef _CTC_SAI_Y1731_H
#define _CTC_SAI_Y1731_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef struct ctc_sai_y1731_meg_s
{
    sai_y1731_meg_type_t meg_type;
    uint8 level;
    char meg_name[SAI_Y1731_MEG_NAME_SIZE];    
} ctc_sai_y1731_meg_t;

typedef struct ctc_sai_y1731_session_s
{
    sai_object_id_t meg_oid;
    sai_y1731_meg_type_t meg_type;
    sai_y1731_session_direction_t dir;
    ctc_oam_key_t oam_key;
    sai_object_id_t bridge_id;
    uint32 lmep_id;
    sai_y1731_session_ccm_period_t ccm_period;
    uint8 ccm_en;
    //uint8 is_p2p_mode;
    uint8 is_link_oam;

    sai_y1731_session_performance_monitor_offload_type_t lm_offload_type;
    sai_y1731_session_performance_monitor_offload_type_t dm_offload_type;

    uint8 lm_en;
    uint8 lm_type;
    uint8 dm_en;

    
    uint8 without_gal;
    uint8 mpls_ttl;
    uint8 exp_or_cos;
    sai_object_id_t tp_rif_oid;

    sai_object_id_t nh_oid;
    
    uint32 lmep_index;

    ctc_slist_t *rmep_head;

} ctc_sai_y1731_session_t;

typedef struct ctc_sai_y1731_rmep_s
{
    sai_object_id_t y1731_session_oid;
    uint32 rmep_id;
    uint32 rmep_index;
} ctc_sai_y1731_rmep_t;

typedef struct  ctc_sai_y1731_rmep_id_s
{
   ctc_slistnode_t node;
   sai_object_id_t rmep_oid;
}ctc_sai_y1731_rmep_id_t;


extern sai_status_t
ctc_sai_y1731_traverse_get_oid_by_mepindex(uint8 lchip, uint32 mepindex, uint8 isremote, sai_object_id_t* obj_id);

extern void 
ctc_sai_y1731_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_y1731_api_init();

extern sai_status_t
ctc_sai_y1731_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_y1731_db_deinit(uint8 lchip);


#endif /*_CTC_SAI_Y1731_H*/

