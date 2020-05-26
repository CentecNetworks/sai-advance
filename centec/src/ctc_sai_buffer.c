
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_queue.h"


#define CTC_SAI_PORT_INGRESS_PG_NUM 8
#define CTC_SAI_QOS_DROP_FACTOR_SHIFT 7

#define CTC_SAI_QOS_BYTES_PER_CELL 288

typedef struct  ctc_sai_buffer_profile_db_s
{
    uint8 mode;
    int8 dynamic_th;
    uint32 static_th;
    uint32 xon_th;
    uint32 xoff_th;
    uint16 ref_cnt;
}ctc_sai_buffer_profile_db_t;

typedef struct  ctc_sai_ingress_pg_db_s
{
    sai_object_id_t buf_prof_id;
}ctc_sai_ingress_pg_db_t;


typedef enum ctc_sai_buffer_drop_factor_s {
    CTC_SAI_BUFFER_FACTOR_1_128 = -7,
    CTC_SAI_BUFFER_FACTOR_1_64  = -6,
    CTC_SAI_BUFFER_FACTOR_1_32  = -5,
    CTC_SAI_BUFFER_FACTOR_1_16  = -4,
    CTC_SAI_BUFFER_FACTOR_1_8   = -3,
    CTC_SAI_BUFFER_FACTOR_1_4   = -2,
    CTC_SAI_BUFFER_FACTOR_1_2   = -1,
    CTC_SAI_BUFFER_FACTOR_1  = 0,
    CTC_SAI_BUFFER_FACTOR_2  = 1,
    CTC_SAI_BUFFER_FACTOR_4  = 2,
    CTC_SAI_BUFFER_FACTOR_8  = 3
} ctc_sai_buffer_drop_factor_t;



static sai_status_t
_ctc_sai_ingress_pg_get_db(sai_object_id_t ingress_pg_id, ctc_sai_ingress_pg_db_t** p_pg)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_ingress_pg_db_t* p_pg_temp = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, ingress_pg_id, &ctc_oid);
    if (ctc_oid.type != SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QUEUE, "Invalid ingress priority group oid type!");
        return SAI_STATUS_INVALID_OBJECT_TYPE;
    }
    lchip = ctc_oid.lchip;

    p_pg_temp = ctc_sai_db_get_object_property(lchip, ingress_pg_id);
    if (NULL == p_pg_temp)
    {
        p_pg_temp = (ctc_sai_ingress_pg_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_ingress_pg_db_t));
        if (NULL == p_pg_temp)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "No memory!");
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_pg_temp, 0, sizeof(ctc_sai_ingress_pg_db_t));
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, ingress_pg_id, p_pg_temp), status, error_return);
    }
    *p_pg = p_pg_temp;
    return SAI_STATUS_SUCCESS;

error_return:
    mem_free(p_pg_temp);
    return status;
}


