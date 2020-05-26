
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_port.h"
#include "ctc_sai_queue.h"


static sai_status_t
_ctc_sai_scheduler_map_attr_to_db(const sai_attribute_t* attr_list, uint32 attr_count, ctc_sai_scheduler_db_t* p_scheduler)
{
    sai_status_t status = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;
    uint8  sch_type_valid = 0;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (attr_value->s32 == SAI_SCHEDULING_TYPE_WRR)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not supported algorithm type value:%d\n", attr_value->s32);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_scheduler->sch_type = attr_value->s32;
        sch_type_valid = 1;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (!sch_type_valid || (p_scheduler->sch_type != SAI_SCHEDULING_TYPE_DWRR))
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Weight need DWRR algorithm!\n");
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_scheduler->weight = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_METER_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (attr_value->s32 != SAI_METER_TYPE_BYTES)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not supported meter type value:%d\n", attr_value->s32);
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_scheduler->min_rate = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_scheduler->min_burst_rate = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_scheduler->max_rate = attr_value->u64;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_scheduler->max_burst_rate = attr_value->u64;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_queue_set_ctc_sched(uint8 lchip, uint32 gport, uint8 ctc_queue_id, uint8 class_id, uint8 weight)
{
    ctc_qos_sched_t sched;
    sal_memset(&sched, 0, sizeof(sched));

    sched.type = CTC_QOS_SCHED_QUEUE;
    sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    sched.sched.queue_sched.queue.gport = gport;
    sched.sched.queue_sched.queue.queue_id = ctc_queue_id;

    if (ctcs_get_chip_type(lchip) < CTC_CHIP_DUET2)
    {//Support for GG
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_CONFIRM_CLASS;
        sched.sched.queue_sched.confirm_class = class_id;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }
    sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
    sched.sched.queue_sched.exceed_class = class_id;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));

    if (weight)
    {
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_WEIGHT;
        sched.sched.queue_sched.exceed_weight = weight;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_queue_map_scheduler(uint8 lchip, uint32 gport, uint8 ctc_queue_id, ctc_sai_scheduler_db_t* p_scheduler, bool enable)
{
    uint8 queue_idx = 0;
    uint8 new_wdrr_class = 0xFF;
    ctc_sai_queue_db_t* p_queue = NULL;
    ctc_sai_scheduler_db_t* p_sched_temp = NULL;
    sai_object_id_t queue_oid;
    ctc_qos_sched_t sched;
    ctc_qos_shape_t shape;

    sal_memset(&shape, 0, sizeof(shape));
    shape.type = CTC_QOS_SHAPE_QUEUE;
    shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    shape.shape.queue_shape.queue.queue_id = ctc_queue_id;
    shape.shape.queue_shape.queue.gport = gport;

    if (!enable)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_set_ctc_sched(lchip, gport, ctc_queue_id, ctc_queue_id, 1));
        shape.shape.queue_shape.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_shape(lchip, &shape));
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_PTR_VALID_CHECK(p_scheduler);

    if (SAI_SCHEDULING_TYPE_STRICT == p_scheduler->sch_type)
    {//sp

        CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_set_ctc_sched(lchip, gport, ctc_queue_id, ctc_queue_id, 1));
        //need config wdrr
        sal_memset(&sched, 0, sizeof(sched));
        sched.type = CTC_QOS_SCHED_QUEUE;
        sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        sched.sched.queue_sched.queue.gport = gport;
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
        for (queue_idx = ctc_queue_id + 1; queue_idx < CTC_QOS_BASIC_Q_NUM; queue_idx++)
        {
            //get exceed_class
            sched.sched.queue_sched.queue.queue_id = queue_idx;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_sched(lchip, &sched));
            if (sched.sched.queue_sched.exceed_class != ctc_queue_id)
            {
                continue;
            }
            new_wdrr_class = (new_wdrr_class != 0xFF) ? new_wdrr_class : queue_idx;
            CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_set_ctc_sched(lchip, gport, queue_idx, new_wdrr_class, 0));
        }
    }
    else
    {//wdrr
        //cfg weight
        CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_set_ctc_sched(lchip, gport, ctc_queue_id, ctc_queue_id , p_scheduler->weight));
        for (queue_idx = 0; queue_idx < CTC_QOS_BASIC_Q_NUM; queue_idx++)
        {
            queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_ALL, queue_idx, gport);
            p_queue = ctc_sai_db_get_object_property(lchip, queue_oid);
            if (!p_queue || !p_queue->sch_id)
            {
                queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_UNICAST, queue_idx, gport);
                p_queue = ctc_sai_db_get_object_property(lchip, queue_oid);
                if (!p_queue || !p_queue->sch_id)
                {
                    continue;
                }
            }
            p_sched_temp = ctc_sai_db_get_object_property(lchip,
                      ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_queue->sch_id));
            if (NULL == p_sched_temp)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Critical error! Not found the DB!!!\n");
                return SAI_STATUS_FAILURE;
            }
            if (p_sched_temp->sch_type == SAI_SCHEDULING_TYPE_DWRR)
            {
                new_wdrr_class = (new_wdrr_class == 0xFF) ? ((ctc_queue_id < queue_idx) ? ctc_queue_id : queue_idx) : new_wdrr_class;
                //if (ctc_queue_id < new_wdrr_class)
                {//need to change the exceed class
                    CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_set_ctc_sched(lchip, gport, queue_idx, new_wdrr_class, 0));
                }
            }
        }
    }

    shape.type = CTC_QOS_SHAPE_QUEUE;
    shape.shape.queue_shape.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    shape.shape.queue_shape.queue.queue_id = ctc_queue_id;
    shape.shape.queue_shape.queue.gport = gport;
    if(p_scheduler->max_rate)
    {
        shape.shape.queue_shape.enable = 1;
        shape.shape.queue_shape.cir = p_scheduler->min_rate * 8 / 1000;
        shape.shape.queue_shape.pir = p_scheduler->max_rate * 8 / 1000;
        /*GG is not supported cbs or pbs*/
        shape.shape.queue_shape.pbs = p_scheduler->max_burst_rate * 8 / 1000;
        shape.shape.queue_shape.cbs = p_scheduler->min_burst_rate * 8 / 1000;
    }
    else
    {
        shape.shape.queue_shape.enable = 0;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_shape(lchip, &shape));

    return SAI_STATUS_SUCCESS;
}

