
/*ctc_sai include file*/
#include "ctc_sai_ptp.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_port.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

/*sdk include file*/
#include "ctcs_api.h"



sai_status_t _ctc_sai_ptp_mapping_ctc_time_offset(sai_timeoffset_t timeoffset, ctc_ptp_time_t* offset_out )
{
    offset_out->is_negative = timeoffset.flag;
    offset_out->nanoseconds = timeoffset.value;
    offset_out->nano_nanoseconds = 0;
    offset_out->seconds = 0;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ptp_build_db(uint8 lchip, sai_object_id_t ptp_domain_id, ctc_sai_ptp_db_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_ptp_db_t* p_ptp_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    p_ptp_info = mem_malloc(MEM_PTP_MODULE, sizeof(ctc_sai_ptp_db_t));
    if (NULL == p_ptp_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_ptp_info, 0, sizeof(ctc_sai_ptp_db_t));
    status = ctc_sai_db_add_object_property(lchip, ptp_domain_id, (void*)p_ptp_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_ptp_info);
        return status;
    }

    *oid_property = p_ptp_info;

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_ptp_remove_db(uint8 lchip, sai_object_id_t ptp_domain_id)
{
    ctc_sai_ptp_db_t* p_ptp_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    p_ptp_info = ctc_sai_db_get_object_property(lchip, ptp_domain_id);
    if (NULL == p_ptp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, ptp_domain_id);
    mem_free(p_ptp_info);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_ptp_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t ptp_domain_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ptp_domain_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_PTP, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ptp_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             ptp_domain_id  = bucket_data->oid;
    ctc_sai_ptp_db_t*       p_db        = (ctc_sai_ptp_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump      = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file      = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt         = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (ptp_domain_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-6d %-6d %-4d %-4d drift_offset flag%-4d value%-12d time_offset flag%-4d  value%-12d %-4d %-4d %-4d %-4d %-4d %-4d\n",
                            *cnt,ptp_domain_id,p_db->enable_type,p_db->device_type,p_db->is_drift_offset,p_db->is_time_offset,
                            p_db->drift_offset.flag,p_db->drift_offset.value,
                            p_db->time_offset.flag,p_db->time_offset.value,
                            p_db->tod_format,p_db->tod_enable,p_db->tod_mode,
                            p_db->leap_second,p_db->pps_status,p_db->pps_accuracy);

    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


#define ________INTERNAL_API________

sai_status_t
ctc_sai_ptp_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{

    uint8 lchip = 0;
    ctc_ptp_time_t ptp_clock_offset;
    sai_object_id_t ptp_domain_id= 0;
    uint32 sync_tod_select = 0;
    ctc_ptp_tod_intf_cfg_t tod_interface_cfg;    
    ctc_ptp_tod_intf_code_t  tod_interface_code ;   
    ctc_sai_ptp_db_t* p_ptp_db = NULL;

    sal_memset(&ptp_clock_offset, 0, sizeof(ptp_clock_offset));
    sal_memset(&tod_interface_cfg, 0, sizeof(tod_interface_cfg));
    sal_memset(&tod_interface_code, 0, sizeof(tod_interface_code));
    tod_interface_cfg.mode = 2;/*disable*/
    /*bug 110353,if the mode ==2, it means the tod intf is disable, don't need config the duty and other fields*/
    tod_interface_cfg.pulse_duty = 10;
    tod_interface_cfg.epoch= 1074;/*3ms*/
    tod_interface_code.msg_class = 0x01;
    tod_interface_code.msg_id= 0x20;
    tod_interface_code.msg_length = 16;


    ptp_domain_id = key->key.object_id;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_ptp_db = ctc_sai_db_get_object_property(lchip, ptp_domain_id);
    
    if (NULL == p_ptp_db)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    switch(attr->id)
    {
    case SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
       CTC_SAI_LOG_ERROR(SAI_API_PTP, "NOTE:NOT SUPPORT SET!");
        break;

    case SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "NOTE:NOT SUPPORT SET!");
        break;
        
    case SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
        CTC_SAI_ERROR_RETURN(_ctc_sai_ptp_mapping_ctc_time_offset(attr->value.timeoffset, &ptp_clock_offset));
        CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_clock_drift(lchip, &ptp_clock_offset));
        p_ptp_db->is_drift_offset = true;
        sal_memcpy(&(p_ptp_db->drift_offset), &(attr->value.timeoffset), sizeof(sai_timeoffset_t));
        break;

    case SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
        CTC_SAI_ERROR_RETURN(_ctc_sai_ptp_mapping_ctc_time_offset(attr->value.timeoffset, &ptp_clock_offset));
        CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_adjust_clock_offset(lchip, &ptp_clock_offset));
        p_ptp_db->is_time_offset = true;
        sal_memcpy(&(p_ptp_db->time_offset), &(attr->value.timeoffset), sizeof(sai_timeoffset_t));
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE:
        if (attr->value.s32 != SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375)
        {
            CTC_SAI_LOG_INFO(SAI_API_PTP, "Failed to set tod interface format, invalid tod_interface_format %d!\n", attr->value.s32);
            p_ptp_db->tod_format = SAI_PTP_TOD_INTERFACE_FORMAT_USER_DEFINE;
            return SAI_STATUS_FAILURE;
        }
        p_ptp_db->tod_format = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375;
        break;


    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
        if(p_ptp_db->tod_enable && (p_ptp_db->tod_mode !=TOD_INTF_DISABLE))
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "NOTE:PLEASE CLOSE THE SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE FIRST!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            p_ptp_db->leap_second = attr->value.s8;
            tod_interface_code.leap_second = p_ptp_db->leap_second;
            tod_interface_code.pps_status = p_ptp_db->pps_status;
            tod_interface_code.pps_accuracy = p_ptp_db->pps_accuracy;
            CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_tod_intf_tx_code(lchip, &tod_interface_code));
            
        }
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
        if(p_ptp_db->tod_enable && (p_ptp_db->tod_mode !=TOD_INTF_DISABLE))
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "NOTE:PLEASE CLOSE THE SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE FIRST!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            p_ptp_db->pps_status = attr->value.u8;
            tod_interface_code.leap_second = p_ptp_db->leap_second;
            tod_interface_code.pps_status = p_ptp_db->pps_status;
            tod_interface_code.pps_accuracy = p_ptp_db->pps_accuracy;
            CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_tod_intf_tx_code(lchip, &tod_interface_code));
        }        
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
        if(p_ptp_db->tod_enable &&  (p_ptp_db->tod_mode !=TOD_INTF_DISABLE))
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "NOTE:PLEASE CLOSE THE SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE FIRST!");
            return SAI_STATUS_FAILURE;
        }
        else
        {
            p_ptp_db->pps_accuracy = attr->value.u8;
            tod_interface_code.leap_second = p_ptp_db->leap_second;
            tod_interface_code.pps_status = p_ptp_db->pps_status;
            tod_interface_code.pps_accuracy = p_ptp_db->pps_accuracy;
            CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_tod_intf_tx_code(lchip, &tod_interface_code));
        }        
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK!");
        return SAI_STATUS_FAILURE;
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK!");
        return SAI_STATUS_FAILURE;
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
        tod_interface_cfg.mode = (uint8)attr->value.s32;
        CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_tod_intf(lchip, &tod_interface_cfg));
        p_ptp_db->tod_mode = attr->value.s32;
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
        if(attr->value.booldata)
        {
            sync_tod_select = CTC_PTP_INTF_SELECT_TOD;
        }
        else
        {
            sync_tod_select = CTC_PTP_INTF_SELECT_NONE;
        }
        CTC_SAI_CTC_ERROR_RETURN (ctcs_ptp_set_global_property(lchip, CTC_PTP_GLOBAL_PROP_SYNC_OR_TOD_INPUT_SELECT, sync_tod_select));
        p_ptp_db->tod_enable = attr->value.booldata;
        break;

    case SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP!");
        return SAI_STATUS_FAILURE;
        break;

    case SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP!");
        return SAI_STATUS_FAILURE;
        break;    

    }

    return  SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_ptp_get_info(sai_object_key_t * key, sai_attribute_t * attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_ptp_db_t* p_ptp_db = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_ptp_time_t ts;
    ctc_ptp_capured_ts_t capured_ts;
    uint32 enable_basedon_port;
    ctc_ptp_device_type_t device_type;
    ctc_ptp_tod_intf_code_t  tod_interface_code;
    
    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_ptp_db = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_ptp_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
    case SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
        ret = ctcs_ptp_get_global_property(lchip, CTC_PTP_GLOBAL_PROP_PORT_BASED_PTP_EN, &enable_basedon_port);
        if(enable_basedon_port)
            {
                attr->value.s32 = SAI_PTP_ENABLE_BASED_ON_PORT;
            }
        else
            {
                attr->value.s32 = SAI_PTP_ENABLE_BASED_ON_VLAN;
            }
        break;

    case SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
        ret = ctcs_ptp_get_device_type(lchip, &device_type);
        attr->value.s32 = device_type;
        break;

    case SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
        sal_memcpy(&(attr->value.timeoffset), &(p_ptp_db->drift_offset), sizeof(sai_timeoffset_t));
        break;
        
    case SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
        sal_memcpy(&(attr->value.timeoffset), &(p_ptp_db->time_offset), sizeof(sai_timeoffset_t));
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE:
        attr->value.s32 = p_ptp_db->tod_format;
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
        attr->value.booldata= p_ptp_db->tod_enable;
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
        attr->value.s32 = (int32)p_ptp_db->tod_mode;
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
        if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_INPUT)
        {
            ret = ctcs_ptp_get_tod_intf_rx_code(lchip, &tod_interface_code);
            attr->value.s8 = tod_interface_code.leap_second;            
        }
        else if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_OUTPUT)
        {
            attr->value.s8 = p_ptp_db->leap_second; 
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "The tod interface is not enable!\n")
        }
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
        if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_INPUT)
        {
            ret = ctcs_ptp_get_tod_intf_rx_code(lchip, &tod_interface_code);
            attr->value.u8 = tod_interface_code.pps_status;       
        }
        else if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_OUTPUT)
        {
            attr->value.u8 = p_ptp_db->pps_status;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "The tod interface is not enable!\n")
        }
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
        if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_INPUT)
        {
            ret = ctcs_ptp_get_tod_intf_rx_code(lchip, &tod_interface_code);
            attr->value.u8 = tod_interface_code.pps_accuracy;       
        }
        else if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_OUTPUT)
        {
            attr->value.u8 = p_ptp_db->pps_accuracy;
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "The tod interface is not enable!\n")
        }
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK:
        if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_INPUT)
        {
            ret = ctcs_ptp_get_tod_intf_rx_code(lchip, &tod_interface_code);
            attr->value.u16 = tod_interface_code.gps_week;   
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK only support input mode!\n")
        }
        break;

    case SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK:
        if(p_ptp_db->tod_mode == SAI_PTP_TOD_INTERFACE_INPUT)
        {
            ret = ctcs_ptp_get_tod_intf_rx_code(lchip, &tod_interface_code);
            attr->value.u32 = tod_interface_code.gps_second_time_of_week; 
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_PTP, "SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK only support input mode!\n")
        }
        break;
        
    case SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP:
        ret = ctcs_ptp_get_clock_timestamp(lchip, &ts);
        attr->value.timespec.tv_nsec = ts.nanoseconds;
        attr->value.timespec.tv_sec = ts.seconds;
        break;

    case SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP:
        ret = ctcs_ptp_get_captured_ts(lchip, &capured_ts);
        attr->value.captured_timespec.port_id = capured_ts.u.lport;
        attr->value.captured_timespec.secquence_id = capured_ts.seq_id;
        attr->value.captured_timespec.timestamp.tv_nsec= capured_ts.ts.nanoseconds;
        attr->value.captured_timespec.timestamp.tv_sec= capured_ts.ts.seconds;
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "Get ptp attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;

    }
    
    return status;
}

