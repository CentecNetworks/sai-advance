#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"

#include "ctcs_api.h"
#include "ctc_sai_port.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_samplepacket.h"

#define CTC_SAI_RANDOM_LOG_MAX_RATE 0x8000


typedef struct ctc_sai_wb_samplepacket_bind_node_s
{
    /*key*/
    uint32        samplepacket_id;
    uint32 index;
    uint32 calc_key_len[0];
    /*data*/
    uint8 ctc_dir;
    uint8 is_acl;
    uint8 acl_log_id;
    uint32 gport;
    uint32 acl_entry_id;
}ctc_sai_wb_samplepacket_bind_node_t;

#define ________SAMPLEPACKET_INTERNAL_______
static sai_status_t
_ctc_sai_samplepacket_db_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_samplepacket_t* p_samplepacket = NULL;
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
    ctc_slistnode_t        *node = NULL, *next_node = NULL;

    p_samplepacket = (ctc_sai_samplepacket_t*)bucket_data->data;
    CTC_SLIST_LOOP_DEL(p_samplepacket->port_list, node, next_node)
    {
        p_bind_node = (ctc_sai_samplepacket_bind_node_t*)node;
        mem_free(p_bind_node);
    }
    ctc_slist_free(p_samplepacket->port_list);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_samplepacket_rate_map_acl_precent(uint8 lchip, uint32 sample_rate, uint32* acl_precent)
{
    uint32 rate = 0;
    uint32 index = 0;
    uint32 precent[CTC_LOG_PERCENT_MAX] = {
        CTC_LOG_PERCENT_POWER_NEGATIVE_0,
        CTC_LOG_PERCENT_POWER_NEGATIVE_1,
        CTC_LOG_PERCENT_POWER_NEGATIVE_2,
        CTC_LOG_PERCENT_POWER_NEGATIVE_3,
        CTC_LOG_PERCENT_POWER_NEGATIVE_4,
        CTC_LOG_PERCENT_POWER_NEGATIVE_5,
        CTC_LOG_PERCENT_POWER_NEGATIVE_6,
        CTC_LOG_PERCENT_POWER_NEGATIVE_7,
        CTC_LOG_PERCENT_POWER_NEGATIVE_8,
        CTC_LOG_PERCENT_POWER_NEGATIVE_9,
        CTC_LOG_PERCENT_POWER_NEGATIVE_10,
        CTC_LOG_PERCENT_POWER_NEGATIVE_11,
        CTC_LOG_PERCENT_POWER_NEGATIVE_12,
        CTC_LOG_PERCENT_POWER_NEGATIVE_13,
        CTC_LOG_PERCENT_POWER_NEGATIVE_14,
        CTC_LOG_PERCENT_POWER_NEGATIVE_15
    };



    for (rate = sample_rate;rate>1 ;rate=rate>>1)
    {
        index++;
    }

    if (index>=CTC_LOG_PERCENT_MAX)
    {
        return SAI_STATUS_FAILURE;
    }

    *acl_precent = precent[index];

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_samplepacket_alloc_samplepacket(ctc_sai_samplepacket_t** p_samplepacket)
{
    ctc_sai_samplepacket_t* p_samplepacket_temp = NULL;

    p_samplepacket_temp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_samplepacket_t));
    if (NULL == p_samplepacket_temp)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_samplepacket_temp, 0, sizeof(ctc_sai_samplepacket_t));

    p_samplepacket_temp->port_list = ctc_slist_new();
    if (NULL == p_samplepacket_temp->port_list)
    {
        mem_free(p_samplepacket_temp);
        return SAI_STATUS_NO_MEMORY;
    }

    *p_samplepacket = p_samplepacket_temp;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_samplepacket_free_samplepacket(ctc_sai_samplepacket_t* p_samplepacket)
{
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
    ctc_slistnode_t        *node = NULL, *next_node = NULL;

    CTC_SLIST_LOOP_DEL(p_samplepacket->port_list, node, next_node)
    {
        p_bind_node = (ctc_sai_samplepacket_bind_node_t*)node;
        mem_free(p_bind_node);
    }
    ctc_slist_free(p_samplepacket->port_list);

    mem_free(p_samplepacket);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_samplepacket_create_samplepacket(
            sai_object_id_t *samplepacket_id,
            sai_object_id_t switch_id,
            uint32_t attr_count,
            const sai_attribute_t *attr_list)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_val  = NULL;
    uint32 attr_idx = 0;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;

    CTC_SAI_PTR_VALID_CHECK(samplepacket_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE, &attr_val, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SAMPLEPACKET, "Missing mandatory attribute samplepacket rate on create of samplepacket\n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_samplepacket_alloc_samplepacket(&p_samplepacket));
    p_samplepacket->sample_rate = attr_val->u32;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SAMPLEPACKET_ATTR_TYPE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_val->s32 > SAI_SAMPLEPACKET_TYPE_SLOW_PATH)
        {
            status = SAI_STATUS_INVALID_ATTR_VALUE_0+attr_idx;
            CTC_SAI_LOG_ERROR(SAI_API_SAMPLEPACKET, "Invalid sample attr type value on create of samplepacket\n");
            goto roll_back_0;
        }
        p_samplepacket->sample_type = attr_val->s32;
    }
    else
    {
        p_samplepacket->sample_type = SAI_SAMPLEPACKET_TYPE_SLOW_PATH;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SAMPLEPACKET_ATTR_MODE, &attr_val, &attr_idx);
    if (!CTC_SAI_ERROR(status))
    {

        if (SAI_SAMPLEPACKET_MODE_EXCLUSIVE != attr_val->s32)
        {
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            CTC_SAI_LOG_ERROR(SAI_API_SAMPLEPACKET, "Invalid sample attr mode value attribute samplepacket rate on create of samplepacket\n");
            goto roll_back_0;
        }
        p_samplepacket->sample_mode = attr_val->s32;
    }
    else
    {
        p_samplepacket->sample_mode = SAI_SAMPLEPACKET_MODE_EXCLUSIVE;
    }

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &p_samplepacket->samplepacket_id), status, roll_back_1);
    *samplepacket_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SAMPLEPACKET, lchip, 0, 0, p_samplepacket->samplepacket_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *samplepacket_id, p_samplepacket), status, roll_back_2);
    CTC_SAI_DB_UNLOCK(lchip);

    return SAI_STATUS_SUCCESS;

