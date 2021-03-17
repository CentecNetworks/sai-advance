
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctcs_api.h"

#include "ctc_sai_vlan.h"
#include "ctc_dkit_api.h"
#include "ctc_sai_tunnel.h"
#include "ctc_sai_router_interface.h"

typedef struct ctc_sai_tunnel_nh_info_s
{
    ctc_slistnode_t    head;
    sai_ip_address_t ip_addr;
    uint32 nh_id;

}ctc_sai_tunnel_nh_info_t;

typedef struct  ctc_sai_wb_tunnel_nh_info_s
{
    /*key*/
   sai_object_id_t tunnel_oid;
   uint32 nh_id;
   uint32 calc_key_len[0];
    /*data*/
   sai_ip_address_t ip_addr;
}ctc_sai_wb_tunnel_nh_info_t;

typedef struct  ctc_sai_wb_tunnel_mapper_s
{
    /*key*/
   sai_object_id_t tunnel_oid;
   sai_object_id_t tunnel_map_oid;
   uint32 calc_key_len[0];
   /*data*/
   uint32  is_encap;
}ctc_sai_wb_tunnel_mapper_t;

#define ________TUNNEL_INNER________
static sai_status_t
_ctc_sai_tunnel_db_map_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;

    p_tunnel_map = (ctc_sai_tunnel_map_t*)bucket_data->data;
    ctc_slist_delete(p_tunnel_map->map_entry_list);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_db_tunnel_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_sai_tunnel_nh_info_t* p_tunnel_info = NULL;
    ctc_slistnode_t        *node = NULL, *next_node = NULL;

    p_tunnel = (ctc_sai_tunnel_t*)bucket_data->data;
    CTC_SLIST_LOOP_DEL(p_tunnel->encap_nh_list, node, next_node)
    {
        p_tunnel_info = (ctc_sai_tunnel_nh_info_t*)node;
        mem_free(p_tunnel_info);
    }
    ctc_slist_free(p_tunnel->encap_nh_list);

    ctc_slist_free(p_tunnel->encap_map_list);

    ctc_slist_free(p_tunnel->decap_map_list);

    return SAI_STATUS_SUCCESS;
}

#define ________TUNNEL_MAP_ENTRY________

