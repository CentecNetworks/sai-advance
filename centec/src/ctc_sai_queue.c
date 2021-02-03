
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_wred.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_port.h"


sai_status_t
_ctc_sai_queue_get_queue_db(sai_object_id_t queue_id, ctc_sai_queue_db_t** p_queue)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_queue_db_t* p_queue_temp = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    if (ctc_oid.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Invalid Queue oid type!\n");
        return SAI_STATUS_INVALID_OBJECT_TYPE;
    }
    lchip = ctc_oid.lchip;

    p_queue_temp = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_temp)
    {
        p_queue_temp = (ctc_sai_queue_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_queue_db_t));
        if (NULL == p_queue_temp)
        {
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "No memory!\n");
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_queue_temp, 0, sizeof(ctc_sai_queue_db_t));
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, queue_id, p_queue_temp), status, error_return);
    }
    *p_queue = p_queue_temp;
    return SAI_STATUS_SUCCESS;

error_return:
    mem_free(p_queue_temp);
    return status;
}

static sai_status_t
_ctc_sai_queue_set_fcdl_detect(sai_object_id_t queue_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint32 gport = 0;
    uint16  ctc_queue_id = 0;
    ctc_object_id_t ctc_oid;
    ctc_qos_resrc_t ctc_resrc;
    ctc_sai_switch_master_t* p_switch = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_INFO(SAI_API_QUEUE, "Queue oid:0x%"PRIx64"\n", queue_id);
    sal_memset(&ctc_resrc, 0, sizeof(ctc_resrc));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    if ((SAI_QUEUE_TYPE_MULTICAST == ctc_oid.sub_type) || (SAI_QUEUE_TYPE_SERVICE == ctc_oid.sub_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Not Supported Mcast or Service queue type!\n");
        return SAI_STATUS_NOT_SUPPORTED;
    }
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    ctc_queue_id = ctc_oid.value2 & 0x3f;

    p_switch = ctc_sai_get_switch_property(lchip);

    ctc_resrc.cfg_type = CTC_QOS_RESRC_CFG_FCDL_DETECT;
    ctc_resrc.u.fcdl_detect.gport = gport;
    ctc_resrc.u.fcdl_detect.priority_class[0] = ctc_queue_id;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_resrc(lchip, &ctc_resrc));

    if(attr->value.booldata)  //enable
    {

    /* old logic
        if(ctc_resrc.u.fcdl_detect.enable)
        {
            if(CTC_MAX_FCDL_DETECT_NUM == ctc_resrc.u.fcdl_detect.valid_num)
            {
                if((ctc_resrc.u.fcdl_detect.priority_class[0] == ctc_queue_id)
                    || (ctc_resrc.u.fcdl_detect.priority_class[1] == ctc_queue_id))
                {
                    ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
                }
                else
                {
                    return SAI_STATUS_INSUFFICIENT_RESOURCES;
                }
            }
            else if(1 == ctc_resrc.u.fcdl_detect.valid_num)
            {
                if(ctc_resrc.u.fcdl_detect.priority_class[0] == ctc_queue_id)
                {
                    ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
                }
                else
                {
                    ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
                    ctc_resrc.u.fcdl_detect.priority_class[1] = ctc_queue_id;
                    ctc_resrc.u.fcdl_detect.valid_num = 2;
                }
            }
        }
        else
        {
            ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
            ctc_resrc.u.fcdl_detect.priority_class[0] = ctc_queue_id;
            ctc_resrc.u.fcdl_detect.valid_num = 1;
            ctc_resrc.u.fcdl_detect.enable = 1;
        }
    
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
    */
        if(ctc_resrc.u.fcdl_detect.enable)
        {
            return SAI_STATUS_SUCCESS;
        }
        else if(!ctc_resrc.u.fcdl_detect.enable && (CTC_MAX_FCDL_DETECT_NUM == ctc_resrc.u.fcdl_detect.valid_num))
        {
            return SAI_STATUS_INSUFFICIENT_RESOURCES;
        }
        
        ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
        ctc_resrc.u.fcdl_detect.priority_class[0] = ctc_queue_id;
        ctc_resrc.u.fcdl_detect.valid_num = 1;
        ctc_resrc.u.fcdl_detect.enable = 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
    }
    else  //disable
    {
        /* old logic
        if(ctc_resrc.u.fcdl_detect.enable)
        {
            if(CTC_MAX_FCDL_DETECT_NUM == ctc_resrc.u.fcdl_detect.valid_num)
            {
                if(ctc_resrc.u.fcdl_detect.priority_class[1] == ctc_queue_id)
                {
                    //disable all
                    ctc_resrc.u.fcdl_detect.enable = 0;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));

                    //enable one queue
                    ctc_resrc.u.fcdl_detect.enable = 1;
                    ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_resrc.u.fcdl_detect.priority_class[0]];
                    ctc_resrc.u.fcdl_detect.priority_class[1] = 0;
                    ctc_resrc.u.fcdl_detect.valid_num = 1;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
                }
                else if(ctc_resrc.u.fcdl_detect.priority_class[0] == ctc_queue_id)
                {
                    //disable all
                    ctc_resrc.u.fcdl_detect.enable = 0;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));

                    //enable one queue
                    ctc_resrc.u.fcdl_detect.enable = 1;
                    ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_resrc.u.fcdl_detect.priority_class[1]];
                    ctc_resrc.u.fcdl_detect.priority_class[0] = ctc_resrc.u.fcdl_detect.priority_class[1];
                    ctc_resrc.u.fcdl_detect.valid_num = 1;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
                }
                else
                {
                    return SAI_STATUS_SUCCESS;
                }

            }
            else if(1 == ctc_resrc.u.fcdl_detect.valid_num)
            {
                if(ctc_resrc.u.fcdl_detect.priority_class[0] == ctc_queue_id)
                {
                    ctc_resrc.u.fcdl_detect.enable = 0;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
                }
                else
                {
                    return SAI_STATUS_SUCCESS;
                }
            }
        }
        else
        {
            return SAI_STATUS_SUCCESS;
        }
        */

        if(!ctc_resrc.u.fcdl_detect.enable)
        {
            return SAI_STATUS_SUCCESS;
        }
        
        ctc_resrc.u.fcdl_detect.detect_mult = p_switch->pfc_dld_interval[ctc_queue_id];
        ctc_resrc.u.fcdl_detect.priority_class[0] = ctc_queue_id;
        ctc_resrc.u.fcdl_detect.valid_num = 1;
        ctc_resrc.u.fcdl_detect.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &ctc_resrc));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_queue_traverse_set_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_queue_traverse_param_t* user_data)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_queue_db_t* p_queue_db = bucket_data->data;
    uint8 lchip = 0;
    ctc_qos_drop_t  ctc_drop;
    ctc_qos_drop_t*  p_set_ctc_drop = NULL;
    ctc_sai_switch_master_t* p_switch = NULL;
    uint32 idx = 0;

    lchip = user_data->lchip;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, bucket_data->oid, &ctc_oid);
    if (lchip != ctc_oid.lchip)
    {
        return SAI_STATUS_SUCCESS;
    }

    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Switch DB not found!\n");
        return SAI_STATUS_FAILURE;
    }
    //sal_memcpy(&ctc_drop, user_data->p_value, sizeof(ctc_qos_drop_t));
    ctc_drop.queue.gport = ctc_oid.value;

    if ((ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
        && (p_switch->port_queues == 16))
    {
        ctc_drop.queue.queue_id = ctc_oid.value2 + CTC_QOS_BASIC_Q_NUM;
        ctc_drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }
    else if (ctc_oid.sub_type == SAI_QUEUE_TYPE_SERVICE)
    {
        ctc_drop.queue.queue_id = ctc_oid.value2 & 0x3F;
        ctc_drop.queue.service_id = (ctc_oid.value2 >> 6);
        ctc_drop.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
    }
    else
    {
        ctc_drop.queue.queue_id = ctc_oid.value2;
        ctc_drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }

    switch (user_data->set_type)
    {
        case CTC_SAI_Q_SET_TYPE_WRED:
            if (*user_data->cmp_value != p_queue_db->wred_id)
            {
                return SAI_STATUS_SUCCESS;
            }

            p_set_ctc_drop = (ctc_qos_drop_t*)user_data->p_value;
            ctc_drop.drop.mode = p_set_ctc_drop->drop.mode;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_drop_scheme(lchip, &ctc_drop));

            ctc_drop.drop.is_coexist = p_set_ctc_drop->drop.is_coexist;
            for(idx = 0; idx < CTC_DROP_PREC_NUM-1; idx++)
            {
                ctc_drop.drop.drop_prob[idx] = p_set_ctc_drop->drop.drop_prob[idx];
                ctc_drop.drop.min_th[idx] = p_set_ctc_drop->drop.min_th[idx];
                ctc_drop.drop.max_th[idx] = p_set_ctc_drop->drop.max_th[idx];
            }

            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &ctc_drop));

            break;

        case CTC_SAI_Q_SET_TYPE_WRED_ECN:
            if (*user_data->cmp_value != p_queue_db->wred_id)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_set_ctc_drop = (ctc_qos_drop_t*)user_data->p_value;
            ctc_drop.drop.mode = p_set_ctc_drop->drop.mode;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_drop_scheme(lchip, &ctc_drop));

            ctc_drop.drop.is_coexist = p_set_ctc_drop->drop.is_coexist;
            for(idx = 0; idx < CTC_DROP_PREC_NUM-1; idx++)
            {
                ctc_drop.drop.ecn_th[idx] = p_set_ctc_drop->drop.ecn_th[idx];
            }

            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &ctc_drop));

            break;

        case CTC_SAI_Q_SET_TYPE_BUFFER:
            if ((user_data->set_type == CTC_SAI_Q_SET_TYPE_BUFFER) && (*user_data->cmp_value != p_queue_db->buf_id))
            {
                return SAI_STATUS_SUCCESS;
            }

            p_set_ctc_drop = (ctc_qos_drop_t*)user_data->p_value;
            ctc_drop.drop.mode = p_set_ctc_drop->drop.mode;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_drop_scheme(lchip, &ctc_drop));

            ctc_drop.drop.is_coexist = p_set_ctc_drop->drop.is_coexist;
            ctc_drop.drop.is_dynamic = p_set_ctc_drop->drop.is_dynamic;
            for(idx = 0; idx < CTC_DROP_PREC_NUM; idx++)
            {
                ctc_drop.drop.max_th[idx] = p_set_ctc_drop->drop.max_th[idx];
                ctc_drop.drop.drop_factor[idx] = p_set_ctc_drop->drop.drop_factor[idx];
            }

            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &ctc_drop));

            break;
        case CTC_SAI_Q_SET_TYPE_DLD:
        {
            sai_attribute_t attr;

            sal_memset(&attr, 0, sizeof(attr));

            if(p_queue_db->pfc_dld_en)
            {
                attr.id = SAI_QUEUE_ATTR_ENABLE_PFC_DLDR;
                attr.value.booldata = TRUE;
                CTC_SAI_ERROR_RETURN(_ctc_sai_queue_set_fcdl_detect(bucket_data->oid, &attr));
            }
            break;

        }
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}



