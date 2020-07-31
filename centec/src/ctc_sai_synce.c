
/*ctc_sai include file*/
#include "ctc_sai_synce.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

/*sdk include file*/
#include "ctcs_api.h"



static sai_status_t
_ctc_sai_synce_build_db(uint8 lchip, sai_object_id_t synce_id, ctc_sai_synce_db_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_synce_db_t* p_synce_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    p_synce_info = mem_malloc(MEM_SYNC_ETHER_MODULE, sizeof(ctc_sai_synce_db_t));
    if (NULL == p_synce_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_synce_info, 0, sizeof(ctc_sai_synce_db_t));
    status = ctc_sai_db_add_object_property(lchip, synce_id, (void*)p_synce_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_synce_info);
        return status;
    }

    *oid_property = p_synce_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_synce_remove_db(uint8 lchip, sai_object_id_t synce_id)
{
    ctc_sai_synce_db_t* p_synce_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    p_synce_info = ctc_sai_db_get_object_property(lchip, synce_id);
    if (NULL == p_synce_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, synce_id);
    mem_free(p_synce_info);
    return SAI_STATUS_SUCCESS;
}



#define ________INTERNAL_API________

sai_status_t
ctc_sai_synce_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{

    uint8 lchip = 0;
    uint16 clock_id = 0;
    ctc_sync_ether_cfg_t synce_cfg;
    ctc_sai_synce_db_t* p_synce_db = NULL;
    sai_object_id_t synce_oid= 0;
    sal_memset(&synce_cfg, 0, sizeof(synce_cfg));
    
    synce_oid = key->key.object_id;
    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));    
    ctcs_sync_ether_get_cfg(lchip, clock_id, &synce_cfg);
    p_synce_db = ctc_sai_db_get_object_property(lchip, synce_oid);
    
    if (NULL == p_synce_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    
    switch(attr->id)
    {

    case SAI_SYNCE_ATTR_RECOVERED_PORT:
        synce_cfg.recovered_clock_lport= attr->value.u16;
        p_synce_db->recovered_clock_lport = attr->value.u16;
        break;

    case SAI_SYNCE_ATTR_CLOCK_DIVIDER:
        synce_cfg.divider= attr->value.u16;
        break;

    }

    CTC_SAI_CTC_ERROR_RETURN (ctcs_sync_ether_set_cfg(lchip, clock_id, &synce_cfg));
    
    return  SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_synce_get_info(sai_object_key_t * key, sai_attribute_t * attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t        status = SAI_STATUS_SUCCESS;
    ctc_sync_ether_cfg_t synce_cfg;
    ctc_sai_synce_db_t* p_synce_db = NULL;
    uint16 clock_id = 0;

    sal_memset(&synce_cfg, 0, sizeof(synce_cfg));
    
    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SYNCE, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_synce_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_synce_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }


    CTC_SAI_ERROR_RETURN(ctcs_sync_ether_get_cfg(lchip, clock_id, &synce_cfg));
    
    switch(attr->id)
    {

    case SAI_SYNCE_ATTR_RECOVERED_PORT:
        attr->value.u16 = synce_cfg.recovered_clock_lport;
        break;

    case SAI_SYNCE_ATTR_CLOCK_DIVIDER:
        attr->value.u16 = synce_cfg.divider;
        break;

    }
    
    return status;
}


static  ctc_sai_attr_fn_entry_t synce_attr_fn_entries[] = 
{
      { SAI_SYNCE_ATTR_RECOVERED_PORT,
      ctc_sai_synce_get_info,
      ctc_sai_synce_set_info},
      { SAI_SYNCE_ATTR_CLOCK_DIVIDER,
      ctc_sai_synce_get_info,
      ctc_sai_synce_set_info},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL},

 };

#define ________SAI_API________