static sai_status_t
_ctc_sai_tunnel_alloc_tunnel_map_entry(ctc_sai_tunnel_map_entry_t** p_tunnel_map_entry)
{
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry_tmp = NULL;

    p_tunnel_map_entry_tmp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_map_entry_t));
    if (NULL == p_tunnel_map_entry_tmp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_tunnel_map_entry_tmp, 0, sizeof(ctc_sai_tunnel_map_entry_t));

    *p_tunnel_map_entry = p_tunnel_map_entry_tmp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_free_tunnel_map_entry(ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry)
{
    mem_free(p_tunnel_map_entry);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_get_tunnel_map_entry_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_tunnel_map_entry = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tunnel_map_entry)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_TUNNEL, "object id %"PRIx64" get tunnel map entry attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE:
            attr->value.s32 = p_tunnel_map_entry->tunnel_map_type;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP:
            attr->value.oid = p_tunnel_map_entry->tunnel_map_id;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY:
            attr->value.u8 = p_tunnel_map_entry->oecn_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE:
            attr->value.u8 = p_tunnel_map_entry->oecn_val;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY:
            attr->value.u8 = p_tunnel_map_entry->uecn_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE:
            attr->value.u8 = p_tunnel_map_entry->uecn_val;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY:
            attr->value.u16 = p_tunnel_map_entry->vlan_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE:
            attr->value.u16 = p_tunnel_map_entry->vlan_val;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY:
            attr->value.u32 = p_tunnel_map_entry->vni_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE:
            attr->value.u32 = p_tunnel_map_entry->vni_val;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY:
            attr->value.oid = p_tunnel_map_entry->brg_id_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE:
            attr->value.oid = p_tunnel_map_entry->brg_id_val;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY:
            attr->value.oid = p_tunnel_map_entry->vrf_key;
            break;
        case SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE:
            attr->value.oid = p_tunnel_map_entry->vrf_val;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel map entry attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_NOT_IMPLEMENTED;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t tunnel_map_entry_attr_fn_entries[] = {
    {SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE, _ctc_sai_tunnel_get_tunnel_map_entry_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
_ctc_sai_tunnel_add_ctc_tunnel(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term);

static sai_status_t
_ctc_sai_tunnel_traverse_tunnel_term_cb(void* bucket_data, void* user_data)
{
    uint8 lchip = ((ctc_sai_db_traverse_param_t*)user_data)->lchip;
    sai_object_id_t tunnel_id = *(sai_object_id_t*)(((ctc_sai_db_traverse_param_t*)user_data)->value0);
    ctc_sai_oid_property_t* p_tunnel_term_property = (ctc_sai_oid_property_t*)bucket_data;
    ctc_sai_tunnel_term_table_entry_t* p_tunnel_term = (ctc_sai_tunnel_term_table_entry_t*)p_tunnel_term_property->data;
    if (tunnel_id == p_tunnel_term->tunnel_id && p_tunnel_term->not_finished)
    {
        int32 ret = 0;
        ret = _ctc_sai_tunnel_add_ctc_tunnel(lchip, p_tunnel_term);
        if (!CTC_SAI_ERROR(ret))
        {
          p_tunnel_term->not_finished = 0;
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_traverse_tunnel_cb(void* bucket_data, void* user_data)
{
    // need tunnel map id, encap or decap,
    uint8 is_find = 0;
    uint8 lchip = ((ctc_sai_db_traverse_param_t*)user_data)->lchip;
    ctc_sai_oid_property_t* p_tunnel_property = (ctc_sai_oid_property_t*)bucket_data;
    ctc_sai_tunnel_t* p_tunnel = (ctc_sai_tunnel_t*)p_tunnel_property->data;
    ctc_slistnode_t* ctc_slistnode = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    ctc_sai_db_traverse_param_t traverse_param = {0};
    sai_object_id_t* p_tunnel_map_id = (sai_object_id_t*)(((ctc_sai_db_traverse_param_t*)user_data)->value0);
    sai_object_id_t tunnel_map_id = 0;

    CTC_SLIST_LOOP(p_tunnel->encap_map_list, ctc_slistnode)
    {
        p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, encap);
        tunnel_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
        if (tunnel_map_id == *p_tunnel_map_id)
        {
            is_find = 1;
            break;
        }
    }
    CTC_SLIST_LOOP(p_tunnel->decap_map_list, ctc_slistnode)
    {
        p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, decap);
        tunnel_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
        if (tunnel_map_id == *p_tunnel_map_id)
        {
            is_find = 1;
            break;
        }
    }
    if (is_find)
    {
        traverse_param.lchip = lchip;
        traverse_param.value0 = &p_tunnel_property->oid;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, _ctc_sai_tunnel_traverse_tunnel_term_cb, &traverse_param);
    }
    return SAI_STATUS_SUCCESS;

}

static sai_status_t
ctc_sai_tunnel_create_tunnel_map_entry(
        sai_object_id_t *tunnel_map_entry_id,
        sai_object_id_t switch_id,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val  = NULL;
    uint32_t                     attr_idx;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    ctc_sai_db_traverse_param_t traverse_param = {0};

    CTC_SAI_PTR_VALID_CHECK(tunnel_map_entry_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel map type on create of tunnel map entry\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else if (attr_val->s32 > SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI)
    {
        return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_alloc_tunnel_map_entry(&p_tunnel_map_entry));
    p_tunnel_map_entry->tunnel_map_type = attr_val->s32;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel map on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    p_tunnel_map_entry->tunnel_map_id = attr_val->oid;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && ((p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN)
        || (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute ocen key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->oecn_key = attr_val->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_OECN_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute ocen value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->oecn_val = attr_val->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute uecn key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else
    {
        p_tunnel_map_entry->uecn_key = attr_val->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_UECN_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status)&& (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute ucen value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->uecn_val = attr_val->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vlan id key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vlan_key = attr_val->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (p_tunnel_map_entry->tunnel_map_type == SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vlan id value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vlan_val = attr_val->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && ((SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID == p_tunnel_map_entry->tunnel_map_type)
        || (SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == p_tunnel_map_entry->tunnel_map_type)
        || (SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID == p_tunnel_map_entry->tunnel_map_type)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vni id key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vni_key = attr_val->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && ((SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type)
        || (SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == p_tunnel_map_entry->tunnel_map_type)
        || (SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vni id value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vni_val = attr_val->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == p_tunnel_map_entry->tunnel_map_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute bridge id key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->brg_id_key = attr_val->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_BRIDGE_ID_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == p_tunnel_map_entry->tunnel_map_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute bridge id value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->brg_id_val = attr_val->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_KEY, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vrf key on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vrf_key = attr_val->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ENTRY_ATTR_VIRTUAL_ROUTER_ID_VALUE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status) && (SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID == p_tunnel_map_entry->tunnel_map_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vrf value on create of tunnel map entry\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto roll_back_0;
    }
    else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    else if (!CTC_SAI_ERROR(status))
    {
        p_tunnel_map_entry->vrf_val = attr_val->oid;
    }

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_tunnel_map_entry->tunnel_map_entry_id), status, roll_back_1);
    *tunnel_map_entry_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, lchip, 0, 0, p_tunnel_map_entry->tunnel_map_entry_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *tunnel_map_entry_id, p_tunnel_map_entry), status, roll_back_2);
    p_tunnel_map = ctc_sai_db_get_object_property(lchip, p_tunnel_map_entry->tunnel_map_id);
    if (NULL == p_tunnel_map)
    {
        status = SAI_STATUS_FAILURE;
        goto roll_back_3;
    }
    ctc_slist_add_tail(p_tunnel_map->map_entry_list, &(p_tunnel_map_entry->head));
    traverse_param.lchip = lchip;
    traverse_param.value0 = &p_tunnel_map_entry->tunnel_map_id;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL, _ctc_sai_tunnel_traverse_tunnel_cb, &traverse_param);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_3:
    ctc_sai_db_remove_object_property(lchip, *tunnel_map_entry_id);

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_map_entry->tunnel_map_entry_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);

roll_back_0:
    _ctc_sai_tunnel_free_tunnel_map_entry(p_tunnel_map_entry);

    return status;
}

static sai_status_t
ctc_sai_tunnel_remove_tunnel_map_entry(
        sai_object_id_t tunnel_map_entry_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, tunnel_map_entry_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    
    p_tunnel_map_entry = ctc_sai_db_get_object_property(lchip, tunnel_map_entry_id);
    if (NULL == p_tunnel_map_entry)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_tunnel_map = ctc_sai_db_get_object_property(lchip, p_tunnel_map_entry->tunnel_map_id);
    if (NULL == p_tunnel_map)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_slist_delete_node(p_tunnel_map->map_entry_list, &(p_tunnel_map_entry->head));
    ctc_sai_db_remove_object_property(lchip, tunnel_map_entry_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_map_entry->tunnel_map_entry_id);

    _ctc_sai_tunnel_free_tunnel_map_entry(p_tunnel_map_entry);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_tunnel_set_tunnel_map_entry_attribute(
        sai_object_id_t tunnel_map_entry_id,
        const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = tunnel_map_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_map_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_map_entry_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, tunnel_map_entry_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_map_entry_attribute(
        sai_object_id_t tunnel_map_entry_id,
        uint32_t attr_count,
        sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = tunnel_map_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_map_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_map_entry_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, loop, tunnel_map_entry_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________TUNNEL_MAP________

static sai_status_t
_ctc_sai_tunnel_alloc_tunnel_map(ctc_sai_tunnel_map_t** p_tunnel_map)
{
    ctc_sai_tunnel_map_t* p_tunnel_map_tmp = NULL;

    p_tunnel_map_tmp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_map_t));
    if (NULL == p_tunnel_map_tmp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_tunnel_map_tmp, 0, sizeof(ctc_sai_tunnel_map_t));

    p_tunnel_map_tmp->map_entry_list = ctc_slist_new();
    if (NULL == p_tunnel_map_tmp->map_entry_list)
    {
        mem_free(p_tunnel_map_tmp);
        return SAI_STATUS_NO_MEMORY;
    }

    *p_tunnel_map = p_tunnel_map_tmp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_free_tunnel_map(ctc_sai_tunnel_map_t* p_tunnel_map)
{
    ctc_slist_delete(p_tunnel_map->map_entry_list);
    mem_free(p_tunnel_map);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_get_tunnel_map_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = NULL;
    ctc_slistnode_t* p_temp_node = NULL;
    sai_object_id_t* p_obj_list = NULL;
    uint32 index = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_tunnel_map = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tunnel_map)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_LOG_INFO(SAI_API_TUNNEL, "object id %"PRIx64" get tunnel map attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_TUNNEL_MAP_ATTR_TYPE:
            attr->value.s32 = p_tunnel_map->tunnel_map_type;
            break;
        case SAI_TUNNEL_MAP_ATTR_ENTRY_LIST:
            p_obj_list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*(p_tunnel_map->map_entry_list->count));
            CTC_SLIST_LOOP(p_tunnel_map->map_entry_list, p_temp_node)
            {
                p_tunnel_map_entry = (ctc_sai_tunnel_map_entry_t*)p_temp_node;
                p_obj_list[index] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, lchip, 0, 0, p_tunnel_map_entry->tunnel_map_entry_id);
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
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel map attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_NOT_IMPLEMENTED;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t tunnel_map_attr_fn_entries[] = {
    {SAI_TUNNEL_MAP_ATTR_TYPE, _ctc_sai_tunnel_get_tunnel_map_property, NULL},
    {SAI_TUNNEL_MAP_ATTR_ENTRY_LIST, _ctc_sai_tunnel_get_tunnel_map_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
ctc_sai_tunnel_create_tunnel_map(
        sai_object_id_t *tunnel_map_id,
        sai_object_id_t switch_id,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val  = NULL;
    uint32                     attr_idx;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;

    CTC_SAI_PTR_VALID_CHECK(tunnel_map_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_MAP_ATTR_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel map type on create of tunnel map\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else if (attr_val->s32 > SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI)
    {
        return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_alloc_tunnel_map(&p_tunnel_map));
    p_tunnel_map->tunnel_map_type = attr_val->s32;

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_tunnel_map->tunnel_map_id), status, roll_back_1);
    *tunnel_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *tunnel_map_id, p_tunnel_map), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_map->tunnel_map_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_tunnel_free_tunnel_map(p_tunnel_map);

    return status;
}

static sai_status_t
ctc_sai_tunnel_remove_tunnel_map(
        sai_object_id_t tunnel_map_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, tunnel_map_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    
    p_tunnel_map = ctc_sai_db_get_object_property(lchip, tunnel_map_id);
    if (NULL == p_tunnel_map)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, tunnel_map_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_map->tunnel_map_id);

    _ctc_sai_tunnel_free_tunnel_map(p_tunnel_map);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_tunnel_set_tunnel_map_attribute(sai_object_id_t tunnel_map_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = tunnel_map_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_map_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_map_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_TUNNEL_MAP, tunnel_map_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_map_attribute(sai_object_id_t tunnel_map_id,
                                                uint32_t attr_count,
                                                sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = tunnel_map_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_map_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_map_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_TUNNEL_MAP, loop, tunnel_map_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________TUNNEL________

static sai_status_t
_ctc_sai_tunnel_alloc_tunnel(ctc_sai_tunnel_t** p_tunnel)
{
    ctc_sai_tunnel_t* p_tunnel_tmp = NULL;

    p_tunnel_tmp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_t));
    if (NULL == p_tunnel_tmp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_tunnel_tmp, 0, sizeof(ctc_sai_tunnel_t));

    p_tunnel_tmp->encap_map_list = ctc_slist_new();
    if (NULL == p_tunnel_tmp->encap_map_list)
    {
        mem_free(p_tunnel_tmp);
        return SAI_STATUS_NO_MEMORY;
    }

    p_tunnel_tmp->decap_map_list = ctc_slist_new();
    if (NULL == p_tunnel_tmp->decap_map_list)
    {
        mem_free(p_tunnel_tmp->encap_map_list);
        mem_free(p_tunnel_tmp);
        return SAI_STATUS_NO_MEMORY;
    }

    p_tunnel_tmp->encap_nh_list = ctc_slist_new();
    if (NULL == p_tunnel_tmp->encap_nh_list)
    {
        mem_free(p_tunnel_tmp->decap_map_list);
        mem_free(p_tunnel_tmp->encap_map_list);
        mem_free(p_tunnel_tmp);
        return SAI_STATUS_NO_MEMORY;
    }

    *p_tunnel = p_tunnel_tmp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_free_tunnel(ctc_sai_tunnel_t* p_tunnel)
{
    ctc_sai_tunnel_nh_info_t* p_tunnel_info = NULL;
    ctc_slistnode_t        *node = NULL, *next_node = NULL;

    CTC_SLIST_LOOP_DEL(p_tunnel->encap_nh_list, node, next_node)
    {
        p_tunnel_info = (ctc_sai_tunnel_nh_info_t*)node;
        mem_free(p_tunnel_info);
    }
    ctc_slist_free(p_tunnel->encap_nh_list);
    ctc_slist_free(p_tunnel->encap_map_list);
    ctc_slist_free(p_tunnel->decap_map_list);

    mem_free(p_tunnel);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_get_tunnel_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_slistnode_t* ctc_slistnode = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    sai_object_id_t* p_sai_ob = NULL;
    uint32 index = 0;
    ctc_chip_device_info_t device_info;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    p_tunnel = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_LOG_INFO(SAI_API_TUNNEL, "object id %"PRIx64" get tunnel attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_TUNNEL_ATTR_TYPE:
            attr->value.s32 = p_tunnel->tunnel_type;
            break;
        case SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE:
            if ((SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type))
            {
                attr->value.oid = p_tunnel->underlay_if;
            }
            else
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0+ attr_idx;
            }
            break;
        case SAI_TUNNEL_ATTR_OVERLAY_INTERFACE:
            if ((SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type))
            {
                attr->value.oid = p_tunnel->overlay_if;
            }
            else
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0+ attr_idx;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_SRC_IP:
            sal_memcpy(&attr->value.ipaddr, &p_tunnel->encap_src_ip, sizeof(sai_ip_address_t));
            break;
        case SAI_TUNNEL_ATTR_ENCAP_TTL_MODE:
            attr->value.u8 = p_tunnel->encap_ttl_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_TTL_VAL:
            attr->value.u8 = p_tunnel->encap_ttl_val;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE:
            attr->value.u8 = p_tunnel->encap_dscp_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL:
            attr->value.u8 = p_tunnel->encap_dscp_val;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID:
            attr->value.booldata = p_tunnel->encap_gre_key_en;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_GRE_KEY:
            attr->value.u32 = p_tunnel->encap_gre_key;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_ECN_MODE:
            attr->value.u8 = p_tunnel->encap_ecn_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MAPPERS:
            p_sai_ob = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)* p_tunnel->encap_map_list->count);
            if (NULL == p_sai_ob)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            CTC_SLIST_LOOP(p_tunnel->encap_map_list, ctc_slistnode)
            {
                p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, encap);

                p_sai_ob[index] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
                index++;
            }
            status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), p_sai_ob, index, &attr->value.objlist);
            if(CTC_SAI_ERROR(status))
            {
                status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            mem_free(p_sai_ob);
            break;
        case SAI_TUNNEL_ATTR_DECAP_ECN_MODE:
            attr->value.u8 = p_tunnel->decap_ecn_mode;
            break;
        case SAI_TUNNEL_ATTR_DECAP_MAPPERS:
            p_sai_ob = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)* p_tunnel->decap_map_list->count);
            if (NULL == p_sai_ob)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            CTC_SLIST_LOOP(p_tunnel->decap_map_list, ctc_slistnode)
            {
                p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, decap);

                p_sai_ob[index] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
                index++;
            }
            status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), p_sai_ob, index, &attr->value.objlist);
            if(CTC_SAI_ERROR(status))
            {
                status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            }
            mem_free(p_sai_ob);
            break;
        case SAI_TUNNEL_ATTR_DECAP_TTL_MODE:
            attr->value.u8 = p_tunnel->decap_ttl_mode;
            break;
        case SAI_TUNNEL_ATTR_DECAP_DSCP_MODE:
            attr->value.u8 = p_tunnel->decap_dscp_mode;
            break;
        case SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST:
            break;
        case SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID:
            attr->value.oid = p_tunnel->encap_nexthop_sai;
            break;
        case SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE:
            attr->value.u8 = p_tunnel->decap_pw_mode;
            break;
        case SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
            attr->value.booldata = p_tunnel->decap_cw_en;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE:
            attr->value.u8 = p_tunnel->encap_pw_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
            attr->value.booldata = p_tunnel->encap_cw_en;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
            if(SAI_TUNNEL_MPLS_PW_MODE_TAGGED == p_tunnel->encap_pw_mode)
            {
                attr->value.u16 = p_tunnel->encap_tagged_vlan;
            }
            else
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
            if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip))
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not support\n", attr->id);
                status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            }
            attr->value.booldata = p_tunnel->decap_esi_label_valid;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
            if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip))
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not support\n", attr->id);
                status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            }
            attr->value.booldata = p_tunnel->encap_esi_label_valid;
            break;
        case SAI_TUNNEL_ATTR_DECAP_SPLIT_HORIZON_ENABLE:
            attr->value.booldata = p_tunnel->split_horizon_valid;
            break;
        case SAI_TUNNEL_ATTR_DECAP_EXP_MODE:
            attr->value.u8 = p_tunnel->decap_exp_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_EXP_MODE:
            attr->value.u8 = p_tunnel->encap_exp_mode;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_EXP_VAL:
            attr->value.u8 = p_tunnel->encap_exp_val;
            break;
        case SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO:
            attr->value.booldata = p_tunnel->decap_acl_use_outer;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
