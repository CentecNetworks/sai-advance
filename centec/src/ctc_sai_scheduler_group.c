#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_port.h"



#define CTC_SAI_SCHED_LEVEL_CHILDS(level)\
        ((level == 0) ?  CTC_SAI_SCHED_PORT_GRP_NUM : ((level == 1) ? CTC_SAI_SCHED_SERVICE_GRP_NUM : CTC_SAI_SCHED_MAX_GRP_NUM))

#define CTC_SAI_SCHED_LEVEL_GROUPS(level)\
        ((level == 0) ?  1 : ((level == 1) ? CTC_SAI_SCHED_PORT_GRP_NUM : ((level == 2)? CTC_SAI_SCHED_MAX_GRP_NUM : CTC_SAI_SCHED_MAX_GRP_NUM)))

#define CTC_SAI_SCHED_CHAN_NODE_DEFAULT 2
#define CTC_SAI_SCHED_ETS_NODE_DEFAULT 2

#define CTC_SAI_SCHED_NODE_IN_EXT_GROUP_DEFAULT 8
#define CTC_SAI_SCHED_NODE_IN_EXT_GROUP_TM 8

#define CTC_SAI_MAX_SERVICE_NUM_TM 384
#define CTC_SAI_MAX_SERVICE_NUM_DEAFULT 384


sai_status_t
_ctc_sai_scheduler_group_get_db(sai_object_id_t sched_group_id, ctc_sai_sched_group_db_t** p_sched_group)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_oid;
    ctc_sai_sched_group_db_t* p_sched_group_temp = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_oid);
    if (ctc_oid.type != SAI_OBJECT_TYPE_SCHEDULER_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Queue oid type!");
        return SAI_STATUS_INVALID_OBJECT_TYPE;
    }
    lchip = ctc_oid.lchip;

    p_sched_group_temp = ctc_sai_db_get_object_property(lchip, sched_group_id);
    if (NULL == p_sched_group_temp)
    {
        p_sched_group_temp = (ctc_sai_sched_group_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_sched_group_db_t));
        if (NULL == p_sched_group_temp)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "No Memory!");
            return SAI_STATUS_NO_MEMORY;
        }
        sal_memset(p_sched_group_temp, 0, sizeof(ctc_sai_sched_group_db_t));
        CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, sched_group_id, p_sched_group_temp), status, error_return);
    }
    *p_sched_group = p_sched_group_temp;
    return SAI_STATUS_SUCCESS;

error_return:
    mem_free(p_sched_group_temp);
    return status;
}


static bool
_ctc_sai_scheduler_group_get_free_group_index(uint8 lchip, uint32 gport, uint8 level, uint16 service_id, uint16* index)
{
    uint8 ii = 0;
    bool find = FALSE;
    sai_object_id_t sched_group_oid;
    uint16 group_index_base = 0;

    if (NULL == index)
    {
        return FALSE;
    }
    
    group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, service_id);
    
    for (ii = 0; ii < CTC_SAI_SCHED_LEVEL_GROUPS(level); ii++)
    {
        sched_group_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, level, ii+group_index_base, gport);
        if (NULL == ctc_sai_db_get_object_property(lchip, sched_group_oid))
        {
            find = TRUE;
            *index = ii+group_index_base;
            break;
        }
    }
    
    return find;
}

static sai_status_t
_ctc_sai_scheduler_group_add_or_del_child(uint8 lchip, sai_object_id_t parent_id, sai_object_id_t child_id, bool is_add)
{
    uint8 ii = 0;
    ctc_object_id_t ctc_parent_oid;
    ctc_object_id_t ctc_child_oid;
    sai_object_type_t obj_type = SAI_OBJECT_TYPE_NULL;
    ctc_sai_sched_group_db_t* p_sched_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_LOG_INFO(SAI_API_SCHEDULER_GROUP, "lchip:%d parent:0x%"PRIx64" child:0x%"PRIx64" op:%s",lchip,parent_id,child_id,is_add?"Add":"Del");
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_type(parent_id, &obj_type));
    if (is_add)
    {
        if (SAI_OBJECT_TYPE_SCHEDULER_GROUP == obj_type)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, parent_id, &ctc_parent_oid);
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, child_id, &ctc_child_oid);
            if ((ctc_child_oid.type != SAI_OBJECT_TYPE_QUEUE)&& (ctc_parent_oid.sub_type >= ctc_child_oid.sub_type))
            {//invalid parent level
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Child Level[%d] Add to Parent Level[%d]!", ctc_child_oid.sub_type, ctc_parent_oid.sub_type);
                return SAI_STATUS_INVALID_PARAMETER;
            }
            p_sched_group = ctc_sai_db_get_object_property(lchip, parent_id);
            if (NULL == p_sched_group)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Parent Node Not Found, oid:0x"PRIx64"!", parent_id);
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            for (ii = 0; ii < p_sched_group->child_cnt; ii++)
            {
                if (p_sched_group->child_list[ii] == child_id)
                {
                    return SAI_STATUS_SUCCESS;
                }
            }
            if (p_sched_group->child_cnt >= p_sched_group->max_childs)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Parent Child Exceed! child count:%d", p_sched_group->child_cnt);
                return SAI_STATUS_TABLE_FULL;
            }
            if (0 == p_sched_group->child_cnt)
            {
               p_sched_group->child_type = ctc_child_oid.type;
            }
            else if (p_sched_group->child_type != ctc_child_oid.type)
            {//diff child type not support
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Child Type Not Match! new type[%d], exist type[%d]", ctc_child_oid.type, p_sched_group->child_type);
                return SAI_STATUS_INVALID_PARAMETER;
            }

            p_sched_group->child_list[p_sched_group->child_cnt++] = child_id;
        }
        else if (SAI_OBJECT_TYPE_PORT == obj_type)
        {
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Parent Object Type[%d]", obj_type);
            return SAI_STATUS_INVALID_OBJECT_TYPE;
        }
    }
    else
    {
        if (SAI_OBJECT_TYPE_SCHEDULER_GROUP == obj_type)
        {
            p_sched_group = ctc_sai_db_get_object_property(lchip, parent_id);
            if (NULL == p_sched_group)
            {
                return SAI_STATUS_SUCCESS;
            }
            for (ii = 0; ii < p_sched_group->child_cnt; ii++)
            {
                if (p_sched_group->child_list[ii] == child_id)
                {
                    break;
                }
            }
            if (ii != p_sched_group->child_cnt)
            {
                p_sched_group->child_cnt--;
                sal_memcpy(&p_sched_group->child_list[ii], &p_sched_group->child_list[p_sched_group->child_cnt], sizeof(sai_object_id_t));
            }
        }
        else if (SAI_OBJECT_TYPE_PORT == obj_type)
        {
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Parent Object Type[%d]", obj_type);
            return SAI_STATUS_INVALID_OBJECT_TYPE;
        }
    }
    return SAI_STATUS_SUCCESS;
}