static sai_status_t
_ctc_sai_queue_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_oid;
    sai_object_id_t queue_id = key->key.object_id;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;

    switch (attr->id)
    {
        case SAI_QUEUE_ATTR_TYPE:
            attr->value.u32 = ctc_oid.sub_type;
            break;
        case SAI_QUEUE_ATTR_PORT:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, ctc_oid.value);
            break;
        case SAI_QUEUE_ATTR_INDEX:
            attr->value.u32 = ctc_oid.value2 & 0x3F;
            break;
        case SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
            if (NULL == p_queue_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            attr->value.oid = p_queue_db->sch_grp ? p_queue_db->sch_grp : SAI_NULL_OBJECT_ID;
            break;
        case SAI_QUEUE_ATTR_WRED_PROFILE_ID:
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
            if (NULL == p_queue_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            attr->value.oid = p_queue_db->wred_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_WRED, lchip, 0, 0, p_queue_db->wred_id) : SAI_NULL_OBJECT_ID;
            break;
        case SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
            if (NULL == p_queue_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            attr->value.oid = p_queue_db->buf_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, lchip, 0, 0, p_queue_db->buf_id) : SAI_NULL_OBJECT_ID;
            break;
        case SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
            if (NULL == p_queue_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            attr->value.oid = p_queue_db->sch_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_queue_db->sch_id) : SAI_NULL_OBJECT_ID;
            break;
        case SAI_QUEUE_ATTR_SERVICE_ID:
            attr->value.u16 = (ctc_oid.value2 >> 6);
            break;
        case SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
            if (NULL == p_queue_db)
            {
                return SAI_STATUS_SUCCESS;
            }
            attr->value.booldata = p_queue_db->pfc_dld_en;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "queue attribute not implement\n");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_queue_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    ctc_object_id_t ctc_oid;
    sai_object_id_t queue_id = key->key.object_id;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    uint8 lchip = 0;
    bool enable = FALSE;
    bool is_update = FALSE;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(queue_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_queue_get_queue_db(queue_id, &p_queue_db));

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        enable = TRUE;
    }

    switch (attr->id)
    {
        case SAI_QUEUE_ATTR_WRED_PROFILE_ID:
            if (enable)
            {
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_WRED, attr->value.oid, &ctc_oid);
                if (lchip != ctc_oid.lchip)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "queue attribute error, lchip invalid:%d\n", ctc_oid.lchip);
                    return SAI_STATUS_INVALID_PARAMETER;
                }
            }
            if (p_queue_db->wred_id && (ctc_oid.value != p_queue_db->wred_id))
            {
                is_update = TRUE;
            }

            CTC_SAI_ERROR_RETURN(ctc_sai_wred_queue_set_wred(queue_id,
                                                        enable ? ctc_oid.value : p_queue_db->wred_id,
                                                        is_update ? p_queue_db->wred_id : 0,
                                                        enable));
            p_queue_db->wred_id = enable ? ctc_oid.value : 0;
            break;
        case SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
            CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_group_queue_set_scheduler(queue_id, attr));
            break;
        case SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_buffer_queue_set_profile(queue_id, attr));
            break;
        case SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_queue_set_scheduler(queue_id, attr));
            break;
        case SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
            CTC_SAI_ERROR_RETURN(_ctc_sai_queue_set_fcdl_detect(queue_id, attr));
            p_queue_db->pfc_dld_en = attr->value.booldata;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "queue attribute not implement\n");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}


