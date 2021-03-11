/*ctc_sai include file*/
#include "sai.h"
#include "ctc_sai_monitor.h"
#include "ctc_sai_port.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

/*sdk include file*/
#include "ctcs_api.h"

static sai_status_t
_ctc_sai_monitor_buffer_build_db(uint8 lchip, sai_object_id_t monitor_buffer_id, ctc_sai_monitor_buffer_db_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    p_monitor_buffer_info = mem_malloc(MEM_MONITOR_MODULE, sizeof(ctc_sai_monitor_buffer_db_t));
    if (NULL == p_monitor_buffer_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_monitor_buffer_info, 0, sizeof(ctc_sai_monitor_buffer_db_t));
    status = ctc_sai_db_add_object_property(lchip, monitor_buffer_id, (void*)p_monitor_buffer_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_monitor_buffer_info);
        return status;
    }

    *oid_property = p_monitor_buffer_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_monitor_latency_build_db(uint8 lchip, sai_object_id_t monitor_latency_id, ctc_sai_monitor_latency_db_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_monitor_latency_db_t* p_monitor_latency_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    p_monitor_latency_info = mem_malloc(MEM_MONITOR_MODULE, sizeof(ctc_sai_monitor_latency_db_t));
    if (NULL == p_monitor_latency_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_monitor_latency_info, 0, sizeof(ctc_sai_monitor_latency_db_t));
    status = ctc_sai_db_add_object_property(lchip, monitor_latency_id, (void*)p_monitor_latency_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_monitor_latency_info);
        return status;
    }

    *oid_property = p_monitor_latency_info;

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_monitor_buffer_remove_db(uint8 lchip, sai_object_id_t monitor_buffer_id)
{
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    p_monitor_buffer_info = ctc_sai_db_get_object_property(lchip, monitor_buffer_id);
    if (NULL == p_monitor_buffer_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, monitor_buffer_id);
    mem_free(p_monitor_buffer_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_monitor_latency_remove_db(uint8 lchip, sai_object_id_t monitor_latency_id)
{
    ctc_sai_monitor_latency_db_t* p_monitor_latency_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    p_monitor_latency_info = ctc_sai_db_get_object_property(lchip, monitor_latency_id);
    if (NULL == p_monitor_latency_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, monitor_latency_id);
    mem_free(p_monitor_latency_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_monitor_buffer_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             monitor_buffer_id  = bucket_data->oid;
    ctc_sai_monitor_buffer_db_t*       p_db        = (ctc_sai_monitor_buffer_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump      = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file      = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt         = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (monitor_buffer_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-16d %-6d %-4d %-4d %-4d %-12d %-4d %-12d %-4d\n",
                            *cnt,monitor_buffer_id,p_db->buffer_mb_enable,p_db->mb_overthreshold_event,p_db->mb_port_thrd_min,
                            p_db->mb_port_thrd_max,p_db->ingress_perio_monitor_enable,
                            p_db->egress_perio_monitor_enable,p_db->ingress_port_perio_monitor_enable,
                            p_db->egress_port_perio_monitor_enable,p_db->perio_monitor_interval);

    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_monitor_latency_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             monitor_latency_id  = bucket_data->oid;
    ctc_sai_monitor_latency_db_t*       p_db        = (ctc_sai_monitor_latency_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump      = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file      = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt         = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (monitor_latency_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-16d %-6d %-8x %-4d  %-8x\n",
                            *cnt,monitor_latency_id,p_db->perio_monitor_interval,p_db->latency_mb_enable,p_db->overthreshold_event_bmp,
                            p_db->perio_monitor_enable, p_db->discard_bmp);

    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_FUNCTION_____


sai_status_t ctc_sai_monitor_mapping_to_byte(uint8 lchip,uint32 cell, uint32* byte )
{
    uint8 chip_type = 0;
    
    chip_type = ctcs_get_chip_type(lchip);
    if ((CTC_CHIP_TSINGMA == chip_type) || (CTC_CHIP_TSINGMA_MX== chip_type))
    {
        *byte = cell * TM_CELL_TO_BYTE;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "not support\n");
        return SAI_STATUS_NOT_SUPPORTED;
    }
    
    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_monitor_mapping_from_byte(uint8 lchip,uint32 byte, uint32* cell )
{
    uint8 chip_type = 0;
    
    chip_type = ctcs_get_chip_type(lchip);
    if ((CTC_CHIP_TSINGMA == chip_type) || (CTC_CHIP_TSINGMA_MX== chip_type))
    {
        *cell = byte / TM_CELL_TO_BYTE;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "not support\n");
        return SAI_STATUS_NOT_SUPPORTED;
    }
    
    return SAI_STATUS_SUCCESS;
}
#define ________BUFFER_MONITOR_____

sai_status_t
ctc_sai_monitor_buffer_get_info(sai_object_key_t * key, sai_attribute_t * attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_db = NULL;
    uint32 watermark =0;
    int32 ret = 0;
    ctc_monitor_watermark_t buffer_monitor_watermark;

    sal_memset(&buffer_monitor_watermark, 0, sizeof(buffer_monitor_watermark));
    buffer_monitor_watermark.monitor_type = CTC_MONITOR_BUFFER;
    buffer_monitor_watermark.u.buffer.buffer_type = CTC_MONITOR_BUFFER_PORT;
    
    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_monitor_buffer_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_monitor_buffer_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    buffer_monitor_watermark.gport = ctc_object_id.value;
    
    switch(attr->id)
    {
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
        attr->value.oid= ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, ctc_object_id.value);
        break;
        
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD:
        attr->value.u32= p_monitor_buffer_db->mb_port_thrd_min;
        break;


    case SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD:
        attr->value.u32= p_monitor_buffer_db->mb_port_thrd_max;
        break;


    case SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
        attr->value.booldata= p_monitor_buffer_db->ingress_port_perio_monitor_enable;
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
        attr->value.booldata= p_monitor_buffer_db->egress_port_perio_monitor_enable;
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK:
        buffer_monitor_watermark.u.buffer.dir = CTC_INGRESS;
        ret = ctcs_monitor_get_watermark(lchip, &buffer_monitor_watermark);
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_to_byte(lchip, buffer_monitor_watermark.u.buffer.max_total_cnt, &watermark));
        attr->value.u32 = watermark;
        break;
        
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK:
        buffer_monitor_watermark.u.buffer.dir = CTC_EGRESS;
        ret = ctcs_monitor_get_watermark(lchip, &buffer_monitor_watermark);
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_to_byte(lchip, buffer_monitor_watermark.u.buffer.max_total_cnt, &watermark));
        attr->value.u32 = watermark;
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK:
        buffer_monitor_watermark.u.buffer.dir = CTC_EGRESS;
        ret = ctcs_monitor_get_watermark(lchip, &buffer_monitor_watermark);
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_to_byte(lchip, buffer_monitor_watermark.u.buffer.max_uc_cnt, &watermark));
        attr->value.u32 = watermark;
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK:
        buffer_monitor_watermark.u.buffer.dir = CTC_EGRESS;
        ret = ctcs_monitor_get_watermark(lchip, &buffer_monitor_watermark);
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_to_byte(lchip, buffer_monitor_watermark.u.buffer.max_mc_cnt, &watermark));
        attr->value.u32 = watermark;
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Get buffer monitor attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;    

    }
    return status;
    
}