typedef enum ctc_sai_sched_grp_iter_ret_s {
    CTC_SAI_SCHED_GRP_ITER_NEXT,
    CTC_SAI_SCHED_GRP_ITER_FIND,
    CTC_SAI_SCHED_GRP_ITER_STOP
} ctc_sai_sched_grp_iter_ret_t;

static ctc_sai_sched_grp_iter_ret_t
_ctc_sai_sched_group_find_sched_group(uint8 lchip, sai_object_id_t node, sai_object_id_t sched_group_id, sai_object_id_t* parent_id)
{
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    p_sched_group_db = ctc_sai_db_get_object_property(lchip, node);
    if (NULL == p_sched_group_db)
    {
        return CTC_SAI_SCHED_GRP_ITER_STOP;
    }
    if (node == sched_group_id)
    {
        return CTC_SAI_SCHED_GRP_ITER_FIND;
    }
    *parent_id = p_sched_group_db->parent_id;
    return CTC_SAI_SCHED_GRP_ITER_NEXT;
}

static sai_status_t
_ctc_sai_sched_group_queue_update_sched_group_foreach(uint8 lchip, sai_object_id_t queue_id, sai_object_id_t sched_group_id)
{
    sai_attribute_t attr;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    ctc_sai_sched_grp_iter_ret_t ret = CTC_SAI_SCHED_GRP_ITER_STOP;
    sai_object_id_t node;
    sai_object_id_t parent_node;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
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
    while (CTC_SAI_SCHED_GRP_ITER_NEXT == (ret = _ctc_sai_sched_group_find_sched_group(lchip, node, sched_group_id, &parent_node)))
    {
        node = parent_node;
        parent_node = SAI_NULL_OBJECT_ID;
    }
    if (ret == CTC_SAI_SCHED_GRP_ITER_FIND)
    {
        sal_memset(&attr, 0, sizeof(attr));
        attr.id = SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE;
        attr.value.oid = p_queue_db->sch_grp;
        CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_group_queue_set_scheduler(queue_id, &attr));
    }
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_scheduler_group_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint8 queue_idx = 0;
    bool is_add = TRUE;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t queue_oid;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    sai_object_id_t sched_group_id = key->key.object_id;
    sai_object_id_t parent_oid = attr->value.oid;
    ctc_sai_sched_group_db_t* p_sched_group = NULL;
    sai_object_id_t port_id;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_slistnode_t *node = NULL;
    ctc_sai_port_service_id_t *p_service_id_node = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, sched_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    p_sched_group = ctc_sai_db_get_object_property(lchip, sched_group_id);
    if (NULL == p_sched_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    switch (attr->id)
    {
        case SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
            CTC_SAI_ERROR_RETURN(ctc_sai_scheduler_group_set_scheduler(sched_group_id, attr));
            break;
        case SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
            if (SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                parent_oid = p_sched_group->parent_id;
                is_add = FALSE;
            }
            CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_group_add_or_del_child(lchip, parent_oid, sched_group_id, is_add));
            p_sched_group->parent_id = is_add ? parent_oid : SAI_NULL_OBJECT_ID;

            //update from basic queue
            for (queue_idx = 0; queue_idx < CTC_QOS_BASIC_Q_NUM; queue_idx++)
            {
                queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_ALL, queue_idx, ctc_object_id.value);
                p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                if (!p_queue_db || !p_queue_db->sch_grp)
                {
                    queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_UNICAST, queue_idx, ctc_object_id.value);
                    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                    if (!p_queue_db || !p_queue_db->sch_grp)
                    {
                        continue;
                    }
                }
                CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_update_sched_group_foreach( lchip,  queue_oid,  sched_group_id));
            }

            //update from ext queue
            port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, ctc_object_id.value);
            _ctc_sai_port_get_port_db(port_id, &p_port_db);
            
            CTC_SLIST_LOOP(p_port_db->service_id_list, node)
            {
                p_service_id_node = _ctc_container_of(node, ctc_sai_port_service_id_t, node);  
                
                for (queue_idx = 0; queue_idx < CTC_QOS_EXT_Q_NUM; queue_idx++)
                {
                    queue_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QUEUE, lchip, SAI_QUEUE_TYPE_SERVICE, (p_service_id_node->service_id << 6) + queue_idx, ctc_object_id.value);
                    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_oid);
                    if (!p_queue_db || !p_queue_db->sch_grp)
                    {
                        continue;
                    }
                    CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_update_sched_group_foreach( lchip,  queue_oid,  sched_group_id));
                }
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group attribute not implement");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_scheduler_group_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_sched_group_db_t* p_sched_group = NULL;
    sai_object_id_t sched_group_id = key->key.object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_ERROR_RETURN(ctc_sai_oid_get_lchip(sched_group_id, &lchip));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_object_id);
    p_sched_group = ctc_sai_db_get_object_property(lchip, sched_group_id);
    if (NULL == p_sched_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }


    switch (attr->id)
    {
        case SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
            attr->value.u32 = p_sched_group->child_cnt;
            break;
        case SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
            CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), (void*)p_sched_group->child_list, p_sched_group->child_cnt, (void*)(&(attr->value.objlist))));
            break;
        case SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, ctc_object_id.value);
            break;
        case SAI_SCHEDULER_GROUP_ATTR_LEVEL:
            attr->value.u8 = ctc_object_id.sub_type;
            break;
        case SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
            attr->value.u8 = p_sched_group->max_childs;
            break;
        case SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
            attr->value.oid = p_sched_group->sched_id;
            break;
        case SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
            attr->value.oid = p_sched_group->parent_id;
            break;
        case SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID:
            attr->value.oid = p_sched_group->service_id;
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group attribute not implement");
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_sched_group_queue_map_ctc_port_level(uint8 lchip, uint32 gport, uint8 queue_idx, uint8 class_id, 
        sai_object_id_t self_sched_group_id, sai_object_id_t parent_sched_group_id, bool is_add)
{
    uint8 index = 0;
    ctc_object_id_t ctc_oid;
    ctc_qos_sched_t sched;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    ctc_sai_sched_group_db_t* p_self_sched_group_db = NULL;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    uint8 is_service_group = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_LOG_INFO(SAI_API_SCHEDULER_GROUP, "lchip:%d gport:0x%x Q_idx:%d class:%d self_sched_group_id:0x%"PRIx64" parent_sched_group_id:0x%"PRIx64" op:%s", 
        lchip,gport,queue_idx,class_id,self_sched_group_id,parent_sched_group_id,is_add?"Add":"Del");
    sal_memset(&sched, 0, sizeof(sched));

    p_self_sched_group_db = ctc_sai_db_get_object_property(lchip, self_sched_group_id);
    if (NULL == p_self_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if(p_self_sched_group_db->service_id)
    {
        is_service_group = 1;
    }

    p_sched_group_db = ctc_sai_db_get_object_property(lchip, parent_sched_group_id);
    if (NULL == p_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, parent_sched_group_id, &ctc_oid);
    index = ctc_oid.value2;

    sched.type = CTC_QOS_SCHED_GROUP;
    sched.sched.group_sched.cfg_type = CTC_QOS_SCHED_CFG_CONFIRM_CLASS;
    sched.sched.group_sched.class_priority = is_add ? index : CTC_SAI_SCHED_CHAN_NODE_DEFAULT; //!is_add = default value 2
    sched.sched.group_sched.queue_class = class_id;
    sched.sched.group_sched.queue.gport = gport;
    sched.sched.group_sched.queue.queue_id = (queue_idx & 0x3F);
    sched.sched.group_sched.queue.queue_type = is_service_group ? CTC_QUEUE_TYPE_SERVICE_INGRESS : CTC_QUEUE_TYPE_NETWORK_EGRESS;
    if(is_service_group)
    {
        sched.sched.group_sched.queue.service_id = p_self_sched_group_db->service_id;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));

    if (p_self_sched_group_db->sched_id != SAI_NULL_OBJECT_ID)
    {
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, p_self_sched_group_db->sched_id);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler DB not found!");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        sched.type = CTC_QOS_SCHED_GROUP;
        sched.sched.group_sched.cfg_type = CTC_QOS_SCHED_CFG_CONFIRM_WEIGHT;
        sched.sched.group_sched.queue.gport = gport;
        sched.sched.group_sched.queue.queue_id = (queue_idx & 0x3F);
        sched.sched.group_sched.queue.queue_type = is_service_group ? CTC_QUEUE_TYPE_SERVICE_INGRESS : CTC_QUEUE_TYPE_NETWORK_EGRESS;
        if(is_service_group)
        {
            sched.sched.group_sched.queue.service_id = p_self_sched_group_db->service_id;
        }
        if (p_scheduler_db->sch_type == SAI_SCHEDULING_TYPE_DWRR)
        {
            sched.sched.group_sched.weight = is_add ? p_scheduler_db->weight : 1;//!is_add = default value 1
        }
        else
        {
            sched.sched.group_sched.weight = 1;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }
    return SAI_STATUS_SUCCESS;
}
#if ETS_SUPPORT
static sai_status_t
_ctc_sai_sched_group_queue_map_ctc_ets_level(uint8 lchip, uint32 gport, uint8 queue_idx, uint8 class_id, 
        sai_object_id_t self_sched_group_id, sai_object_id_t parent_sched_group_id, bool is_add)
{
    uint8 index = 0;
    ctc_object_id_t ctc_oid;
    ctc_qos_sched_t sched;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    ctc_sai_sched_group_db_t* p_self_sched_group_db = NULL;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_LOG_INFO(SAI_API_SCHEDULER_GROUP, "lchip:%d gport:0x%x Q_idx:%d class:%d self_sched_group_id:0x%"PRIx64" parent_sched_group_id:0x%"PRIx64" op:%s", 
        lchip,gport,queue_idx,class_id,self_sched_group_id,parent_sched_group_id,is_add?"Add":"Del");
    sal_memset(&sched, 0, sizeof(sched));

    p_sched_group_db = ctc_sai_db_get_object_property(lchip, parent_sched_group_id);
    if (NULL == p_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, parent_sched_group_id, &ctc_oid);
    index = ctc_oid.value2;

    sched.type = CTC_QOS_SCHED_GROUP;
    sched.sched.group_sched.cfg_type = CTC_QOS_SCHED_CFG_SUB_GROUP_ID;
    sched.sched.group_sched.sub_group_id = is_add ? index : CTC_SAI_SCHED_ETS_NODE_DEFAULT; //!is_add = default value 2, ets0NodeSel = 0
    sched.sched.group_sched.queue_class = class_id;
    sched.sched.group_sched.queue.gport = gport;
    sched.sched.group_sched.queue.queue_id = queue_idx;
    sched.sched.group_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));

    /* TM subgroup 2 do not support WDRR */
    if ((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && (sched.sched.group_sched.sub_group_id == CTC_SAI_SCHED_ETS_NODE_DEFAULT))
    {
        goto next_level;
    }

    p_self_sched_group_db = ctc_sai_db_get_object_property(lchip, self_sched_group_id);
    if (NULL == p_self_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (p_self_sched_group_db->sched_id != SAI_NULL_OBJECT_ID)
    {
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, p_self_sched_group_db->sched_id);
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler DB not found!");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        sched.type = CTC_QOS_SCHED_GROUP;
        sched.sched.group_sched.cfg_type = CTC_QOS_SCHED_CFG_SUB_GROUP_WEIGHT;
        sched.sched.group_sched.queue.gport = gport;
        sched.sched.group_sched.queue.queue_id = queue_idx;
        sched.sched.group_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        if (p_scheduler_db->sch_type == SAI_SCHEDULING_TYPE_DWRR)
        {
            sched.sched.group_sched.weight = is_add ? p_scheduler_db->weight : 1;//!is_add = default value 1
        }
        else
        {
            sched.sched.group_sched.weight = 1;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }

next_level:
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, p_sched_group_db->parent_id, &ctc_oid);
    if(1 == ctc_oid.sub_type) //level 0, map to port
    {
        CTC_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_port_level(lchip, gport, queue_idx, class_id, parent_sched_group_id, p_sched_group_db->parent_id, is_add));
    }
    return SAI_STATUS_SUCCESS;
}
#endif