_ctc_sai_tunnel_set_tunnel_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_ip_tunnel_nh_param_t nh_param;
    struct ctc_slistnode_s* p_temp_node = NULL;
    ctc_sai_tunnel_nh_info_t* p_tunnel_nh_info = NULL;
    uint8 decap_es_update = 0, encap_es_update = 0, decap_cw_update = 0, encap_cw_update = 0, encap_tagged_vlan_update = 0; 
    uint8 acl_use_outer_update = 0;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    uint32 invalid_nh_id[64] = {0};
    ctc_mpls_nexthop_param_t nh_mpls_param;
    ctc_nh_info_t ctc_nh_info;
    ctc_object_id_t ctc_object_id;
    ctc_chip_device_info_t device_info;
    uint8 split_horizon_update = 0;
    
    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));
    sal_memset(&nh_mpls_param,0,sizeof(ctc_mpls_nexthop_param_t));
    sal_memset(&ctc_nh_info,0,sizeof(ctc_nh_info_t));
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    
    p_tunnel = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_TUNNEL, "object id %"PRIx64" set tunnel attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_TUNNEL_ATTR_ENCAP_GRE_KEY:
            p_tunnel->encap_gre_key = attr->value.u32;
            break;
        case SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
            if(SAI_TUNNEL_TYPE_MPLS_L2 != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                break;
            }
            else
            {
                decap_cw_update = 1;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
            if(SAI_TUNNEL_TYPE_MPLS_L2 != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                break;
            }
            else
            {
                encap_cw_update = 1;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
            if(SAI_TUNNEL_MPLS_PW_MODE_TAGGED == p_tunnel->encap_pw_mode && SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
            {
                encap_tagged_vlan_update = 1;
                p_tunnel->encap_tagged_vlan = attr->value.u16;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
            if(SAI_TUNNEL_TYPE_MPLS_L2 != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                break;
            }
            else if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip))
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not support\n", attr->id);
                status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            }
            decap_es_update =1;
            break;
        case SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
            if(SAI_TUNNEL_TYPE_MPLS_L2 != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                break;
            }
            else if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip))
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not support\n", attr->id);
                status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            }
            encap_es_update = 1;
            break;
        case SAI_TUNNEL_ATTR_DECAP_SPLIT_HORIZON_ENABLE:
            if(SAI_TUNNEL_TYPE_MPLS_L2 != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel cfg %d not valid\n", attr->id);
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                break;
            }
            else
            {
                split_horizon_update = 1;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO:
            if(p_tunnel->decap_acl_use_outer == attr->value.booldata)
            {
                break;
            }
            acl_use_outer_update = 1;
            break;
        //encap attr updating allowed when tunnel not bind to nhp
        case SAI_TUNNEL_ATTR_ENCAP_TTL_MODE:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_ttl_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_TTL_VAL:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_ttl_val = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_dscp_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_dscp_val = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_ECN_MODE:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_ecn_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_pw_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_EXP_MODE:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_exp_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_ENCAP_EXP_VAL:
            if( 0 == p_tunnel->egress_ref_cnt )
            {
                p_tunnel->encap_exp_val = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        //decap attr updating allowed when tunnel not bind to mpls insegment
        case SAI_TUNNEL_ATTR_DECAP_ECN_MODE:
            if( 0 == p_tunnel->ingress_ref_cnt )
            {
                p_tunnel->decap_ecn_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_TTL_MODE:
            if( 0 == p_tunnel->ingress_ref_cnt )
            {
                p_tunnel->decap_ttl_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_DSCP_MODE:
            if( 0 == p_tunnel->ingress_ref_cnt )
            {
                p_tunnel->decap_dscp_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE:
            if( 0 == p_tunnel->ingress_ref_cnt )
            {
                p_tunnel->decap_pw_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        case SAI_TUNNEL_ATTR_DECAP_EXP_MODE:
            if( 0 == p_tunnel->ingress_ref_cnt )
            {
                p_tunnel->decap_exp_mode = attr->value.u8;
            }
            else
            {
                status = SAI_STATUS_OBJECT_IN_USE;
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }
    if(decap_cw_update && (0 != p_tunnel->inseg_label))
    {
        ctc_mpls_ilm.label = p_tunnel->inseg_label;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
        if(attr->value.booldata)
        {
            ctc_mpls_ilm.cwen = 1;
        }
        else
        {
            ctc_mpls_ilm.cwen = 0;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        p_tunnel->decap_cw_en = attr->value.booldata;
    }
    else if(decap_cw_update)
    {
        p_tunnel->decap_cw_en = attr->value.booldata;
    }
    if(decap_es_update && (0 != p_tunnel->inseg_label))
    {
        ctc_mpls_ilm.label = p_tunnel->inseg_label;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
        if(attr->value.booldata)
        {
            CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ESLB_EXIST);
        }
        else
        {
            CTC_UNSET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ESLB_EXIST);
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        p_tunnel->decap_esi_label_valid = attr->value.booldata;
    }
    else if(decap_es_update)
    {
        p_tunnel->decap_esi_label_valid = attr->value.booldata;
    }

    if(split_horizon_update && (0 != p_tunnel->inseg_label))
    {
        ctc_mpls_ilm.label = p_tunnel->inseg_label;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
        if(attr->value.booldata)
        {
            ctc_mpls_ilm.logic_port_type = 1;
        }
        else
        {
            ctc_mpls_ilm.logic_port_type = 0;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        p_tunnel->split_horizon_valid = attr->value.booldata;
    }
    else if(split_horizon_update)
    {
        p_tunnel->split_horizon_valid = attr->value.booldata;
    }
    
    if(acl_use_outer_update)
    {
        if((SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type) && (0 != p_tunnel->inseg_label))
        {
            ctc_mpls_ilm.label = p_tunnel->inseg_label;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
            if(attr->value.booldata)
            {
                CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ACL_USE_OUTER_INFO);
            }
            else
            {
                CTC_UNSET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ACL_USE_OUTER_INFO);
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        }
        else if(SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type)
        {
            if(p_tunnel->decap_map_list)
            {
                //need update terminate entry
            }
        }
        p_tunnel->decap_acl_use_outer = attr->value.booldata;
    }
    
    if(encap_cw_update && (0 != p_tunnel->encap_nexthop_sai))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_tunnel->encap_nexthop_sai, &ctc_object_id);
        ctc_nh_info.p_nh_param = &nh_mpls_param;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, ctc_object_id.value, &ctc_nh_info));
        if(attr->value.booldata)
        {
            nh_mpls_param.nh_para.nh_param_push.martini_encap_valid = TRUE;
            nh_mpls_param.nh_para.nh_param_push.martini_encap_type = 0;
        }
        else
        {
            nh_mpls_param.nh_para.nh_param_push.martini_encap_valid = FALSE;
            nh_mpls_param.nh_para.nh_param_push.martini_encap_type = 0;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls(lchip, ctc_object_id.value, &nh_mpls_param));
        p_tunnel->encap_cw_en = attr->value.booldata;
    }
    else if(encap_cw_update)
    {
        p_tunnel->encap_cw_en = attr->value.booldata;
    }
    
    if(encap_tagged_vlan_update && (0 != p_tunnel->encap_nexthop_sai))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_tunnel->encap_nexthop_sai, &ctc_object_id);
        ctc_nh_info.p_nh_param = &nh_mpls_param;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, ctc_object_id.value, &ctc_nh_info));
        nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.output_svid = attr->value.u16;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls(lchip, ctc_object_id.value, &nh_mpls_param));
        p_tunnel->encap_tagged_vlan = attr->value.u16;
    }
    else if(encap_tagged_vlan_update)
    {
        p_tunnel->encap_tagged_vlan = attr->value.u16;
    }
    
    if(encap_es_update && (0 != p_tunnel->encap_nexthop_sai))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_tunnel->encap_nexthop_sai, &ctc_object_id);
        ctc_nh_info.p_nh_param = &nh_mpls_param;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, ctc_object_id.value, &ctc_nh_info));
        nh_mpls_param.nh_para.nh_param_push.eslb_en = attr->value.booldata;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls(lchip, ctc_object_id.value, &nh_mpls_param));
        p_tunnel->encap_esi_label_valid = attr->value.booldata;
    }
    else if(encap_es_update)
    {
        p_tunnel->encap_esi_label_valid = attr->value.booldata;
    }
    
    if (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type)
    {
        CTC_SLIST_LOOP(p_tunnel->encap_nh_list, p_temp_node)
        {
            p_tunnel_nh_info = (ctc_sai_tunnel_nh_info_t*)p_temp_node;
            sal_memset(&nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));
            CTC_SAI_ERROR_RETURN(ctc_sai_tunnel_map_to_nh_ip_tunnel(lchip, key->key.object_id, p_tunnel_nh_info->nh_id, &p_tunnel_nh_info->ip_addr, &nh_param));
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_ip_tunnel(lchip, p_tunnel_nh_info->nh_id, &nh_param));
        }
    }

    return status;
}