sai_status_t
ctc_sai_monitor_buffer_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_monitor_config_t buffer_monitor_cfg;
    ctc_monitor_glb_cfg_t buffer_monitor_glb_cfg;
    ctc_monitor_watermark_t buffer_monitor_watermark;
    sai_object_id_t monitor_buffer_id= 0;
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_db = NULL;
    uint32 min_threshold = 0;
    uint32 max_threshold = 0;

    sal_memset(&buffer_monitor_cfg, 0, sizeof(buffer_monitor_cfg));
    buffer_monitor_cfg.monitor_type = CTC_MONITOR_BUFFER;
    
    sal_memset(&buffer_monitor_watermark, 0, sizeof(buffer_monitor_watermark));
    buffer_monitor_watermark.monitor_type = CTC_MONITOR_BUFFER;
    buffer_monitor_watermark.u.buffer.buffer_type = CTC_MONITOR_BUFFER_PORT;

    sal_memset(&buffer_monitor_glb_cfg, 0, sizeof(buffer_monitor_glb_cfg));
    buffer_monitor_glb_cfg.cfg_type= CTC_MONITOR_GLB_CONFIG_MBURST_THRD;
    monitor_buffer_id = key->key.object_id;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    p_monitor_buffer_db = ctc_sai_db_get_object_property(lchip, monitor_buffer_id);
    buffer_monitor_cfg.buffer_type = CTC_MONITOR_BUFFER_PORT;
    
    if (NULL == p_monitor_buffer_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    buffer_monitor_cfg.gport = ctc_object_id.value;
    buffer_monitor_watermark.gport = ctc_object_id.value;
    
    switch(attr->id)
    {
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
       CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "NOTE:NOT SUPPORT SET SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT!");
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD:
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_from_byte(lchip, attr->value.u32, &min_threshold));
        buffer_monitor_cfg.value = min_threshold;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MIN;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));
        p_monitor_buffer_db->mb_port_thrd_min = attr->value.u32;  
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD:
        CTC_SAI_CTC_ERROR_RETURN (ctc_sai_monitor_mapping_from_byte(lchip, attr->value.u32, &max_threshold));
        buffer_monitor_cfg.value = max_threshold;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MAX;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));
        p_monitor_buffer_db->mb_port_thrd_max = attr->value.u32;  
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
        if(attr->value.booldata == TRUE)
        {
            buffer_monitor_cfg.value = 1; 
        }
        else
        {
            buffer_monitor_cfg.value = 0;
        }
        buffer_monitor_cfg.dir= CTC_INGRESS;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));
        p_monitor_buffer_db->ingress_port_perio_monitor_enable = attr->value.booldata;
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
        if(attr->value.booldata == TRUE)
        {
            buffer_monitor_cfg.value = 1; 
        }
        else
        {
            buffer_monitor_cfg.value = 0;
        }
        buffer_monitor_cfg.dir= CTC_EGRESS;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));
        p_monitor_buffer_db->egress_port_perio_monitor_enable = attr->value.booldata;
        break;
       
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK:
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK:
    case SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK:    
        if(attr->value.u32 != 0 )
        {
            CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:clear SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK,the value should be 0!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            buffer_monitor_watermark.u.buffer.dir = CTC_EGRESS;
            CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_clear_watermark(lchip, &buffer_monitor_watermark));
        }
        break;

    case SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK:
        if(attr->value.u32 != 0 )
        {
            CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:clear SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK,the value should be 0!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            buffer_monitor_watermark.u.buffer.dir = CTC_INGRESS;
            CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_clear_watermark(lchip, &buffer_monitor_watermark));
        }
        break;    
    }

    return  SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_monitor_buffer_recover_info(sai_object_id_t monitor_buffer_id)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_monitor_config_t buffer_monitor_cfg;
    ctc_monitor_watermark_t buffer_monitor_watermark;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, monitor_buffer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    sal_memset(&buffer_monitor_cfg, 0, sizeof(buffer_monitor_cfg));
    buffer_monitor_cfg.gport = ctc_object_id.value;
    buffer_monitor_cfg.monitor_type = CTC_MONITOR_BUFFER;
    buffer_monitor_cfg.buffer_type = CTC_MONITOR_BUFFER_PORT;

    sal_memset(&buffer_monitor_watermark, 0, sizeof(buffer_monitor_watermark));
    buffer_monitor_watermark.gport = ctc_object_id.value;
    buffer_monitor_watermark.monitor_type = CTC_MONITOR_BUFFER;
    buffer_monitor_watermark.u.buffer.buffer_type = CTC_MONITOR_BUFFER_PORT;

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD
    buffer_monitor_cfg.value = 0;
    buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MIN;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD
    buffer_monitor_cfg.value = BUFFER_MB_PORT_THRD_MAX_DEFAULT;
    buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MAX;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE
    buffer_monitor_cfg.value = 0;
    buffer_monitor_cfg.dir= CTC_INGRESS;
    buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE
    buffer_monitor_cfg.value = 0;
    buffer_monitor_cfg.dir= CTC_EGRESS;
    buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg));

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK
    //SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK
    //SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK
    buffer_monitor_watermark.u.buffer.dir = CTC_EGRESS;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_clear_watermark(lchip, &buffer_monitor_watermark));

    //SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK
    buffer_monitor_watermark.u.buffer.dir = CTC_INGRESS;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_clear_watermark(lchip, &buffer_monitor_watermark));

    return  SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t monitor_buffer_attr_fn_entries[] = 
{
     { SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT,
      ctc_sai_monitor_buffer_get_info,
      NULL},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK,
      ctc_sai_monitor_buffer_get_info,
      ctc_sai_monitor_buffer_set_info},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL},
};