static sai_status_t
_ctc_sai_buffer_set_profile_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    sai_object_id_t buf_prof_id = key->key.object_id;
    ctc_sai_buffer_profile_db_t* p_buf_prof = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, buf_prof_id, &ctc_oid);
    lchip = ctc_oid.lchip;

    p_buf_prof = ctc_sai_db_get_object_property(lchip, buf_prof_id);
    if (NULL == p_buf_prof)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "buffer profile DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
            if (p_buf_prof->dynamic_th == attr->value.s8)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_buf_prof->dynamic_th = attr->value.s8;
            break;
        case SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
            if (p_buf_prof->static_th == attr->value.u32)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_buf_prof->static_th = attr->value.u32;
            break;
        case SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
            if (p_buf_prof->xoff_th == attr->value.u32)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_buf_prof->xoff_th = attr->value.u32;
            break;
        case SAI_BUFFER_PROFILE_ATTR_XON_TH:
            if (p_buf_prof->xon_th == attr->value.u32)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_buf_prof->xon_th = attr->value.u32;
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }
    if (p_buf_prof->ref_cnt &&
        ((attr->id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH) || (attr->id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH)))
    {
        ctc_qos_drop_t ctc_drop;
        ctc_sai_queue_traverse_param_t queue_param;
        sal_memset(&ctc_drop, 0, sizeof(ctc_drop));
        sal_memset(&queue_param, 0, sizeof(queue_param));

        ctc_drop.drop.mode = CTC_QUEUE_DROP_WTD;
        if (p_buf_prof->mode == SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC)
        {
            ctc_drop.drop.max_th[0] = p_buf_prof->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//red
            ctc_drop.drop.max_th[1] = p_buf_prof->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//yellow
            ctc_drop.drop.max_th[2] = p_buf_prof->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//green
            ctc_drop.drop.max_th[3] = 0x44;//critical
        }
        else
        {
            ctc_drop.drop.is_dynamic = 1;
            ctc_drop.drop.drop_factor[0] = p_buf_prof->dynamic_th + 7;
            ctc_drop.drop.drop_factor[1] = p_buf_prof->dynamic_th + 7;
            ctc_drop.drop.drop_factor[2] = p_buf_prof->dynamic_th + 7;
            ctc_drop.drop.drop_factor[3] = p_buf_prof->dynamic_th + 7;
        }

        queue_param.lchip = lchip;
        queue_param.set_type = CTC_SAI_Q_SET_TYPE_BUFFER;
        queue_param.cmp_value = &ctc_oid.value;
        queue_param.p_value = &ctc_drop;
        CTC_SAI_ERROR_RETURN(ctc_sai_queue_traverse_set(&queue_param));
    }

    if (p_buf_prof->ref_cnt &&
        ((attr->id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH) || (attr->id == SAI_BUFFER_PROFILE_ATTR_XON_TH)))
    {
        sai_status_t status = SAI_STATUS_SUCCESS;
        uint8 gchip = 0;
        uint8 index = 0;
        uint8 gport = 0;
        uint16 port_idx = 0;
        uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};
        sai_object_id_t sai_oid;
        sai_attribute_t attr_temp;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
        attr_temp.id = SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE;
        attr_temp.value.oid = buf_prof_id;
        for (port_idx = 0; port_idx < capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; port_idx++)
        {
            gport = CTC_MAP_LPORT_TO_GPORT(gchip, port_idx);
            for (index = 0; index < CTC_SAI_PORT_INGRESS_PG_NUM; index++)
            {
                sai_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, lchip, index, 0, gport);
                status = ctc_sai_buffer_ingress_pg_set_profile(sai_oid, &attr_temp);
                if ((status != SAI_STATUS_SUCCESS) && (status != SAI_STATUS_FAILURE))
                {
                    return status;
                }
            }
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_buffer_get_profile_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_object_id_t buf_prof_id = key->key.object_id;
    ctc_sai_buffer_profile_db_t* p_buf_prof = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_ERROR_RETURN(ctc_sai_oid_get_lchip(buf_prof_id, &lchip));
    p_buf_prof = ctc_sai_db_get_object_property(lchip, buf_prof_id);
    if (NULL == p_buf_prof)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "buffer profile DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_BUFFER_PROFILE_ATTR_POOL_ID:
            attr->value.oid = SAI_NULL_OBJECT_ID;
            break;
        case SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE:
            attr->value.u32 = 0;
            break;
        case SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
            attr->value.s32 = p_buf_prof->mode;
            break;
        case SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
            attr->value.s8 = p_buf_prof->dynamic_th;
            break;
        case SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
            attr->value.u32 = p_buf_prof->static_th;
            break;
        case SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
            attr->value.u32 = p_buf_prof->xoff_th;
            break;
        case SAI_BUFFER_PROFILE_ATTR_XON_TH:
            attr->value.u32 = p_buf_prof->xon_th;
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ingress_pg_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_object_id_t ingress_pg_id = key->key.object_id;
    ctc_sai_ingress_pg_db_t* p_pg = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ingress_pg_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_ingress_pg_get_db(ingress_pg_id, &p_pg));
    switch (attr->id)
    {
        case SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
            CTC_SAI_ERROR_RETURN(ctc_sai_buffer_ingress_pg_set_profile(ingress_pg_id, attr));
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ingress_pg_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_index)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_oid;
    sai_object_id_t ingress_pg_id = key->key.object_id;
    ctc_sai_ingress_pg_db_t* p_pg = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, ingress_pg_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    switch (attr->id)
    {
        case SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
            p_pg = ctc_sai_db_get_object_property(lchip, ingress_pg_id);
            if (NULL == p_pg)
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
                return SAI_STATUS_SUCCESS;
            }
            attr->value.oid = p_pg->buf_prof_id;
            break;
        case SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, ctc_oid.value);
            break;
        case SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
            attr->value.u8 = ctc_oid.sub_type;
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_buffer_wb_reload_profile_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t buf_prof_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, buf_prof_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  buffer_profile_attr_fn_entries[] =
{
        { SAI_BUFFER_PROFILE_ATTR_POOL_ID,
          _ctc_sai_buffer_get_profile_attr,
          NULL},
        { SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE,
          _ctc_sai_buffer_get_profile_attr,
          NULL},
        { SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE,
          _ctc_sai_buffer_get_profile_attr,
          NULL},
        { SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH,
          _ctc_sai_buffer_get_profile_attr,
          _ctc_sai_buffer_set_profile_attr},
        { SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH,
          _ctc_sai_buffer_get_profile_attr,
          _ctc_sai_buffer_set_profile_attr},
        { SAI_BUFFER_PROFILE_ATTR_XOFF_TH,
          _ctc_sai_buffer_get_profile_attr,
          _ctc_sai_buffer_set_profile_attr},
        { SAI_BUFFER_PROFILE_ATTR_XON_TH,
          _ctc_sai_buffer_get_profile_attr,
          _ctc_sai_buffer_set_profile_attr},
        { SAI_BUFFER_PROFILE_ATTR_XON_OFFSET_TH,
          NULL,
          NULL},
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};