static  ctc_sai_attr_fn_entry_t ptp_attr_fn_entries[] = 
{
    { SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY,
      ctc_sai_ptp_get_info,
      ctc_sai_ptp_set_info},
      { SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP,
      ctc_sai_ptp_get_info,
      NULL},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK,
      ctc_sai_ptp_get_info,
      NULL},
      { SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK,
      ctc_sai_ptp_get_info,
      NULL},
      { SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP,
      ctc_sai_ptp_get_info,
      NULL},      
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL},

 };

#define ________SAI_DUMP________

void
ctc_sai_ptp_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI PTP MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_PTP_DOMAIN))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "PTP");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_ptp_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-12s %-18s %-18s %-18s %-18s %-18s %-18s %-18s %-18s %-18s %-18s\n",\
            "No.","PTP_Domain_Oid","enable_Type","device_type","is_drift_offset","is_time_offset","drift_offset","time_offset",\
            "tod_format","tod_enable","tod_mode","leap_second","pps_status","pps_accuracy");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_PTP_DOMAIN,
                                                (hash_traversal_fn)_ctc_sai_ptp_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}

#define ________SAI_API________

static sai_status_t ctc_sai_ptp_create_ptp_domain( sai_object_id_t *ptp_domain_id,
                         sai_object_id_t        switch_id,
                         uint32_t               attr_count,
                         const sai_attribute_t *attr_list)

