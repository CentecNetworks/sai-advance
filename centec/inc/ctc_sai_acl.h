/**
 @file ctc_sai_acl.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-01-23

 @version v1.0

\b
     This module defines SAI ACL.
\b
\p
     The ACL Module APIs supported by centec devices:
\p
\b
\t  |   API                                                      |          SUPPORT CHIPS LIST            |
\t  |  create_acl_table                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_table                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_table_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_table_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_acl_entry                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_entry                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_entry_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_entry_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_acl_counter                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_counter                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_counter_attribute                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_counter_attribute                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_acl_range                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_range                                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_range_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_range_attribute                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_acl_table_group                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_table_group                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_table_group_attribute                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_table_group_attribute                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  create_acl_table_group_member                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_acl_table_group_member                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_acl_table_group_member_attribute                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_acl_table_group_member_attribute                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\b
 The ACL IP Type attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_IP_TYPE_ANY                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_IP                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_NON_IP                                    |                   -                    |
\t  |  SAI_ACL_IP_TYPE_IPV4ANY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_NON_IPV4                                  |                   -                    |
\t  |  SAI_ACL_IP_TYPE_IPV6ANY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_NON_IPV6                                  |                   -                    |
\t  |  SAI_ACL_IP_TYPE_ARP                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_ARP_REQUEST                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_TYPE_ARP_REPLY                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL IP Frag attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_IP_FRAG_ANY                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_FRAG_NON_FRAG                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_FRAG_NON_FRAG_OR_HEAD                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_FRAG_HEAD                                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_IP_FRAG_NON_HEAD                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Action Type attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_ACTION_TYPE_REDIRECT                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_ENDPOINT_IP                           |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_REDIRECT_LIST                         |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_PACKET_ACTION                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_FLOOD                                 |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_COUNTER                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_MIRROR_INGRESS                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_MIRROR_EGRESS                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_POLICER                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_DECREMENT_TTL                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_TC                                |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_PACKET_COLOR                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_ID                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_INNER_VLAN_PRI                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_ID                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_OUTER_VLAN_PRI                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_SRC_MAC                           |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_DST_MAC                           |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_SRC_IP                            |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_DST_IP                            |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_SRC_IPV6                          |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_DST_IPV6                          |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_DSCP                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_ECN                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_L4_SRC_PORT                       |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_L4_DST_PORT                       |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INGRESS_SAMPLEPACKET_ENABLE           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_EGRESS_SAMPLEPACKET_ENABLE            |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_ACL_META_DATA                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_EGRESS_BLOCK_PORT_LIST                |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_USER_TRAP_ID                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_SET_DO_NOT_LEARN                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ACTION_TYPE_ACL_DTEL_FLOW_OP                      |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_DTEL_INT_SESSION                      |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_DTEL_DROP_REPORT_ENABLE               |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_DTEL_TAIL_DROP_REPORT_ENABLE          |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_DTEL_FLOW_SAMPLE_PERCENT              |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_DTEL_REPORT_ALL_PACKETS               |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_NO_NAT                                |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INT_INSERT                            |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INT_DELETE                            |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INT_REPORT_FLOW                       |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INT_REPORT_DROPS                      |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_INT_REPORT_TAIL_DROPS                 |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_TAM_INT_OBJECT                        |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_SET_ISOLATION_GROUP                   |                   -                    |
\t  |  SAI_ACL_ACTION_TYPE_MACSEC_FLOW                           |                   -                    |
\b

\p
\b
 The ACL Table Group Type attributes supported by centec devices:
\p
\t  |   ATTRIBUTE                                                |       SUPPORT CHIPS LIST       |
\t  |  SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_TYPE_PARALLEL                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Table Group attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |       SUPPORT CHIPS LIST       |
\t  |  SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_ATTR_TYPE                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Table Group Member attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |       SUPPORT CHIPS LIST       |
\t  |  SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Table attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |       SUPPORT CHIPS LIST       |
\t  |  SAI_ACL_TABLE_ATTR_ACL_STAGE                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_SIZE                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_ACL_ACTION_TYPE_LIST                   |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IPV6                   |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IPV6                   |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_DST_MAC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_SRC_IP                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_DST_IP                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_SRC_IP                     |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_DST_IP                     |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IN_PORTS                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_OUT_PORTS                        |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IN_PORT                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_OUT_PORT                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_SRC_PORT                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_ID                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_PRI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_OUTER_VLAN_CFI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_ID                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_PRI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_VLAN_CFI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_L4_SRC_PORT                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_L4_DST_PORT                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_SRC_PORT                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_L4_DST_PORT                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ETHER_TYPE                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_ETHER_TYPE                 |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IP_PROTOCOL                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_INNER_IP_PROTOCOL                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IP_IDENTIFICATION                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_DSCP                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ECN                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TTL                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TOS                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IP_FLAGS                         |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TCP_FLAGS                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_FRAG                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IPV6_FLOW_LABEL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TC                               |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ICMP_TYPE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ICMP_CODE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_TYPE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ICMPV6_CODE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_PACKET_VLAN                      |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TUNNEL_VNI                       |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_HAS_VLAN_TAG                     |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MACSEC_SCI                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL0_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL1_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL2_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_LABEL                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_TTL                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_EXP                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL3_BOS                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_LABEL                |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_TTL                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_EXP                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_MPLS_LABEL4_BOS                  |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_FDB_DST_USER_META                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ROUTE_DST_USER_META              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_DST_USER_META           |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_PORT_USER_META                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_VLAN_USER_META                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ACL_USER_META                    |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_FDB_NPU_META_DST_HIT             |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT        |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ROUTE_NPU_META_DST_HIT           |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_BTH_OPCODE                       |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_AETH_SYNDROME                    |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+1         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+2         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+3         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+4         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+5         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+6         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+7         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+8         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+9         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+10        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+11        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+12        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+13        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+14        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+15        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MAX           |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_ACL_RANGE_TYPE                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_IPV6_NEXT_HEADER                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_GRE_KEY                          |                    CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_FIELD_TAM_INT_TYPE                     |                   -                    |
\t  |  SAI_ACL_TABLE_ATTR_ENTRY_LIST                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_COUNTER                  |                   -                    |
\e  |  SAI_ACL_TABLE_ATTR_FIELD_INTERFACE_ID                     |                    CTC7132,CTC8180     |
\b

\p
 The ACL Entry attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |       SUPPORT CHIPS LIST       |
\t  |  SAI_ACL_ENTRY_ATTR_TABLE_ID                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_PRIORITY                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ADMIN_STATE                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_SRC_IPV6                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_DST_IPV6                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IPV6                   |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IPV6                   |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_DST_MAC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_DST_IP                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_SRC_IP                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_DST_IP                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORTS                        |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IN_PORT                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_OUT_PORT                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_SRC_PORT                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_ID                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_PRI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_OUTER_VLAN_CFI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_ID                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_PRI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_VLAN_CFI                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_L4_SRC_PORT                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_L4_DST_PORT                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_SRC_PORT                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_L4_DST_PORT                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ETHER_TYPE                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_ETHER_TYPE                 |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IP_PROTOCOL                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_INNER_IP_PROTOCOL                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IP_IDENTIFICATION                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_DSCP                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ECN                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TTL                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TOS                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IP_FLAGS                         |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TCP_FLAGS                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_FRAG                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IPV6_FLOW_LABEL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TC                               |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ICMP_TYPE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ICMP_CODE                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_TYPE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ICMPV6_CODE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_PACKET_VLAN                      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TUNNEL_VNI                       |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_HAS_VLAN_TAG                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MACSEC_SCI                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL0_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL1_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_LABEL                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_TTL                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_EXP                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL2_BOS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_LABEL                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_TTL                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_EXP                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL3_BOS                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_LABEL                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_TTL                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_EXP                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_MPLS_LABEL4_BOS                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_FDB_DST_USER_META                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_DST_USER_META              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_DST_USER_META           |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_PORT_USER_META                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_VLAN_USER_META                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ACL_USER_META                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_FDB_NPU_META_DST_HIT             |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_NEIGHBOR_NPU_META_DST_HIT        |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ROUTE_NPU_META_DST_HIT           |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_BTH_OPCODE                       |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_AETH_SYNDROME                    |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+1         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+2         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+3         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+4         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+5         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+6         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+7         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+8         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+9         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+10        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+11        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+12        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+13        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+14        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+15        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MAX           |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_ACL_RANGE_TYPE                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_IPV6_NEXT_HEADER                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_GRE_KEY                          |                    CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_FIELD_TAM_INT_TYPE                     |                   -                    |
\e  |  SAI_ACL_ENTRY_ATTR_FIELD_INTERFACE_ID                     |                    CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_ENDPOINT_IP                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_REDIRECT_LIST                   |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_FLOOD                           |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_COUNTER                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_EGRESS                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DECREMENT_TTL                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_TC                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_PACKET_COLOR                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_ID               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_INNER_VLAN_PRI              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_ID               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_OUTER_VLAN_PRI              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_MAC                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_MAC                     |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IP                      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IP                      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_SRC_IPV6                    |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_DST_IPV6                    |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_DSCP                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_SRC_PORT                 |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_L4_DST_PORT                 |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_ACL_META_DATA               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_BLOCK_PORT_LIST          |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_USER_TRAP_ID                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_ACL_DTEL_FLOW_OP                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DTEL_INT_SESSION                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DTEL_DROP_REPORT_ENABLE         |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DTEL_TAIL_DROP_REPORT_ENABLE    |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DTEL_FLOW_SAMPLE_PERCENT        |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_DTEL_REPORT_ALL_PACKETS         |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_NO_NAT                          |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INT_INSERT                      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INT_DELETE                      |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_FLOW                 |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_DROPS                |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_INT_REPORT_TAIL_DROPS           |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_TAM_INT_OBJECT                  |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_SET_ISOLATION_GROUP             |                   -                    |
\t  |  SAI_ACL_ENTRY_ATTR_ACTION_MACSEC_FLOW                     |                   -                    |
\b

\p
 The ACL Counter attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_COUNTER_ATTR_TABLE_ID                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_COUNTER_ATTR_ENABLE_PACKET_COUNT                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_COUNTER_ATTR_ENABLE_BYTE_COUNT                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_COUNTER_ATTR_PACKETS                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_COUNTER_ATTR_BYTES                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Range Type attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_RANGE_TYPE_L4_SRC_PORT_RANGE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_RANGE_TYPE_L4_DST_PORT_RANGE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_RANGE_TYPE_OUTER_VLAN                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_RANGE_TYPE_INNER_VLAN                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_RANGE_TYPE_PACKET_LENGTH                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The ACL Range attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                |          SUPPORT CHIPS LIST            |
\t  |  SAI_ACL_RANGE_ATTR_TYPE                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_ACL_RANGE_ATTR_LIMIT                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\e  |  SAI_ACL_RANGE_ATTR_STAGE                                  |                    CTC7132,CTC8180     |
\b
*/


