/**
 @file ctc_sai_mcast.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
 This module defines SAI L2MC Entry, IPMC Entry, RPF GROUP, L2MC Group, IPMC Group And Mcast Fdb Entry.
\b
\p
 The L2MC Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_l2mc_entry                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_l2mc_entry                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_l2mc_entry_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_l2mc_entry_attribute                             |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The L2MC entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_L2MC_ENTRY_ATTR_PACKET_ACTION                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID                  |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The L2MC entry type supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_L2MC_ENTRY_TYPE_SG                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_L2MC_ENTRY_TYPE_XG                               |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC Entry Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_ipmc_entry                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_ipmc_entry                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_ipmc_entry_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_ipmc_entry_attribute                             |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_IPMC_ENTRY_ATTR_PACKET_ACTION                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID                     |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC entry type supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_IPMC_ENTRY_TYPE_SG                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_IPMC_ENTRY_TYPE_XG                               |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The RPF Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_rpf_group                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_rpf_group                                     |    CTC8096,CTC7148,CTC7132     |
\t  |  set_rpf_group_attribute                              |    CTC8096,CTC7148,CTC7132     |
\t  |  get_rpf_group_attribute                              |    CTC8096,CTC7148,CTC7132     |
\t  |  create_rpf_group_member                              |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_rpf_group_member                              |    CTC8096,CTC7148,CTC7132     |
\t  |  set_rpf_group_member_attribute                       |    CTC8096,CTC7148,CTC7132     |
\t  |  get_rpf_group_member_attribute                       |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The RPF Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST                   |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The RPF Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID           |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The L2MC Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_l2mc_group                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_l2mc_group                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_l2mc_group_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_l2mc_group_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  create_l2mc_group_member                             |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_l2mc_group_member                             |    CTC8096,CTC7148,CTC7132     |
\t  |  set_l2mc_group_member_attribute                      |    CTC8096,CTC7148,CTC7132     |
\t  |  get_l2mc_group_member_attribute                      |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The L2MC Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST                 |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The L2MC Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP          |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC Group Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_ipmc_group                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_ipmc_group                                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_ipmc_group_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_ipmc_group_attribute                             |    CTC8096,CTC7148,CTC7132     |
\t  |  create_ipmc_group_member                             |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_ipmc_group_member                             |    CTC8096,CTC7148,CTC7132     |
\t  |  set_ipmc_group_member_attribute                      |    CTC8096,CTC7148,CTC7132     |
\t  |  get_ipmc_group_member_attribute                      |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST                 |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The IPMC Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID            |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Mcast Fdb Module APIs supported by centec devices:
\p
\b
\t  |   API                                                 |       SUPPORT CHIPS LIST       |
\t  |  create_mcast_fdb_entry                               |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_mcast_fdb_entry                               |    CTC8096,CTC7148,CTC7132     |
\t  |  set_mcast_fdb_entry_attribute                        |    CTC8096,CTC7148,CTC7132     |
\t  |  get_mcast_fdb_entry_attribute                        |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Mcast Fdb attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_MCAST_FDB_ENTRY_ATTR_META_DATA                   |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_MCAST_H
#define _CTC_SAI_MCAST_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef enum ctc_sai_opt_type_e
{
    CTC_SAI_ADD,
    CTC_SAI_DELETE,
    CTC_SAI_UPDATE,
    CTC_SAI_MAX
}ctc_sai_opt_type_t;

typedef enum ctc_sai_mcast_ipmc_bind_type_e
{
    CTC_SAI_MCAST_IPMC_BIND_NONE,
    CTC_SAI_MCAST_IPMC_BIND_L2MC,
    CTC_SAI_MCAST_IPMC_BIND_FDB,
    CTC_SAI_MCAST_IPMC_BIND_MAX
}ctc_sai_mcast_ipmc_bind_type_t;

typedef struct  ctc_sai_mcast_entry_travs_data_s
{
    uint16 group_id;
    void *p_entry_data;
}ctc_sai_mcast_entry_travs_data_t;

typedef struct  ctc_sai_rpf_group_property_s
{
   uint32 bmp;
   uint16 intf[CTC_IP_MAX_RPF_IF];
}ctc_sai_rpf_group_property_t;

typedef struct  ctc_sai_mcast_vlan_member_priv_s
{
    uint8 lchip;
    uint8 is_member;
    ctc_sai_opt_type_t opt_type;
    ctc_sai_entry_property_t *p_entry_property;
    ctc_slist_t *new_output_id_head;
    union {
        sai_object_id_t member_id;
        ctc_slist_t *output_id_head;
    }member;
}ctc_sai_mcast_vlan_member_priv_t;

typedef struct  ctc_sai_mcast_entry_node_s
{
   ctc_slistnode_t node;
   ctc_sai_entry_property_t *entry_property;
}ctc_sai_mcast_entry_node_t;

typedef struct  ctc_sai_mcast_member_output_id_s
{
   ctc_slistnode_t node;
   sai_object_id_t output_id;
}ctc_sai_mcast_member_output_id_t;

typedef struct  ctc_sai_mcast_group_property_s
{
   ctc_slist_t *entry_head;
   ctc_slist_t *output_id_head;
}ctc_sai_mcast_group_property_t;

typedef struct  ctc_sai_mcast_entry_bind_node_s
{
   ctc_slistnode_t node;
   uint16 vlan_ptr;
   ctc_sai_mcast_ipmc_bind_type_t bind_type;
}ctc_sai_mcast_entry_bind_node_t;

typedef struct  ctc_sai_mcast_entry_property_s
{
    uint16 group_id;
    sai_object_id_t group_oid;
    sai_object_id_t rpf_group_oid;
    sai_packet_action_t action;
    uint16 cid;
    ctc_slist_t *bind_type_head;
}ctc_sai_mcast_entry_property_t;

typedef struct  ctc_sai_wb_mcast_group_property_s
{
    /*key*/
   sai_object_id_t group_oid;
   uint16 index;
   uint32 calc_key_len[0];
    /*data*/
   sai_object_id_t output_id;
}ctc_sai_wb_mcast_group_property_t;

typedef struct  ctc_sai_wb_mcast_entry_bind_node_s
{
   /*key*/
   uint16 group_id;
   uint16 index;
   uint32 calc_key_len[0];
    /*data*/
   uint16 vlan_ptr;
   ctc_sai_mcast_ipmc_bind_type_t bind_type;
}ctc_sai_wb_mcast_entry_bind_node_t;

extern sai_status_t
ctc_sai_mcast_api_init();

extern sai_status_t
ctc_sai_mcast_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_mcast_db_deinit(uint8 lchip);

extern void
ctc_sai_rpf_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_l2mc_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_ipmc_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_l2mc_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_ipmc_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern void
ctc_sai_mcast_fdb_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_VLAN_H*/

