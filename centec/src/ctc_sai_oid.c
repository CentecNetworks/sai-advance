#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
extern ctc_sai_db_t* g_sai_db[CTC_SAI_MAX_CHIP_NUM];

sai_object_id_t
ctc_sai_create_object_id(sai_object_type_t type, uint8 lchip, uint8 sub_type,uint16 value2,uint32 value)
{
    sai_object_id_t object_id = 0;
    ctc_object_id_t *ctc_object_id = (ctc_object_id_t*)&object_id;

    ctc_object_id->type = type;
    ctc_object_id->lchip = lchip;
    ctc_object_id->sub_type = sub_type;
    ctc_object_id->value2 = value2;
    ctc_object_id->value = value;
    return object_id;
}

sai_status_t
ctc_sai_get_ctc_object_id(sai_object_type_t type, sai_object_id_t object_id, ctc_object_id_t *ctc_object_id)
{
    sal_memcpy(ctc_object_id,&object_id, sizeof(sai_object_id_t));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_get_sai_object_id(sai_object_type_t type, ctc_object_id_t *ctc_object_id,sai_object_id_t *object_id)
{
    if (type != ctc_object_id->type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Ctc object to sai object, ctc object type %u sai object type %u\n", ctc_object_id->type, type);
        return SAI_STATUS_INVALID_OBJECT_TYPE;
    }
    sal_memcpy(object_id, ctc_object_id, sizeof(sai_object_id_t));
    return SAI_STATUS_SUCCESS;
}

bool ctc_sai_is_object_type_valid(sai_object_type_t object_type)
{
    return (object_type > SAI_OBJECT_TYPE_NULL) && (object_type < SAI_OBJECT_TYPE_MAX);
}

sai_status_t
ctc_sai_oid_get_gport(sai_object_id_t oid, uint32_t *gport)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, oid, &ctc_oid));
 #if 0
    if (ctc_oid.type != SAI_OBJECT_TYPE_PORT)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PORT, "Invalid port object type %llu \n",oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
#endif

    *gport = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_oid_get_lchip(sai_object_id_t oid, uint8_t *lchip)
{
    ctc_object_id_t ctc_oid;
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_oid));
    if ((ctc_oid.lchip >= CTC_SAI_MAX_CHIP_NUM) || (NULL == g_sai_db[ctc_oid.lchip]))
    {
        return SAI_STATUS_UNINITIALIZED;
    }
    *lchip = ctc_oid.lchip;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_type(sai_object_id_t oid, sai_object_type_t *type)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_oid));


    *type = ctc_oid.type;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_sub_type(sai_object_id_t oid, uint8_t *sub_type)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, oid, &ctc_oid));


    *sub_type = ctc_oid.sub_type;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_value(sai_object_id_t oid, uint32_t *value)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, oid, &ctc_oid));

    *value = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_oid_get_vlanptr(sai_object_id_t oid, uint16 *vlanptr)
{
    ctc_object_id_t  ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, oid, &ctc_oid));

    if (ctc_oid.type != SAI_OBJECT_TYPE_VLAN)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Invalid vlan object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    *vlanptr = (uint16_t)ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_oid_get_vlan_member_id(sai_object_id_t oid, uint16_t *vlan_ptr, uint32_t *gport)
{
    ctc_object_id_t  ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN_MEMBER, oid, &ctc_oid));

    if (ctc_oid.type != SAI_OBJECT_TYPE_VLAN_MEMBER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Invalid vlan object type 0x%llx \n",oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *gport = ctc_oid.value ;
    *vlan_ptr = ctc_oid.value2 ;

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_oid_get_lag_member_id(sai_object_id_t oid, uint16 *lag_id,uint32 *gport)
{
    ctc_object_id_t  ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_LAG_MEMBER, oid, &ctc_oid));

    if (ctc_oid.type != SAI_OBJECT_TYPE_LAG_MEMBER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_LAG, "Invalid lag member object type %llu \n",oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *gport = ctc_oid.value ;
    *lag_id = ctc_oid.value2 ;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_vrf_id(sai_object_id_t oid, uint16* vrf_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_VIRTUAL_ROUTER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VIRTUAL_ROUTER, "Invalid virtual router object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *vrf_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_l3if_id(sai_object_id_t oid, uint16* l3if_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_ROUTER_INTERFACE)
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_ROUTER_INTERFACE, "Invalid router interface object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *l3if_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_nexthop_id(sai_object_id_t oid, uint32* nexthop_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, oid, &ctc_oid));
    if ((ctc_oid.type != SAI_OBJECT_TYPE_NEXT_HOP)
        &&(ctc_oid.type != SAI_OBJECT_TYPE_NEXT_HOP_GROUP))
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_NEXT_HOP, "Invalid next hop object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *nexthop_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_twamp_session_id(sai_object_id_t oid, uint32* session_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TWAMP, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_TWAMP)
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_TWAMP, "Invalid session id object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *session_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_npm_session_id(sai_object_id_t oid, uint32* session_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NPM, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_NPM)
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_NPM, "Invalid session id object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *session_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_counter_id(sai_object_id_t oid, uint32* counter_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_COUNTER, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_COUNTER)
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_COUNTER, "Invalid counter object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *counter_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_oid_get_debug_counter_id(sai_object_id_t oid, uint32* dbg_counter_id)
{
    ctc_object_id_t ctc_oid;
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_DEBUG_COUNTER, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_DEBUG_COUNTER)
    {
        CTC_SAI_LOG_ERROR(SAI_OBJECT_TYPE_DEBUG_COUNTER, "Invalid debug counter object type 0x%llx \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *dbg_counter_id = ctc_oid.value;
    return SAI_STATUS_SUCCESS;
}