roll_back_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_samplepacket->samplepacket_id);

roll_back_1:
    CTC_SAI_DB_UNLOCK(lchip);

roll_back_0:
    _ctc_sai_samplepacket_free_samplepacket(p_samplepacket);

    return status;
}

static sai_status_t
ctc_sai_samplepacket_remove_samplepacket(sai_object_id_t samplepacket_id)
{
    ctc_object_id_t ctc_oid;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SAMPLEPACKET, samplepacket_id, &ctc_oid));
    CTC_SAI_DB_LOCK(lchip);
    lchip = ctc_oid.lchip;
    p_samplepacket = ctc_sai_db_get_object_property(lchip, samplepacket_id);
    if (NULL == p_samplepacket)
    {
        CTC_SAI_DB_UNLOCK(lchip);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    ctc_sai_db_remove_object_property(lchip, samplepacket_id);
    CTC_SAI_DB_UNLOCK(lchip);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, p_samplepacket->samplepacket_id);

    _ctc_sai_samplepacket_free_samplepacket(p_samplepacket);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
ctc_sai_samplepacket_get_samplepacket_property(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_samplepacket = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_samplepacket)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_SAMPLEPACKET, "object id %"PRIx64" get samplepacket attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE:
            attr->value.u32 = p_samplepacket->sample_rate;
            break;
        case SAI_SAMPLEPACKET_ATTR_TYPE:
            attr->value.s32 = p_samplepacket->sample_type;
            break;
        case SAI_SAMPLEPACKET_ATTR_MODE:
            attr->value.s32 = p_samplepacket->sample_mode;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SAMPLEPACKET, "Samplepacket attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0+attr_idx;
            break;
    }

    return status;
}