typedef enum ctc_sai_sched_iter_ret_s {
    CTC_SAI_SCHED_ITER_NEXT,
    CTC_SAI_SCHED_ITER_FIND,
    CTC_SAI_SCHED_ITER_STOP
} ctc_sai_sched_iter_ret_t;

static ctc_sai_sched_iter_ret_t
_ctc_sai_sched_group_update_sched_profile(uint8 lchip, sai_object_id_t node, sai_object_id_t sched_id, sai_object_id_t* parent_id)
{
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    p_sched_group_db = ctc_sai_db_get_object_property(lchip, node);
    if (NULL == p_sched_group_db)
    {
        return CTC_SAI_SCHED_ITER_STOP;
    }
    if (p_sched_group_db->sched_id == sched_id)
    {
        return CTC_SAI_SCHED_ITER_FIND;
    }
    *parent_id = p_sched_group_db->parent_id;
    return CTC_SAI_SCHED_ITER_NEXT;
}

static sai_status_t
_ctc_sai_queue_update_sched_group_foreach(uint8 lchip, sai_object_id_t queue_id, sai_object_id_t sched_id)
{
    sai_attribute_t attr;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    ctc_sai_sched_iter_ret_t ret = CTC_SAI_SCHED_ITER_STOP;
    sai_object_id_t node;
    sai_object_id_t parent_node;

    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Queue DB not Found!\n");
        return SAI_STATUS_FAILURE;
    }
    if (!p_queue_db->sch_grp)
    {
        return SAI_STATUS_SUCCESS;
    }

    node = p_queue_db->sch_grp;
    while (CTC_SAI_SCHED_ITER_NEXT == (ret = _ctc_sai_sched_group_update_sched_profile(lchip, node, sched_id, &parent_node)))
    {
        node = parent_node;
        parent_node = SAI_NULL_OBJECT_ID;
    }
    if (ret == CTC_SAI_SCHED_ITER_FIND)
    {
        sal_memset(&attr, 0, sizeof(attr));
        attr.id = SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE;
        attr.value.oid = p_queue_db->sch_grp;
        CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_group_queue_set_scheduler(queue_id, &attr));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_object_id_t sched_id = key->key.object_id;
    sai_object_id_t port_oid;
    sai_object_id_t queue_oid;
    ctc_object_id_t ctc_oid;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};
    ctc_sai_scheduler_db_t* p_scheduler= NULL;
    ctc_sai_port_db_t* p_port_db= NULL;
    ctc_sai_queue_db_t* p_queue_db= NULL;
    uint16 port_idx = 0;
    uint8  queue_idx = 0;
    uint8  gchip = 0;
    sai_attribute_t attr_temp;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER, sched_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    p_scheduler = ctc_sai_db_get_object_property(lchip, sched_id);
    if (NULL == p_scheduler)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
            if (p_scheduler->sch_type == attr->value.s32)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->sch_type = attr->value.s32;
            break;
        case SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
            if (p_scheduler->weight == attr->value.u8)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->weight = attr->value.u8;
            break;
        case SAI_SCHEDULER_ATTR_METER_TYPE:
            return SAI_STATUS_SUCCESS;
            break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
            if (p_scheduler->min_rate == attr->value.u64)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->min_rate = attr->value.u64;
            break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
            if (p_scheduler->min_burst_rate == attr->value.u64)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->min_burst_rate = attr->value.u64;
            break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
            if (p_scheduler->max_rate == attr->value.u64)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->max_rate = attr->value.u64;
            break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
            if (p_scheduler->max_burst_rate == attr->value.u64)
            {
                return SAI_STATUS_SUCCESS;
            }
            p_scheduler->max_burst_rate = attr->value.u64;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "scheduler attribute not implement\n");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    for (port_idx = 0; port_idx < capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; port_idx++)
    {
        port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, CTC_MAP_LPORT_TO_GPORT(gchip, port_idx));
        p_port_db = ctc_sai_db_get_object_property(lchip, port_oid);
        if (p_port_db && (p_port_db->sched_id == ctc_oid.value))
        {
            attr_temp.id = SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID;
            attr_temp.value.oid = sched_id;
            CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_port_set_scheduler(port_oid, &attr_temp));
        }
        for (queue_idx = 0; queue_idx < CTC_QOS_BASIC_Q_NUM; queue_idx++)
        {
            queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_ALL, queue_idx, CTC_MAP_LPORT_TO_GPORT(gchip, port_idx));
            p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
            if (!p_queue_db || !p_queue_db->sch_id)
            {
                queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_UNICAST, queue_idx, CTC_MAP_LPORT_TO_GPORT(gchip, port_idx));
                p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                if (!p_queue_db || !p_queue_db->sch_id)
                {
                    continue;
                }
            }
            if (p_queue_db->sch_id == ctc_oid.value)
            {
                attr_temp.id = SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID;
                attr_temp.value.oid = sched_id;
                CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_queue_set_scheduler(queue_oid, &attr_temp));
            }
            if ((attr->id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE) || ((attr->id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT)))
            {
                CTC_SAI_ERROR_RETURN(_ctc_sai_queue_update_sched_group_foreach(lchip, queue_oid, sched_id));
            }
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_object_id_t sched_id = key->key.object_id;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    uint8 lchip = 0;

    CTC_ERROR_RETURN(ctc_sai_oid_get_lchip(sched_id, &lchip));
    p_scheduler_db = ctc_sai_db_get_object_property(lchip, sched_id);
    if (NULL == p_scheduler_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "scheduler DB not found!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
            attr->value.s32 = p_scheduler_db->sch_type;
            break;
        case SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
            attr->value.u8 = p_scheduler_db->weight;
            break;
        case SAI_SCHEDULER_ATTR_METER_TYPE:
            attr->value.s32 = SAI_METER_TYPE_BYTES;
            break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
            attr->value.u64 = p_scheduler_db->min_rate;
            break;
        case SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
            attr->value.u64 = p_scheduler_db->min_burst_rate;
            break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
            attr->value.u64 = p_scheduler_db->max_rate;
            break;
        case SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
            attr->value.u64 = p_scheduler_db->max_burst_rate;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "scheduler attribute not implement\n");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t scheduler_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER, scheduler_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
}


