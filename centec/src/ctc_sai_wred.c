#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_wred.h"
#include "ctc_sai_queue.h"


static sai_status_t
_ctc_sai_wred_map_attr_to_db(const sai_attribute_t* attr_list, uint32 attr_count, ctc_sai_wred_db_t* p_wred)
{
    sai_status_t status = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_GREEN_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->color_en[SAI_PACKET_COLOR_GREEN] = attr_value->booldata ? 1 : 0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->min_th[SAI_PACKET_COLOR_GREEN] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->max_th[SAI_PACKET_COLOR_GREEN] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->drop_prob[SAI_PACKET_COLOR_GREEN] = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_YELLOW_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->color_en[SAI_PACKET_COLOR_YELLOW] = attr_value->booldata ? 1 : 0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->min_th[SAI_PACKET_COLOR_YELLOW] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->max_th[SAI_PACKET_COLOR_YELLOW] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->drop_prob[SAI_PACKET_COLOR_YELLOW] = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_RED_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->color_en[SAI_PACKET_COLOR_RED] = attr_value->booldata ? 1 : 0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_RED_MIN_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->min_th[SAI_PACKET_COLOR_RED] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_RED_MAX_THRESHOLD, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->max_th[SAI_PACKET_COLOR_RED] = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_WRED_ATTR_RED_DROP_PROBABILITY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_wred->drop_prob[SAI_PACKET_COLOR_RED] = attr_value->u32;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_wred_map_db_to_ctc_drop(ctc_sai_wred_db_t* psai_wred, ctc_qos_drop_t* pctc_drop)
{
    uint32 idx = 0;
    uint8 ctc_idx = 0;

    for (idx = SAI_PACKET_COLOR_GREEN; idx <= SAI_PACKET_COLOR_RED; idx++)
    {
        if (idx == SAI_PACKET_COLOR_GREEN)
        {
            ctc_idx = 2;
        }
        else if (idx == SAI_PACKET_COLOR_YELLOW)
        {
            ctc_idx = 1;
        }
        else
        {
            ctc_idx = 0;
        }

        pctc_drop->drop.drop_prob[ctc_idx] = psai_wred->drop_prob[idx] * 31 / 100;//default value is 100%
        if (!psai_wred->color_en[idx])
        {
            continue;
        }
        pctc_drop->drop.min_th[ctc_idx] = psai_wred->min_th[idx];
        pctc_drop->drop.max_th[ctc_idx] = psai_wred->max_th[idx];
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_wred_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_object_id_t wred_id = key->key.object_id;
    ctc_sai_wred_db_t* p_wred_db = NULL;
    uint8 lchip = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(wred_id, &lchip));
    p_wred_db = ctc_sai_db_get_object_property(lchip, wred_id);
    if (NULL == p_wred_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_WRED_ATTR_GREEN_ENABLE:
            attr->value.booldata = p_wred_db->color_en[SAI_PACKET_COLOR_GREEN] ? TRUE : FALSE;
            break;
        case SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
            attr->value.u32 = p_wred_db->min_th[SAI_PACKET_COLOR_GREEN];
            break;
        case SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
            attr->value.u32 = p_wred_db->max_th[SAI_PACKET_COLOR_GREEN];
            break;
        case SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
            attr->value.u32 = p_wred_db->drop_prob[SAI_PACKET_COLOR_GREEN];
            break;
        case SAI_WRED_ATTR_YELLOW_ENABLE:
            attr->value.booldata = p_wred_db->color_en[SAI_PACKET_COLOR_YELLOW] ? TRUE : FALSE;
            break;
        case SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
            attr->value.u32 = p_wred_db->min_th[SAI_PACKET_COLOR_YELLOW];
            break;
        case SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
            attr->value.u32 = p_wred_db->max_th[SAI_PACKET_COLOR_YELLOW];
            break;
        case SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
            attr->value.u32 = p_wred_db->drop_prob[SAI_PACKET_COLOR_YELLOW];
            break;
        case SAI_WRED_ATTR_RED_ENABLE:
            attr->value.booldata = p_wred_db->color_en[SAI_PACKET_COLOR_RED] ? TRUE : FALSE;
            break;
        case SAI_WRED_ATTR_RED_MIN_THRESHOLD:
            attr->value.u32 = p_wred_db->min_th[SAI_PACKET_COLOR_RED];
            break;
        case SAI_WRED_ATTR_RED_MAX_THRESHOLD:
            attr->value.u32 = p_wred_db->max_th[SAI_PACKET_COLOR_RED];
            break;
        case SAI_WRED_ATTR_RED_DROP_PROBABILITY:
            attr->value.u32 = p_wred_db->drop_prob[SAI_PACKET_COLOR_RED];
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred attribute not implement\n");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_wred_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    ctc_object_id_t ctc_oid;
    sai_object_id_t wred_id = key->key.object_id;
    ctc_sai_wred_db_t* p_wred_db = NULL;
    ctc_sai_wred_db_t wred_db_temp;
    ctc_qos_drop_t ctc_drop;
    ctc_sai_queue_traverse_param_t queue_param;
    uint8 lchip = 0;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_WRED, wred_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    p_wred_db = ctc_sai_db_get_object_property(lchip, wred_id);
    if (NULL == p_wred_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&ctc_drop, 0, sizeof(ctc_drop));
    sal_memset(&queue_param, 0, sizeof(queue_param));

    sal_memcpy(&wred_db_temp, p_wred_db, sizeof(ctc_sai_wred_db_t));

    _ctc_sai_wred_map_attr_to_db(attr, 1, &wred_db_temp);

    if (p_wred_db->used_cnt)
    {
        _ctc_sai_wred_map_db_to_ctc_drop(&wred_db_temp, &ctc_drop);
        ctc_drop.drop.mode = CTC_QUEUE_DROP_WRED;
        queue_param.lchip = lchip;
        queue_param.set_type = CTC_SAI_Q_SET_TYPE_WRED;
        queue_param.cmp_value = &ctc_oid.value;
        queue_param.p_value = &ctc_drop;
        CTC_SAI_ERROR_RETURN(ctc_sai_queue_traverse_set(&queue_param));
    }

    sal_memcpy(p_wred_db, &wred_db_temp, sizeof(ctc_sai_wred_db_t));

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  wred_attr_fn_entries[] =
{
        {SAI_WRED_ATTR_GREEN_ENABLE, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_YELLOW_ENABLE, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_RED_ENABLE, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_RED_MIN_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_RED_MAX_THRESHOLD, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_RED_DROP_PROBABILITY, _ctc_sai_wred_get_attr, _ctc_sai_wred_set_attr},
        {SAI_WRED_ATTR_WEIGHT, NULL, NULL },
        {SAI_WRED_ATTR_ECN_MARK_MODE, NULL, NULL },
        { CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL }
};



#define ________INTERNAL_API________
sai_status_t
ctc_sai_wred_queue_set_wred(sai_object_id_t queue_id, uint32 wred_id, uint32 old_wred_id, bool enable)
{
    sai_object_id_t sai_wred_id;
    ctc_object_id_t ctc_oid;
    ctc_sai_wred_db_t* p_wred_db = NULL;
    ctc_qos_drop_t  ctc_drop;
    ctc_sai_switch_master_t* p_switch = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_WRED);
    CTC_SAI_LOG_INFO(SAI_API_WRED, "queue_oid:0x%"PRIx64" wred_id:0x%x old_wred_id:0x%x enable:%s\n", queue_id, wred_id, old_wred_id, enable?"TRUE":"FALSE");

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;

    sai_wred_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_WRED, lchip, 0, 0, wred_id);
    p_wred_db = ctc_sai_db_get_object_property(lchip, sai_wred_id);
    if (NULL == p_wred_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_switch = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Switch DB not found!\n");
        return SAI_STATUS_FAILURE;
    }
    sal_memset(&ctc_drop, 0, sizeof(ctc_qos_drop_t));
    ctc_drop.queue.gport = ctc_oid.value;

    if ((ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
        && (p_switch->port_queues == 16))
    {
        ctc_drop.queue.queue_id = ctc_oid.value2 + CTC_QOS_BASIC_Q_NUM;
    }
    else
    {
        ctc_drop.queue.queue_id = ctc_oid.value2;
    }
    ctc_drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    if (enable)
    {
        ctc_drop.drop.mode = CTC_QUEUE_DROP_WRED;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_drop_scheme(lchip, &ctc_drop));

        _ctc_sai_wred_map_db_to_ctc_drop(p_wred_db, &ctc_drop);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &ctc_drop));
        p_wred_db->used_cnt++;

        if (old_wred_id)
        {
            //to update the old used_cnt
            ctc_sai_wred_db_t* p_wred_db_old = NULL;
            sai_wred_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_WRED, lchip, 0, 0, old_wred_id);
            p_wred_db_old = ctc_sai_db_get_object_property(lchip, sai_wred_id);
            if (NULL == p_wred_db_old)
            {
                CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred DB not found!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if (p_wred_db_old->used_cnt)
            {
                p_wred_db_old->used_cnt--;
            }
        }
    }
    else
    {
        //set the default wtd value, enable wtd
        ctc_drop.drop.mode = CTC_QUEUE_DROP_WTD;
        ctc_drop.drop.max_th[2] = p_switch->default_wtd_thrd[SAI_PACKET_COLOR_GREEN];
        ctc_drop.drop.max_th[1] = p_switch->default_wtd_thrd[SAI_PACKET_COLOR_YELLOW];
        ctc_drop.drop.max_th[0] = p_switch->default_wtd_thrd[SAI_PACKET_COLOR_RED];
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &ctc_drop));
        if (p_wred_db->used_cnt)
        {
            p_wred_db->used_cnt--;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_wred_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t wred_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, wred_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_wred_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             wred_id  = bucket_data->oid;
    ctc_sai_wred_db_t*          p_db     = (ctc_sai_wred_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump   = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file   = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt      = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (wred_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-7d %-6s %-6d %-10d %-10d %-10d\n", *cnt,wred_id,p_db->used_cnt,"Green",p_db->color_en[0],p_db->min_th[0],p_db->max_th[0],p_db->drop_prob[0]);
    CTC_SAI_LOG_DUMP(p_file, "%31s %-6s %-6d %-10d %-10d %-10d\n", "","Yellow",p_db->color_en[1],p_db->min_th[1],p_db->max_th[1],p_db->drop_prob[1]);
    CTC_SAI_LOG_DUMP(p_file, "%31s %-6s %-6d %-10d %-10d %-10d\n", "","Red",p_db->color_en[2],p_db->min_th[2],p_db->max_th[2],p_db->drop_prob[2]);
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


void
ctc_sai_wred_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Wred MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_WRED))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Wred");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_wred_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-7s %-6s %-6s %-10s %-10s %-10s\n", "No.","Wred_Oid","Ref_cnt","Color","Enable","Min_th","Max_th","Drop_prob");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_WRED,
                                                (hash_traversal_fn)_ctc_sai_wred_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}