static ctc_sai_attr_fn_entry_t tunnel_attr_fn_entries[] = {
    {SAI_TUNNEL_ATTR_TYPE, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_OVERLAY_INTERFACE, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_ENCAP_SRC_IP, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_ENCAP_TTL_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_TTL_VAL, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_GRE_KEY, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_ECN_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_MAPPERS, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_DECAP_ECN_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_MAPPERS, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_DECAP_TTL_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_DSCP_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_TERM_TABLE_ENTRY_LIST, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID, _ctc_sai_tunnel_get_tunnel_property, NULL},
    {SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_SPLIT_HORIZON_ENABLE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_EXP_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_EXP_MODE, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_ENCAP_EXP_VAL, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO, _ctc_sai_tunnel_get_tunnel_property, _ctc_sai_tunnel_set_tunnel_property},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
ctc_sai_tunnel_get_map_mappers_val(uint8 lchip, sai_object_id_t tunnel_id, bool is_encap, ctc_sai_tunnel_map_val_t type, uint32* p_value)
{
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_slistnode_t* ctc_slistnode = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    ctc_slistnode_t* p_temp_node      = NULL;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = NULL;
    ctc_slist_t* map_list = NULL;
    bool is_find = FALSE;
    uint16 vlan_ptr = 0;
    ctc_object_id_t ctc_oid;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    map_list = is_encap?p_tunnel->encap_map_list:p_tunnel->decap_map_list;
    CTC_SLIST_LOOP(map_list, ctc_slistnode)
    {
        if (is_encap)
        {
            p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, encap);
        }
        else
        {
            p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, decap);
        }
        CTC_SLIST_LOOP(p_tunnel_map->map_entry_list, p_temp_node)
        {
            p_tunnel_map_entry = (ctc_sai_tunnel_map_entry_t*)p_temp_node;

            if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_OECN_ID == type) && (SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN == p_tunnel_map_entry->tunnel_map_type))
            {
                *p_value = p_tunnel_map_entry->oecn_key;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_OECN_ID == type) && (SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN == p_tunnel_map_entry->tunnel_map_type))
            {
                *p_value = p_tunnel_map_entry->oecn_val;
                is_find = TRUE;
            }
            if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_UECN_ID == type) && (SAI_TUNNEL_MAP_TYPE_UECN_OECN_TO_OECN == p_tunnel_map_entry->tunnel_map_type))
            {
                *p_value = p_tunnel_map_entry->uecn_key;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_UECN_ID == type) && (SAI_TUNNEL_MAP_TYPE_OECN_TO_UECN == p_tunnel_map_entry->tunnel_map_type))
            {
                *p_value = p_tunnel_map_entry->uecn_val;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VLAN_ID == type) && (SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_ptr_from_vlan_id(lchip, p_tunnel_map_entry->vlan_key, &vlan_ptr));
                *p_value = vlan_ptr;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VLAN_ID == type) && (SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_ptr_from_vlan_id(lchip, p_tunnel_map_entry->vlan_val, &vlan_ptr));
                *p_value = vlan_ptr;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VNI_ID == type) && ((SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID == p_tunnel_map_entry->tunnel_map_type)
                || (SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == p_tunnel_map_entry->tunnel_map_type) || (SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID == p_tunnel_map_entry->tunnel_map_type)))
            {
                *p_value = p_tunnel_map_entry->vni_key;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VNI_ID == type) && ((SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type)
                || (SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == p_tunnel_map_entry->tunnel_map_type) || (SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type)))
            {
                *p_value = p_tunnel_map_entry->vni_val;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_BRG_ID == type) && (SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, p_tunnel_map_entry->brg_id_key, &ctc_oid));
                *p_value = ctc_oid.value;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_BRG_ID == type) && (SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, p_tunnel_map_entry->brg_id_val, &ctc_oid));
                *p_value = ctc_oid.value;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VRF_ID == type) && (SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, p_tunnel_map_entry->vrf_key, &ctc_oid));
                *p_value = ctc_oid.value;
                is_find = TRUE;
            }
            else if ((CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VRF_ID == type) && (SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID == p_tunnel_map_entry->tunnel_map_type))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, p_tunnel_map_entry->vrf_val, &ctc_oid));
                *p_value = ctc_oid.value;
                is_find = TRUE;
            }
            if (is_find)
            {
                break;
            }
        }
        if (is_find)
        {
            break;
        }
    }

    if (!is_find)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_tunnel_map_to_nh_ip_tunnel(uint8 lchip, sai_object_id_t tunnel_id, uint32 ctc_nh_id, sai_ip_address_t* ip_da, ctc_ip_tunnel_nh_param_t* p_nh_param)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint32 value = 0;
    int32 ret = CTC_E_NONE;
    ctc_stats_statsid_t stats_statsid;
    ctc_sai_tunnel_nh_info_t* p_tunnel_nh_info = NULL;
    bool have_exist = FALSE;
    struct ctc_slistnode_s* p_temp_node = NULL;
    uint8 if_type = 0;
    uint16 if_vrf_id = 0;
    uint32 if_gport = 0;
    uint16 if_vlan = 0;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    /*ip address*/
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_tunnel->encap_src_ip.addr_family)
    {
        p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_IPV4_IN4;
        if (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type)
        {
            p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_GRE_IN4;
            p_nh_param->tunnel_info.gre_info.protocol_type = 0x0800;
        }
        else if (SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type)
        {
            p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_VXLAN_IN4;
        }
        sal_memcpy(&p_nh_param->tunnel_info.ip_sa.ipv4, &p_tunnel->encap_src_ip.addr.ip4, sizeof(sai_ip4_t));
		CTC_SAI_NTOH_V4(p_nh_param->tunnel_info.ip_sa.ipv4);
        sal_memcpy(&p_nh_param->tunnel_info.ip_da.ipv4, &ip_da->addr.ip4, sizeof(sai_ip4_t));
		CTC_SAI_NTOH_V4(p_nh_param->tunnel_info.ip_da.ipv4);
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_tunnel->encap_src_ip.addr_family)
    {
        p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_IPV6_IN6;
        if (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type)
        {
            p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_GRE_IN6;
            p_nh_param->tunnel_info.gre_info.protocol_type = 0x0800;
        }
        else if (SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type)
        {
            p_nh_param->tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_VXLAN_IN6;
        }
        sal_memcpy(&p_nh_param->tunnel_info.ip_sa.ipv6, &p_tunnel->encap_src_ip.addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_nh_param->tunnel_info.ip_sa.ipv6);
        sal_memcpy(&p_nh_param->tunnel_info.ip_da.ipv6, &ip_da->addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_nh_param->tunnel_info.ip_da.ipv6);
    }

    if ((SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type) && (true == p_tunnel->encap_gre_key_en))
    {
        p_nh_param->tunnel_info.gre_info.gre_key = p_tunnel->encap_gre_key;
        CTC_SET_FLAG(p_nh_param->tunnel_info.flag, CTC_IP_NH_TUNNEL_FLAG_GRE_WITH_KEY);
    }

    /*ttl*/
    if (SAI_TUNNEL_TTL_MODE_PIPE_MODEL == p_tunnel->encap_ttl_mode)
    {
        p_nh_param->tunnel_info.ttl = p_tunnel->encap_ttl_val;
    }
    else
    {
        CTC_SET_FLAG(p_nh_param->tunnel_info.flag, CTC_IP_NH_TUNNEL_FLAG_MAP_TTL);
        p_nh_param->tunnel_info.ttl = 0;
    }

    /*dscp*/
    if (SAI_TUNNEL_DSCP_MODE_PIPE_MODEL == p_tunnel->encap_dscp_mode)
    {
        p_nh_param->tunnel_info.dscp_select = CTC_NH_DSCP_SELECT_ASSIGN;
        p_nh_param->tunnel_info.dscp_or_tos = p_tunnel->encap_dscp_val;
    }
    else
    {
        p_nh_param->tunnel_info.dscp_select = CTC_NH_DSCP_SELECT_PACKET;
    }

    /*ecn*/
    if (SAI_TUNNEL_ENCAP_ECN_MODE_USER_DEFINED == p_tunnel->encap_ecn_mode)
    {
        p_nh_param->tunnel_info.ecn_select = CTC_NH_ECN_SELECT_ASSIGN;

    }
    else
    {
        p_nh_param->tunnel_info.ecn_select = CTC_NH_ECN_SELECT_PACKET;
    }

    /* modify tunnel reroute */
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(p_tunnel->underlay_if, &if_type, &if_vrf_id, &if_gport, &if_vlan));
    if (SAI_ROUTER_INTERFACE_TYPE_PORT == if_type)
    {
        p_nh_param->oif.gport = if_gport;
    }
    else if ((SAI_ROUTER_INTERFACE_TYPE_VLAN == if_type) || (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == if_type))
    {
        p_nh_param->oif.gport = if_gport;
        p_nh_param->oif.vid = if_vlan;
    }
    else if (SAI_ROUTER_INTERFACE_TYPE_LOOPBACK == if_type)
    {
        CTC_SET_FLAG(p_nh_param->tunnel_info.flag, CTC_IP_NH_TUNNEL_FLAG_REROUTE_WITH_TUNNEL_HDR);
    }
    else
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    if (SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type)
    {
        status = ctc_sai_tunnel_get_map_mappers_val(lchip, tunnel_id, TRUE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VNI_ID, &value);
        if (!CTC_SAI_ERROR(status))
        {
            p_nh_param->tunnel_info.vn_id = value;
        }
    }

    sal_memset(&stats_statsid, 0, sizeof(ctc_stats_statsid_t));
    stats_statsid.dir = CTC_EGRESS;
    stats_statsid.type = CTC_STATS_STATSID_TYPE_TUNNEL;

    ret = ctcs_stats_create_statsid(lchip, &stats_statsid);
    status = ctc_sai_mapping_error_ctc(ret);
    if (!CTC_SAI_ERROR(status))
    {
        p_tunnel->encap_stats_id = stats_statsid.stats_id;
        p_nh_param->tunnel_info.stats_id = stats_statsid.stats_id;
    }

    CTC_SLIST_LOOP(p_tunnel->encap_nh_list, p_temp_node)
    {
        p_tunnel_nh_info = (ctc_sai_tunnel_nh_info_t*)p_temp_node;
        if (ctc_nh_id == p_tunnel_nh_info->nh_id)
        {
            have_exist = TRUE;
            break;
        }
    }

    if (!have_exist)
    {
        p_tunnel_nh_info = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_nh_info_t));
        sal_memset(p_tunnel_nh_info, 0, sizeof(ctc_sai_tunnel_nh_info_t));

        p_tunnel_nh_info->nh_id = ctc_nh_id;
        sal_memcpy(&p_tunnel_nh_info->ip_addr, ip_da, sizeof(sai_ip_address_t));

        ctc_slist_add_tail(p_tunnel->encap_nh_list, (void*)p_tunnel_nh_info);
    }


    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_tunnel_unmap_to_nh_ip_tunnel(uint8 lchip, sai_object_id_t tunnel_id, uint32 ctc_nh_id)
{
    ctc_sai_tunnel_t* p_tunnel = NULL;
    struct ctc_slistnode_s* p_temp_node      = NULL;
    ctc_sai_tunnel_nh_info_t* p_tunnel_nh_info = NULL;

    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (0 != p_tunnel->encap_stats_id)
    {
        ctcs_stats_destroy_statsid(lchip, p_tunnel->encap_stats_id);
    }

    CTC_SLIST_LOOP(p_tunnel->encap_nh_list, p_temp_node)
    {
        p_tunnel_nh_info = (ctc_sai_tunnel_nh_info_t*)p_temp_node;
        if (ctc_nh_id == p_tunnel_nh_info->nh_id)
        {
            ctc_slist_delete_node(p_tunnel->encap_nh_list, p_temp_node);
            mem_free(p_temp_node);
            break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_tunnel_create_tunnel(
        sai_object_id_t *tunnel_id,
        sai_object_id_t switch_id,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val = NULL;
    uint32                     attr_idx = 0;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    sai_object_id_t map_obj_id = 0;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    uint32 index = 0;
    uint32 logic_port = 0;

    CTC_SAI_PTR_VALID_CHECK(tunnel_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel type on create of tunnel\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else if (attr_val->s32 > SAI_TUNNEL_TYPE_MPLS_L2)
    {
        return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
    }
    /*
    else if (attr_val->s32 == SAI_TUNNEL_TYPE_MPLS)
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0+attr_idx;
    }
    */
    
    CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_alloc_tunnel(&p_tunnel));
    p_tunnel->tunnel_type = attr_val->s32;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_ACL_USE_OUTER_HDR_INFO, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        p_tunnel->decap_acl_use_outer = attr_val->booldata;
    }
    
    if((SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, &logic_port));
        p_tunnel->logic_port = logic_port;
    }

    if ((SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type))
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_UNDERLAY_INTERFACE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel underlay if on create of tunnel\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
        else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
        {
            status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            goto roll_back_0;
        }
        p_tunnel->underlay_if = attr_val->oid;

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_OVERLAY_INTERFACE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            if (SAI_TUNNEL_TYPE_VXLAN != p_tunnel->tunnel_type)
            {
                CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel overlay if on create of tunnel\n");
                status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
                goto roll_back_0;
            }
        }
        else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
        {
            status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            goto roll_back_0;
        }
        p_tunnel->overlay_if = attr_val->oid;
    }
    else if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_pw_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_cw_en = attr_val->booldata;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_pw_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_cw_en = attr_val->booldata;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_tagged_vlan = attr_val->u16;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_esi_label_valid = attr_val->booldata;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_esi_label_valid = attr_val->booldata;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_SPLIT_HORIZON_ENABLE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->split_horizon_valid = attr_val->booldata;
        }
        else
        {
            p_tunnel->split_horizon_valid = true;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_EXP_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_exp_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_EXP_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_exp_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_EXP_VAL, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_exp_val = attr_val->u8;
        }
    }
    else if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_TTL_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_ttl_mode = attr_val->u8;
        }        
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_EXP_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->decap_exp_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_EXP_MODE, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_exp_mode = attr_val->u8;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_EXP_VAL, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_exp_val = attr_val->u8;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_SRC_IP, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&p_tunnel->encap_src_ip, &attr_val->ipaddr, sizeof(sai_ip_address_t));
    }

    p_tunnel->encap_ttl_mode = SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_TTL_MODE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_val->u8 > SAI_TUNNEL_TTL_MODE_PIPE_MODEL)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->encap_ttl_mode = attr_val->u8;
    }

    if (SAI_TUNNEL_TTL_MODE_PIPE_MODEL == p_tunnel->encap_ttl_mode)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_TTL_VAL, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
             CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel encap tll value on create of tunnel\n");
             status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
             goto roll_back_0;
        }
        p_tunnel->encap_ttl_val = attr_val->u8;
    }

    p_tunnel->encap_dscp_mode = SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_DSCP_MODE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_val->u8 > SAI_TUNNEL_DSCP_MODE_PIPE_MODEL)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->encap_dscp_mode = attr_val->u8;
    }

    if (SAI_TUNNEL_DSCP_MODE_PIPE_MODEL == p_tunnel->encap_dscp_mode)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_DSCP_VAL, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
             CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel encap dscp value on create of tunnel\n");
             status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
             goto roll_back_0;
        }
        p_tunnel->encap_dscp_val = attr_val->u8;
    }

    p_tunnel->encap_gre_key_en = false;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_GRE_KEY_VALID, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
         p_tunnel->encap_gre_key_en = attr_val->booldata;
    }

    if (true == p_tunnel->encap_gre_key_en)
    {
        p_tunnel->encap_gre_key = 0;
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_GRE_KEY, &attr_val, &attr_idx);
        if (!CTC_SAI_ERROR(status))
        {
            p_tunnel->encap_gre_key = attr_val->u32;
        }
    }

    p_tunnel->encap_ecn_mode = SAI_TUNNEL_ENCAP_ECN_MODE_STANDARD;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_ECN_MODE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_val->u8 > SAI_TUNNEL_ENCAP_ECN_MODE_USER_DEFINED)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->encap_ecn_mode = attr_val->u8;
    }

    /* encap tunnel map list*/
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_ENCAP_MAPPERS, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        for (index=0; index<attr_val->objlist.count; index++)
        {
            map_obj_id = attr_val->objlist.list[index];
            p_tunnel_map = ctc_sai_db_get_object_property(lchip, map_obj_id);
            if (NULL == p_tunnel_map)
            {
                status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
                goto roll_back_0;
            }
            ctc_slist_add_tail(p_tunnel->encap_map_list, (void*)&p_tunnel_map->encap);
        }
    }

    p_tunnel->decap_ecn_mode = SAI_TUNNEL_DECAP_ECN_MODE_STANDARD;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_ECN_MODE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_val->u8 > SAI_TUNNEL_DECAP_ECN_MODE_USER_DEFINED)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->decap_ecn_mode = attr_val->u8;
    }

    /* decap tunnel map list*/
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_MAPPERS, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        for (index=0; index<attr_val->objlist.count; index++)
        {
            map_obj_id = attr_val->objlist.list[index];
            p_tunnel_map = ctc_sai_db_get_object_property(lchip, map_obj_id);
            if (NULL == p_tunnel_map)
            {
                status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
                goto roll_back_0;
            }
            ctc_slist_add_tail(p_tunnel->decap_map_list, (void*)&p_tunnel_map->decap);
        }
    }

    if ((SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type))
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_TTL_MODE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel decap tll mode on create of tunnel\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
        else if (attr_val->u8 > SAI_TUNNEL_TTL_MODE_PIPE_MODEL)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->decap_ttl_mode = attr_val->u8;

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_ATTR_DECAP_DSCP_MODE, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel decap dscp mode on create of tunnel\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
        else if (attr_val->u8 > SAI_TUNNEL_DSCP_MODE_PIPE_MODEL)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        }
        p_tunnel->decap_dscp_mode = attr_val->u8;
    }

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_tunnel->tunnel_id), status, roll_back_1);
    *tunnel_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL, lchip, 0, 0, p_tunnel->tunnel_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *tunnel_id, p_tunnel), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel->tunnel_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);