static ctc_sai_attr_fn_entry_t  scheduler_attr_fn_entries[] =
{
        {SAI_SCHEDULER_ATTR_SCHEDULING_TYPE,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        {SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        {SAI_SCHEDULER_ATTR_METER_TYPE,
            _ctc_sai_scheduler_get_attr,
            NULL},
        {SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        {SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        {SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        {SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE,
            _ctc_sai_scheduler_get_attr,
            _ctc_sai_scheduler_set_attr},
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};


#define ________INTERNAL_API________

sai_status_t
ctc_sai_scheduler_port_set_scheduler(sai_object_id_t port_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint8 update_cnt = 1;
    uint32 new_sched_id = 0;
    uint32 old_sched_id = 0;
    uint32 gport = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_qos_shape_t shape;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    sal_memset(&shape, 0, sizeof(shape));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(port_id, &gport));

    p_port_db = ctc_sai_db_get_object_property(lchip, port_id);
    if (NULL == p_port_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Port DB not Found!\n");
        return SAI_STATUS_FAILURE;
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {//enable
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr->value.oid, &ctc_oid);
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "port lchip[%d] not match to scheduler lchip[%d]!\n", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }

        new_sched_id = ctc_oid.value;
        if (p_port_db->sched_id == ctc_oid.value)
        {
            update_cnt = 0;
        }
        else if (p_port_db->sched_id && (p_port_db->sched_id != ctc_oid.value))
        {//is update
            old_sched_id = p_port_db->sched_id;
        }

        p_scheduler_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        shape.type = CTC_QOS_SHAPE_PORT;
        shape.shape.port_shape.gport = gport;
        if(p_scheduler_db->max_rate)
        {
            shape.shape.port_shape.enable = 1;
            shape.shape.port_shape.pir = p_scheduler_db->max_rate * 8 / 1000;
            shape.shape.port_shape.pbs = p_scheduler_db->max_burst_rate * 8 / 1000;
        }
        else
        {
            shape.shape.port_shape.enable = 0;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_shape(lchip, &shape));
        if (update_cnt)
        {
            p_port_db->sched_id = new_sched_id;
            p_scheduler_db->ref_cnt++;
        }
        if (old_sched_id)
        {//update old db
            p_scheduler_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, old_sched_id));
            if (NULL == p_scheduler_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Found old Scheduler DB!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if (p_scheduler_db->ref_cnt)
            {
                p_scheduler_db->ref_cnt--;
            }
        }
    }
    else
    {//disable
        if (!p_port_db->sched_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        p_scheduler_db = ctc_sai_db_get_object_property
                        (lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_port_db->sched_id));
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        shape.type = CTC_QOS_SHAPE_PORT;
        shape.shape.port_shape.gport = gport;
        shape.shape.port_shape.enable = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_shape(lchip, &shape));
        p_port_db->sched_id = 0;
        if (p_scheduler_db->ref_cnt)
        {
            p_scheduler_db->ref_cnt--;
        }
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_scheduler_queue_set_scheduler(sai_object_id_t queue_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint32 new_sched_id = 0;
    uint32 old_sched_id = 0;
    uint32 gport = 0;
    uint8  ctc_queue_id = 0;
    uint8 update_cnt = 1;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    ctc_qos_sched_t sched;
    ctc_qos_shape_t shape;
    ctc_sai_queue_db_t* p_queue = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    CTC_SAI_LOG_INFO(SAI_API_SCHEDULER, "Queue oid:0x%"PRIx64"\n", queue_id);
    sal_memset(&sched, 0, sizeof(sched));
    sal_memset(&shape, 0, sizeof(shape));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    if (SAI_QUEUE_TYPE_MULTICAST == ctc_oid.sub_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Supported Mcast queue type!\n");
        return SAI_STATUS_NOT_SUPPORTED;
    }
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    ctc_queue_id = ctc_oid.value2;

    p_queue = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Queue DB get failed!\n");
        return SAI_STATUS_FAILURE;
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {//enable
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr->value.oid, &ctc_oid);
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "queue lchip[%d] not match to scheduler lchip[%d]!\n", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }

        new_sched_id = ctc_oid.value;
        if (p_queue->sch_id == ctc_oid.value)
        {
            update_cnt = 0;
        }
        else if (p_queue->sch_id && (p_queue->sch_id != ctc_oid.value))
        {
            old_sched_id = p_queue->sch_id;
        }
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if (update_cnt)
        {
            p_queue->sch_id = new_sched_id;
        }
        CTC_SAI_ERROR_GOTO(_ctc_sai_scheduler_queue_map_scheduler(lchip, gport, ctc_queue_id, p_scheduler_db, TRUE), status, error_0);
        if (update_cnt)
        {
            p_scheduler_db->ref_cnt++;
        }
        if (old_sched_id)
        {//update old db
            p_scheduler_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, old_sched_id));
            if (NULL == p_scheduler_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Found old Scheduler DB!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if (p_scheduler_db->ref_cnt)
            {
                p_scheduler_db->ref_cnt--;
            }
        }
    }
    else
    {//disable
        if (!p_queue->sch_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_queue_map_scheduler(lchip, gport, ctc_queue_id, NULL, FALSE));
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_queue->sch_id));
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Found old Scheduler DB!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if (p_scheduler_db->ref_cnt)
        {
            p_scheduler_db->ref_cnt--;
        }
        p_queue->sch_id = 0;
    }
    return SAI_STATUS_SUCCESS;
