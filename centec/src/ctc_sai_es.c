
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctcs_api.h"

#include "ctc_dkit_api.h"
#include "ctc_sai_es.h"
#include "ctc_sai_mpls.h"

#define ________ES_INTERNAL________

static sai_status_t
_ctc_sai_es_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t es_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, es_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ES, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_es_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char es_oid[64] = {'-'};
    ctc_sai_es_t* p_es = NULL;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(es_oid, "0x%016"PRIx64, bucket_data->oid);
    p_es = (ctc_sai_es_t*)bucket_data->data;
    
    CTC_SAI_LOG_DUMP(p_file, "%-8d%-24s%-24d%-10d\n", num_cnt, es_oid, p_es->esi_label, p_es->local_es_id);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

void ctc_sai_es_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Ethernet Segment MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ES))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Ethernet Segment");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-24s%-26s%-10s\n", "No.", "ethernet_segment_id", "ESI Label", "Local ES ID");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ES,
                                            (hash_traversal_fn)_ctc_sai_es_dump_print_cb, (void*)(&sai_cb_data));
    }
}


#define ________ES________

static sai_status_t
_ctc_sai_es_alloc_es(ctc_sai_es_t** p_es)
{
    ctc_sai_es_t* p_es_tmp = NULL;

    p_es_tmp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_es_t));
    if (NULL == p_es_tmp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_es_tmp, 0, sizeof(ctc_sai_es_t));

    *p_es = p_es_tmp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_es_free_es(ctc_sai_es_t* p_es)
{
    mem_free(p_es);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_es_get_es_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_es_t* p_es = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ES);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_es = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_es)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_LOG_INFO(SAI_API_ES, "object id %"PRIx64" get ES attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_ES_ATTR_ESI_LABEL:
            attr->value.s32 = p_es->esi_label;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_ES, "ES attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t es_attr_fn_entries[] = {
    {SAI_ES_ATTR_ESI_LABEL, _ctc_sai_es_get_es_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};


static sai_status_t
ctc_sai_es_create_es(
        sai_object_id_t *es_id,
        sai_object_id_t switch_id,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val = NULL;
    uint32                     attr_idx = 0;
    ctc_sai_es_t* p_es = NULL;
    sai_inseg_entry_t inseg_entry;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    ctc_chip_device_info_t device_info;
    
    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));
    
    CTC_SAI_PTR_VALID_CHECK(es_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_ES);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ES_ATTR_ESI_LABEL, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ES, "Missing mandatory attribute ESI Label on create of ES\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    /* label pre-lookup, return if exist */
    inseg_entry.label = attr_val->s32;
    inseg_entry.switch_id = switch_id;
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, &inseg_entry);
    if(NULL != p_mpls_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_es_alloc_es(&p_es));
    p_es->esi_label = attr_val->s32;

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ES, &p_es->local_es_id), status, roll_back_1);
    *es_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ES, lchip, 0, 0, p_es->local_es_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *es_id, p_es), status, roll_back_2);
    /* add mpls entry for ESI Labe l*/
    ctc_mpls_ilm.label = p_es->esi_label;
    ctc_mpls_ilm.pop = 1;
    /* need set logicport for tm1.1 and tm2 */
    ctc_mpls_ilm.esid = p_es->local_es_id;

    CTC_SAI_CTC_ERROR_GOTO(ctcs_mpls_add_ilm(lchip, &ctc_mpls_ilm), status, roll_back_3);
    
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;
    
roll_back_3:
    ctc_sai_db_remove_object_property(lchip, *es_id);
roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ES, p_es->local_es_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);
    _ctc_sai_es_free_es(p_es);

    return status;
}

static sai_status_t
ctc_sai_es_remove_es(
        sai_object_id_t es_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_es_t* p_es = NULL;
    uint8 lchip = 0;
    ctc_chip_device_info_t device_info;
    ctc_mpls_ilm_t ctc_mpls_ilm;

    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));
    CTC_SAI_LOG_ENTER(SAI_API_ES);
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ES, es_id, &ctc_oid));
    CTC_SAI_DB_LOCK(lchip);
    lchip = ctc_oid.lchip;
    
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    
    p_es = ctc_sai_db_get_object_property(lchip, es_id);
    if (NULL == p_es)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if(p_es->ref_cnt != 0)
    {
        return SAI_STATUS_OBJECT_IN_USE;
    }

    ctc_mpls_ilm.label = p_es->esi_label;
    ctc_mpls_ilm.pop = 1;
    /* need set logicport for tm1.1 and tm2 */
    ctc_mpls_ilm.esid = p_es->local_es_id;

    CTC_SAI_ERROR_RETURN(ctcs_mpls_del_ilm(lchip, &ctc_mpls_ilm));
    
    ctc_sai_db_remove_object_property(lchip, es_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ES, p_es->local_es_id);

    _ctc_sai_es_free_es(p_es);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_es_set_es_attribute(sai_object_id_t es_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = es_id };
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_chip_device_info_t device_info;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_ES);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(es_id, &lchip));
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = es_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_ES, es_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_es_get_es_attribute(sai_object_id_t es_id,
                                                uint32_t attr_count,
                                                sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = es_id };
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_chip_device_info_t device_info;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_ES);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(es_id, &lchip));
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id != 3) || (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = es_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_ES, loop, es_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}


#define ________ES_API________

sai_es_api_t g_ctc_sai_es_api = {
     ctc_sai_es_create_es,
     ctc_sai_es_remove_es,
     ctc_sai_es_set_es_attribute,
     ctc_sai_es_get_es_attribute
};

sai_status_t
ctc_sai_es_db_init(uint8 lchip)
{
    uint8 gchip = 0;
    ctc_sai_db_wb_t wb_info;
    ctc_chip_device_info_t device_info;
    uint32 port,gport = 0,value = 1;

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ES;
    wb_info.data_len = sizeof(ctc_sai_es_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_es_wb_reload_cb;

    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ES, (void*)(&wb_info));
    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);
    
    ctcs_get_gchip_id(lchip, &gchip);
    ctcs_chip_get_property(lchip, CTC_CHIP_PROP_DEVICE_INFO, (void*)&device_info);
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) && device_info.version_id == 3) || CTC_CHIP_TSINGMA < ctcs_get_chip_type(lchip))
    {        
        ctcs_global_ctl_set(lchip, CTC_GLOBAL_ESLB_EN, &value);
        value=0;
        for(port=0;port<128;port++)
        {
            gport=port;
            ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_ESLB, 0);
        }
        return SAI_STATUS_SUCCESS;
    }    

    return SAI_STATUS_SUCCESS;
    
}

sai_status_t
ctc_sai_es_api_init()
{
    ctc_sai_register_module_api(SAI_API_ES, (void*)&g_ctc_sai_es_api);

    return SAI_STATUS_SUCCESS;
}