static sai_status_t
_ctc_sai_sched_group_queue_map_ctc_group_level(uint8 lchip, uint32 gport, uint8 queue_idx, sai_object_id_t queue_id, sai_object_id_t sched_group_id, bool is_add)
{
    uint8 index = 0;
    ctc_object_id_t ctc_oid, ctc_queue_oid;
    ctc_qos_sched_t sched;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    ctc_sai_scheduler_db_t* p_scheduler_db = NULL;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    uint16 group_index_base = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_LOG_INFO(SAI_API_SCHEDULER_GROUP, "lchip:%d gport:0x%x Q_idx:%d sched_grp_oid:0x%"PRIx64" op:%s", lchip,gport,queue_idx,sched_group_id,is_add?"Add":"Del");
    sal_memset(&sched, 0, sizeof(sched));
    sal_memset(&ctc_oid, 0, sizeof(ctc_oid));
    sal_memset(&ctc_queue_oid, 0, sizeof(ctc_queue_oid));
    
    p_sched_group_db = ctc_sai_db_get_object_property(lchip, sched_group_id);
    if (NULL == p_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler group DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "queue DB not found!");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_queue_oid);
   

    if((!p_sched_group_db->service_id) && (ctc_queue_oid.sub_type <= SAI_QUEUE_TYPE_MULTICAST)) //normal queue
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_oid);
        index = ctc_oid.value2; //group node

        sched.type = CTC_QOS_SCHED_QUEUE;
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
        sched.sched.queue_sched.exceed_class = is_add ? index : queue_idx; //!is_add = default value queue_idx
        sched.sched.queue_sched.queue.gport = gport;
        sched.sched.queue_sched.queue.queue_id = queue_idx;
        sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));

    }
    else if((p_sched_group_db->service_id != 0) && (ctc_queue_oid.sub_type == SAI_QUEUE_TYPE_SERVICE)) //service queue
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_oid);

        group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, p_sched_group_db->service_id);

        if(p_sched_group_db->service_id != (ctc_queue_oid.value2 >> 6))
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "queue service id and scheduler group service id not match!");
            return SAI_STATUS_FAILURE;
        }
        
        index = ctc_oid.value2 - group_index_base; //group node

        sched.type = CTC_QOS_SCHED_QUEUE;
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_CLASS;
        sched.sched.queue_sched.exceed_class = is_add ? index : (queue_idx & 0x3F); //!is_add = default value queue_idx
        sched.sched.queue_sched.queue.gport = gport;
        sched.sched.queue_sched.queue.service_id = p_sched_group_db->service_id;
        sched.sched.queue_sched.queue.queue_id = (queue_idx & 0x3F);
        sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }
    