#ifndef _CTC_SAI_ACL_H
#define _CTC_SAI_ACL_H


#include "ctc_sai.h"
#include "sal.h"
/*don't need include other header files*/


#define ACL_DEFAULT_TABLE_SIZE     128
#define ACL_MIN_ENTRY_PRIORITY     1
#define ACL_MAX_ENTRY_PRIORITY     65535
#define ACL_DEFAULT_ENTRY_PRIORITY 1
#define SAI_ACL_KEY_ATTR_NUM       ((SAI_ACL_TABLE_ATTR_FIELD_END - SAI_ACL_TABLE_ATTR_FIELD_START + 1) + (SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_END - SAI_ACL_TABLE_ATTR_CUSTOM_RANGE_START + 1))
#define SAI_ACL_ACTION_ATTR_NUM    (SAI_ACL_ENTRY_ATTR_ACTION_END - SAI_ACL_ENTRY_ATTR_ACTION_START + 1)

#if defined(TSINGMA)
/* ingress acl tcam block 0 used for twamp, 1 used for hostif, block 2~4 used for parallel, block 5~6 used for sequential, block 7 used for blobal switch.
 * egress acl tcam block 0~2 used for parallel, not support sequential and blobal switch.
 */
#define ACL_INGRESS_PARAELL_GROUP_MEMBER_NUM  3U
#define ACL_EGRESS_PARAELL_GROUP_MEMBER_NUM   3U

