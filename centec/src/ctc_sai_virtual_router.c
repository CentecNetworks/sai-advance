/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_router_interface.h"

/*sdk include file*/
#include "ctcs_api.h"

static sai_status_t
_ctc_sai_virtual_router_build_db(uint8 lchip, sai_object_id_t virtual_router_id, ctc_sai_virtual_router_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_virtual_router_t* p_vr_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    p_vr_info = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_virtual_router_t));
    if (NULL == p_vr_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VIRTUAL_ROUTER, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_vr_info, 0, sizeof(ctc_sai_virtual_router_t));
    status = ctc_sai_db_add_object_property(lchip, virtual_router_id, (void*)p_vr_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_vr_info);
    }
    /* default value */
    p_vr_info->v4_state = 1;
    p_vr_info->v6_state = 1;
    ctcs_l3if_get_router_mac(lchip, p_vr_info->src_mac);

    *oid_property = p_vr_info;

    return status;
}

static sai_status_t
_ctc_sai_virtual_router_remove_db(uint8 lchip, sai_object_id_t virtual_router_id)
{
    ctc_sai_virtual_router_t* p_vr_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    p_vr_info = ctc_sai_db_get_object_property(lchip, virtual_router_id);
    if (NULL == p_vr_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, virtual_router_id);
    mem_free(p_vr_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_virtual_router_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint16 vr_id = 0;
    uint32 value = 0;
    uint32 value1 = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;
    ctc_sai_rif_traverse_param_t traverse_param;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_vr_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    ctc_sai_oid_get_vrf_id(key->key.object_id, &vr_id);
    value1 = vr_id;
    if (NULL == p_vr_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.cmp_value = &value1;
    traverse_param.lchip = lchip;
    traverse_param.set_type = CTC_SAI_RIF_SET_TYPE_VRF;
    switch (attr->id)
    {
    case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE:
        p_vr_info->v4_state = attr->value.booldata;
        value = p_vr_info->v4_state;
        traverse_param.l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
        traverse_param.p_value = &value;
        ctc_sai_router_interface_traverse_set(&traverse_param);
        break;
    case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE:
        p_vr_info->v6_state = attr->value.booldata;
        value = p_vr_info->v6_state;
        traverse_param.l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
        traverse_param.p_value = &value;
        ctc_sai_router_interface_traverse_set(&traverse_param);
        break;
    case SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS:
        sal_memcpy(p_vr_info->src_mac, attr->value.mac, sizeof(sai_mac_t));
        traverse_param.l3if_prop = CTC_L3IF_PROP_ROUTE_MAC_LOW_8BITS;
        traverse_param.p_value = (void*)(p_vr_info->src_mac);
        ctc_sai_router_interface_traverse_set(&traverse_param);
        break;
    default:
        return SAI_STATUS_NOT_SUPPORTED;
        break;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_virtual_router_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_vr_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_vr_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
    case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE:
        attr->value.booldata = p_vr_info->v4_state;
        break;
    case SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE:
        attr->value.booldata = p_vr_info->v6_state;
        break;
    case SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS:
        sal_memcpy(attr->value.mac, p_vr_info->src_mac, sizeof(sai_mac_t));
        break;
    default:
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
        break;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_virtual_router_traverse_set_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_vrf_traverse_param_t* user_data)
{
    ctc_sai_virtual_router_t* p_vr_info = bucket_data->data;
    sai_object_key_t key;
    sai_attribute_t attr;
    
    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    
    key.key.object_id = bucket_data->oid;
    if (sal_memcmp(p_vr_info->src_mac, (sai_mac_t*)(user_data->cmp_value), sizeof(sai_mac_t)))
    {
        return SAI_STATUS_SUCCESS;
    }
        
    attr.id = SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS;
    sal_memcpy(&attr.value.mac, (sai_mac_t*)(user_data->p_value), sizeof(sai_mac_t));
    CTC_SAI_ERROR_RETURN(_ctc_sai_virtual_router_set_attr(&key, &attr));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_virtual_router_traverse_set(ctc_sai_vrf_traverse_param_t* traverse_param)
{
    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    CTC_SAI_PTR_VALID_CHECK(traverse_param);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->cmp_value);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->p_value);
    ctc_sai_db_traverse_object_property(traverse_param->lchip, SAI_OBJECT_TYPE_VIRTUAL_ROUTER, (hash_traversal_fn)_ctc_sai_virtual_router_traverse_set_cb, traverse_param);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_virtual_router_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_virtual_router_t*    p_vr_info = (ctc_sai_virtual_router_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char src_mac[64] = {0};

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_get_mac_str(p_vr_info->src_mac, src_mac);
    CTC_SAI_LOG_DUMP(p_file, "%-8d0x%016"PRIx64"  %-10d%-10d%-16s\n", num_cnt, bucket_data->oid, p_vr_info->v4_state, p_vr_info->v6_state, src_mac);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t vr_attr_fn_entries[] = {
    { SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE,
      _ctc_sai_virtual_router_get_attr,
      _ctc_sai_virtual_router_set_attr},
    { SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE,
      _ctc_sai_virtual_router_get_attr,
      _ctc_sai_virtual_router_set_attr},
    { SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS,
      _ctc_sai_virtual_router_get_attr,
      _ctc_sai_virtual_router_set_attr},
    { SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_TTL1_PACKET_ACTION,
      NULL,
      NULL},
    { SAI_VIRTUAL_ROUTER_ATTR_VIOLATION_IP_OPTIONS_PACKET_ACTION,
      NULL,
      NULL},
    { SAI_VIRTUAL_ROUTER_ATTR_UNKNOWN_L3_MULTICAST_PACKET_ACTION,
      NULL,
      NULL},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
#define ________INTERNAL_API________
sai_status_t
ctc_sai_virtual_router_get_vr_info(sai_object_id_t virtual_router_id, uint8* v4_state,
                                                 uint8* v6_state,  sai_mac_t src_mac)
{
    uint8 lchip = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    ctc_sai_oid_get_lchip(virtual_router_id, &lchip);
    p_vr_info = ctc_sai_db_get_object_property(lchip, virtual_router_id);
    if (NULL == p_vr_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (v4_state)
    {
        *v4_state = p_vr_info->v4_state;
    }
    if (v6_state)
    {
        *v6_state = p_vr_info->v6_state;
    }
    if (src_mac)
    {
        sal_memcpy(src_mac, &(p_vr_info->src_mac), sizeof(sai_mac_t));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_virtual_router_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t virtual_router_id = *(sai_object_id_t*)key;
    uint16 ctc_vrf_id = 0;
    ctc_sai_oid_get_vrf_id(virtual_router_id, &ctc_vrf_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_VRF, ctc_vrf_id));
    return status;
}

void ctc_sai_virtual_router_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Virtual Router MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_VIRTUAL_ROUTER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Virtual Router");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_virtual_router_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-20s%-10s%-10s%-16s\n", "No.","virtual_router_id","v4_state", "v6_state", "src_mac");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_VIRTUAL_ROUTER,
                                            (hash_traversal_fn)_ctc_sai_virtual_router_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
static sai_status_t
ctc_sai_virtual_router_create_vr(sai_object_id_t *virtual_router_id, sai_object_id_t switch_id,
                                                              uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_vrf_id = 0;
    sai_object_id_t vr_obj_id = 0;
    uint8 lchip = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;
    uint8          loop = 0;
    sai_object_key_t key;

    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    CTC_SAI_PTR_VALID_CHECK(virtual_router_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);


    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VRF, &ctc_vrf_id), status, out);
    vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, ctc_vrf_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_virtual_router_build_db(lchip, vr_obj_id, &p_vr_info), status, error1);

    sal_memset(&key, 0, sizeof(key));
    key.key.object_id = vr_obj_id;
    while(loop < attr_count)
    {
        status = ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_VIRTUAL_ROUTER,  vr_attr_fn_entries, &attr_list[loop]);
        if (SAI_STATUS_NOT_SUPPORTED == status)
        {
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + loop;
            goto error2;
        }
        loop++;
    }
    *virtual_router_id = vr_obj_id;
    goto out;

error2:
    _ctc_sai_virtual_router_remove_db(lchip, vr_obj_id);
error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VRF, ctc_vrf_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_virtual_router_remove_vr(sai_object_id_t virtual_router_id)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint16 ctc_vrf_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(virtual_router_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    CTC_SAI_ERROR_GOTO(_ctc_sai_virtual_router_remove_db(lchip, virtual_router_id), status, out);
    ctc_sai_oid_get_vrf_id(virtual_router_id, &ctc_vrf_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VRF, ctc_vrf_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_virtual_router_set_vr_attr(sai_object_id_t virtual_router_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(virtual_router_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    key.key.object_id = virtual_router_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_VIRTUAL_ROUTER,  vr_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_virtual_router_get_vr_attr(sai_object_id_t virtual_router_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(virtual_router_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_VIRTUAL_ROUTER);
    key.key.object_id = virtual_router_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_VIRTUAL_ROUTER, loop, vr_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_virtual_router_api_t ctc_sai_virtual_router_api = {
    ctc_sai_virtual_router_create_vr,
    ctc_sai_virtual_router_remove_vr,
    ctc_sai_virtual_router_set_vr_attr,
    ctc_sai_virtual_router_get_vr_attr
};

sai_status_t
ctc_sai_virtual_router_api_init()
{
    ctc_sai_register_module_api(SAI_API_VIRTUAL_ROUTER, (void*)&ctc_sai_virtual_router_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_virtual_router_db_init(uint8 lchip)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t vr_obj_id = 0;
    ctc_sai_virtual_router_t* p_vr_info = NULL;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_VIRTUALROUTER;
    wb_info.data_len = sizeof(ctc_sai_virtual_router_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_virtual_router_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_VIRTUAL_ROUTER, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, 0);
    _ctc_sai_virtual_router_build_db(lchip, vr_obj_id, &p_vr_info);

    return status;
}