static sai_status_t
ctc_sai_samplepacket_set_samplepacket_property(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 log_rate = 0;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;
    ctc_sai_samplepacket_bind_node_t* p_temp_bind_node = NULL;
    struct ctc_slistnode_s* p_temp_node      = NULL;
    ctc_acl_field_action_t action_field;

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));
    p_samplepacket = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_samplepacket)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_SAMPLEPACKET, "object id %"PRIx64" set samplepacket attribute id %d\n", key->key.object_id, attr->id);

    switch(attr->id)
    {
        case SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE:
            p_samplepacket->sample_rate = attr->value.u32;
            CTC_SLIST_LOOP(p_samplepacket->port_list, p_temp_node)
            {
                p_temp_bind_node = (ctc_sai_samplepacket_bind_node_t*)p_temp_node;
                if (false == p_temp_bind_node->is_acl)
                {
                    CTC_SAI_ATTR_ERROR_RETURN(ctcs_port_set_direction_property(lchip, p_temp_bind_node->gport, CTC_PORT_DIR_PROP_RANDOM_LOG_RATE, p_temp_bind_node->ctc_dir, p_samplepacket->sample_rate), 0);
                }
                else
                {
                    CTC_SAI_ATTR_ERROR_RETURN(_ctc_sai_samplepacket_rate_map_acl_precent(lchip, p_samplepacket->sample_rate, &log_rate), 0);
                    sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
                    action_field.type = CTC_ACL_FIELD_ACTION_RANDOM_LOG;
                    action_field.data0 = p_temp_bind_node->acl_log_id;
                    action_field.data1 = log_rate;
                    CTC_SAI_ATTR_ERROR_RETURN(ctcs_acl_add_action_field(lchip, p_temp_bind_node->acl_entry_id, &action_field), 0);
                }
            }
            break;
        case SAI_SAMPLEPACKET_ATTR_TYPE:
        case SAI_SAMPLEPACKET_ATTR_MODE:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SAMPLEPACKET, "Samplepacket attribute %d not implemented\n", attr->id);
            status = SAI_STATUS_ATTR_NOT_IMPLEMENTED_0;
            break;
    }

    return status;
}

static ctc_sai_attr_fn_entry_t samplepacket_attr_fn_entries[] = {
    {SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE, ctc_sai_samplepacket_get_samplepacket_property, ctc_sai_samplepacket_set_samplepacket_property},
    {SAI_SAMPLEPACKET_ATTR_TYPE, ctc_sai_samplepacket_get_samplepacket_property, NULL},
    {SAI_SAMPLEPACKET_ATTR_MODE, ctc_sai_samplepacket_get_samplepacket_property, NULL},
    {CTC_SAI_FUNC_ATTR_END_ID, NULL, NULL}
};

static sai_status_t
ctc_sai_samplepacket_set_samplepacket_attribute(sai_object_id_t samplepacket_id,
                                            const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    sai_object_key_t key = { .key.object_id = samplepacket_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(samplepacket_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = samplepacket_id;
    status = ctc_sai_set_attribute(&key, NULL,
                        SAI_OBJECT_TYPE_SAMPLEPACKET, samplepacket_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}

static sai_status_t
ctc_sai_samplepacket_get_samplepacket_attribute(sai_object_id_t samplepacket_id,
                                        uint32_t attr_count,
                                        sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint16 loop = 0;
    sai_object_key_t key = { .key.object_id = samplepacket_id };
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(samplepacket_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = samplepacket_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
              SAI_OBJECT_TYPE_SAMPLEPACKET, loop, samplepacket_attr_fn_entries, &attr_list[loop]), status, roll_back_0);
        loop++;
    }

roll_back_0:

    CTC_SAI_DB_UNLOCK(lchip);

    return status;
}


#define ________SAMPLEPACKET_WB_______

static sai_status_t
_ctc_sai_samplepacket_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int ret = 0;
    ctc_sai_samplepacket_t *p_samplepacket = (ctc_sai_samplepacket_t *)data;
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_wb_samplepacket_bind_node_t wb_bind_port_data = {0};
    ctc_wb_data_t wb_data;
    uint16  max_entry_cnt = 0;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_samplepacket_bind_node_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_SAMPLEPACKET);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_samplepacket->port_list, node)
    {
        p_bind_node = (ctc_sai_samplepacket_bind_node_t*)node;

        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_bind_port_data.samplepacket_id = p_samplepacket->samplepacket_id;
        wb_bind_port_data.index = index++;
        wb_bind_port_data.ctc_dir = p_bind_node->ctc_dir;
        wb_bind_port_data.is_acl = p_bind_node->is_acl;
        wb_bind_port_data.acl_log_id = p_bind_node->acl_log_id;
        wb_bind_port_data.gport = p_bind_node->gport;
        wb_bind_port_data.acl_entry_id = p_bind_node->acl_entry_id;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_bind_port_data, (wb_data.key_len + wb_data.data_len));
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

    return SAI_STATUS_SUCCESS;

out:
done:
    if (wb_data.buffer)
    {
        CTC_WB_FREE_BUFFER(wb_data.buffer);
    }

    return status;
}

static sai_status_t
_ctc_sai_samplepacket_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t samplepacket_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_oid;

    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, samplepacket_id, &ctc_oid);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_oid.value));
    return status;
}