roll_back_0:
    if((SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type))
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, logic_port);
    }
    _ctc_sai_tunnel_free_tunnel(p_tunnel);

    return status;
}

static sai_status_t
ctc_sai_tunnel_remove_tunnel(
        sai_object_id_t tunnel_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL, tunnel_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }
    if( (0 != p_tunnel->egress_ref_cnt) || (0 != p_tunnel->ingress_ref_cnt) )
    {
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }
    

    ctc_sai_db_remove_object_property(lchip, tunnel_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel->tunnel_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, p_tunnel->logic_port);
    
    _ctc_sai_tunnel_free_tunnel(p_tunnel);
    

    return SAI_STATUS_SUCCESS;
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_stats(
        sai_object_id_t tunnel_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        uint64_t *counters)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    ctc_stats_basic_t stats_encap;
    ctc_stats_basic_t stats_decap;
    uint32 index = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&stats_encap, 0, sizeof(ctc_stats_basic_t));
    sal_memset(&stats_decap, 0, sizeof(ctc_stats_basic_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL, tunnel_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_tunnel->encap_stats_id, &stats_encap), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_tunnel->decap_stats_id, &stats_decap), status, out);
    for (index = 0; index < number_of_counters; index ++ )
    {
        switch(counter_ids[index])
        {
            case SAI_TUNNEL_STAT_IN_OCTETS:
                counters[index] = stats_encap.byte_count;
                break;
            case SAI_TUNNEL_STAT_IN_PACKETS:
                counters[index] = stats_encap.packet_count;
                break;
            case SAI_TUNNEL_STAT_OUT_OCTETS:
                counters[index] = stats_decap.byte_count;
                break;
            case SAI_TUNNEL_STAT_OUT_PACKETS:
                counters[index] = stats_decap.packet_count;
                break;
            default:
                CTC_SAI_DB_UNLOCK(lchip);
                return SAI_STATUS_INVALID_PARAMETER;
                break;
        }

    }
out:    
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_stats_ext(
        sai_object_id_t tunnel_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        sai_stats_mode_t mode,
        uint64_t *counters)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    ctc_stats_basic_t stats_encap;
    ctc_stats_basic_t stats_decap;
    uint32 index = 0;
    bool encap_en = FALSE;
    bool decap_en = FALSE;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&stats_encap, 0, sizeof(ctc_stats_basic_t));
    sal_memset(&stats_decap, 0, sizeof(ctc_stats_basic_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL, tunnel_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_tunnel->encap_stats_id, &stats_encap), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_tunnel->decap_stats_id, &stats_decap), status, out);
    for (index = 0; index < number_of_counters; index ++ )
    {
        switch(counter_ids[index])
        {
            case SAI_TUNNEL_STAT_IN_OCTETS:
                encap_en = TRUE;
                counters[index] = stats_encap.byte_count;
                break;
            case SAI_TUNNEL_STAT_IN_PACKETS:
                encap_en = TRUE;
                counters[index] = stats_encap.packet_count;
                break;
            case SAI_TUNNEL_STAT_OUT_OCTETS:
                decap_en = TRUE;
                counters[index] = stats_decap.byte_count;
                break;
            case SAI_TUNNEL_STAT_OUT_PACKETS:
                decap_en = TRUE;
                counters[index] = stats_decap.packet_count;
                break;
            default:
                CTC_SAI_DB_UNLOCK(lchip);
                return SAI_STATUS_INVALID_PARAMETER;
                break;
        }

    }
    

    if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
    {
        if (encap_en)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_stats(lchip, p_tunnel->encap_stats_id), status, out);
        }
        if (decap_en)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_stats(lchip, p_tunnel->decap_stats_id), status, out);
        }
    }
out:    
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_clear_tunnel_stats(
        sai_object_id_t tunnel_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    uint32 index = 0;
    uint32 flag = 0;
    uint32 tmp_flag = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));


    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL, tunnel_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);
    if (NULL == p_tunnel)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    for (index = 0; index < number_of_counters; index ++ )
    {
        switch(counter_ids[index])
        {
            case SAI_TUNNEL_STAT_IN_OCTETS:
            case SAI_TUNNEL_STAT_IN_PACKETS:
            case SAI_TUNNEL_STAT_OUT_OCTETS:
            case SAI_TUNNEL_STAT_OUT_PACKETS:
                CTC_BIT_SET(flag, counter_ids[index]);
                break;
            default:
                CTC_SAI_DB_UNLOCK(lchip);
                return SAI_STATUS_INVALID_PARAMETER;
                break;
        }

        /* must both in octes and in packets */
        tmp_flag = flag&0x3;
        if ((tmp_flag !=0) && (tmp_flag != 3))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_NOT_SUPPORTED;
        }

        /* must both out octes and out packets */
        tmp_flag = (flag>>2)&0x3;
        if ((tmp_flag !=0) && (tmp_flag != 3))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_NOT_SUPPORTED;
        }

        if (CTC_IS_BIT_SET(flag, SAI_TUNNEL_STAT_IN_OCTETS) && CTC_IS_BIT_SET(flag, SAI_TUNNEL_STAT_IN_PACKETS))
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_stats(lchip, p_tunnel->encap_stats_id), status, out);
        }

        if (CTC_IS_BIT_SET(flag, SAI_TUNNEL_STAT_OUT_OCTETS) && CTC_IS_BIT_SET(flag, SAI_TUNNEL_STAT_OUT_PACKETS))
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_clear_stats(lchip, p_tunnel->decap_stats_id), status, out);
        }
    }