#define ACL_INGRESS_RESERVE_TCAM_BLOCK_BASE   0U
#define ACL_INGRESS_PARAELL_TCAM_BLOCK_BASE   2U
#define ACL_INGRESS_SEQUENT_TCAM_BLOCK_BASE   5U
#define ACL_INGRESS_GLOBAL_TCAM_BLOCK_BASE    7U

#define ACL_EGRESS_PARAELL_TCAM_BLOCK_BASE    0U
#define ACL_EGRESS_GLOBAL_TCAM_BLOCK_BASE     0U

#define ACL_INGRESS_PER_BLOCK_TCAM_SLICE      1U
#define ACL_EGRESS_PER_BLOCK_TCAM_SLICE       1U

#define ACL_TCAM_BLOCK_NUM                    8U

#elif defined(TSINGMA_MX)
#define ACL_INGRESS_PARAELL_GROUP_MEMBER_NUM  2U
#define ACL_EGRESS_PARAELL_GROUP_MEMBER_NUM   3U

#define ACL_INGRESS_RESERVE_TCAM_BLOCK_BASE   0U
#define ACL_INGRESS_PARAELL_TCAM_BLOCK_BASE   4U
#define ACL_INGRESS_SEQUENT_TCAM_BLOCK_BASE  10U
#define ACL_INGRESS_GLOBAL_TCAM_BLOCK_BASE   13U

