#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

#include "ctcs_api.h"
#include "ctc_sai_port.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_isolation_group.h"


#define ________ISOLATION_GROUP_INTERNAL_______

static sai_status_t
_ctc_sai_isolation_group_db_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_isolation_group_t* p_ist_grp = NULL;

    p_ist_grp = (ctc_sai_isolation_group_t*)bucket_data->data;
    ctc_slist_free(p_ist_grp->port_list);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_isolation_group_alloc_group(ctc_sai_isolation_group_t** p_ist_grp)
{
    ctc_sai_isolation_group_t* p_ist_grp_temp = NULL;

    p_ist_grp_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_isolation_group_t));
    if (NULL == p_ist_grp_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_ist_grp_temp, 0, sizeof(ctc_sai_isolation_group_t));

    p_ist_grp_temp->port_list = ctc_slist_new();
    if (NULL == p_ist_grp_temp->port_list)
    {
        mem_free(p_ist_grp_temp);
        return SAI_STATUS_NO_MEMORY;
    }

    *p_ist_grp = p_ist_grp_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_isolation_group_free_group(ctc_sai_isolation_group_t* p_ist_grp)
{
    ctc_sai_isolation_group_member_t* p_member = NULL;
    ctc_slistnode_t        *node = NULL, *next_node = NULL;

    CTC_SLIST_LOOP_DEL(p_ist_grp->port_list, node, next_node)
    {
        p_member = (ctc_sai_isolation_group_member_t*)node;
        mem_free(p_member);
    }
    ctc_slist_free(p_ist_grp->port_list);

    mem_free(p_ist_grp);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_isolation_group_create_group(
        _Out_ sai_object_id_t *isolation_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val  = NULL;
    uint32 attr_idx = 0;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;
    ctc_port_isolation_t port_isolation;

    CTC_SAI_PTR_VALID_CHECK(isolation_group_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    sal_memset(&port_isolation, 0, sizeof(ctc_port_isolation_t));
    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ISOLATION_GROUP_ATTR_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ISOLATION_GROUP, "Missing mandatory attribute group type on create of isolation group\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_isolation_group_alloc_group(&p_ist_grp));
    p_ist_grp->ist_type = attr_val->s32;

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP, &p_ist_grp->ist_grp_id), status, roll_back_1);
    *isolation_group_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP, lchip, 0, 0, p_ist_grp->ist_grp_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *isolation_group_id, p_ist_grp), status, roll_back_2);

    port_isolation.use_isolation_id = 1;
    port_isolation.gport = p_ist_grp->ist_grp_id;
    port_isolation.pbm[0] = 1<<p_ist_grp->ist_grp_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_isolation(lchip, &port_isolation), status, roll_back_3);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;
roll_back_3:
    ctc_sai_db_remove_object_property(lchip, *isolation_group_id);

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP, p_ist_grp->ist_grp_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_isolation_group_free_group(p_ist_grp);

    return status;
}