{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 count = 0;
    const sai_attribute_value_t *attr_value;
    ctc_sai_ptp_db_t* p_ptp_info = NULL;
    ctc_ptp_tod_intf_code_t  tod_interface_code;
    sai_object_id_t ptp_domain_oid = 0;
    sai_object_key_t key ;
    uint32                   attr_index = 0;
    uint32  sai_ptp_domain_id = 0;
    uint32 enable_basedon_port;

    sal_memset(&tod_interface_code, 0, sizeof(tod_interface_code));
    tod_interface_code.msg_class = 0x01;
    tod_interface_code.msg_id= 0x20;
    tod_interface_code.msg_length = 16;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    CTC_SAI_PTR_VALID_CHECK(ptp_domain_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_get_object_property_count(lchip, SAI_OBJECT_TYPE_PTP_DOMAIN, &count), status, out);
    if(count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:ONE PTP DOMAIN HAS BEEN CREATED!ONLY SUPPORT ONE PTP DOMAIN!");
        status =  SAI_STATUS_FAILURE;
        goto out;
    }    
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_PTP, &sai_ptp_domain_id), status, out);
   
    ptp_domain_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, lchip, 0, 0, sai_ptp_domain_id);
    CTC_SAI_LOG_INFO(SAI_API_PTP, "create ptp_domain_id = 0x%"PRIx64"\n", ptp_domain_oid);
    CTC_SAI_ERROR_GOTO(_ctc_sai_ptp_build_db(lchip, ptp_domain_oid, &p_ptp_info), status, error1);

    key.key.object_id = ptp_domain_oid;
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (attr_value->s32 == SAI_PTP_ENABLE_BASED_ON_PORT)
            {
                enable_basedon_port = 1;
            }
            else
            {
                enable_basedon_port = 0;
            }
        CTC_SAI_ERROR_GOTO (ctcs_ptp_set_global_property(lchip, CTC_PTP_GLOBAL_PROP_PORT_BASED_PTP_EN, enable_basedon_port), status, error2);
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto error2;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO (ctcs_ptp_set_device_type(lchip,attr_value->s32), status, error2);
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto error2;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_ptp_set_info(&key, &attr_list[attr_index]), status, error2);
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_ptp_set_info(&key, &attr_list[attr_index]), status, error2);
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_ptp_set_info(&key, &attr_list[attr_index]), status, error2);
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    CTC_SAI_ERROR_GOTO (ctcs_ptp_get_tod_intf_tx_code(lchip, &tod_interface_code), status, error2);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        tod_interface_code.leap_second = attr_value->s8;
        p_ptp_info->leap_second = attr_value->s8;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        tod_interface_code.pps_status = attr_value->u8;
        p_ptp_info->pps_status = attr_value->u8;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        tod_interface_code.pps_accuracy= attr_value->u8;
        p_ptp_info->pps_accuracy = attr_value->u8;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    CTC_SAI_ERROR_GOTO (ctcs_ptp_set_tod_intf_tx_code(lchip, &tod_interface_code), status, error2);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_WEEK!");
        status =  SAI_STATUS_FAILURE;
        goto error2;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TOD_INTF_GPS_SECOND_OF_WEEK!");
        status =  SAI_STATUS_FAILURE;
        goto error2;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_ptp_set_info(&key, &attr_list[attr_index]), status, error2);
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_ptp_set_info(&key, &attr_list[attr_index]), status, error2);
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP!");
        status = SAI_STATUS_FAILURE;
        goto error2;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "error:CAN NOT SET SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP!");
        status =  SAI_STATUS_FAILURE;
        goto error2;
    }
    else
    {
        status = SAI_STATUS_SUCCESS;
    }

    *ptp_domain_id = ptp_domain_oid;

    goto out;
    