#define ________SAI_API________

sai_status_t
ctc_sai_wred_create_wred_id(
        _Out_ sai_object_id_t *wred_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    sai_object_id_t wred_oid;
    ctc_sai_wred_db_t* p_wred_db = NULL;
    uint32  ctc_wred_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_WRED);
    CTC_SAI_PTR_VALID_CHECK(wred_id);
    *wred_id = 0;

    sal_memset(&wred_oid, 0, sizeof(wred_oid));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    p_wred_db = (ctc_sai_wred_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_wred_db_t));
    if (NULL == p_wred_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "No memory.\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error_0;
    }
    sal_memset(p_wred_db, 0, sizeof(ctc_sai_wred_db_t));

    p_wred_db->drop_prob[SAI_PACKET_COLOR_GREEN] = 100;
    p_wred_db->drop_prob[SAI_PACKET_COLOR_YELLOW] = 100;
    p_wred_db->drop_prob[SAI_PACKET_COLOR_RED] = 100;

    _ctc_sai_wred_map_attr_to_db(attr_list, attr_count, p_wred_db);

    //opf alloc wred id
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_wred_id);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Failed to alloc opf.\n");
        goto error_1;
    }
    wred_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_WRED, lchip, 0, 0, ctc_wred_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, wred_oid, p_wred_db), status, error_2);
    *wred_id = wred_oid;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_wred_id);