static ctc_sai_attr_fn_entry_t  ingress_pg_attr_fn_entries[] =
{
        { SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT,
          _ctc_sai_ingress_pg_get_attr,
          NULL},
        { SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX,
          _ctc_sai_ingress_pg_get_attr,
          NULL},
        { SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE,
          _ctc_sai_ingress_pg_get_attr,
          _ctc_sai_ingress_pg_set_attr},
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};



#define ________INTERNAL_API________

sai_status_t
ctc_sai_buffer_queue_set_profile(sai_object_id_t queue_id, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint8 queue_idx = 0;
    uint8 update_cnt = 1;
    uint32 gport = 0;
    uint32 old_buf_id = 0;
    ctc_object_id_t ctc_oid;
    ctc_qos_drop_t drop;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    ctc_sai_buffer_profile_db_t* p_buf_prof_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    sal_memset(&drop, 0, sizeof(drop));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    queue_idx = (ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST) ? (ctc_oid.value2 + 8) : ctc_oid.value2;

    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Queue DB get failed!\n");
        return SAI_STATUS_FAILURE;
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, attr->value.oid, &ctc_oid);
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Queue lchip[%d] not match to buffer profile lchip[%d]!\n", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        if (p_queue_db->buf_id == ctc_oid.value)
        {
            update_cnt = 0;
        }
        else if (p_queue_db->buf_id && (p_queue_db->buf_id != ctc_oid.value))
        {
            old_buf_id = p_queue_db->buf_id;
        }
        p_buf_prof_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_buf_prof_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer profile DB get failed!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        //config wtd, color red/yellow/green
        drop.drop.mode = CTC_QUEUE_DROP_WTD;
        if (p_buf_prof_db->mode == SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC)
        {
            drop.drop.max_th[0] = p_buf_prof_db->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//red
            drop.drop.max_th[1] = p_buf_prof_db->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//yellow
            drop.drop.max_th[2] = p_buf_prof_db->static_th / CTC_SAI_QOS_BYTES_PER_CELL;//green
            drop.drop.max_th[3] = 0x44;//critical
        }
        else
        {
            drop.drop.is_dynamic = 1;
            drop.drop.drop_factor[0] = p_buf_prof_db->dynamic_th + CTC_SAI_QOS_DROP_FACTOR_SHIFT;
            drop.drop.drop_factor[1] = drop.drop.drop_factor[0];
            drop.drop.drop_factor[2] = drop.drop.drop_factor[0];
            drop.drop.drop_factor[3] = drop.drop.drop_factor[0];
        }
        drop.queue.gport = gport;
        drop.queue.queue_id = queue_idx;
        drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &drop));
        if (update_cnt)
        {
            p_buf_prof_db->ref_cnt++;
            p_queue_db->buf_id = ctc_oid.value;
        }
        if (old_buf_id)
        {
            p_buf_prof_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, lchip, 0, 0, old_buf_id));
            if (NULL == p_buf_prof_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Old Buffer profile DB get failed!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if(p_buf_prof_db->ref_cnt)
            {
                p_buf_prof_db->ref_cnt--;
            }
        }
    }
    else
    {
        if (!p_queue_db->buf_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        p_buf_prof_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, lchip, 0, 0, p_queue_db->buf_id));
        if (NULL == p_buf_prof_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer profile DB get failed!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        drop.drop.mode = CTC_QUEUE_DROP_WTD;
        drop.drop.is_dynamic = 1;
        drop.drop.drop_factor[0] = 0;
        drop.drop.drop_factor[1] = 0;
        drop.drop.drop_factor[2] = 0;
        drop.drop.drop_factor[3] = 0;
        drop.queue.gport = gport;
        drop.queue.queue_id = queue_idx;
        drop.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_drop_scheme(lchip, &drop));
        if(p_buf_prof_db->ref_cnt)
        {
            p_buf_prof_db->ref_cnt--;
        }
        p_queue_db->buf_id = 0;
    }
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_buffer_ingress_pg_set_profile(sai_object_id_t ingress_pg_id, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 gport = 0;
    uint8 index = 0;
    uint8 update_cnt = 1;
    ctc_qos_resrc_t resrc;
    sai_object_id_t old_buf_id = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_ingress_pg_db_t* p_pg_db = NULL;
    ctc_sai_buffer_profile_db_t* p_buf_prof_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    sal_memset(&resrc, 0, sizeof(resrc));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, ingress_pg_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    index = ctc_oid.sub_type;

    p_pg_db = ctc_sai_db_get_object_property(lchip, ingress_pg_id);
    if (NULL == p_pg_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Ingress Priority Group DB get failed!\n");
        return SAI_STATUS_FAILURE;
    }

    resrc.cfg_type = CTC_QOS_RESRC_CFG_FLOW_CTL;
    resrc.u.flow_ctl.gport = gport;
    resrc.u.flow_ctl.priority_class = index;
    resrc.u.flow_ctl.is_pfc = 1;
    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, attr->value.oid, &ctc_oid);
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Ingress PG lchip[%d] not match to buffer profile lchip[%d]!\n", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        if (p_pg_db->buf_prof_id == attr->value.oid)
        {
            update_cnt = 0;
        }
        else if (p_pg_db->buf_prof_id && (p_pg_db->buf_prof_id != attr->value.oid))
        {
            old_buf_id = p_pg_db->buf_prof_id;
        }
        p_buf_prof_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_buf_prof_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer profile DB get failed!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_resrc(lchip, &resrc));
        resrc.u.flow_ctl.xon_thrd = p_buf_prof_db->xon_th / CTC_SAI_QOS_BYTES_PER_CELL;
        resrc.u.flow_ctl.xoff_thrd = p_buf_prof_db->xoff_th / CTC_SAI_QOS_BYTES_PER_CELL;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &resrc));
        if (update_cnt)
        {
            p_buf_prof_db->ref_cnt++;
            p_pg_db->buf_prof_id = attr->value.oid;
        }
        if (old_buf_id)
        {
            p_buf_prof_db = ctc_sai_db_get_object_property(lchip, old_buf_id);
            if (NULL == p_buf_prof_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Old Buffer profile DB get failed!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if(p_buf_prof_db->ref_cnt)
            {
                p_buf_prof_db->ref_cnt--;
            }
        }
    }
    else
    {
        if (!p_pg_db->buf_prof_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        p_buf_prof_db = ctc_sai_db_get_object_property(lchip, p_pg_db->buf_prof_id);
        if (NULL == p_buf_prof_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer profile DB get failed!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_resrc(lchip, &resrc));
        resrc.u.flow_ctl.xon_thrd = 256;
        resrc.u.flow_ctl.xoff_thrd = 224;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_resrc(lchip, &resrc));
        p_buf_prof_db->ref_cnt--;
        p_pg_db->buf_prof_id = SAI_NULL_OBJECT_ID;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_port_get_ingress_pg_num(sai_object_id_t port_id, sai_attribute_t* attr)
{
    CTC_PTR_VALID_CHECK(attr);
    attr->value.u32 = CTC_SAI_PORT_INGRESS_PG_NUM;
    return SAI_STATUS_SUCCESS;
}
sai_status_t
ctc_sai_buffer_port_get_ingress_pg_list(sai_object_id_t port_id, sai_attribute_t* attr)
{
    uint8 ii = 0;
    uint8 lchip = 0;
    uint32 gport = 0;
    ctc_object_id_t ctc_oid;
    sai_object_id_t ingress_pg_list[CTC_SAI_PORT_INGRESS_PG_NUM];

    CTC_PTR_VALID_CHECK(attr);
    CTC_PTR_VALID_CHECK(attr->value.objlist.list);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    for (ii= 0; ii < CTC_SAI_PORT_INGRESS_PG_NUM; ii++)
    {
        ingress_pg_list[ii] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, lchip, ii, 0, gport);
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), (void*)ingress_pg_list, CTC_SAI_PORT_INGRESS_PG_NUM, (void*)(&(attr->value.objlist))));

    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________