out:    
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_set_tunnel_attribute(sai_object_id_t tunnel_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = tunnel_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_TUNNEL, tunnel_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_attribute(sai_object_id_t tunnel_id,
                                                uint32_t attr_count,
                                                sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = tunnel_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_TUNNEL, loop, tunnel_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________TUNNEL_TERM________
static sai_status_t
_ctc_sai_tunnel_alloc_tunnel_term_table_entry(ctc_sai_tunnel_term_table_entry_t** p_tunnel_term)
{
    ctc_sai_tunnel_term_table_entry_t* p_tunnel_term_tmp = NULL;

    p_tunnel_term_tmp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_term_table_entry_t));
    if (NULL == p_tunnel_term_tmp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_tunnel_term_tmp, 0, sizeof(ctc_sai_tunnel_term_table_entry_t));

    *p_tunnel_term = p_tunnel_term_tmp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_free_tunnel_term_table_entry(ctc_sai_tunnel_term_table_entry_t* p_tunnel_term)
{
    mem_free(p_tunnel_term);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_get_tunnel_term_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_term_table_entry_t* p_tunnel_term = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_tunnel_term = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_tunnel_term)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_TUNNEL, "object id %"PRIx64" get tunnel term attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID:
            attr->value.oid = p_tunnel_term->vrf_id;
            break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE:
            attr->value.s32 = p_tunnel_term->tunnel_term_table_type;
            break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP:
            sal_memcpy(&attr->value.ipaddr, &p_tunnel_term->dst_ip, sizeof(sai_ip_address_t));
            break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP:
            sal_memcpy(&attr->value.ipaddr, &p_tunnel_term->src_ip, sizeof(sai_ip_address_t));
            break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE:
            attr->value.s32 = p_tunnel_term->tunnel_type;
            break;
        case SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID:
            attr->value.oid = p_tunnel_term->tunnel_id;
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Tunnel term attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t tunnel_term_attr_fn_entries[] = {
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID, _ctc_sai_tunnel_get_tunnel_term_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
_ctc_sai_tunnel_term_map_ip_tunnel_key(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term, ctc_ipuc_tunnel_param_t* p_ipuc_tunnel_param)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    /*vrf id*/
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, p_tunnel_term->vrf_id, &ctc_oid));
	
    p_ipuc_tunnel_param->vrf_id = ctc_oid.value;

    /*ip version*/
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_tunnel_term->dst_ip.addr_family)
    {
        p_ipuc_tunnel_param->ip_ver = CTC_IP_VER_4;
        sal_memcpy(&p_ipuc_tunnel_param->ip_da.ipv4, &p_tunnel_term->dst_ip.addr.ip4, sizeof(sai_ip4_t));
		CTC_SAI_NTOH_V4(p_ipuc_tunnel_param->ip_da.ipv4);
        p_ipuc_tunnel_param->payload_type = CTC_IPUC_TUNNEL_PAYLOAD_TYPE_V4;
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_tunnel_term->dst_ip.addr_family)
    {
        p_ipuc_tunnel_param->ip_ver = CTC_IP_VER_6;
        sal_memcpy(&p_ipuc_tunnel_param->ip_da.ipv6, &p_tunnel_term->dst_ip.addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_ipuc_tunnel_param->ip_da.ipv6);
        p_ipuc_tunnel_param->payload_type = CTC_IPUC_TUNNEL_PAYLOAD_TYPE_V6;
    }
    else
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    /*ip sa*/
    if (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P == p_tunnel_term->tunnel_term_table_type)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_tunnel_term->src_ip.addr_family)
        {
            sal_memcpy(&p_ipuc_tunnel_param->ip_sa.ipv4, &p_tunnel_term->src_ip.addr.ip4, sizeof(sai_ip4_t));
			CTC_SAI_NTOH_V4(p_ipuc_tunnel_param->ip_sa.ipv4);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_tunnel_term->src_ip.addr_family)
        {
            sal_memcpy(&p_ipuc_tunnel_param->ip_sa.ipv6, &p_tunnel_term->src_ip.addr.ip6, sizeof(sai_ip6_t));
            CTC_SAI_NTOH_V6(p_ipuc_tunnel_param->ip_sa.ipv6);
        }
        CTC_SET_FLAG(p_ipuc_tunnel_param->flag, CTC_IPUC_TUNNEL_FLAG_LKUP_WITH_IPSA);
    }

    if (SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel_term->tunnel_type)
    {
        p_ipuc_tunnel_param->payload_type = CTC_IPUC_TUNNEL_PAYLOAD_TYPE_GRE;
        if (p_tunnel->encap_gre_key_en)
        {
            p_ipuc_tunnel_param->gre_key = p_tunnel->encap_gre_key;
            CTC_SET_FLAG(p_ipuc_tunnel_param->flag, CTC_IPUC_TUNNEL_FLAG_GRE_WITH_KEY);
        }
    }

    if (p_tunnel->use_flex)
    {
        CTC_SET_FLAG(p_ipuc_tunnel_param->flag, CTC_IPUC_TUNNEL_FLAG_USE_FLEX);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_term_map_ip_tunnel_action(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term, ctc_ipuc_tunnel_param_t* p_ipuc_tunnel_param)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_stats_statsid_t stats_statsid;
    int32 ret = CTC_E_NONE;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&stats_statsid, 0, sizeof(ctc_stats_statsid_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    sal_memset(&stats_statsid, 0, sizeof(ctc_stats_statsid_t));
    stats_statsid.dir = CTC_INGRESS;
    stats_statsid.type = CTC_STATS_STATSID_TYPE_TUNNEL;

    ret = ctcs_stats_create_statsid(lchip, &stats_statsid);
    status = ctc_sai_mapping_error_ctc(ret);
    if (!CTC_SAI_ERROR(status))
    {
        p_tunnel->decap_stats_id = stats_statsid.stats_id;
        p_ipuc_tunnel_param->stats_id = stats_statsid.stats_id;
        CTC_SET_FLAG(p_ipuc_tunnel_param->flag, CTC_IPUC_TUNNEL_FLAG_STATS_EN);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_term_unmap_ip_tunnel_action(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term)
{
    ctc_sai_tunnel_t* p_tunnel = NULL;

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (0 != p_tunnel->decap_stats_id)
    {
        ctcs_stats_destroy_statsid(lchip, p_tunnel->decap_stats_id);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_term_map_vxlan_tunnel_key(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term, ctc_overlay_tunnel_param_t* p_vxlan_param)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint32 value = 0;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_vxlan_param->type = CTC_OVERLAY_TUNNEL_TYPE_VXLAN;
    /*vrf id*/
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, p_tunnel_term->vrf_id, &ctc_oid));
    p_vxlan_param->vrf_id = ctc_oid.value;

    /*ip version*/
    if (SAI_IP_ADDR_FAMILY_IPV4 == p_tunnel_term->dst_ip.addr_family)
    {
        sal_memcpy(&p_vxlan_param->ipda.ipv4, &p_tunnel_term->dst_ip.addr.ip4, sizeof(sai_ip4_t));
		CTC_SAI_NTOH_V4(p_vxlan_param->ipda.ipv4);
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == p_tunnel_term->dst_ip.addr_family)
    {
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_IP_VER_6);
        sal_memcpy(&p_vxlan_param->ipda.ipv6, &p_tunnel_term->dst_ip.addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_vxlan_param->ipda.ipv6);
    }
    else
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    /*ip sa*/
    if (SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P == p_tunnel_term->tunnel_term_table_type)
    {
        if (SAI_IP_ADDR_FAMILY_IPV4 == p_tunnel_term->src_ip.addr_family)
        {
            sal_memcpy(&p_vxlan_param->ipsa.ipv4, &p_tunnel_term->src_ip.addr.ip4, sizeof(sai_ip4_t));
			CTC_SAI_NTOH_V4(p_vxlan_param->ipsa.ipv4);
        }
        else if (SAI_IP_ADDR_FAMILY_IPV6 == p_tunnel_term->src_ip.addr_family)
        {
            sal_memcpy(&p_vxlan_param->ipsa.ipv6, &p_tunnel_term->src_ip.addr.ip6, sizeof(sai_ip6_t));
            CTC_SAI_NTOH_V6(p_vxlan_param->ipsa.ipv6);
        }
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_USE_IPSA);
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_tunnel_get_map_mappers_val(lchip, p_tunnel_term->tunnel_id, FALSE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_SRC_VNI_ID, &value));
    p_vxlan_param->src_vn_id = value;

    status = ctc_sai_tunnel_get_map_mappers_val(lchip, p_tunnel_term->tunnel_id, FALSE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VLAN_ID, &value);
    if (!CTC_SAI_ERROR(status))
    {
        p_vxlan_param->fid = value;
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_FID);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_overlay_tunnel_set_fid(lchip, p_vxlan_param->src_vn_id, value));
    }
    status = ctc_sai_tunnel_get_map_mappers_val(lchip, p_tunnel_term->tunnel_id, FALSE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_BRG_ID, &value);
    if (!CTC_SAI_ERROR(status))
    {
        p_vxlan_param->fid = value;
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_FID);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_overlay_tunnel_set_fid(lchip, p_vxlan_param->src_vn_id, value));
    }

    status = ctc_sai_tunnel_get_map_mappers_val(lchip, p_tunnel_term->tunnel_id, FALSE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VRF_ID, &value);
    if (!CTC_SAI_ERROR(status))
    {
        p_vxlan_param->vrf_id = value;
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_VRF);
    }

    if (p_tunnel->use_flex)
    {
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_USE_FLEX);
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_term_map_vxlan_action(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term, ctc_overlay_tunnel_param_t* p_vxlan_param)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_stats_statsid_t stats_statsid;
    int32 ret = CTC_E_NONE;
    uint32 value = 0;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    sal_memset(&stats_statsid, 0, sizeof(ctc_stats_statsid_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    sal_memset(&stats_statsid, 0, sizeof(ctc_stats_statsid_t));
    stats_statsid.dir = CTC_INGRESS;
    stats_statsid.type = CTC_STATS_STATSID_TYPE_TUNNEL;

    ret = ctcs_stats_create_statsid(lchip, &stats_statsid);
    status = ctc_sai_mapping_error_ctc(ret);
    if (!CTC_SAI_ERROR(status))
    {
        p_tunnel->decap_stats_id = stats_statsid.stats_id;
        p_vxlan_param->stats_id = stats_statsid.stats_id;
        CTC_SET_FLAG(p_vxlan_param->flag, CTC_OVERLAY_TUNNEL_FLAG_STATS_EN);
    }
    ctc_sai_tunnel_get_map_mappers_val(lchip, p_tunnel_term->tunnel_id, FALSE, CTC_SAI_TUNNEL_MAP_VAL_TYPE_DEST_VNI_ID, &value);
    p_vxlan_param->action.dst_vn_id = value;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_term_unmap_vxlan_action(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term)
{
    ctc_sai_tunnel_t* p_tunnel = NULL;

    p_tunnel = ctc_sai_db_get_object_property(lchip, p_tunnel_term->tunnel_id);
    if (NULL == p_tunnel)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if (0 != p_tunnel->decap_stats_id)
    {
        ctcs_stats_destroy_statsid(lchip, p_tunnel->decap_stats_id);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_add_ctc_tunnel(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term)
{
    ctc_ipuc_tunnel_param_t ipuc_tunnel_param;
    ctc_overlay_tunnel_param_t vxlan_param;
    int32 ret = CTC_E_NONE;

    sal_memset(&ipuc_tunnel_param, 0, sizeof(ctc_ipuc_tunnel_param_t));
    sal_memset(&vxlan_param, 0, sizeof(ctc_overlay_tunnel_param_t));

    switch(p_tunnel_term->tunnel_type)
    {
        case SAI_TUNNEL_TYPE_IPINIP:
        case SAI_TUNNEL_TYPE_IPINIP_GRE:
            CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_term_map_ip_tunnel_key(lchip, p_tunnel_term, &ipuc_tunnel_param));
            CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_term_map_ip_tunnel_action(lchip, p_tunnel_term, &ipuc_tunnel_param));
            ret = ctcs_ipuc_add_tunnel(lchip, &ipuc_tunnel_param);
            if (CTC_E_HASH_CONFLICT == ret)
            {
                CTC_SET_FLAG(ipuc_tunnel_param.flag, CTC_IPUC_TUNNEL_FLAG_USE_FLEX);
                ret = ctcs_ipuc_add_tunnel(lchip, &ipuc_tunnel_param);
                if (ret < CTC_E_NONE)
                {
                    _ctc_sai_tunnel_term_unmap_ip_tunnel_action(lchip, p_tunnel_term);
                    return ctc_sai_mapping_error_ctc(ret);
                }
            }
            else if(ret < CTC_E_NONE)
            {
                _ctc_sai_tunnel_term_unmap_ip_tunnel_action(lchip, p_tunnel_term);
                return ctc_sai_mapping_error_ctc(ret);
            }
            break;
        case SAI_TUNNEL_TYPE_VXLAN:
            vxlan_param.scl_id = 1;
            CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_term_map_vxlan_tunnel_key(lchip, p_tunnel_term, &vxlan_param));
            CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_term_map_vxlan_action(lchip, p_tunnel_term, &vxlan_param));
            ret = ctcs_overlay_tunnel_add_tunnel(lchip, &vxlan_param);
            if (CTC_E_HASH_CONFLICT == ret)
            {
                CTC_SET_FLAG(ipuc_tunnel_param.flag, CTC_OVERLAY_TUNNEL_FLAG_USE_FLEX);
                ret = ctcs_overlay_tunnel_add_tunnel(lchip, &vxlan_param);
                if (ret < CTC_E_NONE)
                {
                    _ctc_sai_tunnel_term_unmap_vxlan_action(lchip, p_tunnel_term);
                    return ctc_sai_mapping_error_ctc(ret);
                }
            }
            else if(ret < CTC_E_NONE)
            {
                _ctc_sai_tunnel_term_unmap_vxlan_action(lchip, p_tunnel_term);
                return ctc_sai_mapping_error_ctc(ret);
            }
            break;
        case SAI_TUNNEL_TYPE_MPLS:
        case SAI_TUNNEL_TYPE_MPLS_L2:

            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_remove_ctc_tunnel(uint8 lchip, ctc_sai_tunnel_term_table_entry_t* p_tunnel_term)
{
    ctc_ipuc_tunnel_param_t ipuc_tunnel_param;
    ctc_overlay_tunnel_param_t vxlan_param;

    sal_memset(&ipuc_tunnel_param, 0, sizeof(ctc_ipuc_tunnel_param_t));
    sal_memset(&vxlan_param, 0, sizeof(ctc_overlay_tunnel_param_t));

    switch(p_tunnel_term->tunnel_type)
    {
        case SAI_TUNNEL_TYPE_IPINIP:
        case SAI_TUNNEL_TYPE_IPINIP_GRE:
            _ctc_sai_tunnel_term_unmap_ip_tunnel_action(lchip, p_tunnel_term);
            _ctc_sai_tunnel_term_map_ip_tunnel_key(lchip, p_tunnel_term, &ipuc_tunnel_param);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_remove_tunnel(lchip, &ipuc_tunnel_param));
            break;
        case SAI_TUNNEL_TYPE_VXLAN:
            _ctc_sai_tunnel_term_unmap_vxlan_action(lchip, p_tunnel_term);
            _ctc_sai_tunnel_term_map_vxlan_tunnel_key(lchip, p_tunnel_term, &vxlan_param);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_overlay_tunnel_remove_tunnel(lchip, &vxlan_param));
            break;
        case SAI_TUNNEL_TYPE_MPLS:
        case SAI_TUNNEL_TYPE_MPLS_L2:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_tunnel_create_tunnel_term_table_entry(
        sai_object_id_t *tunnel_term_table_entry_id,
        sai_object_id_t switch_id,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val = NULL;
    uint32_t                     attr_idx = 0;
    int32 ret = 0;
    ctc_sai_tunnel_term_table_entry_t* p_tunnel_term = NULL;

    CTC_SAI_PTR_VALID_CHECK(tunnel_term_table_entry_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel term table entry type on create of tunnel term table entry\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else if (attr_val->s32 > SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2MP)
    {
        return SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_tunnel_alloc_tunnel_term_table_entry(&p_tunnel_term));
    p_tunnel_term->tunnel_term_table_type = attr_val->s32;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute vrf id on create of tunnel term table entry\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    p_tunnel_term->vrf_id = attr_val->oid;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute dst ip on create of tunnel term table entry\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    sal_memcpy(&p_tunnel_term->dst_ip, &attr_val->ipaddr, sizeof(sai_ip_address_t));

    if ((SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P == p_tunnel_term->tunnel_term_table_type))
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP, &attr_val, &attr_idx);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute src ip on create of tunnel term table entry\n");
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto roll_back_0;
        }
        sal_memcpy(&p_tunnel_term->src_ip, &attr_val->ipaddr, sizeof(sai_ip_address_t));
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TUNNEL_TYPE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
         CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute tunnel type on create of tunnel term table entry\n");
         status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
         goto roll_back_0;
    }
    else if (attr_val->s32 >= SAI_TUNNEL_TYPE_MPLS)
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    p_tunnel_term->tunnel_type = attr_val->s32;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
         CTC_SAI_LOG_ERROR(SAI_API_TUNNEL, "Missing mandatory attribute action tunnel id on create of tunnel term table entry\n");
         status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
         goto roll_back_0;
    }
    else if ((!CTC_SAI_ERROR(status)) && (false == ctc_sai_db_check_object_property_exist(lchip, attr_val->oid)))
    {
        status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
        goto roll_back_0;
    }
    p_tunnel_term->tunnel_id = attr_val->oid;

    ret = _ctc_sai_tunnel_add_ctc_tunnel(lchip, p_tunnel_term);
    if (ret)
    {
        p_tunnel_term->not_finished = 1;
    }
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_tunnel_term->tunnel_term_table_id), status, roll_back_1);
    *tunnel_term_table_entry_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, lchip, 0, 0, p_tunnel_term->tunnel_term_table_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *tunnel_term_table_entry_id, p_tunnel_term), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_term->tunnel_term_table_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_tunnel_remove_ctc_tunnel(lchip, p_tunnel_term);