error_1:
    mem_free(p_wred_db);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_wred_remove_wred_id(
        _In_ sai_object_id_t wred_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_wred_db_t* p_wred_db = NULL;
    sai_status_t status = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_WRED);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, wred_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_WRED)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Object id is not SAI_OBJECT_TYPE_WRED!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_wred_db = ctc_sai_db_get_object_property(lchip, wred_id);
    if (NULL == p_wred_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "wred DB not found!\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    if (p_wred_db->used_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Object In use!\n");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto error_return;
    }

    mem_free(p_wred_db);
    ctc_sai_db_remove_object_property(lchip, wred_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value);

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_wred_set_attribute(
        _In_ sai_object_id_t wred_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = wred_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_WRED);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_WRED, wred_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_WRED)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Object id is not SAI_OBJECT_TYPE_WRED!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_WRED,  wred_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Failed to set wred attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_wred_get_attribute(
        _In_ sai_object_id_t wred_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = wred_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_WRED);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_WRED, wred_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_WRED)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Object id is not SAI_OBJECT_TYPE_WRED!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_WRED, loop, wred_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_WRED, "Failed to get wred attr:%d\n", status);
    }
    return status;
}

sai_wred_api_t g_ctc_sai_wred_api = {
    ctc_sai_wred_create_wred_id,
    ctc_sai_wred_remove_wred_id,
    ctc_sai_wred_set_attribute,
    ctc_sai_wred_get_attribute
};

sai_status_t
ctc_sai_wred_api_init()
{
    ctc_sai_register_module_api(SAI_API_WRED, (void*)&g_ctc_sai_wred_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_wred_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_WRED;
    wb_info.data_len = sizeof(ctc_sai_wred_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_wred_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_WRED, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