#if 1
    //p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    //if (NULL == p_queue_db)
    //{
    //    CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "queue DB not found!");
    //    return SAI_STATUS_ITEM_NOT_FOUND;
    //}
    
    if (p_queue_db->sch_id != SAI_NULL_OBJECT_ID)
    {
        p_scheduler_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER, lchip, 0, 0, p_queue_db->sch_id));
        if (NULL == p_scheduler_db)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "scheduler DB not found!");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        sched.type = CTC_QOS_SCHED_QUEUE;
        sched.sched.queue_sched.cfg_type = CTC_QOS_SCHED_CFG_EXCEED_WEIGHT;
        sched.sched.queue_sched.queue.gport = gport;
        sched.sched.queue_sched.queue.queue_id = (queue_idx & 0x3F);        
        if((p_sched_group_db->service_id != 0) && (ctc_queue_oid.sub_type == SAI_QUEUE_TYPE_SERVICE))
        {
            sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_SERVICE_INGRESS;
            sched.sched.queue_sched.queue.service_id = p_sched_group_db->service_id;
        }
        else
        {
            sched.sched.queue_sched.queue.queue_type = CTC_QUEUE_TYPE_NETWORK_EGRESS;
        }
        if (p_scheduler_db->sch_type == SAI_SCHEDULING_TYPE_DWRR)
        {
            sched.sched.queue_sched.exceed_weight = is_add ? p_scheduler_db->weight : 1;//!is_add = default value 1
        }
        else
        {
            sched.sched.queue_sched.exceed_weight = 1;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_sched(lchip, &sched));
    }
