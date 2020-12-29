/**
 @file ctc_sai_router_interface.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI Routing Interface.
\b
\p
 The Routing Interface Module APIs supported by centec devices:
\p
\b
\t  |   API                                               |           SUPPORT CHIPS LIST           |
\t  |  create_router_interface                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_router_interface                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_router_interface_attribute                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_router_interface_attribute                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_router_interface_stats                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_router_interface_stats_ext                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  clear_router_interface_stats                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b
\p
 The Routing Interface attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |           SUPPORT CHIPS LIST           |
\t  |  SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_TYPE                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_PORT_ID                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_VLAN_ID                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID                   |                  -                     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_MTU                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL                     |            CTC7132,CTC8180             |
\t  |  SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL                      |            CTC7132,CTC8180             |
\t  |  SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_LOOPBACK_PACKET_ACTION          |                  -                     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL                      |         CTC7148,CTC7132,CTC8180        |
\t  |  SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID                     |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP              |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP           |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP    |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP                     |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE              |            CTC7132,CTC8180             |
\e  |  SAI_ROUTER_INTERFACE_ATTR_DECREMENT_TTL                   |                  -                     |
\b

*/

#ifndef _CTC_SAI_ROUTER_INTERFACE_H
#define _CTC_SAI_ROUTER_INTERFACE_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

#define L3IF_RSV_START 4093
#define L3IF_RSV_END 4094

typedef enum ctc_sai_rif_set_type_e
{
    CTC_SAI_RIF_SET_TYPE_PORT = 0,
    CTC_SAI_RIF_SET_TYPE_VRF,
    CTC_SAI_RIF_SET_TYPE_MAX,
}ctc_sai_rif_set_type_t;

typedef enum ctc_sai_rif_nat_zone_id_e
{
    CTC_SAI_RIF_NAT_ZONE_EXTERNAL = 0,
    CTC_SAI_RIF_NAT_ZONE_INTERNAL,
    CTC_SAI_RIF_NAT_ZONE_MAX,
}ctc_sai_rif_nat_zone_id_t;
    

typedef struct  ctc_sai_rif_traverse_param_s
{
   uint8 lchip;
   ctc_sai_rif_set_type_t set_type;
   uint32* cmp_value;
   ctc_l3if_property_t l3if_prop;
   void* p_value;
}ctc_sai_rif_traverse_param_t;

typedef struct  ctc_sai_router_interface_s
{
   sai_object_id_t vlan_oid;
   sai_packet_action_t neighbor_miss_action;
   uint32 gport;
   uint16 vrf_id;
   uint16 bridge_id;
   uint32 mtu;
   sai_mac_t src_mac;

   uint32 v4_state:1;
   uint32 v6_state:1;
   uint32 v4_mc_state:1;
   uint32 v6_mc_state:1;
   uint32 is_virtual:1;
   uint32 snat_en:1;
   uint32 nat_iftype:1;
   uint32 rsv:25;
   uint32 ing_statsid;
   uint32 egs_statsid;
   uint32 stats_state:1;
   sai_object_id_t dot1d_bridge_id;
   uint32 actual_l3if_id;
   uint64 igs_packet_count;
   uint64 igs_byte_count;
   uint64 egs_packet_count;
   uint64 egs_byte_count;
   uint16 outer_vlan_id;
   uint16 inner_vlan_id;        

   uint32 tc_color_to_dscp_map_id;
   uint32 dscp_to_tc_map_id;
   uint32 dscp_to_color_map_id;

   
}ctc_sai_router_interface_t;

extern sai_status_t
ctc_sai_router_interface_api_init();

extern sai_status_t
ctc_sai_router_interface_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_router_interface_get_rif_info(sai_object_id_t router_interface_id, uint8* type, uint16* vrf_id, uint32* gport, uint16* vlan);

extern sai_status_t
ctc_sai_router_interface_get_vlan_ptr(sai_object_id_t router_interface_id, uint16* vlan_ptr);

extern sai_status_t
ctc_sai_router_interface_get_src_mac(sai_object_id_t router_interface_id, sai_mac_t src_mac);

extern sai_status_t
ctc_sai_router_interface_lookup_rif_oid(uint8 lchip, uint8 type, uint32 gport, uint16 vlan, sai_object_id_t* router_interface_id);

extern sai_status_t
ctc_sai_router_interface_get_miss_action(sai_object_id_t router_interface_id, sai_packet_action_t* action);

extern sai_status_t
ctc_sai_router_interface_traverse_set(ctc_sai_rif_traverse_param_t* traverse_param);

extern sai_status_t
ctc_sai_router_interface_get_param(ctc_sai_rif_traverse_param_t* traverse_param);

extern sai_status_t
ctc_sai_router_interface_update_bridge_rif(uint8 lchip, uint16 l3if_id, uint16 vlan_id, bool is_add);

extern void
ctc_sai_router_interface_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_qos_map_port_set_map(sai_object_id_t port_or_l3if_oid, uint32 map_id, sai_qos_map_type_t map_type, bool enable);


#endif /*_CTC_SAI_ROUTER_INTERFACE_H*/

