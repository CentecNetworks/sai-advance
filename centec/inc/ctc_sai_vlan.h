/**
 @file ctc_sai_vlan.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI VLAN.
\b

\p
 The VLAN Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_vlan                                          |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_vlan                                          |    CTC8096,CTC7148,CTC7132     |
\t  |  set_vlan_attribute                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  get_vlan_attribute                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  create_vlan_member                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_vlan_member                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  set_vlan_member_attribute                            |    CTC8096,CTC7148,CTC7132     |
\t  |  get_vlan_member_attribute                            |    CTC8096,CTC7148,CTC7132     |
\t  |  create_vlan_members                                  |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_vlan_members                                  |    CTC8096,CTC7148,CTC7132     |
\t  |  get_vlan_stats                                       |    CTC8096,CTC7148,CTC7132     |
\t  |  get_vlan_stats_ext                                   |    CTC8096,CTC7148,CTC7132     |
\t  |  clear_vlan_stats                                     |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The VLAN attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_VLAN_ATTR_VLAN_ID                                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_MEMBER_LIST                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_STP_INSTANCE                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_LEARN_DISABLE                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_UNKNOWN_NON_IP_MCAST_OUTPUT_GROUP_ID   |              -                 |
\t  |  SAI_VLAN_ATTR_UNKNOWN_IPV4_MCAST_OUTPUT_GROUP_ID     |              -                 |
\t  |  SAI_VLAN_ATTR_UNKNOWN_IPV6_MCAST_OUTPUT_GROUP_ID     |              -                 |
\t  |  SAI_VLAN_ATTR_UNKNOWN_LINKLOCAL_MCAST_OUTPUT_GROUP_ID|              -                 |
\t  |  SAI_VLAN_ATTR_INGRESS_ACL                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_EGRESS_ACL                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_META_DATA                              |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP            |              -                 |
\t  |  SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP          |              -                 |
\t  |  SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_BROADCAST_FLOOD_GROUP                  |              -                 |
\t  |  SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_ATTR_TAM_OBJECT                             |              -                 |
\e  |  SAI_VLAN_ATTR_PTP_DOMAIN_ID                          |            CTC7132             |
\e  |  SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE                    |            CTC7132             |
\e  |  SAI_VLAN_ATTR_POLICER_ID                             |            CTC7132             |
\b

\p
 The VLAN MEMBER attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_VLAN_MEMBER_ATTR_VLAN_ID                         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE               |    CTC8096,CTC7148,CTC7132     |
\b

*/

#ifndef _CTC_SAI_VLAN_H
#define _CTC_SAI_VLAN_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef struct ctc_sai_vlan_user_s
{
    uint16 user_vlanptr;/*fid = user_vlanptr*/
    uint16 vlan_id;
    uint32 stats_id_in;
    uint32 stats_id_eg;
    uint8 stp_id;
    uint32 ukwn_flood_ctr[3]; /* ukwn_flood_ctr[0]:unicast; ukwn_flood_ctr[1]:muticast; ukwn_flood_ctr[2]:broadcast; */
    uint8 ipv4_mcast_lookup_type;
    uint8 ipv6_mcast_lookup_type;
    uint64 igs_packet_count;
    uint64 igs_byte_count;
    uint64 egs_packet_count;
    uint64 egs_byte_count;
    uint32 ptp_domain_id;
    uint32 policer_id;

    uint32 vlan_member_port_bind_bits[8];
    uint32 vlan_member_lag_bind_bits[8];
    uint32 vlan_member_port_bind_count;
    uint32 vlan_member_lag_bind_count;
}ctc_sai_vlan_user_t;

enum ctc_sai_vlan_pkt_type_e
{
    CTC_SAI_VLAN_UNICAST_PKT,
    CTC_SAI_VLAN_MUTIICAST_PKT,
    CTC_SAI_VLAN_BROADCAST_PKT,
};
typedef enum ctc_sai_vlan_pkt_type_e ctc_sai_vlan_pkt_type_t;

typedef struct  ctc_sai_vlan_traverse_param_s
{
   uint16 vlan_id;
   uint16 vlan_ptr;
   uint32 is_found;
}ctc_sai_vlan_traverse_param_t;

#define VLAN_NUM 4096
extern sai_status_t
ctc_sai_vlan_api_init();

extern sai_status_t
ctc_sai_vlan_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_vlan_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx);

extern sai_status_t
ctc_sai_vlan_get_vlan_id(sai_object_id_t oid, uint16 *vlan_id);

extern sai_status_t
ctc_sai_vlan_get_vlan_id_from_vlan_ptr(uint8 lchip, uint16 vlan_ptr, uint16 *vlan_id);

extern sai_status_t
ctc_sai_vlan_get_vlan_ptr_from_vlan_id(uint8 lchip, uint16 vlan_id, uint16* vlan_ptr);

extern sai_status_t
ctc_sai_vlan_get_vlan_member(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx);

extern sai_status_t
ctc_sai_vlan_traverse_set_unkown_pkt_action(uint8 lchip, void* p_sw_master, uint8 fdb_unknown_type);

extern void
ctc_sai_vlan_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_VLAN_H*/