#define ________LANTENCY_MONITOR_____

sai_status_t
ctc_sai_monitor_latency_get_info(sai_object_key_t * key, sai_attribute_t * attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 index = 0;
    int32 ret = 0;
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_monitor_latency_db_t* p_monitor_latency_db = NULL;
    ctc_monitor_watermark_t latency_monitor_watermark;

    sal_memset(&latency_monitor_watermark, 0, sizeof(latency_monitor_watermark));
    latency_monitor_watermark.monitor_type = CTC_MONITOR_LATENCY;
    
    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_monitor_latency_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_monitor_latency_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    
    switch(attr->id)
    {
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
        attr->value.oid= ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, ctc_object_id.value);
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE:
        attr->value.booldata= p_monitor_latency_db->latency_mb_enable;
        break;
        
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
        for(index = 0; index < MB_LEVEL; index++)
        {
            attr->value.boollist.list[index] = CTC_IS_BIT_SET(p_monitor_latency_db->overthreshold_event_bmp, index);
        }        
        break;
              
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
        attr->value.booldata = p_monitor_latency_db->perio_monitor_enable;
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
        for(index = 0; index < MB_LEVEL; index++)
        {
            attr->value.boollist.list[index]= CTC_IS_BIT_SET(p_monitor_latency_db->discard_bmp, index);
        }
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
        latency_monitor_watermark.gport = ctc_object_id.value;
        ret = ctcs_monitor_get_watermark(lchip, &latency_monitor_watermark);
        attr->value.u32 = latency_monitor_watermark.u.latency.max_latency;                 
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Get latency monitor attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;    

    }
    return status;
    
}