static sai_status_t
_ctc_sai_samplepacket_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_samplepacket_t *p_samplepacket = NULL;
    ctc_sai_wb_samplepacket_bind_node_t wb_bind_port_data = {0};
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
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

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_samplepacket_bind_node_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_SAMPLEPACKET);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_bind_port_data, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_samplepacket_bind_node_t));
        p_samplepacket = ctc_sai_db_get_object_property(lchip, wb_bind_port_data.samplepacket_id);
        if (!p_samplepacket)
        {
            continue;
        }

        p_bind_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_samplepacket_bind_node_t));
        if (!p_bind_node)
        {
            continue;
        }

        p_bind_node->ctc_dir = wb_bind_port_data.ctc_dir;
        p_bind_node->is_acl = wb_bind_port_data.is_acl;
        p_bind_node->acl_log_id = wb_bind_port_data.acl_log_id;
        p_bind_node->gport = wb_bind_port_data.gport;
        p_bind_node->acl_entry_id = wb_bind_port_data.acl_entry_id;

        ctc_slist_add_tail(p_samplepacket->port_list, &(p_bind_node->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return SAI_STATUS_SUCCESS;
}

#define ________SAMPLEPACKET_DUMP________

static sai_status_t
_ctc_sai_samplepacket_dump_samplepacket_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  samplepkt_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_samplepacket_t* p_samplepkt = NULL;

    samplepkt_oid = bucket_data->oid;
    p_samplepkt = (ctc_sai_samplepacket_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (samplepkt_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-8d %-4d %-4d %-8d\n", num_cnt, samplepkt_oid, p_samplepkt->sample_rate,\
           p_samplepkt->sample_type, p_samplepkt->sample_mode, p_samplepkt->port_list->count);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_samplepacket_dump_samplepacket_bind_info_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  samplepkt_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_samplepacket_t* p_samplepkt = NULL;
    ctc_sai_samplepacket_bind_node_t* p_samplepkt_bind_node = NULL;
    struct ctc_slistnode_s* p_temp_node      = NULL;

    samplepkt_oid = bucket_data->oid;
    p_samplepkt = (ctc_sai_samplepacket_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (samplepkt_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SLIST_LOOP(p_samplepkt->port_list, p_temp_node)
    {
        p_samplepkt_bind_node = (ctc_sai_samplepacket_bind_node_t*)p_temp_node;

        if (p_samplepkt_bind_node->is_acl)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-6s %-10d %-6s 0x%016"PRIx64"\n", num_cnt, samplepkt_oid, "Y",\
                p_samplepkt_bind_node->acl_log_id, "-", p_samplepkt_bind_node->acl_entry_id);
        }
        else
        {
            CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64" %-6s %-10s %-6d %-16s\n", num_cnt, samplepkt_oid, "N",\
                "-", p_samplepkt_bind_node->gport, "-");
        }

        (*((uint32 *)(p_cb_data->value1)))++;
    }

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_samplepacket_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;

    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Samplepacket MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_SAMPLEPACKET))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Samplepacket");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_samplepacket_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-8s %-4s %-4s %-8s\n", "No.", "Samplepacket_id", "Rate", "Type", "Mode", "Port_cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_SAMPLEPACKET,
                                            (hash_traversal_fn)_ctc_sai_samplepacket_dump_samplepacket_print_cb, (void*)(&sai_cb_data));

        num_cnt = 1;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_samplepacket_bind_node_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-6s %-10s %-6s %-18s\n", "No.", "Samplepacket_id", "Is_acl", "Acl_log_id", "Gport", "Acl_entry_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_SAMPLEPACKET,
                                            (hash_traversal_fn)_ctc_sai_samplepacket_dump_samplepacket_bind_info_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAMPLEPACKET_API________

sai_samplepacket_api_t g_ctc_sai_samplepacket_api = {
     ctc_sai_samplepacket_create_samplepacket,
     ctc_sai_samplepacket_remove_samplepacket,
     ctc_sai_samplepacket_set_samplepacket_attribute,
     ctc_sai_samplepacket_get_samplepacket_attribute
};