static sai_status_t ctc_sai_synce_create_synce( sai_object_id_t *synce_id,
                         sai_object_id_t        switch_id,
                         uint32_t               attr_count,
                         const sai_attribute_t *attr_list)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 count = 0;
    const sai_attribute_value_t *attr_value;
    ctc_sync_ether_cfg_t synce_cfg;
    sai_object_id_t synce_oid = 0;
    uint32                   attr_index = 0;
    uint32  sai_synce_id = 0;
    uint8 clock_id = 0;
    ctc_sai_synce_db_t* p_synce_info = NULL;
    
    sal_memset(&synce_cfg, 0, sizeof(synce_cfg));
    synce_cfg.link_status_detect_en = 1;
    synce_cfg.clock_output_en = 1;
    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    CTC_SAI_PTR_VALID_CHECK(synce_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_SYNCE, &count), status, out);
    if(count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "error:ONE SyncE HAS BEEN CREATED!ONLY SUPPORT ONE SyncE!");
        status =  SAI_STATUS_FAILURE;
        goto out;
    }  

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SYNCE, &sai_synce_id), status, out);
    synce_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SYNCE, lchip, 0, 0, sai_synce_id);
    CTC_SAI_LOG_INFO(SAI_API_SYNCE, "create synce_id = 0x%"PRIx64"\n", synce_oid);
    CTC_SAI_ERROR_GOTO(_ctc_sai_synce_build_db(lchip, synce_oid, &p_synce_info), status, error1);

  
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SYNCE_ATTR_RECOVERED_PORT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        synce_cfg.recovered_clock_lport = attr_value->u16;
        p_synce_info->recovered_clock_lport = attr_value->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SYNCE_ATTR_CLOCK_DIVIDER, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        synce_cfg.divider = attr_value->u16;
    }

    CTC_SAI_ERROR_GOTO (ctcs_sync_ether_set_cfg(lchip, clock_id, &synce_cfg), status, error2);
    *synce_id = synce_oid;
    status = SAI_STATUS_SUCCESS;
    goto out;
    
error2:
    CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "rollback to error2\n");
    _ctc_sai_synce_remove_db(lchip, synce_oid);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SYNCE, sai_synce_id);    
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;

}



sai_status_t
ctc_sai_synce_remove_synce( _In_ sai_object_id_t synce_id)
{
    ctc_object_id_t ctc_object_id;
    sai_status_t status = 0;
    uint8 clock_id = 0;
    uint8 lchip = 0;
    ctc_sync_ether_cfg_t synce_cfg;
    uint32 synceid = 0;
    ctc_sai_synce_db_t* p_synce_info = NULL;
    sal_memset(&synce_cfg, 0, sizeof(synce_cfg));

    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SYNCE, synce_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SYNCE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "Object Type is Not SAI_OBJECT_TYPE_SYNCE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    
    p_synce_info = ctc_sai_db_get_object_property(lchip, synce_id);    
    if (NULL == p_synce_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_CTC_ERROR_GOTO (ctcs_sync_ether_set_cfg(lchip, clock_id, &synce_cfg), status, out);
    ctc_sai_oid_get_value(synce_id, &synceid);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SYNCE, synceid);    
    _ctc_sai_synce_remove_db(lchip, synce_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
}



static sai_status_t ctc_sai_synce_set_synce_attribute(sai_object_id_t synce_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = synce_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(synce_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_SYNCE,  synce_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "Failed to set synce attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}



static sai_status_t ctc_sai_synce_get_synce_attribute( sai_object_id_t  synce_id, sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = synce_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SYNCE);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(synce_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_SYNCE, loop, synce_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SYNCE, "Failed to get synce attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}


const sai_synce_api_t g_ctc_sai_synce_api = {
    ctc_sai_synce_create_synce,
    ctc_sai_synce_remove_synce,
    ctc_sai_synce_set_synce_attribute,
    ctc_sai_synce_get_synce_attribute
};


sai_status_t
ctc_sai_synce_api_init()
{
    ctc_sai_register_module_api(SAI_API_SYNCE, (void*)&g_ctc_sai_synce_api);

    return SAI_STATUS_SUCCESS;
}