static sai_status_t
_ctc_sai_buffer_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_object_id_t             ctc_oid;
    sai_object_id_t             sai_id = bucket_data->oid;
    ctc_sai_dump_grep_param_t*  p_dump   = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file   = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt      = (uint32 *)(p_cb_data->value1);
    uint32                      dump_flag = *((uint32 *)(p_cb_data->value3));

    if (p_dump->key.key.object_id && (sai_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    if (dump_flag)
    {
        ctc_sai_ingress_pg_db_t* p_db = (ctc_sai_ingress_pg_db_t*)bucket_data->data;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, sai_id, &ctc_oid);
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" 0x%.4x %-5d 0x%-16"PRIx64"\n",*cnt,sai_id,ctc_oid.value,ctc_oid.sub_type,p_db->buf_prof_id);

    }
    else
    {
        ctc_sai_buffer_profile_db_t* p_db = (ctc_sai_buffer_profile_db_t*)bucket_data->data;
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-7d %-4d %-10d %-10d %-10d %-10d\n",
                *cnt,sai_id,p_db->ref_cnt, p_db->mode, p_db->dynamic_th,p_db->static_th,p_db->xon_th,p_db->xoff_th);
    }
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


void
ctc_sai_buffer_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    uint32 dump_flag = 0;/*0:buffer profile, 1: ingress pg*/

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;
    sai_cb_data.value3 = &dump_flag;

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Buffer MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_BUFFER_PROFILE))
    {
        /*DUMP buffer profile db*/
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Buffer Profile");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_buffer_profile_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-7s %-4s %-10s %-10s %-10s %-10s\n", "No.","Buf_Prof_Oid","Ref_cnt", "Mode","Dynamic_th","Static_th","Xon_th","Xoff_th");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BUFFER_PROFILE,
                                                (hash_traversal_fn)_ctc_sai_buffer_dump_print_cb, (void*)(&sai_cb_data));
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP))
    {
        /*DUMP Ingress Priority Group db*/
        dump_flag = 1;
        num_cnt = 1;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Ingress Priority Group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_ingress_pg_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-6s %-5s %-18s\n", "No.","Buf_Prof_Oid","Gport", "Index","Buf_Prof_Oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP,
                                                (hash_traversal_fn)_ctc_sai_buffer_dump_print_cb, (void*)(&sai_cb_data));

    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}