error_0:
    if (update_cnt)
    {
        p_queue->sch_id = 0;
    }
    return status;
}

sai_status_t
ctc_sai_scheduler_group_set_scheduler(sai_object_id_t sch_group_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint8 update_cnt = 1;
    sai_object_id_t new_sched_id = 0;
    sai_object_id_t old_sched_id = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    sai_object_id_t queue_oid;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};
    ctc_sai_queue_db_t* p_queue_db= NULL;
    uint16 port_idx = 0;
    uint8  queue_idx = 0;
    uint8  gchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(attr);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sch_group_id, &lchip));
    p_sched_group_db = ctc_sai_db_get_object_property(lchip, sch_group_id);
    if (NULL == p_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Scheduler group DB get failed!\n");
        return SAI_STATUS_FAILURE;
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {//enable
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER, attr->value.oid, &ctc_oid);
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Scheduler group lchip[%d] not match to scheduler lchip[%d]!\n", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));

        new_sched_id = attr->value.oid;
        if (p_sched_group_db->sched_id == attr->value.oid)
        {
            update_cnt = 0;
        }
        else if ((p_sched_group_db->sched_id != SAI_NULL_OBJECT_ID) && (p_sched_group_db->sched_id != attr->value.oid))
        {
            old_sched_id = p_sched_group_db->sched_id;
        }
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if (update_cnt)
        {
            p_sched_group_db->sched_id = new_sched_id;
            p_scheduler_db->ref_cnt++;
        }

        for (port_idx = 0; port_idx < capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; port_idx++)
        {
            for (queue_idx = 0; queue_idx < CTC_QOS_BASIC_Q_NUM; queue_idx++)
            {
                queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_ALL, queue_idx, CTC_MAP_LPORT_TO_GPORT(gchip, port_idx));
                p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                if (!p_queue_db || !p_queue_db->sch_grp)
                {
                    queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_UNICAST, queue_idx, CTC_MAP_LPORT_TO_GPORT(gchip, port_idx));
                    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                    if (!p_queue_db || !p_queue_db->sch_grp)
                    {
                        continue;
                    }
                }
                CTC_SAI_ERROR_RETURN(_ctc_sai_queue_update_sched_group_foreach(lchip, queue_oid, new_sched_id));
            }
        }

        if (old_sched_id)
        {//update old db
            p_scheduler_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, old_sched_id));
            if (NULL == p_scheduler_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Found old Scheduler DB!\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if (p_scheduler_db->ref_cnt)
            {
                p_scheduler_db->ref_cnt--;
            }
        }
    }
    else
    {//disable
        if (!p_sched_group_db->sched_id)
        {
            return SAI_STATUS_SUCCESS;
        }
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, p_sched_group_db->sched_id);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Not Found old Scheduler DB!\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if (p_scheduler_db->ref_cnt)
        {
            p_scheduler_db->ref_cnt--;
        }
        p_sched_group_db->sched_id = SAI_NULL_OBJECT_ID;
    }
    return SAI_STATUS_SUCCESS;
}

