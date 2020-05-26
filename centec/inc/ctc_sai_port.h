/**
 @file ctc_sai_port.h

 @author  Copyright (C) 2011 Centec Networks Inc.  All rights reserved.

 @date 2011-11-09

 @version v2.0

\p
 This module defines SAI Port.
\b
\p
 The PORT Module APIs supported by centec devices:
\p
\b
\t  |   API                                |       SUPPORT CHIPS LIST       |
\t  |  create_port                         |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_port                         |    CTC8096,CTC7148,CTC7132     |
\t  |  set_port_attribute                  |    CTC8096,CTC7148,CTC7132     |
\t  |  get_port_attribute                  |    CTC8096,CTC7148,CTC7132     |
\t  |  get_port_stats                      |    CTC8096,CTC7148,CTC7132     |
\t  |  get_port_stats_ext                  |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_port_stats                    |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_port_all_stats                |    CTC8096,CTC7148,CTC7132     |
\t  |  create_port_pool                    |              -                 |
\t  |  remove_port_pool                    |              -                 |
\t  |  set_port_pool_attribute             |              -                 |
\t  |  get_port_pool_attribute             |              -                 |
\t  |  get_port_pool_stats                 |              -                 |
\t  |  get_port_pool_stats_ext             |              -                 |
\t  |  clear_port_pool_stats               |              -                 |
\b

\p
 The PORT attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                            |       SUPPORT CHIPS LIST       |
\t  |  SAI_PORT_ATTR_TYPE                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_OPER_STATUS                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_QUEUE_LIST                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_SPEED                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_FEC_MODE                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_SPEED                 |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_FEC_MODE              |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_HALF_DUPLEX_SPEED     |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_AUTO_NEG_MODE         |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_FLOW_CONTROL_MODE     |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_ASYMMETRIC_PAUSE_MODE |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_MEDIA_TYPE            |              -                 |
\t  |  SAI_PORT_ATTR_REMOTE_ADVERTISED_OUI_CODE              |              -                 |
\t  |  SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EYE_VALUES                              |              -                 |
\t  |  SAI_PORT_ATTR_OPER_SPEED                              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_HW_LANE_LIST                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_SPEED                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_FULL_DUPLEX_MODE                        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_AUTO_NEG_MODE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_ADMIN_STATE                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_MEDIA_TYPE                              |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_SPEED                        |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_FEC_MODE                     |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_HALF_DUPLEX_SPEED            |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_AUTO_NEG_MODE                |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_FLOW_CONTROL_MODE            |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_ASYMMETRIC_PAUSE_MODE        |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_MEDIA_TYPE                   |              -                 |
\t  |  SAI_PORT_ATTR_ADVERTISED_OUI_CODE                     |              -                 |
\t  |  SAI_PORT_ATTR_PORT_VLAN_ID                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_DROP_UNTAGGED                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_DROP_TAGGED                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_FEC_MODE                                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_UPDATE_DSCP                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_MTU                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_INGRESS_ACL                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EGRESS_ACL                              |              -                 |
\t  |  SAI_PORT_ATTR_INGRESS_MIRROR_SESSION                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EGRESS_MIRROR_SESSION                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_POLICER_ID                              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_DEFAULT_TC                          |              -                 |
\t  |  SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_TC_TO_QUEUE_MAP                     |              -                 |
\t  |  SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_TC_TO_PRIORITY_GROUP_MAP            |              -                 |
\t  |  SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP  |              -                 |
\t  |  SAI_PORT_ATTR_QOS_PFC_PRIORITY_TO_QUEUE_MAP           |              -                 |
\t  |  SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_QOS_INGRESS_BUFFER_PROFILE_LIST         |              -                 |
\t  |  SAI_PORT_ATTR_QOS_EGRESS_BUFFER_PROFILE_LIST          |              -                 |
\t  |  SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_META_DATA                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_HW_PROFILE_ID                           |              -                 |
\t  |  SAI_PORT_ATTR_EEE_ENABLE                              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_EEE_IDLE_TIME                           |              -                 |
\t  |  SAI_PORT_ATTR_EEE_WAKE_TIME                           |              -                 |
\t  |  SAI_PORT_ATTR_PORT_POOL_LIST                          |              -                 |
\t  |  SAI_PORT_ATTR_ISOLATION_GROUP                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_PKT_TX_ENABLE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_PORT_ATTR_TAM_OBJECT                              |              -                 |
\t  |  SAI_PORT_ATTR_SERDES_PREEMPHASIS                      |              -                 |
\t  |  SAI_PORT_ATTR_SERDES_IDRIVER                          |              -                 |
\t  |  SAI_PORT_ATTR_SERDES_IPREDRIVER                       |              -                 |
\t  |  SAI_PORT_ATTR_LINK_TRAINING_ENABLE                    |              -                 |
\t  |  SAI_PORT_ATTR_PTP_MODE                                |              -                 |
\t  |  SAI_PORT_ATTR_PORT_SERDES_ID                          |              -                 |
\t  |  SAI_PORT_ATTR_ES                                      |            CTC7132             |

\b
*/