static ctc_sai_attr_fn_entry_t  queue_attr_fn_entries[] =
{
        {SAI_QUEUE_ATTR_TYPE, _ctc_sai_queue_get_attr, NULL},
        {SAI_QUEUE_ATTR_PORT, _ctc_sai_queue_get_attr, NULL},
        {SAI_QUEUE_ATTR_INDEX, _ctc_sai_queue_get_attr, NULL},
        {SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, _ctc_sai_queue_get_attr, _ctc_sai_queue_set_attr},
        {SAI_QUEUE_ATTR_WRED_PROFILE_ID, _ctc_sai_queue_get_attr, _ctc_sai_queue_set_attr},
        {SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, _ctc_sai_queue_get_attr, _ctc_sai_queue_set_attr},
        {SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, _ctc_sai_queue_get_attr, _ctc_sai_queue_set_attr},
        {SAI_QUEUE_ATTR_PAUSE_STATUS, NULL, NULL},
        {SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, _ctc_sai_queue_get_attr, _ctc_sai_queue_set_attr},
        {SAI_QUEUE_ATTR_SERVICE_ID, _ctc_sai_queue_get_attr, NULL},
        { CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL }
};

static sai_status_t
_ctc_sai_queue_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_object_id_t             ctc_oid;
    sai_object_id_t             queue_id = bucket_data->oid;
    ctc_sai_queue_db_t*         p_db     = (ctc_sai_queue_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump   = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file   = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt      = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (queue_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" 0x%-.4x %-4d %-5d 0x%-16"PRIx64" 0x%-16"PRIx64" 0x%-16"PRIx64" 0x%-16"PRIx64"\n",
                            *cnt,queue_id,ctc_oid.value,ctc_oid.sub_type,ctc_oid.value2,p_db->sch_grp,
                            p_db->sch_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, ctc_oid.lchip,0,0,p_db->sch_id) : 0,
                            p_db->wred_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_WRED, ctc_oid.lchip,0,0,p_db->wred_id) : 0,
                            p_db->buf_id ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, ctc_oid.lchip,0,0,p_db->buf_id) : 0);

    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