#define ________SAI_API________


sai_status_t
ctc_sai_buffer_create_profile_id(
        _Out_ sai_object_id_t *buffer_profile_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    bool mode_set = FALSE;
    sai_object_id_t temp_oid = 0;
    uint32  temp_value = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;
    ctc_sai_buffer_profile_db_t buf_prof;
    ctc_sai_buffer_profile_db_t* p_prof_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(buffer_profile_id);
    *buffer_profile_id = 0;

    sal_memset(&buf_prof, 0, sizeof(buf_prof));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_POOL_ID, &attr_value, &attr_index);
    if ((status == SAI_STATUS_SUCCESS) && (attr_value->oid != SAI_NULL_OBJECT_ID))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "SAI_BUFFER_PROFILE_ATTR_POOL_ID Only Support SAI_NULL_OBJECT_ID!");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error_0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE, &attr_value, &attr_index);
    if ((status == SAI_STATUS_SUCCESS) && (attr_value->u32 != 0))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "SAI_BUFFER_PROFILE_ATTR_RESERVED_BUFFER_SIZE Only Support 0!");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto error_0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Not Found SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE!");
        goto error_0;
    }
    else
    {
        buf_prof.mode = attr_value->s32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (buf_prof.mode != SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC)
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Mode isNot SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC!");
            status = SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_index;
            goto error_0;
        }
        if ((attr_value->s8 < CTC_SAI_BUFFER_FACTOR_1_128) || (attr_value->s8 > CTC_SAI_BUFFER_FACTOR_8))
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH Only Support [-7,3]!");
            status = SAI_STATUS_NOT_SUPPORTED;
            goto error_0;
        }
        buf_prof.dynamic_th = attr_value->s8;
        mode_set = TRUE;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (mode_set || (buf_prof.mode != SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC))
        {
            CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Mode is Not SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC!");
            status = SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_index;
            goto error_0;
        }
        buf_prof.static_th = attr_value->u32;
        mode_set = TRUE;
    }
    if (!mode_set)
    {
        status = SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_index;
        goto error_0;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_XOFF_TH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        buf_prof.xoff_th= attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BUFFER_PROFILE_ATTR_XON_TH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        buf_prof.xon_th= attr_value->u32;
    }
    p_prof_db = mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_buffer_profile_db_t));
    if (p_prof_db == NULL)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "No Memory!");
        status = SAI_STATUS_NO_MEMORY;
        goto error_0;
    }
    sal_memcpy(p_prof_db, &buf_prof, sizeof(ctc_sai_buffer_profile_db_t));
    //opf alloc scheduler id
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &temp_value);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Opf Alloc Buffer profile id Failed!");
        goto error_1;
    }
    temp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BUFFER_PROFILE, lchip, 0, 0, temp_value);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, temp_oid, p_prof_db), status, error_2);
    *buffer_profile_id = temp_oid;
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, temp_value);
error_1:
    mem_free(p_prof_db);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_buffer_remove_profile_id(
        _In_ sai_object_id_t buffer_profile_id)
{

    ctc_object_id_t ctc_object_id;
    ctc_sai_buffer_profile_db_t* p_buf_prof_db = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, buffer_profile_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_BUFFER_PROFILE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_buf_prof_db = ctc_sai_db_get_object_property(lchip, buffer_profile_id);
    if (NULL == p_buf_prof_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer Profile DB Not Found!");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    if (p_buf_prof_db->ref_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Buffer Profile Oid in Use!");
        status = SAI_STATUS_OBJECT_IN_USE;
        goto error_return;
    }
    mem_free(p_buf_prof_db);
    ctc_sai_db_remove_object_property(lchip, buffer_profile_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value);