error2:
    CTC_SAI_LOG_ERROR(SAI_API_PTP, "rollback to error2\n");
    _ctc_sai_ptp_remove_db(lchip, ptp_domain_oid);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_PTP, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_PTP, sai_ptp_domain_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;

}



sai_status_t
ctc_sai_ptp_remove_ptp_domain( _In_ sai_object_id_t ptp_domain_id)
{
    ctc_object_id_t ctc_object_id;
    sai_status_t status = 0;
    ctc_sai_ptp_db_t* p_ptp_db = NULL;
    uint32 ptp_id = 0;
    uint8 lchip = 0;
    ctc_ptp_tod_intf_cfg_t tod_interface_cfg;
    ctc_ptp_time_t ptp_clock_offset;

    sal_memset(&ptp_clock_offset, 0, sizeof(ptp_clock_offset));
    sal_memset(&tod_interface_cfg, 0, sizeof(tod_interface_cfg));
    tod_interface_cfg.mode = 2;
    /*bug 110353,if the mode ==2, it means the tod intf is disable, don't need config the duty and other fields*/
    tod_interface_cfg.pulse_duty = 10;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ptp_domain_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_PTP_DOMAIN)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "Object Type isNot SAI_OBJECT_TYPE_PTP_DOMAIN!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    p_ptp_db = ctc_sai_db_get_object_property(lchip, ptp_domain_id);    
    if (NULL == p_ptp_db)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_set_global_property(lchip, CTC_PTP_GLOBAL_PROP_PORT_BASED_PTP_EN, 0), status, out);
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_set_global_property(lchip, CTC_PTP_GLOBAL_PROP_SYNC_OR_TOD_INPUT_SELECT, CTC_PTP_INTF_SELECT_NONE), status, out);
    /*bugid 110350,CTC_PTP_DEVICE_NONE means that the device processing the message as normal packet*/
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_set_device_type(lchip,CTC_PTP_DEVICE_NONE), status, out);
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_set_tod_intf(lchip, &tod_interface_cfg), status, out);
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_set_clock_drift(lchip, &ptp_clock_offset), status, out);
    CTC_SAI_CTC_ERROR_GOTO (ctcs_ptp_adjust_clock_offset(lchip, &ptp_clock_offset), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_ptp_clear_tod_intf_code(lchip), status, out);

    ctc_sai_oid_get_value(ptp_domain_id, &ptp_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_PTP, ptp_id);    
    _ctc_sai_ptp_remove_db(lchip, ptp_domain_id);
        
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
}



static sai_status_t ctc_sai_ptp_set_ptp_domain_attribute(sai_object_id_t ptp_domain_id, const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = ptp_domain_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ptp_domain_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_PTP_DOMAIN,  ptp_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "Failed to set ptp attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}



static sai_status_t ctc_sai_ptp_get_ptp_domain_attribute( sai_object_id_t  ptp_domain_id, sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = ptp_domain_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_PTP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ptp_domain_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_PTP_DOMAIN, loop, ptp_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_PTP, "Failed to get ptp attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}


const sai_ptp_api_t g_ctc_sai_ptp_api = {
    ctc_sai_ptp_create_ptp_domain,
    ctc_sai_ptp_remove_ptp_domain,
    ctc_sai_ptp_set_ptp_domain_attribute,
    ctc_sai_ptp_get_ptp_domain_attribute
};


sai_status_t
ctc_sai_ptp_api_init()
{
    ctc_sai_register_module_api(SAI_API_PTP, (void*)&g_ctc_sai_ptp_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_ptp_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_PTP;
    wb_info.data_len = sizeof(ctc_sai_ptp_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_ptp_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_PTP_DOMAIN, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