#define ACL_EGRESS_PARAELL_TCAM_BLOCK_BASE    0U
#define ACL_EGRESS_GLOBAL_TCAM_BLOCK_BASE     3U

#define ACL_INGRESS_PER_BLOCK_TCAM_SLICE      3U
#define ACL_EGRESS_PER_BLOCK_TCAM_SLICE       1U

#define ACL_TCAM_BLOCK_NUM                    6U

#endif

#define ACL_VLAN_RANGE_NUM                    64U
#define ACL_PARAELL_LOOKUP_NUM                ((ACL_INGRESS_PARAELL_GROUP_MEMBER_NUM >  ACL_EGRESS_PARAELL_GROUP_MEMBER_NUM) ? ACL_INGRESS_PARAELL_GROUP_MEMBER_NUM : ACL_EGRESS_PARAELL_GROUP_MEMBER_NUM)

/* Common part */
/* group or table bind point info */
struct ctc_sai_acl_bind_point_info_s
{
    ctc_slistnode_t head;
    uint8 bind_type;
    sai_object_id_t bind_index;
};
typedef struct ctc_sai_acl_bind_point_info_s ctc_sai_acl_bind_point_info_t;

struct ctc_sai_acl_group_member_s
{
    ctc_slistnode_t head;
    sai_object_id_t table_id;
    uint16 members_prio;
};
typedef struct ctc_sai_acl_group_member_s ctc_sai_acl_group_member_t;

struct ctc_sai_acl_group_s
{
    uint8 group_stage;
    uint8 group_type;
    uint8 bind_point_list;
    uint32 lookup_type;
    ctc_slist_t* member_list;       /* all the members(table) in the group */
    ctc_slist_t* bind_points;       /* the group (as bind unit) is bound to these bind points */
};
typedef struct ctc_sai_acl_group_s ctc_sai_acl_group_t;

