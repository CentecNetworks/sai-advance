/**
 @file ctc_sai_tunnel.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2017-11-09

 @version v2.0

\p
This module defines SAI Tunnel.
\b
\p
 The Tunnel Module APIs supported by centec devices:
\p
\b
\t  |   API                                                     |       SUPPORT CHIPS LIST       |
\t  |  create_tunnel_map                                        |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_tunnel_map                                        |    CTC8096,CTC7148,CTC7132     |
\t  |  set_tunnel_map_attribute                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_map_attribute                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  create_tunnel                                            |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_tunnel                                            |    CTC8096,CTC7148,CTC7132     |
\t  |  set_tunnel_attribute                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_attribute                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_stats                                         |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_stats_ext                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_tunnel_stats                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  create_tunnel_term_table_entry                           |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_tunnel_term_table_entry                           |    CTC8096,CTC7148,CTC7132     |
\t  |  set_tunnel_term_table_entry_attribute                    |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_term_table_entry_attribute                    |    CTC8096,CTC7148,CTC7132     |
\t  |  create_tunnel_map_entry                                  |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_tunnel_map_entry                                  |    CTC8096,CTC7148,CTC7132     |
\t  |  set_tunnel_map_entry_attribute                           |    CTC8096,CTC7148,CTC7132     |
\t  |  get_tunnel_map_entry_attribute                           |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Tunnel map type supported by centec devices:
\p
\b
\t  |   TRAP TYPE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN                         |              -                 |
\t  |  SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN                    |              -                 |
\t  |  SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI             |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Tunnel map entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY                       |              -                 |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE                     |              -                 |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY                       |              -                 |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE                     |              -                 |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE        |    CTC8096,CTC7148,CTC7132     |
\b
 The Tunnel map attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_MAP_ATTR_TYPE                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_MAP_ATTR_ENTRY_LIST                           |    CTC8096,CTC7148,CTC7132     |
\b
 The Tunnel type supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_TYPE_IPINIP                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TYPE_IPINIP_GRE                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TYPE_VXLAN                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TYPE_MPLS                                     |              -                 |
\b
 The Tunnel attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_ATTR_TYPE                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_OVERLAY_INTERFACE                        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_SRC_IP                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_TTL_MODE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_TTL_VAL                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_GRE_KEY                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_ECN_MODE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_ENCAP_MAPPERS                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_DECAP_ECN_MODE                           |              -                 |
\t  |  SAI_TUNNEL_ATTR_DECAP_MAPPERS                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_DECAP_TTL_MODE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_DECAP_DSCP_MODE                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST                    |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID                         |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE                       |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE                       |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW                    |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW                    |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN                |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID                    |            CTC7132             |
\e  |  SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID                    |            CTC7132             |
\e  |  SAI_TUNNEL_ATTR_DECAP_SPLIT_HORIZON_ENABLE               |            CTC7132             |
\e  |  SAI_TUNNEL_ATTR_DECAP_EXP_MODE                           |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_EXP_MODE                           |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_ENCAP_EXP_VAL                            |    CTC8096,CTC7148,CTC7132     |
\e  |  SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO             |    CTC8096,CTC7148,CTC7132     |
\b
 The Tunnel term table entry type supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2MP                    |    CTC8096,CTC7148,CTC7132     |
\b
 The Tunnel term table entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                               |       SUPPORT CHIPS LIST       |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID        |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_TUNNEL_H
#define _CTC_SAI_TUNNEL_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

typedef enum ctc_sai_tunnel_map_val_s
{
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_OECN_ID = 0,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_OECN_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_UECN_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_UECN_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VLAN_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VLAN_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VNI_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VNI_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_BRG_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_BRG_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VRF_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VRF_ID,
    CTC_SAI_TUNNEL_MAP_VAL_TYPE_MAX,
}ctc_sai_tunnel_map_val_t;

typedef struct ctc_sai_tunnel_map_entry_s
{
    ctc_slistnode_t    head;                /* keep head top!! */
    uint32   tunnel_map_entry_id;
    uint8    tunnel_map_type;
    sai_object_id_t tunnel_map_id;
    uint8 oecn_key;
    uint8 oecn_val;
    uint8 uecn_key;
    uint8 uecn_val;
    uint16 vlan_key;
    uint16 vlan_val;
    uint32 vni_key;
    uint32 vni_val;
    sai_object_id_t brg_id_key;
    sai_object_id_t brg_id_val;
    sai_object_id_t vrf_key;
    sai_object_id_t vrf_val;
}ctc_sai_tunnel_map_entry_t;