sai_status_t
ctc_sai_samplepacket_set_port_samplepacket(uint8 lchip, uint32 gport, const sai_attribute_t *attr, void* p_port_db)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 value = 0;
    uint8 dir = 0;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
    ctc_sai_samplepacket_bind_node_t* p_temp_bind_node = NULL;
    struct ctc_slistnode_s* p_temp_node      = NULL;
    sai_object_id_t sai_oid = 0;
    ctc_sai_port_db_t* p_port_db_temp = NULL;

    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_PTR_VALID_CHECK(p_port_db);

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    if ((SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE != attr->id)
        && (SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }


    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);

    /* direction:ingress or egress */
    dir = (attr->id == SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE)?CTC_INGRESS:CTC_EGRESS;

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        sai_oid = attr->value.oid;
    }
    else
    {
        CTC_SAI_PTR_VALID_CHECK(p_port_db);
        p_port_db_temp = (ctc_sai_port_db_t*)p_port_db;
        if (SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE == attr->id)
        {
            sai_oid = p_port_db_temp->ingress_samplepacket_id;
        }
        else
        {
            sai_oid = p_port_db_temp->egress_samplepacket_id;
        }
    }

    p_samplepacket = ctc_sai_db_get_object_property(lchip, sai_oid);
    if (NULL == p_samplepacket)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SLIST_LOOP(p_samplepacket->port_list, p_temp_node)
    {
        p_temp_bind_node = (ctc_sai_samplepacket_bind_node_t*)p_temp_node;
        if ((0 == p_temp_bind_node->is_acl) && (gport == p_temp_bind_node->gport))
        {
            p_bind_node = p_temp_bind_node;
            break;
        }
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        if (p_bind_node)
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }


        /*get random log rate*/
        if( 0 == p_samplepacket->sample_rate)
        {
            value = 0;
        }
        else
        {
            value = (p_samplepacket->sample_rate >= CTC_SAI_RANDOM_LOG_MAX_RATE)? CTC_SAI_RANDOM_LOG_MAX_RATE: (CTC_SAI_RANDOM_LOG_MAX_RATE/p_samplepacket->sample_rate);
        }

        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_direction_property(lchip, gport, CTC_PORT_DIR_PROP_RANDOM_LOG_RATE, dir, value));

        /*enable port log */
        value = true;
    }
    else
    {
        if (NULL == p_bind_node)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        value = false;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_direction_property(lchip, gport, CTC_PORT_DIR_PROP_RANDOM_LOG_EN, dir, value));


    if (value)
    {
        p_bind_node = (ctc_sai_samplepacket_bind_node_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_samplepacket_bind_node_t));
        if (NULL == p_bind_node)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto roll_back_0;
        }
        p_bind_node->is_acl = false;
        p_bind_node->gport = gport;
        p_bind_node->ctc_dir = dir;
        ctc_slist_add_tail(p_samplepacket->port_list, &(p_bind_node->head));
    }
    else
    {
        ctc_slist_delete_node(p_samplepacket->port_list, &(p_bind_node->head));
        mem_free(p_bind_node);
    }

    return SAI_STATUS_SUCCESS;

roll_back_0:
    ctcs_port_set_direction_property(lchip, gport, CTC_PORT_DIR_PROP_RANDOM_LOG_EN, dir, 0);

    return status;
}

