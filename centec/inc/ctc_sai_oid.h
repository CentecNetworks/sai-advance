/**
 @file ctc_sai_oid.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

   This file contains all sai object data structure, enum, macro and proto.
*/

#ifndef _CTC_SAI_OID_H
#define _CTC_SAI_OID_H
#include "sal.h"
#include "ctcs_api.h"
#include "ctc_sai.h"

/*don't need include other header files*/

struct ctc_object_id_s
{
    uint32  type:7;
    uint32  lchip:6;
    uint32  sub_type:3;
    uint32  value2:16;
    uint32  value;
};
typedef struct ctc_object_id_s ctc_object_id_t;

extern sai_object_id_t
ctc_sai_create_object_id(sai_object_type_t type, uint8 lchip, uint8 sub_type,uint16 value2,uint32 value);
extern sai_status_t
ctc_sai_get_ctc_object_id(sai_object_type_t type, sai_object_id_t object_id, ctc_object_id_t *ctc_object_id);
extern sai_status_t
ctc_sai_get_sai_object_id(sai_object_type_t type, ctc_object_id_t *ctc_oid,sai_object_id_t *object_id);
extern bool
ctc_sai_is_object_type_valid(sai_object_type_t object_type);
extern sai_status_t
ctc_sai_oid_get_gport(sai_object_id_t oid, uint32 *gport);

extern sai_status_t
ctc_sai_oid_get_vlanptr(sai_object_id_t oid, uint16 *vlanptr);
extern sai_status_t
ctc_sai_oid_get_lchip(sai_object_id_t oid, uint8_t *lchip);
extern sai_status_t
ctc_sai_oid_get_type(sai_object_id_t oid, sai_object_type_t *type);
extern sai_status_t
ctc_sai_oid_get_sub_type(sai_object_id_t oid, uint8_t *sub_type);
extern sai_status_t
ctc_sai_oid_get_value(sai_object_id_t oid, uint32_t *value);

extern sai_status_t
ctc_sai_oid_get_vlan_member_id(sai_object_id_t oid, uint16_t *vlan_id,uint32_t *gport);
extern sai_status_t
ctc_sai_oid_get_vrf_id(sai_object_id_t oid, uint16* vrf_id);
extern sai_status_t
ctc_sai_oid_get_l3if_id(sai_object_id_t oid, uint16* l3if_id);
extern sai_status_t
ctc_sai_oid_get_nexthop_id(sai_object_id_t oid, uint32* nexthop_id);
extern sai_status_t
ctc_sai_oid_get_twamp_session_id(sai_object_id_t oid, uint32* session_id);
extern sai_status_t
ctc_sai_oid_get_npm_session_id(sai_object_id_t oid, uint32* session_id);
extern sai_status_t
ctc_sai_oid_get_lag_member_id(sai_object_id_t oid, uint16* lag_id,uint32 *gport);
extern sai_status_t
ctc_sai_oid_get_counter_id(sai_object_id_t oid, uint32* counter_id);
extern sai_status_t
ctc_sai_oid_get_debug_counter_id(sai_object_id_t oid, uint32* dbg_counter_id);

#endif /*_CTC_SAI_OID_H*/