sai_status_t
ctc_sai_monitor_latency_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_monitor_config_t latency_monitor_cfg;
    ctc_monitor_glb_cfg_t latency_monitor_glb_cfg;
    ctc_monitor_watermark_t latency_monitor_watermark;
    sai_object_id_t monitor_latency_id= 0;
    ctc_sai_monitor_latency_db_t* p_monitor_latency_db = NULL;
    uint8 index = 0;

    sal_memset(&latency_monitor_cfg, 0, sizeof(latency_monitor_cfg));
    latency_monitor_cfg.monitor_type = CTC_MONITOR_LATENCY;

    sal_memset(&latency_monitor_watermark, 0, sizeof(latency_monitor_watermark));
    latency_monitor_watermark.monitor_type = CTC_MONITOR_LATENCY;
    
    sal_memset(&latency_monitor_glb_cfg, 0, sizeof(latency_monitor_glb_cfg));
    latency_monitor_glb_cfg.cfg_type= CTC_MONITOR_GLB_CONFIG_LATENCY_THRD;
    monitor_latency_id = key->key.object_id;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    p_monitor_latency_db = ctc_sai_db_get_object_property(lchip, monitor_latency_id);
    
    if (NULL == p_monitor_latency_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    latency_monitor_cfg.gport = ctc_object_id.value;
    latency_monitor_watermark.gport = ctc_object_id.value;
    
    switch(attr->id)
    {
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
       CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "NOTE:NOT SUPPORT SET SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT!");
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE:
        if(attr->value.booldata == TRUE ) 
        {
            latency_monitor_cfg.value = 1; 
        }
        else
        {
            latency_monitor_cfg.value = 0;
        }
        latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_EN;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
        p_monitor_latency_db->latency_mb_enable = attr->value.booldata;
        break;
        
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
        for(index = 0; index < MB_LEVEL; index++)
        {
            latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LOG_THRD_LEVEL;
            latency_monitor_cfg.level= index;
            if(attr->value.boollist.list[index] == TRUE)
            {
                latency_monitor_cfg.value = 1; 
            }
            else
            {
                latency_monitor_cfg.value = 0;
            }
            CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
            if(attr->value.boollist.list[index] == TRUE)
            {
                CTC_BIT_SET(p_monitor_latency_db->overthreshold_event_bmp, index);
            }
            else
            {
                CTC_BIT_UNSET(p_monitor_latency_db->overthreshold_event_bmp, index);
            }
        }
        break;
        
    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
        if(attr->value.booldata == TRUE)
        {
            latency_monitor_cfg.value = 1; 
        }
        else
        {
            latency_monitor_cfg.value = 0;
        }
        latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
        p_monitor_latency_db->perio_monitor_enable = attr->value.booldata;
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
        for(index = 0; index < MB_LEVEL; index++)
        {
            latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LANTENCY_DISCARD_THRD_LEVEL;
            latency_monitor_cfg.level= index;
            if(attr->value.boollist.list[index] == TRUE)
            {
                latency_monitor_cfg.value = 1;
            }
            else
            {
                latency_monitor_cfg.value = 0 ;
            }
            CTC_SAI_CTC_ERROR_RETURN(ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
            if(attr->value.boollist.list[index] == TRUE)
            {
                CTC_BIT_SET(p_monitor_latency_db->discard_bmp, index);
            }
            else
            {
                CTC_BIT_UNSET(p_monitor_latency_db->discard_bmp, index);
            }
        }
        break;

    case SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
        if(attr->value.u32 != 0 )
        {
            CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:clear SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK,the value should be 0!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            latency_monitor_watermark.gport = ctc_object_id.value;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_monitor_clear_watermark(lchip, &latency_monitor_watermark));
        }
            
        break;
    }
    return  SAI_STATUS_SUCCESS;

}