sai_status_t
ctc_sai_samplepacket_set_acl_samplepacket(uint8 lchip, uint8 ctc_dir, uint8 acl_priority, sai_object_id_t acl_entry_id, sai_attribute_t *attr, uint32* ctc_log_id, uint32* ctc_session_id, uint32* ctc_log_rate)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 cpu_gport = 0;
    uint32 log_value = 0;
    uint32 log_rate = 0;
    uint8  session_id = 0;
    uint8  gchip_id = 0;
    uint8  log_id = 0;
    ctc_sai_samplepacket_t* p_samplepacket = NULL;
    ctc_sai_samplepacket_bind_node_t* p_bind_node = NULL;
    ctc_sai_samplepacket_bind_node_t* p_temp_bind_node = NULL;
    struct ctc_slistnode_s* p_temp_node      = NULL;
    ctc_acl_field_action_t action_field;
    ctc_mirror_dest_t ctc_mirror;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    sai_object_id_t sai_oid = 0;

    CTC_SAI_PTR_VALID_CHECK(attr);

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);
    sal_memset(&action_field, 0, sizeof(ctc_acl_field_action_t));
    sal_memset(&ctc_mirror, 0, sizeof(ctc_mirror_dest_t));

    if ((SAI_ACL_ENTRY_ATTR_ACTION_INGRESS_SAMPLEPACKET_ENABLE != attr->id)
        && (SAI_ACL_ENTRY_ATTR_ACTION_EGRESS_SAMPLEPACKET_ENABLE != attr->id))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_LOG_ENTER(SAI_API_SAMPLEPACKET);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip_id));
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_master)
    {
        return SAI_STATUS_NOT_EXECUTED;
    }
    if (CTC_FLAG_ISSET(p_switch_master->flag, CTC_SAI_SWITCH_FLAG_CPU_ETH_EN))
    {
        cpu_gport = p_switch_master->cpu_eth_port;
    }
    else
    {
        cpu_gport = CTC_GPORT_RCPU(gchip_id);
    }

    if (SAI_NULL_OBJECT_ID != attr->value.aclaction.parameter.oid)
    {
        sai_oid = attr->value.aclaction.parameter.oid;
    }
    else
    {
        return SAI_STATUS_SUCCESS;
    }

    p_samplepacket = ctc_sai_db_get_object_property(lchip, sai_oid);
    if (NULL == p_samplepacket)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SLIST_LOOP(p_samplepacket->port_list, p_temp_node)
    {
        p_temp_bind_node = (ctc_sai_samplepacket_bind_node_t*)p_temp_node;
        if ((true == p_temp_bind_node->is_acl) && (acl_entry_id == p_temp_bind_node->acl_entry_id))
        {
            p_bind_node = p_temp_bind_node;
            break;
        }
    }

    if (attr->value.aclaction.enable)
    {
        if (p_bind_node)
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }

        CTC_SAI_ERROR_RETURN(_ctc_sai_samplepacket_rate_map_acl_precent(lchip, p_samplepacket->sample_rate, &log_rate));
        /*enable port log */
        log_value = true;
    }
    else
    {
        if (NULL == p_bind_node)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        log_value = false;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_mirror_alloc_sess_res_index(lchip, ctc_dir, acl_priority, &log_id, &session_id));
    if (log_value)
    {
        ctc_mirror.session_id = session_id;
        ctc_mirror.dir = ctc_dir;
        ctc_mirror.type = CTC_MIRROR_ACLLOG_SESSION;
        ctc_mirror.acl_priority = log_id;
        ctc_mirror.dest_gport = cpu_gport;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_mirror_add_session(lchip, &ctc_mirror), status, roll_back_0);

        p_bind_node = (ctc_sai_samplepacket_bind_node_t*)mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_samplepacket_bind_node_t));
        if (NULL == p_bind_node)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto roll_back_1;
        }
        p_bind_node->is_acl = true;
        p_bind_node->acl_log_id = session_id;
        p_bind_node->acl_entry_id = acl_entry_id;
        ctc_slist_add_tail(p_samplepacket->port_list, &(p_bind_node->head));
    }
    else
    {
        ctc_slist_delete_node(p_samplepacket->port_list, &(p_bind_node->head));

        ctc_mirror.session_id = p_bind_node->acl_log_id;
        ctc_mirror.dir = ctc_dir;
        ctc_mirror.type = CTC_MIRROR_ACLLOG_SESSION;
        ctc_mirror.acl_priority = log_id;
        ctc_mirror.dest_gport = cpu_gport;
        ctcs_mirror_remove_session(lchip, &ctc_mirror);

        ctc_sai_mirror_free_sess_res_index(lchip, ctc_dir, acl_priority, p_bind_node->acl_log_id);
        mem_free(p_bind_node);
    }
    if ((NULL != ctc_log_id) && (NULL != ctc_log_rate) && (NULL != ctc_session_id))
    {
        *ctc_log_id = log_id;
        *ctc_log_rate = log_rate;
        *ctc_session_id = session_id;
    }
    return SAI_STATUS_SUCCESS;

roll_back_1:
    ctcs_mirror_remove_session(lchip, &ctc_mirror);
roll_back_0:
    ctc_sai_mirror_free_sess_res_index(lchip, ctc_dir, acl_priority, session_id);

    return status;
}

sai_status_t
ctc_sai_samplepacket_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_SAMPLEPACKET;
    wb_info.data_len = sizeof(ctc_sai_samplepacket_t);
    wb_info.wb_sync_cb = _ctc_sai_samplepacket_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_samplepacket_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_samplepacket_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_SAMPLEPACKET, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_samplepacket_db_deinit(uint8 lchip)
{
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_SAMPLEPACKET, (hash_traversal_fn)_ctc_sai_samplepacket_db_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_samplepacket_api_init()
{
    ctc_sai_register_module_api(SAI_API_SAMPLEPACKET, (void*)&g_ctc_sai_samplepacket_api);

    return SAI_STATUS_SUCCESS;
}