#ifndef _CTC_SAI_PORT_H
#define _CTC_SAI_PORT_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"
#include "ctc_sai_db.h"

/*don't need include other header files*/


#define    CTC_SAI_PORT_SPEED_1G 1000
#define    CTC_SAI_PORT_SPEED_100M 100
#define    CTC_SAI_PORT_SPEED_10M 10
#define    CTC_SAI_PORT_SPEED_2G5 2500
#define    CTC_SAI_PORT_SPEED_10G 10000
#define    CTC_SAI_PORT_SPEED_20G 20000
#define    CTC_SAI_PORT_SPEED_40G 40000
#define    CTC_SAI_PORT_SPEED_100G 100000
#define    CTC_SAI_PORT_SPEED_5G 5000
#define    CTC_SAI_PORT_SPEED_25G 25000
#define    CTC_SAI_PORT_SPEED_50G 50000

#define MAX_LANES 4

typedef struct ctc_sai_port_db_s
{
    /*policer*/
    uint32 policer_id;              //ctc policer id, not obj_id, refer to policer_oid.value
    uint32 stmctl_flood_policer_id;
    uint32 stmctl_bc_policer_id;
    uint32 stmctl_mc_policer_id;
    /*qosmap*/
    uint32 dot1p_to_tc_map_id;                //SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP
    uint32 dot1p_to_color_map_id;             //SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP
    uint32 tc_color_to_dot1p_map_id;          //SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP
    uint32 tc_color_to_dscp_map_id;    
    uint32 dscp_to_tc_map_id;
    uint32 dscp_to_color_map_id;

    /* samplepacket */
    sai_object_id_t ingress_samplepacket_id;
    sai_object_id_t egress_samplepacket_id;

    /*scheduler*/
    uint32 sched_id;
    uint8 flow_ctl_mode;        //SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE
    
    sai_object_id_t ethernet_segment;
    uint8 y1731_oam_en;
    uint8 y1731_lm_en;
    uint8 y1731_mip_bitmap;

    /*ptp*/
    uint32 ptp_domain_id;       //ctc ptp domain id, not obj_id, refer to policer_oid.value
    uint64 ptp_path_delay;
    uint64 ptp_ingr_asy;
    uint64 ptp_egr_asy;
    sai_port_ptp_mode_t ptp_mode;
    int32 sub_port_ref_cnt;

    /*router interface*/
    int32 sub_if_ref_cnt;
}ctc_sai_port_db_t;


typedef enum _ctc_sai_port_drop_type_t
{
    CTC_SAI_PORT_DROP_UNTAGGED = 0,
    CTC_SAI_PORT_DROP_TAGGED,
}ctc_sai_port_drop_type_t;

extern sai_status_t
ctc_sai_port_api_init();
extern sai_status_t
ctc_sai_port_db_init(uint8 lchip);
extern sai_status_t
ctc_sai_port_db_deinit(uint8 lchip);
void
ctc_sai_port_mapping_tags_mode(ctc_sai_port_drop_type_t drop_type, bool data, ctc_vlantag_ctl_t* mode, ctc_vlantag_ctl_t  mode_old );

extern void
ctc_sai_port_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
_ctc_sai_port_get_port_db(sai_object_id_t port_id, ctc_sai_port_db_t** p_port);
#endif /*_CTC_SAI_PORT_H*/