static sai_status_t
ctc_sai_isolation_group_remove_group(
            _In_ sai_object_id_t isolation_group_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;
    ctc_port_isolation_t port_isolation;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&port_isolation, 0, sizeof(ctc_port_isolation_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP, isolation_group_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_ist_grp = ctc_sai_db_get_object_property(lchip, isolation_group_id);
    if (NULL == p_ist_grp)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, isolation_group_id);
    CTC_SAI_DB_UNLOCK(lchip);

    port_isolation.use_isolation_id = 1;
    port_isolation.gport = p_ist_grp->ist_grp_id;
    port_isolation.pbm[0] = 0;
    ctcs_port_set_isolation(lchip, &port_isolation);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP, p_ist_grp->ist_grp_id);

    _ctc_sai_isolation_group_free_group(p_ist_grp);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_isolation_group_get_group_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = NULL;
    ctc_slistnode_t* p_temp_node = NULL;
    sai_object_id_t* p_obj_list = NULL;
    uint32 index = 0;

    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_ist_grp = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_ist_grp)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_ISOLATION_GROUP, "object id %"PRIx64" get isolation group attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_ISOLATION_GROUP_ATTR_TYPE:
            attr->value.s32 = p_ist_grp->ist_type;
            break;
        case SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST:
            p_obj_list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*(p_ist_grp->port_list->count));
            CTC_SLIST_LOOP(p_ist_grp->port_list, p_temp_node)
            {
                p_ist_grp_mem = (ctc_sai_isolation_group_member_t*)p_temp_node;
                p_obj_list[index] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, lchip, 0, 0, p_ist_grp_mem->ist_grp_mem_id);
                index++;
            }

            status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), p_obj_list, index, &attr->value.objlist);
            if(CTC_SAI_ERROR(status))
            {
                status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            mem_free(p_obj_list);
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_ISOLATION_GROUP, "Isolation group attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t isolation_group_attr_fn_entries[] = {
    {SAI_ISOLATION_GROUP_ATTR_TYPE, ctc_sai_isolation_group_get_group_property, NULL},
    {SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST, ctc_sai_isolation_group_get_group_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
ctc_sai_isolation_group_set_group_attribute(
        _In_ sai_object_id_t isolation_group_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = isolation_group_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(isolation_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = isolation_group_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_ISOLATION_GROUP, isolation_group_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_isolation_group_get_group_attribute(
        _In_ sai_object_id_t isolation_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = isolation_group_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(isolation_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = isolation_group_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_ISOLATION_GROUP, loop, isolation_group_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________ISOLATION_GROUP_MEMBER_INTERNAL_______

static sai_status_t
_ctc_sai_isolation_group_alloc_member(ctc_sai_isolation_group_member_t** p_ist_grp_mem)
{
    ctc_sai_isolation_group_member_t* p_ist_grp_mem_temp = NULL;

    p_ist_grp_mem_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_isolation_group_member_t));
    if (NULL == p_ist_grp_mem_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_ist_grp_mem_temp, 0, sizeof(ctc_sai_isolation_group_member_t));

    *p_ist_grp_mem = p_ist_grp_mem_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_isolation_group_free_member(ctc_sai_isolation_group_member_t* p_ist_grp_mem)
{

    mem_free(p_ist_grp_mem);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_isolation_group_create_member(
        _Out_ sai_object_id_t *isolation_group_member_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    const sai_attribute_value_t *attr_grp_val  = NULL;
    uint32 attr_grp_idx = 0;
    const sai_attribute_value_t *attr_port_val  = NULL;
    uint32 attr_port_idx = 0;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = NULL;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;
    ctc_port_restriction_t port_restriction;
    uint32 isolation_id = 0;

    CTC_SAI_PTR_VALID_CHECK(isolation_group_member_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID, &attr_grp_val, &attr_grp_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ISOLATION_GROUP, "Missing mandatory attribute isolation group id on create of isolation group member\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP_PORT, attr_grp_val->oid, &ctc_object_id);
    isolation_id = ctc_object_id.value;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT, &attr_port_val, &attr_port_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ISOLATION_GROUP, "Missing mandatory attribute isolation port object on create of isolation group member\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP_PORT, attr_port_val->oid, &ctc_object_id);
    if ((SAI_OBJECT_TYPE_PORT != ctc_object_id.type) && (SAI_OBJECT_TYPE_BRIDGE_PORT != ctc_object_id.type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    if ((SAI_OBJECT_TYPE_BRIDGE_PORT == ctc_object_id.type) && (SAI_BRIDGE_PORT_TYPE_PORT != ctc_object_id.sub_type))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_isolation_group_alloc_member(&p_ist_grp_mem));
    p_ist_grp_mem->ist_grp_id = attr_grp_val->oid;
    p_ist_grp_mem->port_id = attr_port_val->oid;

    CTC_SAI_DB_LOCK(lchip);

    p_ist_grp_mem->ist_grp_mem_id = ctc_object_id.value;

    *isolation_group_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, lchip, 0, 0, p_ist_grp_mem->ist_grp_mem_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *isolation_group_member_id, p_ist_grp_mem), status, roll_back_1);
    p_ist_grp = ctc_sai_db_get_object_property(lchip, p_ist_grp_mem->ist_grp_id);
    if (NULL == p_ist_grp)
    {
        status = SAI_STATUS_FAILURE;
        goto roll_back_2;
    }
    if (((SAI_ISOLATION_GROUP_TYPE_PORT == p_ist_grp->ist_type) && (SAI_OBJECT_TYPE_PORT != ctc_object_id.type))
        || ((SAI_ISOLATION_GROUP_TYPE_BRIDGE_PORT == p_ist_grp->ist_type) && (SAI_OBJECT_TYPE_BRIDGE_PORT != ctc_object_id.type)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_grp_idx;
        goto roll_back_2;
    }
    ctc_slist_add_tail(p_ist_grp->port_list, &(p_ist_grp_mem->head));

    port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
    port_restriction.type = CTC_PORT_ISOLATION_ALL;
    port_restriction.dir = CTC_EGRESS;
    port_restriction.isolated_id = isolation_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_restriction(lchip, ctc_object_id.value, &port_restriction), status, roll_back_3);

    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_3:
    ctc_slist_delete_node(p_ist_grp->port_list, &(p_ist_grp_mem->head));

roll_back_2:
    ctc_sai_db_remove_object_property(lchip, *isolation_group_member_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_isolation_group_free_member(p_ist_grp_mem);

    return status;
}

static sai_status_t
ctc_sai_isolation_group_remove_member(
        _In_ sai_object_id_t isolation_group_member_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = NULL;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;
    uint8 lchip = 0;
    ctc_port_restriction_t port_restriction;

    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&port_restriction, 0, sizeof(ctc_port_restriction_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, isolation_group_member_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_ist_grp_mem = ctc_sai_db_get_object_property(lchip, isolation_group_member_id);
    if (NULL == p_ist_grp_mem)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_ist_grp = ctc_sai_db_get_object_property(lchip, p_ist_grp_mem->ist_grp_id);
    if (NULL == p_ist_grp)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_slist_delete_node(p_ist_grp->port_list, &(p_ist_grp_mem->head));
    ctc_sai_db_remove_object_property(lchip, isolation_group_member_id);

    port_restriction.mode = CTC_PORT_RESTRICTION_PORT_ISOLATION;
    port_restriction.type = CTC_PORT_ISOLATION_ALL;
    port_restriction.dir = CTC_EGRESS;
    port_restriction.isolated_id = 0;
    ctcs_port_set_restriction(lchip, ctc_oid.value, &port_restriction);

    CTC_SAI_DB_UNLOCK(lchip);

    _ctc_sai_isolation_group_free_member(p_ist_grp_mem);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_isolation_group_get_member_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_ist_grp_mem = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_ist_grp_mem)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_ISOLATION_GROUP, "object id %"PRIx64" get isolation group member attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID:
            attr->value.oid = p_ist_grp_mem->ist_grp_id;
            break;
        case SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT:
            attr->value.oid = p_ist_grp_mem->port_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_ISOLATION_GROUP, "Isolation group member attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t isolation_group_member_attr_fn_entries[] = {
    {SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID, ctc_sai_isolation_group_get_member_property, NULL},
    {SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT, ctc_sai_isolation_group_get_member_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
ctc_sai_isolation_group_set_member_attribute(
        _In_ sai_object_id_t isolation_group_member_id,
        _In_ const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = isolation_group_member_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(isolation_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = isolation_group_member_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, isolation_group_member_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_isolation_group_get_member_attribute(
        _In_ sai_object_id_t isolation_group_member_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = isolation_group_member_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_ISOLATION_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(isolation_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = isolation_group_member_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, loop, isolation_group_member_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________ISOLATION_GROUP_WB_______

static sai_status_t
_ctc_sai_isolation_group_wb_reload_member_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t ist_grp_mem_id = *(sai_object_id_t*)key;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = (ctc_sai_isolation_group_member_t*)data;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ist_grp_mem_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));

    p_ist_grp = ctc_sai_db_get_object_property(lchip, p_ist_grp_mem->ist_grp_id);
    if (NULL == p_ist_grp)
    {
        return SAI_STATUS_FAILURE;
    }
    ctc_slist_add_tail(p_ist_grp->port_list, &(p_ist_grp_mem->head));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_isolation_group_wb_reload_group_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t ist_grp_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_oid;
    ctc_sai_isolation_group_t* p_ist_grp = (ctc_sai_isolation_group_t*)data;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ist_grp_id, &ctc_oid);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ISOLATION_GROUP, ctc_oid.value));

    p_ist_grp->port_list = ctc_slist_new();
    if (NULL == p_ist_grp->port_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    return status;
}

#define ________ISOLATION_GROUP_DUMP________

static sai_status_t
_ctc_sai_isolation_group_dump_group_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  ist_grp_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_isolation_group_t* p_ist_grp = NULL;

    ist_grp_oid = bucket_data->oid;
    p_ist_grp = (ctc_sai_isolation_group_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (ist_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d %-8d\n", num_cnt, ist_grp_oid,\
           p_ist_grp->ist_type, p_ist_grp->port_list->count);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_isolation_group_dump_member_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  ist_grp_mem_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_isolation_group_member_t* p_ist_grp_mem = NULL;

    ist_grp_mem_oid = bucket_data->oid;
    p_ist_grp_mem = (ctc_sai_isolation_group_member_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (ist_grp_mem_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" 0x%016"PRIx64" 0x%016"PRIx64"\n", num_cnt, ist_grp_mem_oid,\
                p_ist_grp_mem->port_id, p_ist_grp_mem->ist_grp_id);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_isolation_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;

    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Isolation Group MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ISOLATION_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Isolation Group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_isolation_group_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-8s\n", "No.", "Ist_grp_id", "Type", "Port_cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ISOLATION_GROUP,
                                            (hash_traversal_fn)_ctc_sai_isolation_group_dump_group_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Isolation Group Member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_isolation_group_member_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-18s %-18s\n", "No.", "Ist_grp_mem_id", "Port_id", "Ist_grp_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ISOLATION_GROUP,
                                            (hash_traversal_fn)_ctc_sai_isolation_group_dump_member_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________ISOLATION_GROUP_API________

sai_isolation_group_api_t g_ctc_sai_isolation_group_api = {
     ctc_sai_isolation_group_create_group,
     ctc_sai_isolation_group_remove_group,
     ctc_sai_isolation_group_set_group_attribute,
     ctc_sai_isolation_group_get_group_attribute,
     ctc_sai_isolation_group_create_member,
     ctc_sai_isolation_group_remove_member,
     ctc_sai_isolation_group_set_member_attribute,
     ctc_sai_isolation_group_get_member_attribute,
};

sai_status_t
ctc_sai_isolation_group_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ISOLATION_GROUP;
    wb_info.data_len = sizeof(ctc_sai_isolation_group_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_isolation_group_wb_reload_group_cb;
    wb_info.wb_reload_cb1 = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ISOLATION_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ISOLATION_GROUP;
    wb_info.data_len = sizeof(ctc_sai_isolation_group_member_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_isolation_group_wb_reload_member_cb;
    wb_info.wb_reload_cb1 = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_isolation_group_db_deinit(uint8 lchip)
{
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ISOLATION_GROUP, (hash_traversal_fn)_ctc_sai_isolation_group_db_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_isolation_group_api_init()
{
    ctc_sai_register_module_api(SAI_API_ISOLATION_GROUP, (void*)&g_ctc_sai_isolation_group_api);

    return SAI_STATUS_SUCCESS;
}