#endif
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, p_sched_group_db->parent_id, &ctc_oid);
    if(1 == ctc_oid.sub_type) //level 1, map to chan node
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_port_level(lchip, gport, queue_idx, index, sched_group_id, p_sched_group_db->parent_id, is_add));
    }
#if 0
    else if(2 == ctc_oid.sub_type) //level 1, map to ets
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_ets_level(lchip, gport, queue_idx, index, sched_group_id, p_sched_group_db->parent_id, is_add));
    }
#endif    
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_sched_group_apply_queue_to_group(sai_object_id_t queue_id, sai_object_id_t sched_group_id, bool is_add)
{
    uint8 lchip = 0;
    uint32 gport = 0;
    uint8 queue_idx = 0;
    uint8 level = 0;
    ctc_object_id_t ctc_oid;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    queue_idx = ctc_oid.value2;
    gport = ctc_oid.value;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_oid);
    level = ctc_oid.sub_type;
    switch (level)
    {
        case 1:
            //should not jump from queue to port level
            CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_port_level(lchip, gport, queue_idx, queue_idx, queue_id, sched_group_id, is_add));
            break;
        case 2:
            //should not jump from queue to ets level
            //CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_ets_level(lchip, gport, queue_idx, queue_idx, queue_id, sched_group_id, is_add));

            CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_group_level(lchip, gport, queue_idx, queue_id, sched_group_id, is_add));
            break;
        //case 3:
            //CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_queue_map_ctc_group_level(lchip, gport, queue_idx, queue_id, sched_group_id, is_add));
            //break;
        default:
            break;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_sched_group_create_service_group(uint8 lchip, uint32 gport, uint16 service_id)
{
    uint8 ii = 0;
    uint16 group_index_base = 0;
    sai_object_id_t sched_group_oid;
    ctc_qos_queue_cfg_t que_cfg;
    ctc_qos_service_info_t srv_queue_info;
    
    sai_object_id_t port_id;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_slistnode_t *node = NULL;
    ctc_sai_port_service_id_t *p_service_id_node_data = NULL;
    ctc_sai_port_service_id_t *p_service_id_node = NULL;
    

    if(!service_id)
    {
        return SAI_STATUS_SUCCESS;
    }

    group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, service_id);
    
    for (ii = 0; ii < CTC_SAI_SCHED_MAX_GRP_NUM; ii++)
    {
        sched_group_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, 2, ii+group_index_base, gport);
        if (NULL != ctc_sai_db_get_object_property(lchip, sched_group_oid))
        {
            return SAI_STATUS_SUCCESS;
        }
    }
       
    //create service
    sal_memset(&que_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    sal_memset(&srv_queue_info, 0, sizeof(ctc_qos_service_info_t));

    srv_queue_info.opcode = CTC_QOS_SERVICE_ID_CREATE;
    srv_queue_info.service_id = service_id;

    sal_memcpy(&que_cfg.value.srv_queue_info, &srv_queue_info, sizeof(srv_queue_info));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));

    //bind to port
    sal_memset(&que_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    sal_memset(&srv_queue_info, 0, sizeof(ctc_qos_service_info_t));
    
    srv_queue_info.opcode = CTC_QOS_SERVICE_ID_BIND_DESTPORT;
    srv_queue_info.service_id = service_id;
    srv_queue_info.gport = gport;

    sal_memcpy(&que_cfg.value.srv_queue_info, &srv_queue_info, sizeof(srv_queue_info));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));
    
    //update port db
    port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, gport);
    _ctc_sai_port_get_port_db(port_id, &p_port_db);

    /* add service id into port service id list */
    CTC_SLIST_LOOP(p_port_db->service_id_list, node)
    {
        p_service_id_node_data = _ctc_container_of(node, ctc_sai_port_service_id_t, node);
        if (service_id == p_service_id_node_data->service_id)
        {
            // already created 
            return SAI_STATUS_SUCCESS;
        }        
    }

    p_service_id_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_port_service_id_t));
    if (!p_service_id_node)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    p_service_id_node->service_id = service_id;
    ctc_slist_add_tail(p_port_db->service_id_list, &(p_service_id_node->node));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_sched_group_destroy_service_group(uint8 lchip, uint32 gport, uint16 service_id)
{
    uint8 ii = 0;
    uint16 group_index_base = 0;
    sai_object_id_t sched_group_oid;
    ctc_qos_queue_cfg_t que_cfg;
    ctc_qos_service_info_t srv_queue_info;

    sai_object_id_t port_id;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_slistnode_t *node = NULL;
    ctc_sai_port_service_id_t *p_service_id_node = NULL;

    if(!service_id)
    {
        return SAI_STATUS_SUCCESS;
    }

    group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, service_id);
    
    for (ii = 0; ii < CTC_SAI_SCHED_MAX_GRP_NUM; ii++)
    {
        sched_group_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, 2, ii+group_index_base, gport);
        if (NULL != ctc_sai_db_get_object_property(lchip, sched_group_oid))
        {
            return SAI_STATUS_SUCCESS;
        }
    }
        
    //unbind to port
    sal_memset(&que_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    sal_memset(&srv_queue_info, 0, sizeof(ctc_qos_service_info_t));
    
    srv_queue_info.opcode = CTC_QOS_SERVICE_ID_UNBIND_DESTPORT;
    srv_queue_info.service_id = service_id;
    srv_queue_info.gport = gport;

    sal_memcpy(&que_cfg.value.srv_queue_info, &srv_queue_info, sizeof(srv_queue_info));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));

    //destroy service
    sal_memset(&que_cfg, 0, sizeof(ctc_qos_queue_cfg_t));
    sal_memset(&srv_queue_info, 0, sizeof(ctc_qos_service_info_t));

    srv_queue_info.opcode = CTC_QOS_SERVICE_ID_DESTROY;
    srv_queue_info.service_id = service_id;

    sal_memcpy(&que_cfg.value.srv_queue_info, &srv_queue_info, sizeof(srv_queue_info));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &que_cfg));


    //update port db
    port_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, SAI_PORT_TYPE_LOGICAL, 0, gport);
    _ctc_sai_port_get_port_db(port_id, &p_port_db);
    
    /* del from service list */
    CTC_SLIST_LOOP(p_port_db->service_id_list, node)
    {
        p_service_id_node = _ctc_container_of(node, ctc_sai_port_service_id_t, node);        

        if (service_id == p_service_id_node->service_id)
        {
            ctc_slist_delete_node(p_port_db->service_id_list, node);
            mem_free(p_service_id_node);
            break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static uint16
_ctc_sai_scheduler_group_get_max_service_id(uint8 lchip, uint8 level)
{
    uint16 max_service_id = 0;

    if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) 
    {
        if(level == 2)
        {
            max_service_id = CTC_SAI_MAX_SERVICE_NUM_TM;
        }
    }
    else
    {
        if(level == 2)
        {
            max_service_id = CTC_SAI_MAX_SERVICE_NUM_DEAFULT;
        }
    }

    return max_service_id;
}

static ctc_sai_attr_fn_entry_t  scheduler_group_attr_fn_entries[] =
{
        { SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { SAI_SCHEDULER_GROUP_ATTR_PORT_ID,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { SAI_SCHEDULER_GROUP_ATTR_LEVEL,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID,
          _ctc_sai_scheduler_group_get_attr,
          _ctc_sai_scheduler_group_set_attr },
        { SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE,
          _ctc_sai_scheduler_group_get_attr,
          _ctc_sai_scheduler_group_set_attr },
        { SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID,
          _ctc_sai_scheduler_group_get_attr,
          NULL },
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};


#define ________INTERNAL_API________

uint16
ctc_sai_scheduler_group_get_group_index_base(uint8 lchip, uint16 service_id)
{
    uint16 group_index_base = 0;
    
    if(CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) 
    {
        group_index_base = service_id * CTC_SAI_SCHED_NODE_IN_EXT_GROUP_TM;
    }
    else
    {
        group_index_base = service_id * CTC_SAI_SCHED_NODE_IN_EXT_GROUP_DEFAULT;
    }

    return group_index_base;
}

sai_status_t
ctc_sai_scheduler_group_port_get_sched_group_num(sai_object_id_t port_id, sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint32 gport = 0;
    uint8 level = 0;
    uint8 index = 0;
    sai_object_id_t sai_oid;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    uint16 service_id = 0, group_index_base = 0, max_service_id = 0;

    attr->value.u32 = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(port_id, &gport));
    
    for (level = 0; level < CTC_SAI_MAX_SCHED_LEVELS; level++)
    {
        max_service_id = _ctc_sai_scheduler_group_get_max_service_id(lchip, level);

        for (service_id = 0; service_id <= max_service_id; service_id++)
        {
            group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, service_id);
            
            for (index = 0; index < CTC_SAI_SCHED_LEVEL_GROUPS(level); index++)
            {
                sai_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, level, index+group_index_base, gport);
                p_sched_group_db = ctc_sai_db_get_object_property(lchip, sai_oid);
                if (NULL == p_sched_group_db)
                {
                    continue;
                }
                attr->value.u32++;
            }
        }
    }
    return SAI_STATUS_SUCCESS;
}
sai_status_t
ctc_sai_scheduler_group_port_get_sched_group_list(sai_object_id_t port_id, sai_attribute_t *attr)
{
    uint8 grp_cnt = 0;
    uint8 lchip = 0;
    uint32 gport = 0;
    uint8 level = 0;
    uint8 index = 0;
    sai_object_id_t sai_oid;
    sai_object_id_t sched_group_oid[20];
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    uint16 service_id = 0, group_index_base = 0, max_service_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_id, &lchip));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_gport(port_id, &gport));

    for (level = 0; level < CTC_SAI_MAX_SCHED_LEVELS; level++)
    {
        max_service_id = _ctc_sai_scheduler_group_get_max_service_id(lchip, level);

        for (service_id = 0; service_id <= max_service_id; service_id++)
        {
            group_index_base = ctc_sai_scheduler_group_get_group_index_base(lchip, service_id);
            
            for (index = 0; index < CTC_SAI_SCHED_LEVEL_GROUPS(level); index++)
            {                
                sai_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, level, index+group_index_base, gport);
                p_sched_group_db = ctc_sai_db_get_object_property(lchip, sai_oid);
                if (NULL == p_sched_group_db)
                {
                    continue;
                }
                sched_group_oid[grp_cnt++] = sai_oid;
            }
        }
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t), (void*)sched_group_oid, grp_cnt, (void*)(&(attr->value.objlist))));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_scheduler_group_queue_set_scheduler(sai_object_id_t queue_id, const sai_attribute_t *attr)
{
    uint8 lchip = 0;
    uint32 gport = 0;
    ctc_object_id_t ctc_oid;
    ctc_sai_queue_db_t* p_queue_db = NULL;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_PTR_VALID_CHECK(attr);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QUEUE, queue_id, &ctc_oid);
    lchip = ctc_oid.lchip;
    gport = ctc_oid.value;
    if (ctc_oid.sub_type == SAI_QUEUE_TYPE_MULTICAST)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Queue type!");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_queue_db = ctc_sai_db_get_object_property(lchip, queue_id);
    if (NULL == p_queue_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Queue DB get failed!");
        return SAI_STATUS_FAILURE;
    }

    if (SAI_NULL_OBJECT_ID != attr->value.oid)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, attr->value.oid, &ctc_oid);
        if (lchip != ctc_oid.lchip)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Queue lchip[%d] not match to scheduler group lchip[%d]!", lchip, ctc_oid.lchip);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        if (gport != ctc_oid.value)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Queue port[0x%x] not match to scheduler group port[0x%x]!", gport, ctc_oid.value);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        if (ctc_oid.type == SAI_OBJECT_TYPE_SCHEDULER_GROUP)
        {
            p_sched_group_db = ctc_sai_db_get_object_property(lchip, attr->value.oid);
            if (NULL == p_sched_group_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Sched Group DB not Found, oid:0x%"PRIx64"!", attr->value.oid);
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_apply_queue_to_group(queue_id, attr->value.oid, TRUE));
            CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_group_add_or_del_child(lchip, attr->value.oid, queue_id, TRUE));
        }
        else if (ctc_oid.type == SAI_OBJECT_TYPE_PORT)
        {//do nothing
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Queue apply to Invalid Parent oid Type!");
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_queue_db->sch_grp = attr->value.oid;
    }
    else
    {
        if (!p_queue_db->sch_grp)
        {
            return SAI_STATUS_SUCCESS;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, p_queue_db->sch_grp, &ctc_oid);
        if (ctc_oid.type == SAI_OBJECT_TYPE_SCHEDULER_GROUP)
        {
            p_sched_group_db = ctc_sai_db_get_object_property(lchip, p_queue_db->sch_grp);
            if (NULL == p_sched_group_db)
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Sched Group DB not Found!");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            CTC_SAI_ERROR_RETURN(_ctc_sai_sched_group_apply_queue_to_group(queue_id, p_queue_db->sch_grp, FALSE));
            CTC_SAI_ERROR_RETURN(_ctc_sai_scheduler_group_add_or_del_child(lchip, p_queue_db->sch_grp, queue_id, FALSE));
        }
        p_queue_db->sch_grp = SAI_NULL_OBJECT_ID;
    }
    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_scheduler_group_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_object_id_t             ctc_oid;
    sai_object_id_t             sched_group_id = bucket_data->oid;
    ctc_sai_sched_group_db_t*   p_db     = (ctc_sai_sched_group_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump   = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file   = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt      = (uint32 *)(p_cb_data->value1);
    uint32 ii = 0;

    if (p_dump->key.key.object_id && (sched_group_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, sched_group_id, &ctc_oid);

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" 0x%.4x %-5d %-5d %-7d 0x%-16"PRIx64" 0x%-16"PRIx64" %-6d %-5d 0x%-16"PRIx64"\n",
        *cnt,sched_group_id,ctc_oid.value, ctc_oid.value2, ctc_oid.sub_type, p_db->max_childs,p_db->parent_id,p_db->sched_id,
        p_db->child_type, p_db->child_cnt, p_db->child_cnt ? p_db->child_list[ii] : 0);

    for (ii = 1; ii < p_db->child_cnt; ii++)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-101s 0x%-16"PRIx64"","", p_db->child_list[ii]);
        CTC_SAI_LOG_DUMP(p_file, "\n");
    }
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