/* Table */
struct ctc_sai_acl_table_member_s
{
    ctc_slistnode_t head;
    sai_object_id_t entry_id;
    uint16 priority;
};
typedef struct ctc_sai_acl_table_member_s ctc_sai_acl_table_member_t;

struct ctc_sai_acl_table_group_list_s
{
    ctc_slistnode_t head;
    sai_object_id_t group_id;
};
typedef struct ctc_sai_acl_table_group_list_s ctc_sai_acl_table_group_list_t;

struct ctc_sai_acl_table_udf_group_s
{
    ctc_slistnode_t head;
    uint8           index;
    sai_object_id_t group_id;
};
typedef struct ctc_sai_acl_table_udf_group_s ctc_sai_acl_table_udf_group_t;

struct ctc_sai_acl_table_s
{
    uint8  table_stage;
    uint8  bind_point_list;
    uint32 table_size;
    uint32 lookup_type;
    uint32 created_entry_count;
    uint32 table_key_bmp[(SAI_ACL_KEY_ATTR_NUM-1)/32 + 1];          /* bit 0 <--> SAI_ACL_TABLE_ATTR_FIELD_SRC_IPV6; bit 1 <--> SAI_ACL_TABLE_ATTR_FIELD_DST_IPV6 */
    uint8  range_type_bmp;

    ctc_slist_t* entry_list;                                        /* all entries added to this table */
    ctc_slist_t* group_list;                                        /* the table is a member of these groups */
    ctc_slist_t* bind_points;                                       /* the table (as bind unit) is bound to these bind points */
    ctc_slist_t* udf_groups;
};
typedef struct ctc_sai_acl_table_s ctc_sai_acl_table_t;

/* Entry */
struct ctc_sai_acl_entry_s
{
    sai_object_id_t table_id;
    uint16 priority;
    uint8 entry_valid;     /* admin stats or not */
    uint8 key_type;
    uint8 ctc_session_id;

    /* key and action attribute list */
    sai_attribute_t* key_attr_list;
    sai_attribute_t* action_attr_list;
};
typedef struct ctc_sai_acl_entry_s ctc_sai_acl_entry_t;

/* member */
struct ctc_sai_acl_table_group_member_s
{
    sai_object_id_t group_id;
    sai_object_id_t table_id;
    uint32 member_priority;
};
typedef struct ctc_sai_acl_table_group_member_s ctc_sai_acl_table_group_member_t;

/* Range */
struct ctc_sai_acl_range_s
{
    uint8  stage;
    uint8  group_id;
    uint8  range_type;
    uint32 range_min;
    uint32 range_max;
    uint32 ref_cnt; /* to record how many sai entry(s) use this acl range object id */
};
typedef struct ctc_sai_acl_range_s ctc_sai_acl_range_t;

/* Counter */
struct ctc_sai_acl_counter_s
{
    sai_object_id_t table_id;
    bool enable_pkt_cnt;
    bool enable_byte_cnt;
    uint32 stats_id;         /* sai sdk stats id*/
    uint16 ref_ins_cnt;
    uint16 ref_oid_cnt;
};
typedef struct ctc_sai_acl_counter_s ctc_sai_acl_counter_t;

extern sai_status_t
ctc_sai_acl_api_init();

extern sai_status_t
ctc_sai_acl_db_init(uint8 lchip);

extern sai_status_t
ctc_sai_acl_db_deinit(uint8 lchip);

extern sai_status_t
ctc_sai_acl_bind_point_set(sai_object_key_t *key, const sai_attribute_t *attr);

extern void
ctc_sai_acl_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_acl_set_mirror_sample_rate(uint8 lchip,sai_object_id_t mirror_oid);

extern sai_status_t
ctc_sai_acl_init_resource(uint8 lchip);

extern sai_status_t
ctc_sai_acl_init_key_template(uint8 lchip);

#endif /*_CTC_SAI_ACL_H*/