error_return:
    if (status != SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Remove BUffer Profile Error! buffer_profile_oid:0x%"PRIx64" status=%d", buffer_profile_id, status);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_buffer_set_profile_attribute(
        _In_ sai_object_id_t buffer_profile_id,
        _In_ const sai_attribute_t *attr)
{

    sai_object_key_t key = { .key.object_id = buffer_profile_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, buffer_profile_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_BUFFER_PROFILE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_BUFFER_PROFILE,  buffer_profile_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Failed to set buffer_profile attr:%d", status);
    }
    return status;
}

sai_status_t
ctc_sai_buffer_get_profile_attribute(
        _In_ sai_object_id_t buffer_profile_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = buffer_profile_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, buffer_profile_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_BUFFER_PROFILE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_BUFFER_PROFILE, loop, buffer_profile_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Failed to get buffer_profile attr:%d", status);
    }
    return status;
}

sai_status_t
ctc_sai_ingress_pg_create_group_id(
        _Out_ sai_object_id_t *ingress_priority_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 index = 0;
    uint32 gport = 0;
    sai_object_id_t port_oid = 0;
    sai_object_id_t temp_oid = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_ingress_pg_db_t* p_pg = NULL;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(ingress_priority_group_id);
    *ingress_priority_group_id = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Not Found SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT!");
        goto error_0;
    }
    else
    {
        port_oid = attr_value->oid;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_oid, &ctc_oid);
    if ((ctc_oid.lchip != lchip) || (ctc_oid.type != SAI_OBJECT_TYPE_PORT))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Ingress PG Object Id Type!");
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto error_0;
    }
    gport = ctc_oid.value;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Not Found SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX!");
        goto error_0;
    }
    else
    {
        index = attr_value->u8;
    }
    if (index >= 8)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Index Should be <8 !");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error_0;
    }

    temp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, lchip, index, 0, gport);
    CTC_SAI_ERROR_GOTO(_ctc_sai_ingress_pg_get_db(temp_oid, &p_pg), status, error_0);
    *ingress_priority_group_id = temp_oid;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sai_attribute_t attr_temp;
        attr_temp.id = SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE;
        attr_temp.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(ctc_sai_buffer_ingress_pg_set_profile(*ingress_priority_group_id, &attr_temp), status, error_0);
    }