void
ctc_sai_scheduler_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI Scheduler Group MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_SCHEDULER_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Scheduler Group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_sched_group_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-6s %-5s %-5s %-7s %-18s %-18s %-6s %-5s %-18s\n", "No.","Sched_grp_Oid","Gport", "Index", "Level", "Max_cnt","Parent_Oid","Sched_Oid", "C_type", "C_cnt","Child_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_SCHEDULER_GROUP,
                                                (hash_traversal_fn)_ctc_sai_scheduler_group_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}


#define ________SAI_API________

sai_status_t
ctc_sai_scheduler_group_create_group_id(
        _Out_ sai_object_id_t *scheduler_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    uint8 level = 0;
    uint8 max_childs = 0;
    uint16 group_index = 0;
    uint32 gport = 0;
    uint32 gport_temp = 0;
    sai_status_t status = 0;
    ctc_object_id_t ctc_oid;
    sai_object_id_t sched_group_oid;
    sai_object_id_t sched_oid = SAI_NULL_OBJECT_ID;
    sai_object_id_t parent_oid;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    uint16 service_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_PTR_VALID_CHECK(scheduler_group_id);
    *scheduler_group_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_LEVEL, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Not Found SAI_SCHEDULER_GROUP_ATTR_LEVEL");
        goto error_0;
    }
    level = attr_value->u8;
    if (level >= CTC_SAI_MAX_SCHED_LEVELS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Error!! Level Max:%d", CTC_SAI_MAX_SCHED_LEVELS);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error_0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_PORT_ID, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Not Found SAI_SCHEDULER_GROUP_ATTR_PORT_ID");
        goto error_0;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, attr_value->oid, &ctc_oid);
    if (ctc_oid.type != SAI_OBJECT_TYPE_PORT)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Port Oid Type!!!");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error_0;
    }
    gport = ctc_oid.value;
    if (level > 0)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, &attr_value, &attr_index);
        if (CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Levl:%d Not Found SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE!!!", level);
            goto error_0;
        }
        CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_gport(attr_value->oid, &gport_temp), status, error_0);
        if (gport_temp != gport)
        {
            CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Current group port[0x%x] Not Match to Parent Gport[0x%x]!!!", gport, gport_temp);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error_0;
        }
    }
    parent_oid = attr_value->oid;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Not Found SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS!");
        goto error_0;
    }
    max_childs = attr_value->u8;
    if (max_childs > CTC_SAI_SCHED_LEVEL_CHILDS(level))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Error! Level[%d] Max Childs[%d]!", level, CTC_SAI_SCHED_LEVEL_CHILDS(level));
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error_0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        sched_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_SCHEDULER_GROUP_ATTR_SERVICE_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if(attr_value->u16)
        {
            if(level != 2) //Tsingma only level 2 support service group
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Scheduler group for service can only be level 2!");
                status = SAI_STATUS_NOT_SUPPORTED;
                goto error_0;
            }

            if(attr_value->u16 > CTC_SAI_MAX_SERVICE_NUM_TM) 
            {
                CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Scheduler group for service, service id must less than %d!", CTC_SAI_MAX_SERVICE_NUM_TM);
                status = SAI_STATUS_NOT_SUPPORTED;
                goto error_0;
            }
            service_id = attr_value->u16;
            //CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SCH_GRP_SERVICE_ID, &service_id), status, error_0);

            CTC_SAI_ERROR_GOTO(_ctc_sai_sched_group_create_service_group(lchip, gport, service_id), status, error_0);
        }
    }
    

    if (FALSE == _ctc_sai_scheduler_group_get_free_group_index(lchip, gport, level, service_id, &group_index))
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Exceed Level[%d] Max Group Num!", level);
        status = SAI_STATUS_TABLE_FULL;
        goto error_1;
    }

    sched_group_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SCHEDULER_GROUP, lchip, level, group_index, gport);
    CTC_SAI_ERROR_GOTO(_ctc_sai_scheduler_group_get_db(sched_group_oid, &p_sched_group_db), status, error_1);
    CTC_SAI_ERROR_GOTO(_ctc_sai_scheduler_group_add_or_del_child(lchip, parent_oid, sched_group_oid, TRUE), status, error_2);
    p_sched_group_db->max_childs = max_childs;
    p_sched_group_db->parent_id = parent_oid;
    p_sched_group_db->sched_id = sched_oid;
    p_sched_group_db->service_id = service_id;    
    *scheduler_group_id = sched_group_oid;
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;
    