sai_status_t
ctc_sai_monitor_latency_recover_info(sai_object_id_t monitor_latency_id)
{
    uint8 lchip = 0;
    uint8 index = 0;
    ctc_object_id_t ctc_object_id;
    ctc_monitor_config_t latency_monitor_cfg;
    ctc_monitor_watermark_t latency_monitor_watermark;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, monitor_latency_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    sal_memset(&latency_monitor_cfg, 0, sizeof(latency_monitor_cfg));
    latency_monitor_cfg.gport = ctc_object_id.value;
    latency_monitor_cfg.monitor_type = CTC_MONITOR_LATENCY;

    sal_memset(&latency_monitor_watermark, 0, sizeof(latency_monitor_watermark));
    latency_monitor_watermark.gport = ctc_object_id.value;
    latency_monitor_watermark.monitor_type = CTC_MONITOR_LATENCY;

    //SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE
    latency_monitor_cfg.value = 0;
    latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_EN;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));

    //SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT
    for(index = 0; index < MB_LEVEL; index++)
    {
        latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LOG_THRD_LEVEL;
        latency_monitor_cfg.level= index;
        latency_monitor_cfg.value = 0;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
    }

    //SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE
    latency_monitor_cfg.value = 0;
    latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
    CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));

    //SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD
    for(index = 0; index < MB_LEVEL; index++)
    {
        latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LANTENCY_DISCARD_THRD_LEVEL;
        latency_monitor_cfg.level= index;
        latency_monitor_cfg.value = 0;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_monitor_set_config(lchip, &latency_monitor_cfg));
    }

    //SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK
    CTC_SAI_CTC_ERROR_RETURN(ctcs_monitor_clear_watermark(lchip, &latency_monitor_watermark));

    return  SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t monitor_latency_attr_fn_entries[] = 
{
     { SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT,
      ctc_sai_monitor_latency_get_info,
      NULL},
      { SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE,
      ctc_sai_monitor_latency_get_info,
      ctc_sai_monitor_latency_set_info},
      { SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT,
      ctc_sai_monitor_latency_get_info,
      ctc_sai_monitor_latency_set_info}, 
      { SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE,
      ctc_sai_monitor_latency_get_info,
      ctc_sai_monitor_latency_set_info},
      { SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD,
      ctc_sai_monitor_latency_get_info,
      ctc_sai_monitor_latency_set_info},
      { SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK,
      ctc_sai_monitor_latency_get_info,
      ctc_sai_monitor_buffer_set_info},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL},      
};

#define ________SAI_DUMP________

void
ctc_sai_monitor_buffer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI MONITOR MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "MONITOR");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_monitor_buffer_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, " ");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR,
                                                (hash_traversal_fn)_ctc_sai_monitor_buffer_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}


void
ctc_sai_monitor_latency_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI MONITOR MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "MONITOR");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_monitor_latency_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, " ");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR,
                                                (hash_traversal_fn)_ctc_sai_monitor_latency_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}


#define ________SAI_API________