roll_back_0:
    _ctc_sai_tunnel_free_tunnel_term_table_entry(p_tunnel_term);

    return status;
}

static sai_status_t
ctc_sai_tunnel_remove_tunnel_term_table_entry(
        sai_object_id_t tunnel_term_table_entry_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_tunnel_term_table_entry_t* p_tunnel_term = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, tunnel_term_table_entry_id, &ctc_oid));
    lchip = ctc_oid.lchip;
    CTC_SAI_DB_LOCK(lchip);
    p_tunnel_term = ctc_sai_db_get_object_property(lchip, tunnel_term_table_entry_id);
    if (NULL == p_tunnel_term)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    _ctc_sai_tunnel_remove_ctc_tunnel(lchip, p_tunnel_term);

    ctc_sai_db_remove_object_property(lchip, tunnel_term_table_entry_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_term->tunnel_term_table_id);

    _ctc_sai_tunnel_free_tunnel_term_table_entry(p_tunnel_term);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_tunnel_set_tunnel_term_table_entry_attribute(
            sai_object_id_t tunnel_term_table_entry_id,
            const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = tunnel_term_table_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_term_table_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_term_table_entry_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, tunnel_term_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_tunnel_get_tunnel_term_table_entry_attribute(
            sai_object_id_t tunnel_term_table_entry_id,
            uint32_t attr_count,
            sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = tunnel_term_table_entry_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_TUNNEL);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_term_table_entry_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = tunnel_term_table_entry_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, loop, tunnel_term_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

#define ________TUNNEL_WB________
static sai_status_t
_ctc_sai_tunnel_wb_reload_tunnel_map_entry_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t tunnel_map_entry_id = *(sai_object_id_t*)key;
    ctc_sai_tunnel_map_entry_t* p_tunnel_map_entry = (ctc_sai_tunnel_map_entry_t*)data;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, tunnel_map_entry_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));

    p_tunnel_map = ctc_sai_db_get_object_property(lchip, p_tunnel_map_entry->tunnel_map_id);
    if (NULL == p_tunnel_map)
    {
        return SAI_STATUS_FAILURE;
    }
    ctc_slist_add_tail(p_tunnel_map->map_entry_list, &(p_tunnel_map_entry->head));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_wb_reload_tunnel_map_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_map_t* p_tunnel_map = (ctc_sai_tunnel_map_t*)data;

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_tunnel_map->tunnel_map_id));

    p_tunnel_map->map_entry_list = ctc_slist_new();
    if (NULL == p_tunnel_map->map_entry_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return status;
}

static sai_status_t
_ctc_sai_tunnel_wb_reload_tunnel_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t tunnel_map_entry_id = *(sai_object_id_t*)key;
    ctc_sai_tunnel_t* p_tunnel = (ctc_sai_tunnel_t*)data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL, tunnel_map_entry_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));

    if((SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type) || (SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_LOGIC_PORT, p_tunnel->logic_port));
    }
    
    p_tunnel->encap_map_list = ctc_slist_new();
    p_tunnel->decap_map_list = ctc_slist_new();
    p_tunnel->encap_nh_list = ctc_slist_new();
    if ((NULL == p_tunnel->encap_map_list) || (NULL == p_tunnel->decap_map_list) || (NULL == p_tunnel->encap_nh_list))
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_wb_reload_tunnel_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_tunnel_t *p_tunnel = NULL;
    ctc_sai_wb_tunnel_nh_info_t wb_tunnel_info_node = {0};
    ctc_sai_wb_tunnel_mapper_t wb_tunnel_mapper_node = {0};
    ctc_sai_tunnel_nh_info_t* p_tunnel_nh_info = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    ctc_wb_query_t wb_query;
    uint16 entry_cnt = 0;
    uint32 offset = 0;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_tunnel_nh_info_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_NH_ID);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_tunnel_info_node, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_tunnel_nh_info_t));
        p_tunnel = ctc_sai_db_get_object_property(lchip, wb_tunnel_info_node.tunnel_oid);
        if (!p_tunnel)
        {
            continue;
        }

        p_tunnel_nh_info = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_tunnel_nh_info_t));
        if (!p_tunnel_nh_info)
        {
            continue;
        }
        p_tunnel_nh_info->nh_id = wb_tunnel_info_node.nh_id;
        sal_memcpy(&p_tunnel_nh_info->ip_addr, &wb_tunnel_info_node.ip_addr, sizeof(sai_ip_address_t));
        ctc_slist_add_tail(p_tunnel->encap_nh_list, &(p_tunnel_nh_info->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_tunnel_mapper_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_MAPPER_INFO);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_tunnel_mapper_node, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_tunnel_mapper_t));
        p_tunnel = ctc_sai_db_get_object_property(lchip, wb_tunnel_mapper_node.tunnel_oid);
        if (!p_tunnel)
        {
            continue;
        }

        p_tunnel_map = ctc_sai_db_get_object_property(lchip, wb_tunnel_mapper_node.tunnel_map_oid);
        if (!p_tunnel_map)
        {
            continue;
        }

        if (wb_tunnel_mapper_node.is_encap)
        {
            ctc_slist_add_tail(p_tunnel->encap_map_list, (void*)&p_tunnel_map->encap);
        }
        else
        {
            ctc_slist_add_tail(p_tunnel->decap_map_list, (void*)&p_tunnel_map->decap);
        }
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_tunnel_wb_tunnel_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    sai_object_id_t tunnel_id = *(sai_object_id_t*)key;
    ctc_sai_tunnel_t *p_tunnel = (ctc_sai_tunnel_t *)data;
    ctc_sai_tunnel_nh_info_t* p_tunnel_nh_info = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_wb_tunnel_nh_info_t wb_tunnel_info_node = {0};
    ctc_wb_data_t wb_data;
    uint16  max_entry_cnt = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_tunnel_nh_info_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_NH_ID);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_tunnel->encap_nh_list, node)
    {
        p_tunnel_nh_info = (ctc_sai_tunnel_nh_info_t*)node;

        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_tunnel_info_node.tunnel_oid = tunnel_id;
        wb_tunnel_info_node.nh_id = p_tunnel_nh_info->nh_id;
        sal_memcpy(&wb_tunnel_info_node.ip_addr, &p_tunnel_nh_info->ip_addr, sizeof(sai_ip_address_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_tunnel_info_node, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }

    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_tunnel_mapper_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_TUNNEL_MAPPER_INFO);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_tunnel->encap_map_list, node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_tunnel_info_node, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    CTC_SLIST_LOOP(p_tunnel->decap_map_list, node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_tunnel_info_node, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }


out:
done:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return status;
}

static sai_status_t
_ctc_sai_tunnel_wb_reload_tunnel_term_table_entry_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t tunnel_map_entry_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, tunnel_map_entry_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}