#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_scheduler_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             sched_id = bucket_data->oid;
    ctc_sai_scheduler_db_t*     p_db     = (ctc_sai_scheduler_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump   = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file   = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt      = (uint32 *)(p_cb_data->value1);

    if (p_dump->key.key.object_id && (sched_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" %-7d %-4d %-6d %-10d %-10d %-10d %-10d\n",
                        *cnt,sched_id,p_db->ref_cnt, p_db->sch_type,p_db->weight,
                        p_db->min_rate,p_db->min_burst_rate,p_db->max_rate,p_db->max_burst_rate);
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


void
ctc_sai_scheduler_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Scheduler MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_SCHEDULER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Scheduler");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_scheduler_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-7s %-4s %-6s %-10s %-10s %-10s %-10s\n", "No.","Sched_Oid","Ref_cnt", "Type","Weight","Cir","Cbs","Pir","Pbs");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_SCHEDULER,
                                                (hash_traversal_fn)_ctc_sai_scheduler_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}

#define ________SAI_API________

sai_status_t
ctc_sai_scheduler_create_scheduler_id(
        _Out_ sai_object_id_t *scheduler_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    sai_object_id_t scheduler_oid;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    uint32  ctc_scheduler_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(scheduler_id);
    *scheduler_id = 0;

    sal_memset(&scheduler_oid, 0, sizeof(scheduler_oid));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    p_scheduler_db = (ctc_sai_scheduler_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_scheduler_db_t));
    if (NULL == p_scheduler_db)
    {
        status = SAI_STATUS_NO_MEMORY;
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "No memory!\n");
        goto error_0;
    }
    sal_memset(p_scheduler_db, 0, sizeof(ctc_sai_scheduler_db_t));

    /*default value*/
    p_scheduler_db->sch_type = SAI_SCHEDULING_TYPE_DWRR;
    p_scheduler_db->weight = 1;

    CTC_SAI_ERROR_GOTO(_ctc_sai_scheduler_map_attr_to_db(attr_list, attr_count, p_scheduler_db), status, error_1);

    //opf alloc scheduler id
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_scheduler_id);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Opf Alloc Scheduler id Failed!\n");
        goto error_1;
    }
    scheduler_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, ctc_scheduler_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, scheduler_oid, p_scheduler_db), status, error_2);
    *scheduler_id = scheduler_oid;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_scheduler_id);