static sai_status_t ctc_sai_monitor_create_monitor_buffer( sai_object_id_t *monitor_buffer_id,
                         sai_object_id_t        switch_id,
                         uint32_t               attr_count,
                         const sai_attribute_t *attr_list)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 gchip = 0;
    uint32 num = 0;
    uint32 gport_value = 0;
    bool port_check_flag = false;
    ctc_global_panel_ports_t local_panel_ports;
    ctc_monitor_config_t buffer_monitor_cfg;
    ctc_monitor_glb_cfg_t buffer_monitor_glb_cfg;
    const sai_attribute_value_t *attr_value;
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_info = NULL;
    sai_object_id_t monitor_buffer_oid = 0;
    ctc_object_id_t ctc_object_id;
    uint32                   attr_index = 0;
    uint32 gport;
    uint32 min_threshold = 0;
    uint32 max_threshold = 0;
    
    sal_memset(&buffer_monitor_cfg, 0, sizeof(buffer_monitor_cfg));
    buffer_monitor_cfg.monitor_type = CTC_MONITOR_BUFFER;
    buffer_monitor_cfg.buffer_type = CTC_MONITOR_BUFFER_PORT;

    sal_memset(&buffer_monitor_glb_cfg, 0, sizeof(buffer_monitor_glb_cfg));
    buffer_monitor_glb_cfg.cfg_type= CTC_MONITOR_GLB_CONFIG_MBURST_THRD;
    
    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_PTR_VALID_CHECK(monitor_buffer_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_value->oid, &ctc_object_id);
        if (ctc_object_id.type != SAI_OBJECT_TYPE_PORT)
        {

            status = SAI_STATUS_INVALID_OBJECT_TYPE;
            CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to create monitor buffer, invalid port id:%d\n", status);
            goto out;
        }
        gport = ctc_object_id.value;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "MANDATORY attribute SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT missing !\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }

    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
    ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);
    ctcs_get_gchip_id(lchip, &gchip);
    for (num = 0; num < local_panel_ports.count; num++)
    {
        gport_value = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
        if(gport == gport_value)
        {
            port_check_flag = true;
            break;
        }
    }

    if (port_check_flag == false) {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "MANDATORY attribute SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT error,no port %d !\n", gport);
        status = SAI_STATUS_INVALID_PORT_NUMBER;
        goto out;
    }

    monitor_buffer_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, lchip,  0, 0, gport);
    CTC_SAI_LOG_INFO(SAI_API_MONITOR, "create monitor_buffer_id = 0x%"PRIx64"\n", monitor_buffer_oid);
    CTC_SAI_ERROR_GOTO(_ctc_sai_monitor_buffer_build_db(lchip, monitor_buffer_oid, &p_monitor_buffer_info), status, out);

    buffer_monitor_cfg.gport = gport;
        
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MIN_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO (ctc_sai_monitor_mapping_from_byte(lchip, attr_value->u32, &min_threshold), status, out);
        buffer_monitor_cfg.value = min_threshold;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MIN;
        CTC_SAI_CTC_ERROR_GOTO (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg), status, error1);            
        p_monitor_buffer_info->mb_port_thrd_min= attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_MAX_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO (ctc_sai_monitor_mapping_from_byte(lchip, attr_value->u32, &max_threshold), status, out);
        buffer_monitor_cfg.value = max_threshold;
        buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_MAX;
        CTC_SAI_CTC_ERROR_GOTO (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg), status, error1);            
        p_monitor_buffer_info->mb_port_thrd_max=attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if(attr_value->booldata == TRUE )
        {
            buffer_monitor_cfg.value = 1; 
            buffer_monitor_cfg.dir= CTC_INGRESS;
            buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
            CTC_SAI_ERROR_GOTO (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg), status, error1);            
            p_monitor_buffer_info->ingress_port_perio_monitor_enable= attr_value->booldata;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if(attr_value->booldata == TRUE)
        {
            buffer_monitor_cfg.value = 1; 
            buffer_monitor_cfg.dir= CTC_EGRESS;
            buffer_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
            CTC_SAI_ERROR_GOTO (ctcs_monitor_set_config(lchip, &buffer_monitor_cfg), status, error1);            
            p_monitor_buffer_info->egress_port_perio_monitor_enable = attr_value->booldata;
        }
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:can not create SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK!");
        status =  SAI_STATUS_FAILURE;
        goto error1;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:can not create  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK!");
        status =  SAI_STATUS_FAILURE;
        goto error1;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:can not create  SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK!");
        status =  SAI_STATUS_FAILURE;
        goto error1;
    }    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error:can not create  SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK!");
        status =  SAI_STATUS_FAILURE;
        goto error1;
    }  

    *monitor_buffer_id = monitor_buffer_oid;
    status = SAI_STATUS_SUCCESS;
    goto out;
    
