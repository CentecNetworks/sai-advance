/**
 @file ctc_sai_hostif.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-03-02

 @version v2.0

\p
 This module defines SAI Hostif.
\b
\p
 The Hostif Module APIs supported by centec devices:
\p
\b
\t  |   API                                          |       SUPPORT CHIPS LIST       |
\t  |  create_hostif                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_hostif                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  set_hostif_attribute                          |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_attribute                          |    CTC8096,CTC7148,CTC7132     |
\t  |  create_hostif_table_entry                     |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_hostif_table_entry                     |    CTC8096,CTC7148,CTC7132     |
\t  |  set_hostif_table_entry_attribute              |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_table_entry_attribute              |    CTC8096,CTC7148,CTC7132     |
\t  |  create_hostif_trap_group                      |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_hostif_trap_group                      |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_trap_group_attribute               |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_trap_group_attribute               |    CTC8096,CTC7148,CTC7132     |
\t  |  create_hostif_trap                            |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_hostif_trap                            |    CTC8096,CTC7148,CTC7132     |
\t  |  set_hostif_trap_attribute                     |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_trap_attribute                     |    CTC8096,CTC7148,CTC7132     |
\t  |  create_hostif_user_defined_trap               |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_hostif_user_defined_trap               |    CTC8096,CTC7148,CTC7132     |
\t  |  set_hostif_user_defined_trap_attribute        |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hostif_user_defined_trap_attribute        |    CTC8096,CTC7148,CTC7132     |
\t  |  recv_hostif_packet                            |              -                 |
\t  |  send_hostif_packet                            |    CTC8096,CTC7148,CTC7132     |
\b
\p
 The Hostif trap group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_TRAP_GROUP_ATTR_ADMIN_STATE               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_GROUP_ATTR_QUEUE                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_GROUP_ATTR_POLICER                   |    CTC8096,CTC7148,CTC7132     |
\b
 The Hostif trap attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_TRAP_ATTR_TRAP_TYPE                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_ATTR_PACKET_ACTION                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_ATTR_TRAP_PRIORITY                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_ATTR_EXCLUDE_PORT_LIST               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_ATTR_TRAP_GROUP                      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_ATTR_MIRROR_SESSION                  |              -                 |
\t  |  SAI_HOSTIF_TRAP_ATTR_COUNTER_ID                      |    CTC8096,CTC7148,CTC7132     |
\b
 The Hostif user defined trap attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TYPE               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_PRIORITY      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_TRAP_GROUP         |    CTC8096,CTC7148,CTC7132     |
\b
 The Hostif attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_ATTR_TYPE                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_ATTR_OBJ_ID                               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_ATTR_NAME                                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_ATTR_OPER_STATUS                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_ATTR_QUEUE                                |              -                 |
\t  |  SAI_HOSTIF_ATTR_VLAN_TAG                             |    CTC8096,CTC7148,CTC7132     |
\b
 The Hostif table entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_TABLE_ENTRY_ATTR_TYPE                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TABLE_ENTRY_ATTR_OBJ_ID                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TABLE_ENTRY_ATTR_TRAP_ID                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TABLE_ENTRY_ATTR_CHANNEL_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TABLE_ENTRY_ATTR_HOST_IF                  |    CTC8096,CTC7148,CTC7132     |
\b
 The Hostif packet attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT                  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_INGRESS_LAG                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_HOSTIF_TX_TYPE                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_EGRESS_PORT_OR_LAG            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID                     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_PACKET_ATTR_TIMESTAMP                     |              -                 |
\b
 The Hostif trap type supported by centec devices:
\p
\b
\t  |   TRAP TYPE                                           |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_TRAP_TYPE_STP                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_LACP                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_EAPOL                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_LLDP                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_PVRST                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_QUERY                 |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_LEAVE                 |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V1_REPORT             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V2_REPORT             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IGMP_TYPE_V3_REPORT             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_SAMPLEPACKET                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_UDLD                            |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_CDP                             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_VTP                             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_DTP                             |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_PAGP                            |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_ARP_REQUEST                     |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_ARP_RESPONSE                    |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_DHCP                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_OSPF                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_PIM                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_VRRP                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_DHCPV6                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_OSPFV6                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_VRRPV6                          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_IPV6_NEIGHBOR_DISCOVERY         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_V2                  |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_REPORT              |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IPV6_MLD_V1_DONE                |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_MLD_V2_REPORT                   |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_UNKNOWN_L3_MULTICAST            |        CTC7148,CTC7132         |
\t  |  SAI_HOSTIF_TRAP_TYPE_IP2ME                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_SSH                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_SNMP                            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_BGP                             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_BGPV6                           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_L3_MTU_ERROR                    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_TTL_ERROR                       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_TRAP_TYPE_STATIC_FDB_MOVE                 |              -                 |
\t  |  SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_EGRESS_BUFFER  |              -                 |
\t  |  SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_WRED           |              -                 |
\t  |  SAI_HOSTIF_TRAP_TYPE_PIPELINE_DISCARD_ROUTER         |              -                 |
\t  |  SAI_HOSTIF_TRAP_TYPE_PTP                             |           CTC7132              |
\t  |  SAI_HOSTIF_TRAP_TYPE_PTP_TX_EVENT                    |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_DM       |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LT       |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LBR      |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_LMR      |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_CV_FAIL |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_APS      |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DLM   |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_Y1731_TP_DM    |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_MICROBURST_LOG |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_LATENCY_OVERFLOW_LOG  |           CTC7132              |
\e  |  SAI_HOSTIF_TRAP_TYPE_CUSTOM_EXCEPTION_ISIS           |           CTC7132              |

\b
 The Hostif user defined trap type supported by centec devices:
\p
\b
\t  |   USER DEFINED TRAP TYPE                              |       SUPPORT CHIPS LIST       |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ROUTER             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_NEIGHBOR           |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_ACL                |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HOSTIF_USER_DEFINED_TRAP_TYPE_FDB                |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_HOSTIF_H
#define _CTC_SAI_HOSTIF_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/


#define CTC_SAI_DEFAULT_ETH_SWID 0
#define CTC_SAI_DEFAULT_VRID     0
#define CTC_SAI_DEFAULT_RIF_MTU  1500
#define CTC_SAI_DEFAULT_ACL_HOST_IF_PRIORITY 1
#define CTC_SAI_CTC_CPU_REASON_ID_MASK 0xFFFF
#define CTC_SAI_CPU_MAX_QNUM_PER_GROUP 8

typedef enum ctc_hostif_l2pdu_macda_index_s
{
    CTC_HOSTIF_L2PDU_PVRST_INDEX = 1,
    CTC_HOSTIF_L2PDU_UDLD_INDEX,
    CTC_HOSTIF_L2PDU_ISIS_BROADCAST_INDEX,
    CTC_HOSTIF_L2PDU_ISIS_P2P_INDEX,

}ctc_hostif_l2pdu_macda_index_t;

typedef enum ctc_hostif_l2pdu_prot_index_s
{
    CTC_HOSTIF_L2PDU_CDP_INDEX = 1,
    CTC_HOSTIF_L2PDU_VTP_INDEX,
    CTC_HOSTIF_L2PDU_DDP_INDEX,
    CTC_HOSTIF_L2PDU_PAGP_INDEX,

}ctc_hostif_l2pdu_prot_index_t;
    

typedef enum ctc_hostif_l2pdu_action_index_s
{
    CTC_HOSTIF_L2PDU_ACTION_PVRST_INDEX = CTC_L2PDU_ACTION_INDEX_FIP+1,
    CTC_HOSTIF_L2PDU_ACTION_UDLD_INDEX,
    CTC_HOSTIF_L2PDU_ACTION_CDP_INDEX,
    CTC_HOSTIF_L2PDU_ACTION_VTP_INDEX,
    CTC_HOSTIF_L2PDU_ACTION_DTP_INDEX,
    CTC_HOSTIF_L2PDU_ACTION_PAGP_INDEX,
    CTC_HOSTIF_L2PDU_ACTION_ISIS_INDEX,

}ctc_hostif_l2pdu_action_index_t;

typedef enum ctc_hostif_l3pdu_classify_index_s
{
    CTC_HOSTIF_L3PDU_CLASSIFY_SNMP_INDEX = 0,
    CTC_HOSTIF_L3PDU_CLASSIFY_SSH_INDEX,

}ctc_hostif_l3pdu_classify_index_t;

typedef enum ctc_hostif_l3pdu_action_index_s
{
    CTC_HOSTIF_L3PDU_ACTION_BGPV6_INDEX = CTC_L3PDU_ACTION_INDEX_MRD+1,
    CTC_HOSTIF_L3PDU_ACTION_OSPFV6_INDEX,
    CTC_HOSTIF_L3PDU_ACTION_VRRPV6_INDEX,
    CTC_HOSTIF_L3PDU_ACTION_SNMP_INDEX,
    CTC_HOSTIF_L3PDU_ACTION_SSH_INDEX,

}ctc_hostif_l3pdu_action_index_t;

typedef enum ctc_pkt_cpu_reason_custom_s
{
    CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_LEAVE = CTC_PKT_CPU_REASON_CUSTOM_BASE+1,
    CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V1_REPORT,
    CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V2_REPORT,
    CTC_PKT_CPU_REASON_CUSTOM_IGMP_TYPE_V3_REPORT,
    CTC_PKT_CPU_REASON_CUSTOM_SAMPLEPACKET,
    CTC_PKT_CPU_REASON_CUSTOM_ARP_RESPONSE,
    CTC_PKT_CPU_REASON_CUSTOM_DHCPV6,
    CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_V2,
    CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_REPORT,
    CTC_PKT_CPU_REASON_CUSTOM_IPV6_MLD_V1_DONE,
    CTC_PKT_CPU_REASON_CUSTOM_MLD_V2_REPORT,
    CTC_PKT_CPU_REASON_CUSTOM_UNKNOWN_L3_MULTICAST,
}ctc_pkt_cpu_reason_custom_t;


typedef struct ctc_sai_hostif_s
{
    uint8 hostif_type;
    uint8 port_type;
    uint8 vlan_tag;
    bool oper_status;
    char ifname[32];
    uint32 queue_id;
    sai_object_id_t port_id;
    int32  fd;
}ctc_sai_hostif_t;

typedef struct ctc_sai_hostif_table_s
{
    uint32 hostif_table_id;
    uint8 hostif_table_type;
    uint8 channel_type;
    sai_object_id_t obj_id;
    sai_object_id_t trap_id;
    sai_object_id_t hostif_id;
}ctc_sai_hostif_table_t;

typedef struct ctc_sai_hostif_trap_t
{
    uint32 trap_type;
    bool enable;
    bool is_user_defined;
    sai_object_id_t hostif_group_id;
    uint32 acl_match_entry_id;
    uint32 custom_reason_id;
    uint32 priority;
    uint32 action;
    sai_object_list_t exclude_port_list;
    uint32 ref_count;
    sai_object_id_t counter_id;
}ctc_sai_hostif_trap_t;

typedef struct ctc_sai_hostif_trap_group_s
{
    uint32 hostif_group_id;
    bool admin_sate;
    uint32 queue_id;
    sai_object_id_t policer_id;
}ctc_sai_hostif_trap_group_t;

typedef struct ctc_sai_hostif_lookup_channel_s
{
    /*key*/
    sai_object_id_t trap_id;
    sai_object_id_t port_id;

    /*data*/
    uint8 is_match;
    uint8 hostif_table_type;
    sai_hostif_table_entry_channel_type_t channel_type;
}ctc_sai_hostif_lookup_channel_t;

typedef struct ctc_sai_hostif_lookup_s
{
    /*key*/
    sai_object_id_t vlan_id;
    sai_object_id_t port_id;
    int32 fd;

    /*data*/
    uint8 is_match;
    ctc_sai_hostif_t* p_hostif;
}ctc_sai_hostif_lookup_t;

extern sai_status_t
ctc_sai_hostif_l3if_en(uint8 lchip, uint32 gport, uint32 enable);

extern sai_status_t
ctc_sai_hostif_api_init();

extern sai_status_t
ctc_sai_hostif_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_hostif_db_deinit(uint8 lchip);

extern void
ctc_sai_hostif_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif  /*_CTC_SAI_HOSTIF_H*/