sai_status_t
ctc_sai_queue_traverse_set(ctc_sai_queue_traverse_param_t* p_param)
{
    CTC_SAI_PTR_VALID_CHECK(p_param);
    CTC_SAI_PTR_VALID_CHECK(p_param->cmp_value);
    CTC_SAI_PTR_VALID_CHECK(p_param->p_value);
    ctc_sai_db_traverse_object_property(p_param->lchip, SAI_OBJECT_TYPE_QUEUE, (hash_traversal_fn)_ctc_sai_queue_traverse_set_cb, p_param);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_queue_port_get_queue_num(sai_object_id_t port_id, uint32* queue_num)
{
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch = NULL;
    ctc_sai_port_db_t* p_port_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(queue_num);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        return SAI_STATUS_FAILURE;
    }

    *queue_num = CTC_QOS_BASIC_Q_NUM;
    if (p_switch->port_queues == 16)
    {
        //uc + mc
         *queue_num += CTC_QOS_16Q_MCAST_Q_NUM;
    }

    _ctc_sai_port_get_port_db(port_id, &p_port_db);
    *queue_num += p_port_db->service_id_list->count * CTC_QOS_EXT_Q_NUM;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_queue_port_get_queue_list(sai_object_id_t port_id, sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    uint16 queue_num = 0, total_queue_num = 0;
    uint16 idx = 0, start_idx = 0;
    uint8 queue_type = 0;
    uint8 queue_idx = 0;
    sai_object_id_t *queue_list = NULL;
    ctc_sai_switch_master_t* p_switch = NULL;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_slistnode_t *node = NULL;
    ctc_sai_port_service_id_t *p_service_id_node = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(attr);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_oid);
    lchip = ctc_oid.lchip;

    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        return SAI_STATUS_FAILURE;
    }

    _ctc_sai_port_get_port_db(port_id, &p_port_db);

    queue_num = CTC_QOS_BASIC_Q_NUM;
    if (p_switch->port_queues == 16)
    {
        //uc + mc
         queue_num += CTC_QOS_16Q_MCAST_Q_NUM;
    }

    total_queue_num = queue_num + p_port_db->service_id_list->count * CTC_QOS_EXT_Q_NUM;

    queue_list = (sai_object_id_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(sai_object_id_t)*total_queue_num);

    for (idx = 0; idx < queue_num; idx++)
    {
        if (p_switch->port_queues == 8)
        {
            queue_type = SAI_QUEUE_TYPE_ALL;
            queue_idx = idx;
        }
        else if (idx < CTC_QOS_BASIC_Q_NUM)
        {
            queue_type = SAI_QUEUE_TYPE_UNICAST;
            queue_idx = idx;
        }
        else
        {
            queue_type = SAI_QUEUE_TYPE_MULTICAST;
            queue_idx = idx - CTC_QOS_BASIC_Q_NUM;
        }
        queue_list[idx] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, queue_type,queue_idx, ctc_oid.value);
    }

    start_idx = queue_num;

    //add service queue

    queue_num = CTC_QOS_EXT_Q_NUM;
    CTC_SLIST_LOOP(p_port_db->service_id_list, node)
    {
        p_service_id_node = _ctc_container_of(node, ctc_sai_port_service_id_t, node);

        for (idx = 0; idx < queue_num; idx++)
        {
            queue_type = SAI_QUEUE_TYPE_SERVICE;
            queue_idx = idx;

            queue_list[start_idx + idx] =
                ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, queue_type, (p_service_id_node->service_id << 6) + queue_idx, ctc_oid.value);
        }
        start_idx += queue_num;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), queue_list, total_queue_num, (void*)(&(attr->value.objlist))));

    mem_free(queue_list);
    return SAI_STATUS_SUCCESS;
}