typedef struct ctc_sai_tunnel_map_s
{
    ctc_slistnode_t encap;
    ctc_slistnode_t decap;
    uint32        tunnel_map_id;
    uint8         tunnel_map_type;
    uint8         rsv[3];
    ctc_slist_t*   map_entry_list;    /* bind tunnel map entry list*/
}ctc_sai_tunnel_map_t;

typedef struct ctc_sai_tunnel_s
{
    uint32        tunnel_id;
    uint8         tunnel_type;

    /*encap attribute*/
    uint8         encap_ttl_mode;
    uint8         encap_ttl_val;
    uint8         encap_dscp_mode;
    uint8         encap_dscp_val;
    uint8         encap_ecn_mode;
    bool          encap_gre_key_en;
    uint32        encap_gre_key;
    sai_ip_address_t encap_src_ip;

    /*decap attribute*/
    uint8         decap_ecn_mode;
    uint8         decap_ttl_mode;
    uint8         decap_dscp_mode;

    sai_object_id_t underlay_if;
    sai_object_id_t overlay_if;

    ctc_slist_t*   encap_map_list;
    ctc_slist_t*   decap_map_list;

    uint8         use_flex;
    ctc_slist_t*   encap_nh_list;    /* encap nexthop list*/
    uint32        encap_stats_id;
    uint32        decap_stats_id;
    sai_object_id_t encap_nexthop_sai;
    uint8         decap_pw_mode;
    uint8         encap_pw_mode;
    bool          decap_cw_en;
    bool          encap_cw_en;
    uint16        logic_port;
    uint16        encap_tagged_vlan;
    uint32        inseg_label;
    bool          decap_esi_label_valid;
    bool          encap_esi_label_valid;
    uint8         decap_exp_mode;
    uint8         encap_exp_mode;
    uint8         encap_exp_val;
    bool          decap_acl_use_outer;
    bool          split_horizon_valid;
    uint32        ref_cnt;
}ctc_sai_tunnel_t;

typedef struct ctc_sai_tunnel_term_table_entry_s
{
    uint32        tunnel_term_table_id;
    uint8         tunnel_term_table_type;
    uint8         tunnel_type;
    uint8         not_finished;
    sai_object_id_t vrf_id;
    sai_object_id_t tunnel_id;
    sai_ip_address_t dst_ip;
    sai_ip_address_t src_ip;

}ctc_sai_tunnel_term_table_entry_t;

extern sai_status_t
ctc_sai_tunnel_api_init();

extern sai_status_t
ctc_sai_tunnel_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_tunnel_db_deinit(uint8 lchip);

extern sai_status_t
ctc_sai_tunnel_map_to_nh_ip_tunnel(uint8 lchip, sai_object_id_t tunnel_id, uint32 ctc_nh_id, sai_ip_address_t* ip_da, ctc_ip_tunnel_nh_param_t* p_nh_param);

extern sai_status_t
ctc_sai_tunnel_unmap_to_nh_ip_tunnel(uint8 lchip, sai_object_id_t tunnel_id, uint32 ctc_nh_id);

extern void
ctc_sai_tunnel_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param);

#endif  /*_CTC_SAI_TUNNEL_H*/