error_2:
    CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "rollback to error2\n");
    mem_free(p_sched_group_db);
    ctc_sai_db_remove_object_property(lchip, sched_group_oid);
error_1:
    CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "rollback to error1\n");
    _ctc_sai_sched_group_destroy_service_group(lchip, gport, service_id);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_scheduler_group_remove_group_id(
        _In_ sai_object_id_t scheduler_group_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_sched_group_db_t* p_sched_group_db = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint16 service_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Object Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_sched_group_db = ctc_sai_db_get_object_property(lchip, scheduler_group_id);
    if (NULL == p_sched_group_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "DB not Found!");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    service_id = p_sched_group_db->service_id;
    CTC_SAI_ERROR_GOTO(_ctc_sai_scheduler_group_add_or_del_child(lchip, p_sched_group_db->parent_id, scheduler_group_id, FALSE), status, error_return);

    
    mem_free(p_sched_group_db);
    ctc_sai_db_remove_object_property(lchip, scheduler_group_id);

    _ctc_sai_sched_group_destroy_service_group(lchip, ctc_object_id.value, service_id);

error_return:
    if (status != SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Remove Scheduler Group Error! sched_group_oid:0x%"PRIx64" status=%d", scheduler_group_id, status);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


sai_status_t
ctc_sai_scheduler_group_set_attribute(
        _In_ sai_object_id_t scheduler_group_id,
        _In_ const sai_attribute_t *attr)
{

    sai_object_key_t key = { .key.object_id = scheduler_group_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Object Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_SCHEDULER_GROUP,  scheduler_group_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Failed to set scheduler group attr:%d", status);
    }
    return status;
}

sai_status_t
ctc_sai_scheduler_group_get_attribute(
        _In_ sai_object_id_t scheduler_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = scheduler_group_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_SCHEDULER_GROUP);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, scheduler_group_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_SCHEDULER_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Invalid Object Type!");
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_SCHEDULER_GROUP, loop, scheduler_group_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SCHEDULER_GROUP, "Failed to get scheduler group attr:%d", status);
    }
    return status;
}


sai_scheduler_group_api_t g_ctc_sai_scheduler_group_api = {
    ctc_sai_scheduler_group_create_group_id,
    ctc_sai_scheduler_group_remove_group_id,
    ctc_sai_scheduler_group_set_attribute,
    ctc_sai_scheduler_group_get_attribute
};

sai_status_t
ctc_sai_scheduler_group_api_init()
{
    ctc_sai_register_module_api(SAI_API_SCHEDULER_GROUP, (void*)&g_ctc_sai_scheduler_group_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_scheduler_group_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_SCHEDULERGROUP;
    wb_info.data_len = sizeof(ctc_sai_sched_group_db_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_SCHEDULER_GROUP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}