error1:
    CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "rollback to error1\n");
    _ctc_sai_monitor_buffer_remove_db(lchip, monitor_buffer_oid);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;

}



sai_status_t
ctc_sai_monitor_remove_monitor_buffer( _In_ sai_object_id_t monitor_buffer_id)
{
    ctc_object_id_t ctc_object_id;
    sai_status_t status = 0;
    ctc_sai_monitor_buffer_db_t* p_monitor_buffer_info = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, monitor_buffer_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Object Type isNot SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    p_monitor_buffer_info = ctc_sai_db_get_object_property(lchip, monitor_buffer_id);    
    if (NULL == p_monitor_buffer_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_monitor_buffer_recover_info(monitor_buffer_id), status, out);
 
    _ctc_sai_monitor_buffer_remove_db(lchip, monitor_buffer_id);
        
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
}



static sai_status_t ctc_sai_monitor_set_monitor_buffer_attribute(sai_object_id_t monitor_buffer_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = monitor_buffer_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(monitor_buffer_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,  SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR,  monitor_buffer_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to set buffer monitor attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_monitor_get_monitor_buffer_attribute( sai_object_id_t  monitor_buffer_id, sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = monitor_buffer_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(monitor_buffer_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, loop, monitor_buffer_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to get buffer monitor attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}


static sai_status_t ctc_sai_monitor_create_monitor_latency( sai_object_id_t *monitor_latency_id,
                         sai_object_id_t        switch_id,
                         uint32_t               attr_count,
                         const sai_attribute_t *attr_list)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 gchip = 0;
    uint32 num = 0;
    uint32 gport_value = 0;
    bool port_check_flag = false;
    ctc_global_panel_ports_t local_panel_ports;
    ctc_monitor_config_t latency_monitor_cfg;
    ctc_monitor_glb_cfg_t latency_monitor_glb_cfg;
    const sai_attribute_value_t *attr_value;
    ctc_sai_monitor_latency_db_t* p_monitor_latency_info = NULL;
    sai_object_id_t monitor_latency_oid = 0;
        ctc_object_id_t ctc_object_id;
    sai_object_key_t key ;
    uint8 index = 0;
    uint32 gport;
    uint32                   attr_index = 0;

    sal_memset(&latency_monitor_cfg, 0, sizeof(latency_monitor_cfg));
    latency_monitor_cfg.monitor_type = CTC_MONITOR_LATENCY;

    sal_memset(&latency_monitor_glb_cfg, 0, sizeof(latency_monitor_glb_cfg));
    latency_monitor_glb_cfg.cfg_type= CTC_MONITOR_GLB_CONFIG_LATENCY_THRD;
    
    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_PTR_VALID_CHECK(monitor_latency_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_value->oid, &ctc_object_id);
        if (ctc_object_id.type != SAI_OBJECT_TYPE_PORT)
        {
            status = SAI_STATUS_INVALID_OBJECT_TYPE;
            CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to create monitor latency, invalid port id:%d\n", status);
            goto out;
        }
        gport = ctc_object_id.value;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "MANDATORY attribute SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT missing !\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }

    sal_memset(&local_panel_ports, 0, sizeof(ctc_global_panel_ports_t));
    ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports);
    ctcs_get_gchip_id(lchip, &gchip);
    for (num = 0; num < local_panel_ports.count; num++)
    {
        gport_value = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
        if(gport == gport_value)
        {
            port_check_flag = true;
            break;
        }
    }

    if (port_check_flag == false) {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "MANDATORY attribute SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT error,no port %d !\n", gport);
        status = SAI_STATUS_INVALID_PORT_NUMBER;
        goto out;
    }

    latency_monitor_cfg.gport = gport;
    
    monitor_latency_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, lchip,  0, 0, gport);
    CTC_SAI_LOG_INFO(SAI_API_MONITOR, "create monitor_latency_id = 0x%"PRIx64"\n", monitor_latency_oid);
    CTC_SAI_ERROR_GOTO(_ctc_sai_monitor_latency_build_db(lchip, monitor_latency_oid, &p_monitor_latency_info), status, out);
    key.key.object_id = monitor_latency_oid;
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_OVER_MAX_THRESHOLD_INFORM_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if(attr_value->booldata == TRUE)
        {
            latency_monitor_cfg.value = 1; 
            latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_INFORM_EN;
            CTC_SAI_ERROR_GOTO (ctcs_monitor_set_config(lchip, &latency_monitor_cfg), status, error1);
            p_monitor_latency_info->latency_mb_enable = attr_value->booldata;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        for(index = 0; index < MB_LEVEL; index++)
        {
            if(attr_value->boollist.list[index] == TRUE)
            {
                latency_monitor_cfg.value = 1;
                latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LOG_EN;
                latency_monitor_cfg.level= index;
                CTC_SAI_ERROR_GOTO (ctcs_monitor_set_config(lchip, &latency_monitor_cfg), status, error1);
                CTC_BIT_SET(p_monitor_latency_info->overthreshold_event_bmp, index);
            }
        }        
    }   
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if(attr_value->booldata == TRUE )
        {
            latency_monitor_cfg.value = 1;
            latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_MON_SCAN_EN;
            CTC_SAI_ERROR_GOTO (ctcs_monitor_set_config(lchip, &latency_monitor_cfg), status, error1);
            p_monitor_latency_info->perio_monitor_enable = attr_value->booldata;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD, &attr_value, &attr_index); 
    if (status == SAI_STATUS_SUCCESS)
    {
        for(index = 0; index < MB_LEVEL; index++)
        {
            if(attr_value->boollist.list[index] == TRUE)
            {
                latency_monitor_cfg.cfg_type = CTC_MONITOR_CONFIG_LANTENCY_DISCARD_THRD_LEVEL;
                latency_monitor_cfg.level= index;
                CTC_SAI_ERROR_GOTO(ctcs_monitor_set_config(lchip, &latency_monitor_cfg), status, error1);
                CTC_BIT_SET(p_monitor_latency_info->discard_bmp, index);
            }
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "error: can not create SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK!");
        status =  SAI_STATUS_FAILURE;
        goto error1;
    }

    *monitor_latency_id = monitor_latency_oid;
    status = SAI_STATUS_SUCCESS;
    goto out;
    
