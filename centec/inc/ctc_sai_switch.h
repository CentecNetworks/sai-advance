/**
 @file ctc_sai_oid.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
 This module defines SAI Switch.
\b
\p
 The SWITCH Module APIs supported by centec devices:
\p
\b
\t  |   API                                  |           SUPPORT CHIPS LIST           |
\t  |  create_switch                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  remove_switch                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  set_switch_attribute                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_switch_attribute                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_switch_stats                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  get_switch_stats_ext                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  clear_switch_stats                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\b

\p
 The SWITCH attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                                             |           SUPPORT CHIPS LIST           |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PORT_NUMBER                                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PORT_LIST                                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PORT_MAX_MTU                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_CPU_PORT                                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_TABLE_SIZE                                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_LAG_MEMBERS                                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_LAGS                                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ECMP_MEMBERS                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_QUEUES                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_OPER_STATUS                                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_TEMP_LIST                                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_TEMP                                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVERAGE_TEMP                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_DEFAULT_VLAN_ID                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_STP_INSTANCE                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_INGRESS_ACL                                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_EGRESS_ACL                                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_TRAFFIC_CLASSES                      |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUP_HIERARCHY_LEVELS     |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_SCHEDULER_GROUPS_PER_HIERARCHY_LEVEL |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MAX_NUMBER_OF_CHILDS_PER_SCHEDULER_GROUP           |                   -                    |
\t  |  SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE                                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_INGRESS_BUFFER_POOL_NUM                                |                   -                    |
\t  |  SAI_SWITCH_ATTR_EGRESS_BUFFER_POOL_NUM                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_DOUBLE_NAT_ENTRY                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE                                    |                   -                    |
\t  |  SAI_SWITCH_ATTR_AVAILABLE_ACL_TABLE_GROUP                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP                                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ECMP_HASH                                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_LAG_HASH                                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_RESTART_WARM                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_WARM_RECOVER                                           |                   -                    |
\t  |  SAI_SWITCH_ATTR_RESTART_TYPE                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NV_STORAGE_SIZE                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_CAPABILITY                                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY                              |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCHING_MODE                                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_SRC_MAC_ADDRESS                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_AGING_TIME                                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION                       |                CTC7148                 |
\t  |  SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ECMP_HASH_IPV4                                         |                   -                    |
\t  |  SAI_SWITCH_ATTR_ECMP_HASH_IPV4_IN_IPV4                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_ECMP_HASH_IPV6                                         |                   -                    |
\t  |  SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED                                  |                   -                    |
\t  |  SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_LAG_HASH_IPV4                                          |                   -                    |
\t  |  SAI_SWITCH_ATTR_LAG_HASH_IPV4_IN_IPV4                                  |                   -                    |
\t  |  SAI_SWITCH_ATTR_LAG_HASH_IPV6                                          |                   -                    |
\t  |  SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL                               |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_DEFAULT_TC                                         |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP                                 |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP                                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCH_PROFILE_ID                                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO                                   |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_PATH_NAME                                     |                   -                    |
\t  |  SAI_SWITCH_ATTR_INIT_SWITCH                                            |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCH_STATE_CHANGE_NOTIFY                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SWITCH_SHUTDOWN_REQUEST_NOTIFY                         |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SHUTDOWN_REQUEST_NOTIFY                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FDB_EVENT_NOTIFY                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PORT_STATE_CHANGE_NOTIFY                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_PACKET_EVENT_NOTIFY                                    |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_FAST_API_ENABLE                                        |                   -                    |
\t  |  SAI_SWITCH_ATTR_MIRROR_TC                                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_ACL_STAGE_INGRESS                                      |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ACL_STAGE_EGRESS                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_SEGMENTROUTE_MAX_SID_DEPTH                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_SEGMENTROUTE_TLV_TYPE                                  |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES                                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_QUEUE_PFC_DEADLOCK_NOTIFY                              |            CTC7132,CTC8180             |
\t  |  SAI_SWITCH_ATTR_PFC_DLR_PACKET_ACTION                                  |                   -                    |
\t  |  SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL_RANGE                              |            CTC7132,CTC8180             |
\t  |  SAI_SWITCH_ATTR_PFC_TC_DLD_INTERVAL                                    |            CTC7132,CTC8180             |
\t  |  SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL_RANGE                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_PFC_TC_DLR_INTERVAL                                    |                   -                    |
\t  |  SAI_SWITCH_ATTR_SUPPORTED_PROTECTED_OBJECT_TYPE                        |                   -                    |
\t  |  SAI_SWITCH_ATTR_TPID_OUTER_VLAN                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_TPID_INNER_VLAN                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_CRC_CHECK_ENABLE                                       |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_BFD_SESSION_STATE_CHANGE_NOTIFY                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION                                  |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_BFD_SESSION                                        |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE                |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MIN_BFD_RX                                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MIN_BFD_TX                                             |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_ECN_ECT_THRESHOLD_ENABLE                               |                   -                    |
\t  |  SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC                               |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT                                     |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_MAX_MIRROR_SESSION                                     |                   -                    |
\t  |  SAI_SWITCH_ATTR_MAX_SAMPLED_MIRROR_SESSION                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE                          |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_TAM_OBJECT_ID                                          |                   -                    |
\t  |  SAI_SWITCH_ATTR_TAM_EVENT_NOTIFY                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_SUPPORTED_OBJECT_TYPE_LIST                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_PRE_SHUTDOWN                                           |    CTC8096,CTC7148,CTC7132,CTC8180     |
\t  |  SAI_SWITCH_ATTR_NAT_ZONE_COUNTER_OBJECT_ID                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_NAT_ENABLE                                             |                   -                    |
\t  |  SAI_SWITCH_ATTR_HARDWARE_ACCESS_BUS                                    |                   -                    |
\t  |  SAI_SWITCH_ATTR_PLATFROM_CONTEXT                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_REGISTER_READ                                          |                   -                    |
\t  |  SAI_SWITCH_ATTR_REGISTER_WRITE                                         |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_BROADCAST                            |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_LOAD_METHOD                                   |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_LOAD_TYPE                                     |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_DOWNLOAD_EXECUTE                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_BROADCAST_STOP                                |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_VERIFY_AND_INIT_SWITCH                        |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_STATUS                                        |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_MAJOR_VERSION                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_FIRMWARE_MINOR_VERSION                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_PORT_CONNECTOR_LIST                                    |                   -                    |
\t  |  SAI_SWITCH_ATTR_PROPOGATE_PORT_STATE_FROM_LINE_TO_SYSTEM_PORT_SUPPORT  |                   -                    |
\t  |  SAI_SWITCH_ATTR_TYPE                                                   |                   -                    |
\t  |  SAI_SWITCH_ATTR_MACSEC_OBJECT_ID                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_TC_MAP                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_MPLS_EXP_TO_COLOR_MAP                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_SWITCH_ID                                              |                   -                    |
\t  |  SAI_SWITCH_ATTR_MAX_SYSTEM_CORES                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_SYSTEM_PORT_CONFIG_LIST                                |                   -                    |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_SYSTEM_PORTS                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_SYSTEM_PORT_LIST                                       |                   -                    |
\t  |  SAI_SWITCH_ATTR_NUMBER_OF_FABRIC_PORTS                                 |                   -                    |
\t  |  SAI_SWITCH_ATTR_FABRIC_PORT_LIST                                       |                   -                    |
\e  |  SAI_SWITCH_ATTR_Y1731_SESSION_STATE_CHANGE_NOTIFY                      |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION                                |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MAX_Y1731_SESSION                                      |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE      |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_ECN_ACTION_ENABLE                                      |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_NOTIFY                                  |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_LATENCY_NOTIFY                                 |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE                       |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_MIN_THRD               |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_MAX_THRD               |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT               |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD              |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE  |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_QUEUE_PERIODIC_MONITOR_ENABLE |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL                   |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK               |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK                |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MIN_THRESHOLD                  |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_MAX_THRESHOLD                  |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD                |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL                       |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_SIGNAL_DEGRADE_EVENT_NOTIFY                            |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_PACKET_EVENT_PTP_TX_NOTIFY                             |            CTC7132,CTC8180             |
\e  |  SAI_SWITCH_ATTR_MAX_TWAMP_SESSION                                      |            CTC7132,CTC8180             |
\b
*/

#ifndef _CTC_SAI_SWITCH_H
#define _CTC_SAI_SWITCH_H

#define CTC_SAI_SWITCH_ATTR_NUMBER_OF_QUEUES 128        /* used in ctc_sai_switch_get_global_property */
#define CTC_SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUE 0    /* used in ctc_sai_switch_get_global_property */
#define CTC_SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL 1000*10    /* used in ctc_sai_switch_get_global_property */
#define CTC_SAI_SWITCH_ATTR_NV_STORAGE_SIZE 1024*10     /* used in ctc_sai_switch_get_global_property */
#define CTC_SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL 60 /* used in ctc_sai_switch_get_global_property */

#define CTC_SAI_SWITCH_ATTR_MAX_FCDL_INTERVAL_TIME 53   /* refer to SYS_MAX_FCDL_INTERVAL_TIME */


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
#include "ctc_sai_db.h"

/*don't need include other header files*/

extern sai_status_t ctc_sai_switch_api_init();
extern sai_status_t ctc_sai_switch_db_init(uint8 lchip);

extern void
ctc_sai_switch_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_SWITCH_H*/