#define ________TUNNEL_DUMP________
static sai_status_t
_ctc_sai_tunnel_dump_tunnel_map_entry_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  tnl_map_entry_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_tunnel_map_entry_t* p_tnl_map_entry = NULL;

    tnl_map_entry_oid = bucket_data->oid;
    p_tnl_map_entry = (ctc_sai_tunnel_map_entry_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (tnl_map_entry_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d 0x%016"PRIx64" %-8d %-8d %-7d %-7d 0x%016"PRIx64" 0x%016"PRIx64"\n", num_cnt, tnl_map_entry_oid, p_tnl_map_entry->tunnel_map_type, \
           p_tnl_map_entry->tunnel_map_id, p_tnl_map_entry->vlan_key, p_tnl_map_entry->vlan_val, p_tnl_map_entry->vni_key, p_tnl_map_entry->vni_val, (SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI == p_tnl_map_entry->tunnel_map_type)?p_tnl_map_entry->brg_id_key:p_tnl_map_entry->vrf_key, \
           (SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF == p_tnl_map_entry->tunnel_map_type)?p_tnl_map_entry->brg_id_val:p_tnl_map_entry->vrf_val);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_dump_tunnel_map_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  tnl_map_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_tunnel_map_t* p_tnl_map = NULL;

    tnl_map_oid = bucket_data->oid;
    p_tnl_map = (ctc_sai_tunnel_map_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (tnl_map_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d\n", num_cnt, tnl_map_oid, p_tnl_map->tunnel_map_type);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_dump_tunnel_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t  tnl_oid = 0;
    sai_object_id_t  tnl_map_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_tunnel_t* p_tnl = NULL;
    ctc_slistnode_t* ctc_slistnode = NULL;
    ctc_sai_tunnel_map_t* p_tunnel_map = NULL;
    uint32 index =0;
    uint8 lchip = 0;
    char ip_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char* tunnel_type[SAI_TUNNEL_TYPE_MPLS_L2+1] = {"IPINIP", "IPINIP_GRE", "VXLAN", "MPLS","MPLS_L2_VPN"};

    tnl_oid = bucket_data->oid;
    p_tnl = (ctc_sai_tunnel_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    status = ctc_sai_oid_get_lchip(tnl_oid, &lchip);
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_SUCCESS;
    }

    if ((0 != p_dmp_grep->key.key.object_id) && (tnl_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_get_ip_str(&p_tnl->encap_src_ip, ip_buf);
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "NO:%-3d Tunnel_id:0x%016"PRIx64" Type:%-15s\n", num_cnt, tnl_oid, tunnel_type[p_tnl->tunnel_type]);
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    CTC_SAI_LOG_DUMP(p_file, "Encap_ttl_mode:%-2d Encap_ttl_val:%-2d Encap_dscp_mode:%-2d Encap_dscp_val:%-2d\n", p_tnl->encap_ttl_mode, \
        p_tnl->encap_ttl_val, p_tnl->encap_dscp_mode, p_tnl->encap_dscp_val);
    CTC_SAI_LOG_DUMP(p_file, "Encap_gre_key_en:%-2d Encap_gre_key:0x%-4x Encap_stats_id:%-6d Encap_src_ip:%s\n", p_tnl->encap_gre_key_en, \
        p_tnl->encap_gre_key, p_tnl->encap_stats_id, ip_buf);
    CTC_SAI_LOG_DUMP(p_file, "Underlay_if:0x%016"PRIx64" Overlay_if:0x%016"PRIx64"\n", p_tnl->underlay_if, \
        p_tnl->overlay_if);
    CTC_SAI_LOG_DUMP(p_file, "Decap_ecn_mode:%-2d Decap_ttl_mode:%-2d Decap_dscp_mode:%-2d Decap_stats_id:%-6d\n", p_tnl->decap_ecn_mode, \
        p_tnl->decap_ttl_mode, p_tnl->decap_dscp_mode, p_tnl->decap_stats_id);

    CTC_SAI_LOG_DUMP(p_file, "Encap_map_list:");
    CTC_SLIST_LOOP(p_tnl->encap_map_list, ctc_slistnode)
    {
        p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, encap);
        if (index == 6)
        {
            index = 0;
            CTC_SAI_LOG_DUMP(p_file, "\n");
            CTC_SAI_LOG_DUMP(p_file, "               ");
        }

        tnl_map_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
        CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", tnl_map_oid);
        index++;
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");

    index = 0;
    CTC_SAI_LOG_DUMP(p_file, "Decap_map_list:");
    CTC_SLIST_LOOP(p_tnl->decap_map_list, ctc_slistnode)
    {
        p_tunnel_map = _ctc_container_of(ctc_slistnode, ctc_sai_tunnel_map_t, decap);

        if (index == 6)
        {
            index = 0;
            CTC_SAI_LOG_DUMP(p_file, "\n");
            CTC_SAI_LOG_DUMP(p_file, "               ");
        }

        tnl_map_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_TUNNEL_MAP, lchip, 0, p_tunnel_map->tunnel_map_type, p_tunnel_map->tunnel_map_id);
        CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", tnl_map_oid);
        index++;
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_tunnel_dump_tunnel_term_table_entry_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t  tnl_term_tbl_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_tunnel_term_table_entry_t* p_tnl_term_tab_entry = NULL;
    char ip_src_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char ip_dst_buf[CTC_IPV6_ADDR_STR_LEN] = {0};

    tnl_term_tbl_oid = bucket_data->oid;
    p_tnl_term_tab_entry = (ctc_sai_tunnel_term_table_entry_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (tnl_term_tbl_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_get_ip_str(&p_tnl_term_tab_entry->src_ip, ip_src_buf);
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_get_ip_str(&p_tnl_term_tab_entry->dst_ip, ip_dst_buf);
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-4d 0x%016"PRIx64" 0x%016"PRIx64" %-39s %-39s\n", num_cnt, tnl_term_tbl_oid, p_tnl_term_tab_entry->tunnel_term_table_type, \
           p_tnl_term_tab_entry->vrf_id, p_tnl_term_tab_entry->tunnel_id, ip_dst_buf, ip_dst_buf);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_tunnel_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;

    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Tunnel MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Tunnel Map Entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_tunnel_map_entry_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-18s %-8s %-8s %-7s %-7s %-18s %-18s\n", "No.", "Tnl_map_entry_id", "Type", "Tnl_map_id", "Vlan_key", "Vlan_val", "Vni_key", "Vni_val", "brg_id_key/vrf_key", "brg_id_val/vrf_val");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY,
                                            (hash_traversal_fn)_ctc_sai_tunnel_dump_tunnel_map_entry_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_TUNNEL_MAP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Tunnel Map");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_tunnel_map_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s\n", "No.", "Tnl_map_id", "Type");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL_MAP,
                                            (hash_traversal_fn)_ctc_sai_tunnel_dump_tunnel_map_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_TUNNEL))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Tunnel");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_tunnel_t");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL,
                                            (hash_traversal_fn)_ctc_sai_tunnel_dump_tunnel_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Tunnel term table entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_tunnel_term_table_entry_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-4s %-18s %-18s %-39s %-39s\n", "No.", "Tnl_term_tab_id", "Type", "Vrf_id", "Tnl_id", "Dst_ip", "Src_ip");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY,
                                            (hash_traversal_fn)_ctc_sai_tunnel_dump_tunnel_term_table_entry_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________TUNNEL_API________

sai_tunnel_api_t g_ctc_sai_tunnel_api = {
     ctc_sai_tunnel_create_tunnel_map,
     ctc_sai_tunnel_remove_tunnel_map,
     ctc_sai_tunnel_set_tunnel_map_attribute,
     ctc_sai_tunnel_get_tunnel_map_attribute,
     ctc_sai_tunnel_create_tunnel,
     ctc_sai_tunnel_remove_tunnel,
     ctc_sai_tunnel_set_tunnel_attribute,
     ctc_sai_tunnel_get_tunnel_attribute,
     ctc_sai_tunnel_get_tunnel_stats,
     ctc_sai_tunnel_get_tunnel_stats_ext,
     ctc_sai_tunnel_clear_tunnel_stats,
     ctc_sai_tunnel_create_tunnel_term_table_entry,
     ctc_sai_tunnel_remove_tunnel_term_table_entry,
     ctc_sai_tunnel_set_tunnel_term_table_entry_attribute,
     ctc_sai_tunnel_get_tunnel_term_table_entry_attribute,
     ctc_sai_tunnel_create_tunnel_map_entry,
     ctc_sai_tunnel_remove_tunnel_map_entry,
     ctc_sai_tunnel_set_tunnel_map_entry_attribute,
     ctc_sai_tunnel_get_tunnel_map_entry_attribute
};

sai_status_t
ctc_sai_tunnel_db_init(uint8 lchip)
{
    uint8 gchip = 0;
    uint16 port_idx = 0;
    uint32 gport = 0;
    ctc_port_scl_property_t port_scl_property;
    ctc_global_panel_ports_t local_panel_ports;
    //ctc_dkit_tbl_reg_wr_t dkit_wr;
    //uint8 table_name[CTC_MAX_TABLE_DATA_LEN];
    //uint8 field1_name[CTC_MAX_TABLE_DATA_LEN];
    //uint8 field2_name[CTC_MAX_TABLE_DATA_LEN];
    ctc_sai_db_wb_t wb_info;

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TUNNEL;
    wb_info.data_len = sizeof(ctc_sai_tunnel_map_entry_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_tunnel_wb_reload_tunnel_map_entry_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TUNNEL;
    wb_info.data_len = sizeof(ctc_sai_tunnel_map_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_tunnel_wb_reload_tunnel_map_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TUNNEL_MAP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TUNNEL;
    wb_info.data_len = sizeof(ctc_sai_tunnel_t);
    wb_info.wb_sync_cb = _ctc_sai_tunnel_wb_tunnel_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_tunnel_wb_reload_tunnel_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_tunnel_wb_reload_tunnel_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TUNNEL, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_TUNNEL;
    wb_info.data_len = sizeof(ctc_sai_tunnel_term_table_entry_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_tunnel_wb_reload_tunnel_term_table_entry_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
/*
    sal_memset(&dkit_wr, 0, sizeof(ctc_dkit_tbl_reg_wr_t));
    sal_memset(table_name, 0, CTC_MAX_TABLE_DATA_LEN);
    sal_memset(field1_name, 0, CTC_MAX_TABLE_DATA_LEN);
    sal_memset(field2_name, 0, CTC_MAX_TABLE_DATA_LEN);

    sal_strncpy((char*)table_name, "DsPhyPortExt", sal_strlen("DsPhyPortExt"));
    sal_strncpy((char*)field1_name, "ipv4VxlanTunnelHashEn2", sal_strlen("ipv4VxlanTunnelHashEn2"));
    sal_strncpy((char*)field2_name, "ipv6VxlanTunnelHashEn2", sal_strlen("ipv6VxlanTunnelHashEn2"));
    dkit_wr.table_name = table_name;
    dkit_wr.value[0] = 1;
*/
    ctcs_get_gchip_id(lchip, &gchip);
    ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);

    sal_memset(&port_scl_property, 0, sizeof(port_scl_property));
    port_scl_property.scl_id = 1;
    port_scl_property.direction = CTC_INGRESS;
    port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_TUNNEL;
    port_scl_property.action_type = CTC_PORT_SCL_ACTION_TYPE_TUNNEL;

    for(port_idx = 0; port_idx < local_panel_ports.count; port_idx++)
    {
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[port_idx]);

        CTC_SAI_ERROR_RETURN(ctcs_port_set_scl_property(lchip, gport, &port_scl_property));
/*
        dkit_wr.field_name = field1_name;
        dkit_wr.table_index = local_panel_ports.lport[port_idx];
        ctc_dkit_write_table(lchip, &dkit_wr);
        dkit_wr.field_name = field2_name;
        ctc_dkit_write_table(lchip, &dkit_wr);
*/
    }

    /* Set again for VXLAN type, DT2/TM support, GG do not */
    port_scl_property.direction = CTC_INGRESS;
	port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_VXLAN;
    port_scl_property.action_type = CTC_PORT_SCL_ACTION_TYPE_TUNNEL;
    for(port_idx = 0; port_idx < local_panel_ports.count; port_idx++)
    {
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[port_idx]);
        CTC_SAI_ERROR_RETURN(ctcs_port_set_scl_property(lchip, gport, &port_scl_property));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_tunnel_db_deinit(uint8 lchip)
{

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL_MAP, (hash_traversal_fn)_ctc_sai_tunnel_db_map_deinit_cb, NULL);
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_TUNNEL, (hash_traversal_fn)_ctc_sai_tunnel_db_tunnel_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_tunnel_api_init()
{
    ctc_sai_register_module_api(SAI_API_TUNNEL, (void*)&g_ctc_sai_tunnel_api);

    return SAI_STATUS_SUCCESS;
}