error1:
    CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "rollback to error1\n");
    _ctc_sai_monitor_latency_remove_db(lchip, monitor_latency_oid);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;

}



sai_status_t
ctc_sai_monitor_remove_monitor_latency( _In_ sai_object_id_t monitor_latency_id)
{
    ctc_object_id_t ctc_object_id;
    sai_status_t status = 0;
    ctc_sai_monitor_latency_db_t* p_monitor_latency_info = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, monitor_latency_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Object Type isNot SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    p_monitor_latency_info = ctc_sai_db_get_object_property(lchip, monitor_latency_id);    
    if (NULL == p_monitor_latency_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_monitor_buffer_recover_info(monitor_latency_id), status, out);
 
    _ctc_sai_monitor_latency_remove_db(lchip, monitor_latency_id);
        
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
}



static sai_status_t ctc_sai_monitor_set_monitor_latency_attribute(sai_object_id_t monitor_latency_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = monitor_latency_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(monitor_latency_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,  SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR,  monitor_latency_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to set latency monitor attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}

static sai_status_t ctc_sai_monitor_get_monitor_latency_attribute( sai_object_id_t  monitor_latency_id, sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = monitor_latency_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MONITOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(monitor_latency_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, loop, monitor_latency_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MONITOR, "Failed to get latency monitor attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}



const sai_monitor_api_t g_ctc_sai_monitor_api = {
    
        ctc_sai_monitor_create_monitor_buffer,
        ctc_sai_monitor_remove_monitor_buffer,
        ctc_sai_monitor_set_monitor_buffer_attribute,
        ctc_sai_monitor_get_monitor_buffer_attribute,
        
        ctc_sai_monitor_create_monitor_latency,
        ctc_sai_monitor_remove_monitor_latency,
        ctc_sai_monitor_set_monitor_latency_attribute,
        ctc_sai_monitor_get_monitor_latency_attribute
};

sai_status_t
ctc_sai_monitor_api_init()
{
    ctc_sai_register_module_api(SAI_API_MONITOR, (void*)&g_ctc_sai_monitor_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_monitor_buffer_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_MONITOR;
    wb_info.data_len = sizeof(ctc_sai_monitor_buffer_db_t);
    wb_info.wb_sync_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_MONITOR_BUFFER_MONITOR, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_monitor_latency_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_MONITOR;
    wb_info.data_len = sizeof(ctc_sai_monitor_latency_db_t);
    wb_info.wb_sync_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_MONITOR_LATENCY_MONITOR, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