error_1:
    mem_free(p_scheduler_db);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_scheduler_remove_scheduler_id(
        _In_ sai_object_id_t scheduler_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Invalid Object Type!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_scheduler_db = ctc_sai_db_get_object_property(lchip, scheduler_id);
    if (NULL == p_scheduler_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "DB not Found!\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    if (p_scheduler_db->ref_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Object In use! ref_cnt:%d\n",p_scheduler_db->ref_cnt);
        status = SAI_STATUS_OBJECT_IN_USE;
        goto error_return;
    }

    mem_free(p_scheduler_db);
    ctc_sai_db_remove_object_property(lchip, scheduler_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value);

error_return:
    if (status != SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Remove Scheduler Error! scheduler_oid:0x%"PRIx64" status=%d\n", scheduler_id, status);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


sai_status_t
ctc_sai_scheduler_set_attribute(
        _In_ sai_object_id_t scheduler_id,
        _In_ const sai_attribute_t *attr)
{

    sai_object_key_t key = { .key.object_id = scheduler_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Invalid Object Type!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_SCHEDULER,  scheduler_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Failed to set scheduler attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_scheduler_get_attribute(
        _In_ sai_object_id_t scheduler_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{

    sai_object_key_t key ={ .key.object_id = scheduler_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Invalid Object Type!\n");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_SCHEDULER, loop, scheduler_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER, "Failed to get scheduler attr:%d\n", status);
    }
    return status;
}


sai_scheduler_api_t g_ctc_sai_scheduler_api = {
    ctc_sai_scheduler_create_scheduler_id,
    ctc_sai_scheduler_remove_scheduler_id,
    ctc_sai_scheduler_set_attribute,
    ctc_sai_scheduler_get_attribute
};

sai_status_t
ctc_sai_scheduler_api_init()
{
    ctc_sai_register_module_api(SAI_API_SCHEDULER, (void*)&g_ctc_sai_scheduler_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_scheduler_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_SCHEDULER;
    wb_info.data_len = sizeof(ctc_sai_scheduler_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_scheduler_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_SCHEDULER, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