error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_ingress_pg_remove_group_id(
        _In_ sai_object_id_t ingress_priority_group_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_ingress_pg_db_t* p_pg_db = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ingress_priority_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_pg_db = ctc_sai_db_get_object_property(lchip, ingress_priority_group_id);
    if (NULL == p_pg_db)
    {
        status = SAI_STATUS_SUCCESS;
        goto error_return;
    }
    mem_free(p_pg_db);
    ctc_sai_db_remove_object_property(lchip, ingress_priority_group_id);

error_return:
    if (status != SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Remove Ingress PG Error! ingress_pg_oid:0x%"PRIx64" status=%d", ingress_priority_group_id, status);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


sai_status_t
ctc_sai_ingress_pg_set_attribute(
        _In_ sai_object_id_t ingress_priority_group_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = ingress_priority_group_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ingress_priority_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP,  ingress_pg_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Failed to set ingress_pg attr:%d", status);
    }
    return status;
}

sai_status_t
ctc_sai_ingress_pg_get_attribute(
        _In_ sai_object_id_t ingress_priority_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = ingress_priority_group_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_BUFFER);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, ingress_priority_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Invalid Object Id Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, loop, ingress_pg_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BUFFER, "Failed to get ingress_pg attr:%d", status);
    }
    return status;
}

sai_status_t
ctc_sai_buffer_create_pool_id(
        _Out_ sai_object_id_t *buffer_pool_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_remove_pool_id(
        _In_ sai_object_id_t buffer_pool_id)
{
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_buffer_set_pool_attribute(
        _In_ sai_object_id_t buffer_pool_id,
        _In_ const sai_attribute_t *attr)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_get_pool_attribute(
        _In_ sai_object_id_t buffer_pool_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_get_pool_stats(
        _In_ sai_object_id_t buffer_pool_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_get_pool_stats_ext(
        _In_ sai_object_id_t buffer_pool_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_clear_pool_stats(
        _In_ sai_object_id_t buffer_pool_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_ingress_pg_get_stats(
        _In_ sai_object_id_t ingress_priority_group_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _Out_ uint64_t *counters)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_ingress_pg_get_stats_ext(
        _In_ sai_object_id_t ingress_priority_group_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids,
        _In_ sai_stats_mode_t mode,
        _Out_ uint64_t *counters)
{
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_ingress_pg_clear_stats(
        _In_ sai_object_id_t ingress_priority_group_id,
        _In_ uint32_t number_of_counters,
        _In_ const sai_stat_id_t *counter_ids)
{
    return SAI_STATUS_SUCCESS;
}


sai_buffer_api_t g_ctc_sai_buffer_api = {
    ctc_sai_buffer_create_pool_id,
    ctc_sai_buffer_remove_pool_id,
    ctc_sai_buffer_set_pool_attribute,
    ctc_sai_buffer_get_pool_attribute,
    ctc_sai_buffer_get_pool_stats,
    ctc_sai_buffer_get_pool_stats_ext,
    ctc_sai_buffer_clear_pool_stats,
    ctc_sai_ingress_pg_create_group_id,
    ctc_sai_ingress_pg_remove_group_id,
    ctc_sai_ingress_pg_set_attribute,
    ctc_sai_ingress_pg_get_attribute,
    ctc_sai_ingress_pg_get_stats,
    ctc_sai_ingress_pg_get_stats_ext,
    ctc_sai_ingress_pg_clear_stats,
    ctc_sai_buffer_create_profile_id,
    ctc_sai_buffer_remove_profile_id,
    ctc_sai_buffer_set_profile_attribute,
    ctc_sai_buffer_get_profile_attribute
};

sai_status_t
ctc_sai_buffer_api_init()
{
    ctc_sai_register_module_api(SAI_API_BUFFER, (void*)&g_ctc_sai_buffer_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_buffer_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_BUFFER;
    wb_info.data_len = sizeof(ctc_sai_buffer_profile_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_buffer_wb_reload_profile_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_BUFFER_PROFILE, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_BUFFER;
    wb_info.data_len = sizeof(ctc_sai_ingress_pg_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}