#define ________SAI_DUMP________

void
ctc_sai_queue_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Queue MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_QUEUE))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Queue");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_queue_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-6s %-4s %-5s %-18s %-18s %-18s %-18s\n", "No.","Queue_Oid","Gport","Type","Index","Sched_Group","Scheduler","Wred","Buffer");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_QUEUE,
                                                (hash_traversal_fn)_ctc_sai_queue_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}


#define ________SAI_API________

sai_status_t
ctc_sai_queue_create_queue_id(
        _Out_ sai_object_id_t *queue_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;
    sai_object_id_t queue_oid;
    ctc_object_id_t ctc_object_id;
    sai_object_key_t key;
    sai_attribute_t attr;
    uint8  queue_type = 0;
    uint8  sub_index = 0;
    uint32 gport = 0;
    uint16 service_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(queue_id);
    *queue_id = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_TYPE, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Not Found SAI_QUEUE_ATTR_TYPE!\n");
        goto error_0;
    }
    else
    {
        queue_type = attr_value->u32;
        if ((queue_type > SAI_QUEUE_TYPE_MULTICAST) && (queue_type != SAI_QUEUE_TYPE_SERVICE))
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to create queue, invalid type:%d\n", status);
            goto error_0;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_PORT, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Not Found SAI_QUEUE_ATTR_PORT!\n");
        goto error_0;
    }
    else
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_value->oid, &ctc_object_id);
        if (ctc_object_id.type != SAI_OBJECT_TYPE_PORT)
        {

            status = SAI_STATUS_INVALID_OBJECT_TYPE;
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to create queue, invalid port id:%d\n", status);
            goto error_0;
        }
        gport = ctc_object_id.value;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_INDEX, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to create queue, invalid index:%d\n", status);
        goto error_0;
    }
    else
    {
        if((CTC_QOS_EXT_Q_NUM <= attr_value->u8)&&(queue_type == SAI_QUEUE_TYPE_SERVICE))
        {
            status = SAI_STATUS_INVALID_PARAMETER;

            goto error_0;
        }
        sub_index = attr_value->u8;
    }

    if(queue_type == SAI_QUEUE_TYPE_SERVICE)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_SERVICE_ID, &attr_value, &attr_index);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to create queue, invalid service id:%d\n", status);
            goto error_0;
        }
        else
        {
            service_id = attr_value->u16;
        }
    }

    queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, queue_type, (service_id << 6) + sub_index, gport);

    key.key.object_id = queue_oid;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_WRED_PROFILE_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_WRED, attr_value->oid, &ctc_object_id);
        if (lchip != ctc_object_id.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to apply Wred_id:0x"PRIx64"\n",attr_value->oid);
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto error_0;
        }
        attr.id = SAI_QUEUE_ATTR_WRED_PROFILE_ID;
        attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_queue_set_attr(&key, &attr), status, error_0);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        attr.id = SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID;
        attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_queue_set_attr(&key, &attr), status, error_0);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        attr.id = SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE;
        attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_queue_set_attr(&key, &attr), status, error_0);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        attr.id = SAI_QUEUE_ATTR_BUFFER_PROFILE_ID;
        attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_queue_set_attr(&key, &attr), status, error_0);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        attr.id = SAI_QUEUE_ATTR_ENABLE_PFC_DLDR;
        attr.value.booldata = attr_value->booldata;
        CTC_SAI_ERROR_GOTO(_ctc_sai_queue_set_attr(&key, &attr), status, error_0);
    }

    *queue_id = queue_oid;
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_queue_remove_queue_id(
        _In_ sai_object_id_t queue_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    sai_status_t status = 0;
    uint8 lchip = 0;
    sai_object_key_t key;
    sai_attribute_t attr;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    if (ctc_oid.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_db)
    {
        status = SAI_STATUS_SUCCESS;
        goto error_return;
    }
    if (p_queue_db->wred_id)
    {
        //to remove wred
        ctc_sai_wred_queue_set_wred(queue_id, p_queue_db->wred_id, 0, FALSE);
    }
    key.key.object_id = queue_id;
    if (p_queue_db->sch_grp)
    {
        attr.id = SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE;
        attr.value.oid = SAI_NULL_OBJECT_ID;
        _ctc_sai_queue_set_attr(&key, &attr);
    }
    if (p_queue_db->sch_id)
    {
        attr.id = SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID;
        attr.value.oid = SAI_NULL_OBJECT_ID;
        _ctc_sai_queue_set_attr(&key, &attr);
    }
    if (p_queue_db->buf_id)
    {
        attr.id = SAI_QUEUE_ATTR_BUFFER_PROFILE_ID;
        attr.value.oid = SAI_NULL_OBJECT_ID;
        _ctc_sai_queue_set_attr(&key, &attr);
    }
    if (p_queue_db->pfc_dld_en)
    {
        attr.id = SAI_QUEUE_ATTR_ENABLE_PFC_DLDR;
        attr.value.booldata = FALSE;
        _ctc_sai_queue_set_attr(&key, &attr);
    }

    mem_free(p_queue_db);
    ctc_sai_db_remove_object_property(lchip, queue_id);

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_queue_set_attribute(
        _In_ sai_object_id_t queue_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = queue_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_QUEUE,  queue_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to set queue attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_queue_get_attribute(
        _In_ sai_object_id_t queue_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = queue_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_QUEUE, loop, queue_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_queue_get_stats(
        _In_ sai_object_id_t queue_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters)
{
    uint32_t         attr_idx    = 0;
    ctc_qos_queue_stats_t queue_stats;
    ctc_object_id_t ctc_oid;
    ctc_sai_switch_master_t* p_switch = NULL;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    
    uint8   lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    sal_memset(&queue_stats, 0, sizeof(ctc_qos_queue_stats_t));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    if (ctc_oid.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Switch DB not found!\n");
        return SAI_STATUS_FAILURE;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_queue_get_queue_db(queue_id, &p_queue_db));

    if ((ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
        && (p_switch->port_queues == 16))
    {
        queue_stats.queue.queue_id = ctc_oid.value2 + CTC_QOS_BASIC_Q_NUM;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }
    else if (ctc_oid.sub_type == SAI_QUEUE_TYPE_SERVICE)
    {
        queue_stats.queue.queue_id = ctc_oid.value2 & 0x3F;
        queue_stats.queue.service_id = (ctc_oid.value2 >> 6);
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
    }
    else
    {
        queue_stats.queue.queue_id = ctc_oid.value2;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }

    queue_stats.queue.gport = ctc_oid.value;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_queue_stats(lchip, &queue_stats));

    for(attr_idx = 0; attr_idx < number_of_counters; attr_idx++)
    {
        switch(counter_ids[attr_idx])
        {
            case SAI_QUEUE_STAT_PACKETS:
                counters[attr_idx] = queue_stats.stats.deq_packets + queue_stats.stats.drop_packets - p_queue_db->queue_all_pkt;
                break;
            case SAI_QUEUE_STAT_BYTES:
                if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
                {
                    counters[attr_idx] = queue_stats.stats.deq_bytes + queue_stats.stats.drop_bytes - p_queue_db->queue_all_byte;
                }
                if(CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats,tmm not support\n");
                    return SAI_STATUS_NOT_SUPPORTED;
                }
                break;
            case SAI_QUEUE_STAT_DROPPED_PACKETS:
                counters[attr_idx] = queue_stats.stats.drop_packets - p_queue_db->queue_drop_pkt;
                break;
            case SAI_QUEUE_STAT_DROPPED_BYTES:
                if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
                {
                    counters[attr_idx] = queue_stats.stats.drop_bytes - p_queue_db->queue_drop_byte;
                }
                if(CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats,tmm not support\n");
                    return SAI_STATUS_NOT_SUPPORTED;
                }
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats, not support\n");
                return SAI_STATUS_NOT_SUPPORTED;
                break;
        }
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_queue_get_stats_ext(
        _In_ sai_object_id_t queue_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters)
{
    uint32_t         attr_idx    = 0;
    ctc_qos_queue_stats_t queue_stats;
    ctc_object_id_t ctc_oid;
    ctc_sai_switch_master_t* p_switch = NULL;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    uint8   lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    sal_memset(&queue_stats, 0, sizeof(ctc_qos_queue_stats_t));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    if (ctc_oid.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Switch DB not found!\n");
        return SAI_STATUS_FAILURE;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_queue_get_queue_db(queue_id, &p_queue_db));

    if ((ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
        && (p_switch->port_queues == 16))
    {
        queue_stats.queue.queue_id = ctc_oid.value2 + CTC_QOS_BASIC_Q_NUM;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }
    else if (ctc_oid.sub_type == SAI_QUEUE_TYPE_SERVICE)
    {
        queue_stats.queue.queue_id = ctc_oid.value2 & 0x3F;
        queue_stats.queue.service_id = (ctc_oid.value2 >> 6);
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
    }
    else
    {
        queue_stats.queue.queue_id = ctc_oid.value2;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }

    queue_stats.queue.gport = ctc_oid.value;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_queue_stats(lchip, &queue_stats));

    for(attr_idx = 0; attr_idx < number_of_counters; attr_idx++)
    {
        switch(counter_ids[attr_idx])
        {
            case SAI_QUEUE_STAT_PACKETS:
                counters[attr_idx] = queue_stats.stats.deq_packets + queue_stats.stats.drop_packets - p_queue_db->queue_all_pkt;
                break;
            case SAI_QUEUE_STAT_BYTES:
                if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
                {
                    counters[attr_idx] = queue_stats.stats.deq_bytes + queue_stats.stats.drop_bytes - p_queue_db->queue_all_byte;
                }
                if(CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats,tmm not support\n");
                    return SAI_STATUS_NOT_SUPPORTED;
                }
                break;
            case SAI_QUEUE_STAT_DROPPED_PACKETS:
                counters[attr_idx] = queue_stats.stats.drop_packets - p_queue_db->queue_drop_pkt;
                break;
            case SAI_QUEUE_STAT_DROPPED_BYTES:
                if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
                {
                    counters[attr_idx] = queue_stats.stats.drop_bytes - p_queue_db->queue_drop_byte;
                }
                if(CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats,tmm not support\n");
                    return SAI_STATUS_NOT_SUPPORTED;
                }
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Failed to get queue stats, not support\n");
                return SAI_STATUS_NOT_SUPPORTED;
                break;
        }
    }

    if (SAI_STATS_MODE_READ_AND_CLEAR == mode)
    {
        p_queue_db->queue_all_pkt = queue_stats.stats.deq_packets + queue_stats.stats.drop_packets;
        p_queue_db->queue_all_byte = queue_stats.stats.deq_bytes + queue_stats.stats.drop_bytes;
        p_queue_db->queue_drop_pkt = queue_stats.stats.drop_packets;
        p_queue_db->queue_drop_byte = queue_stats.stats.drop_bytes;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_queue_clear_stats(
        _In_ sai_object_id_t queue_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids)
{
    ctc_qos_queue_stats_t queue_stats;
    ctc_object_id_t ctc_oid;
    ctc_sai_switch_master_t* p_switch = NULL;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    uint8   lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QUEUE);
    sal_memset(&queue_stats, 0, sizeof(ctc_qos_queue_stats_t));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    if (ctc_oid.type != SAI_OBJECT_TYPE_QUEUE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Object type isNot SAI_OBJECT_TYPE_QUEUE!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Switch DB not found!\n");
        return SAI_STATUS_FAILURE;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_queue_get_queue_db(queue_id, &p_queue_db));

    if ((ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
        && (p_switch->port_queues == 16))
    {
        queue_stats.queue.queue_id = ctc_oid.value2 + CTC_QOS_BASIC_Q_NUM;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }
    else if (ctc_oid.sub_type == SAI_QUEUE_TYPE_SERVICE)
    {
        queue_stats.queue.queue_id = ctc_oid.value2 & 0x3F;
        queue_stats.queue.service_id = (ctc_oid.value2 >> 6);
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
    }
    else
    {
        queue_stats.queue.queue_id = ctc_oid.value2;
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    }

    queue_stats.queue.gport = ctc_oid.value;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_queue_stats(lchip, &queue_stats));
    p_queue_db->queue_all_pkt = queue_stats.stats.deq_packets + queue_stats.stats.drop_packets;
    p_queue_db->queue_all_byte = queue_stats.stats.deq_bytes + queue_stats.stats.drop_bytes;
    p_queue_db->queue_drop_pkt = queue_stats.stats.drop_packets;
    p_queue_db->queue_drop_byte = queue_stats.stats.drop_bytes;

    return SAI_STATUS_SUCCESS;
}

sai_queue_api_t g_ctc_sai_queue_api = {
    ctc_sai_queue_create_queue_id,
    ctc_sai_queue_remove_queue_id,
    ctc_sai_queue_set_attribute,
    ctc_sai_queue_get_attribute,
    ctc_sai_queue_get_stats,
    ctc_sai_queue_get_stats_ext,
    ctc_sai_queue_clear_stats
};


sai_status_t
ctc_sai_queue_api_init()
{
    ctc_sai_register_module_api(SAI_API_QUEUE, (void*)&g_ctc_sai_queue_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_queue_db_init(uint8 lchip)
{
    uint8 chip_type = 0;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_PORT;
    wb_info.data_len = sizeof(ctc_sai_queue_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;

    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_QUEUE, (void*)(&wb_info));
    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    chip_type = ctcs_get_chip_type(lchip);
#ifndef SAI_ON_TMMX
    if (CTC_CHIP_TSINGMA == chip_type)
    {
        uint8 gchip = 0;
        ctc_qos_queue_cfg_t que_cfg;

        sal_memset(&que_cfg, 0, sizeof(que_cfg));

        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
        que_cfg.type = CTC_QOS_QUEUE_CFG_QUEUE_STATS_EN;
        que_cfg.value.stats.stats_en = 1;
        que_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        que_cfg.value.stats.queue.gport = CTC_MAP_LPORT_TO_GPORT(gchip, 0);
        if (ctcs_get_chip_type(lchip) == CTC_CHIP_GOLDENGATE)
        {
            ctc_global_panel_ports_t local_panel_ports;
            uint16 num = 0;

            sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
            CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));

            que_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
            for (num = 0; num < local_panel_ports.count; num++)
            {
                que_cfg.value.stats.queue.gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
                CTC_SAI_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));
            }
            que_cfg.value.stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
        }

        CTC_SAI_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));
    }
#endif
    return SAI_STATUS_SUCCESS;
}

