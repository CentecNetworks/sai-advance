/**
 @file ctc_sai_warmboot.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-03-15

 @version v2.0

   This file contains all sai object data structure, enum, macro and proto.
*/

#ifndef _CTC_SAI_WARMBOOT_H
#define _CTC_SAI_WARMBOOT_H

#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"

#define SYS_WB_VERSION_ACL                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_BRIDGE             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_BUFFER             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_FDB                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_HASH               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_HOSTIF             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_IPMC               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_IPMCGROUP          CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_L2MC               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_L2MCGROUP          CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_LAG                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_MCASTFDB           CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_MIRROR             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_MPLS               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_NEIGHBOR           CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_NEXTHOP            CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_NEXTHOPGROUP       CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_POLICER            CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_PORT               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_QOSMAP             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_QUEUE              CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_ROUTE              CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_ROUTERINTERFACE    CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_RPFGROUP           CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_SAMPLEPACKET       CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_SCHEDULER          CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_SCHEDULERGROUP     CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_SEGMENTROUTE       CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_STP                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_SWITCH             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_TAM                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_TUNNEL             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_UBURST             CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_UDF                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_VIRTUALROUTER      CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_VLAN               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_WRED               CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_ISOLATION_GROUP    CTC_WB_VERSION(1,0)

#define SYS_WB_VERSION_COUNTER            CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_DEBUG_COUNTER      CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_NAT                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_BFD                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_TWAMP              CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_NPM                CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_Y1731              CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_ES                 CTC_WB_VERSION(1,0)
#define SYS_WB_VERSION_PTP              CTC_WB_VERSION(1,0)

typedef enum ctc_sai_wb_user_def_sub_type_e
{
    CTC_SAI_WB_USER_DEF_SUB_TYPE_QOSMAP = 0,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_HASH,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_SESSION,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_MIRROR_VEC,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_GROUP_OUTPUT_LIST,  // for l2mc
    CTC_SAI_WB_USER_DEF_SUB_TYPE_IP_MCAST_GROUP_OUTPUT_LIST, // for ipmc
    CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_ENTRY_BIND_LIST,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_SAMPLEPACKET,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_NEIGHBOR,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_NEXT_HOP,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_NH_ID,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_MAPPER_INFO,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_MEMBER,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_BIND_POINT,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_MEMBER,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_TABLE_GROUP_LIST,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_KEY,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_ACL_ENTRY_ACTION,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_BFD_GLOBAL,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_Y1731,
    CTC_SAI_WB_USER_DEF_SUB_TYPE_MAX
}ctc_sai_wb_user_def_sub_type_t;

typedef enum ctc_sai_wb_type_e
{
    CTC_SAI_WB_TYPE_OID = CTC_FEATURE_MAX,
    CTC_SAI_WB_TYPE_ENTRY,
    CTC_SAI_WB_TYPE_VECTOR,
    CTC_SAI_WB_TYPE_VERSION,
    CTC_SAI_WB_TYPE_USER_DEF,
    CTC_SAI_WB_TYPE_MAX
}ctc_sai_wb_type_t;

#define CTC_SAI_WARMBOOT_STATUS_CHECK(lchip) \
{ \
        if(CTC_WB_STATUS_DONE != ctc_sai_warmboot_get_status(lchip)) \
        { \
             return SAI_STATUS_SUCCESS; \
        } \
}
extern sai_status_t
ctc_sai_warmboot_sync(uint8 lchip);

extern sai_status_t
ctc_sai_warmboot_init(uint8 lchip, uint8 reloading);

extern sai_status_t
ctc_sai_warmboot_init_done(uint8 lchip, uint8 reloading);

extern uint8
ctc_sai_warmboot_get_status(uint8 lchip);

extern sai_status_t
ctc_sai_warmboot_register_cb(uint8 lchip, uint32 wb_type, uint32 wb_sub_type, void* wb_info);

#endif /*_CTC_SAI_WARMBOOT_H*/

