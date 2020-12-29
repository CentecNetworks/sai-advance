/**
 @file ctc_sai_bridge.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2017-11-09

 @version v2.0

\p
 This module defines SAI Bridge.
\b
\p
 The Bridge Module APIs supported by centec devices:
\p
\b
\t  |   API                                        |           SUPPORT CHIPS LIST           |
\t  |  create_bridge                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_bridge                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_bridge_attribute                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_bridge_attribute                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_bridge_stats                            |                   -                    |
\t  |  get_bridge_stats_ext                        |                   -                    |
\t  |  clear_bridge_stats                          |                   -                    |
\t  |  create_bridge_port                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_bridge_port                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_bridge_port_attribute                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_bridge_port_attribute                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_bridge_port_stats                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_bridge_port_stats_ext                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  clear_bridge_port_stats                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Bridge attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |           SUPPORT CHIPS LIST           |
\t  |  SAI_BRIDGE_ATTR_TYPE                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_PORT_LIST                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_LEARN_DISABLE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP          |                   -                    |
\t  |  SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP        |                   -                    |
\t  |  SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP                |                   -                    |
\b
\p
 The Bridge port attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                       |           SUPPORT CHIPS LIST           |
\t  |  SAI_BRIDGE_PORT_ATTR_TYPE                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_PORT_ID                                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_TAGGING_MODE                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_VLAN_ID                                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_RIF_ID                                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_TUNNEL_ID                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_BRIDGE_ID                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_ADMIN_STATE                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\e  |  SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT                   |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE                  |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_FRR_NHP_GRP                                 |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID                  |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID                  |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_ID                    |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS_MODE              |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS                   |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_CUSTOMER_VLAN_ID                            |            CTC7132,CTC8180             |
\e  |  SAI_BRIDGE_PORT_ATTR_NEED_FLOOD                                  |            CTC7132,CTC8180             |
\b
*/

#ifndef _CTC_SAI_BRIDGE_H
#define _CTC_SAI_BRIDGE_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef struct ctc_sai_bridge_port_s
{
    uint8         port_type;
    bool          admin_state;
    uint8         tag_mode;
    uint8         fdb_learn_mode;
    uint16        gport;
    uint16        vlan_id;
    uint16        bridge_id;
    uint16        l3if_id;
    uint16        logic_port;
    uint32        nh_id;
    uint32        limit_num;
    uint32        limit_action;
    sai_object_id_t  tunnel_id;
    sai_object_id_t  cross_connect_port;
    uint64 igs_packet_count;
    uint64 igs_byte_count;
    uint64 egs_packet_count;
    uint64 egs_byte_count;
    uint8 bridge_type;
    uint8 sub_port_or_tunnel_oam_en;
    uint32 sub_port_or_tunnel_policer_id;
    uint16 sub_port_or_tunnel_service_id;
    bool ingress_filter;
    bool egress_filter;
    sai_object_id_t isolation_group_oid;

    
    uint32 stp_port_bind_bits[4];  // stp instance 
    uint32 stp_port_bind_count;
    uint8  stp_port_state[128];

    
    uint32 vlan_member_bind_bits[128]; // vlan member binded vlanptr 
    uint32 vlan_member_bind_count;
    uint8  vlan_member_tag_mode[4096];
    sai_object_id_t  frr_nhp_grp_id;
    uint16 service_vlan_id;
    uint8 service_vlan_cos;
    uint32 scl_entry_id;
    uint16        cvlan_id;
    uint16 outgoing_svid;
    uint8 outgoing_scos;
    int32 outgoing_scos_mode;
    bool need_flood;
}
ctc_sai_bridge_port_t;

extern sai_status_t
ctc_sai_bridge_api_init();

extern sai_status_t
ctc_sai_bridge_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_bridge_get_fid(sai_object_id_t bv_id, uint16 *fid);

extern sai_status_t
ctc_sai_bridge_get_bridge_port_oid(uint8 lchip, uint32 gport, uint8 is_logic, sai_object_id_t* bridge_port_id);

extern sai_status_t
ctc_sai_bridge_traverse_get_bridge_port_info(uint8 lchip, uint16 bridge_id, uint16 logic_port, uint32* gport, uint16* vlan_id);

extern sai_status_t
ctc_sai_bridge_traverse_get_sub_port_info(uint8 lchip, uint32 gport, uint16 vlan_id, uint16 cvlan_id, uint32* logic_port);

extern void
ctc_sai_bridge_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif  /*_CTC_SAI_BRIDGE_H*/

