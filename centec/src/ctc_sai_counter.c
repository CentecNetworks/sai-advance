/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_route.h"


/*sdk include file*/
#include "ctcs_api.h"

static sai_status_t
_ctc_sai_counter_build_db(uint8 lchip, sai_object_id_t stats_id, ctc_sai_counter_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    p_counter_info = mem_malloc(MEM_STATS_MODULE, sizeof(ctc_sai_counter_t));
    if (NULL == p_counter_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_COUNTER, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_counter_info, 0, sizeof(ctc_sai_counter_t));
    status = ctc_sai_db_add_object_property(lchip, stats_id, (void*)p_counter_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_counter_info);
        return status;
    }

    *oid_property = p_counter_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_counter_remove_db(uint8 lchip, sai_object_id_t counter_id)
{
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, counter_id);
    mem_free(p_counter_info);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_counter_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_COUNTER_ATTR_TYPE, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        if (attr_value->u32 != SAI_COUNTER_TYPE_REGULAR)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }        
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_counter_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_counter_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
    case SAI_COUNTER_ATTR_TYPE:
        {
            p_counter_info->counter_type = attr->value.s32;
        }
        break;
    default:
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_counter_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_counter_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
    case SAI_COUNTER_ATTR_TYPE:
        {
            attr->value.s32 = p_counter_info->counter_type;
        }
        break;
    default:
        return SAI_STATUS_NOT_SUPPORTED;
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t counter_attr_fn_entries[] = {
    { SAI_COUNTER_ATTR_TYPE,
      _ctc_sai_counter_get_attr,
      _ctc_sai_counter_set_attr},
};

static sai_status_t
_ctc_sai_counter_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t counter_obj_id = *(sai_object_id_t*)key;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, counter_obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COUNTER, ctc_object_id.value));  

    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_counter_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  counter_oid_cur = 0;
    ctc_sai_counter_t    ctc_sai_counter_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char queue_id[64] = {'-'};
    char cpu_reason[64] = {'-'};

    sal_memset(&ctc_sai_counter_cur, 0, sizeof(ctc_sai_counter_t));

    counter_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_counter_t*)(&ctc_sai_counter_cur), bucket_data->data, sizeof(ctc_sai_counter_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (counter_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    if(ctc_sai_counter_cur.is_trap_stats)
    {
        sal_sprintf(queue_id, "%d", ctc_sai_counter_cur.statsinfo.hostif_queue.queue_id);
        sal_sprintf(cpu_reason, "/%d", ctc_sai_counter_cur.statsinfo.hostif_queue.cpu_reason);
        sal_strcat(queue_id, cpu_reason);
        
        CTC_SAI_LOG_DUMP(p_file, "%-4d  0x%016"PRIx64 "  %-12d  %-14d  %-18s  %-18s\n",\
            num_cnt, counter_oid_cur, ctc_sai_counter_cur.ctc_sai_counter_type, ctc_sai_counter_cur.is_trap_stats, "-", queue_id);

    }
    else
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d  0x%016"PRIx64 "  %-12d  %-14d  %-18d  %-18s\n",\
            num_cnt, counter_oid_cur, ctc_sai_counter_cur.ctc_sai_counter_type, ctc_sai_counter_cur.is_trap_stats, ctc_sai_counter_cur.statsinfo.stats_id, "-");
    }

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________

sai_status_t    
ctc_sai_counter_id_hostif_trap_create(sai_object_id_t counter_id, ctc_sai_counter_type_t counter_type, uint16 cpu_reason, uint16 queue_id)
{
    uint8 lchip = 0;
    ctc_object_id_t counter_obj_id;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_COUNTER, counter_id, &counter_obj_id);

    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_counter_info->counter_type = counter_type;
    p_counter_info->statsinfo.hostif_queue.cpu_reason = cpu_reason;
    p_counter_info->statsinfo.hostif_queue.queue_id = queue_id;

    return SAI_STATUS_SUCCESS;
}
sai_status_t    
ctc_sai_counter_id_hostif_trap_remove(sai_object_id_t counter_id, ctc_sai_counter_type_t counter_type)
{
    uint8 lchip = 0;
    ctc_object_id_t counter_obj_id;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_COUNTER, counter_id, &counter_obj_id);

    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_counter_info->counter_type = CTC_SAI_COUNTER_TYPE_MAX;
    p_counter_info->statsinfo.hostif_queue.cpu_reason = 0;
    p_counter_info->statsinfo.hostif_queue.queue_id = 0;

    return SAI_STATUS_SUCCESS;
}


sai_status_t    
ctc_sai_counter_id_create(sai_object_id_t counter_id, ctc_sai_counter_type_t counter_type, uint32* stats_id)
{
    ctc_stats_statsid_t stats_statsid;
    uint8 lchip = 0;
    ctc_object_id_t counter_obj_id;
    ctc_sai_counter_t* p_counter_info = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_COUNTER, counter_id, &counter_obj_id);

    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
        
    if(counter_type == CTC_SAI_COUNTER_TYPE_ROUTE)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_IP;
        stats_statsid.dir = CTC_INGRESS;
    }
    else if (counter_type == CTC_SAI_COUNTER_TYPE_NEXTHOP)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_NEXTHOP;
        stats_statsid.dir = CTC_EGRESS;
    }
    else if (counter_type == CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_NEXTHOP_MPLS_PW;
        stats_statsid.dir = CTC_EGRESS;
    }
    else if (counter_type == CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_NEXTHOP_MPLS_LSP;
        stats_statsid.dir = CTC_EGRESS;
    }
    else if (counter_type == CTC_SAI_COUNTER_TYPE_ECMP)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_ECMP;
        stats_statsid.dir = CTC_INGRESS;
    }
    else if (counter_type == CTC_SAI_COUNTER_TYPE_TUNNEL_IGS)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_TUNNEL;
        stats_statsid.dir = CTC_INGRESS;
    }  
    else if (counter_type == CTC_SAI_COUNTER_TYPE_TUNNEL_EGS)
    {
        stats_statsid.type = CTC_STATS_STATSID_TYPE_TUNNEL;
        stats_statsid.dir = CTC_EGRESS;
    }  
    
    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_create_statsid(lchip, &stats_statsid));
    
    p_counter_info->statsinfo.stats_id = stats_statsid.stats_id;    
    p_counter_info->ctc_sai_counter_type = counter_type;

    *stats_id = stats_statsid.stats_id;
        
    return SAI_STATUS_SUCCESS;
}

sai_status_t    
ctc_sai_counter_id_remove(sai_object_id_t counter_id, ctc_sai_counter_type_t counter_type)
{
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);

    if (counter_id == SAI_NULL_OBJECT_ID)
    {
        return SAI_STATUS_SUCCESS;
    }
    if(counter_type == CTC_SAI_COUNTER_TYPE_HOSTIF)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_destroy_statsid(lchip, p_counter_info->statsinfo.stats_id));

    p_counter_info->statsinfo.stats_id = 0;
    p_counter_info->ctc_sai_counter_type = CTC_SAI_COUNTER_TYPE_MAX;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_counter_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Counter MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_COUNTER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Counter");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_counter_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s  %-18s  %-12s  %-14s  %-18s  %-18s \n", \
            "No.", "Counter_oid", "Counter Type", "Is Trap stats", "Stats_id", "Queue_id&CpuReason");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_COUNTER,
                                            (hash_traversal_fn)_ctc_sai_counter_dump_print_cb, (void*)(&sai_cb_data));
    }
}


#define ________Counter______

sai_status_t ctc_sai_counter_create_counter (
         sai_object_id_t *counter_id,
         sai_object_id_t switch_id,
         uint32_t attr_count,
         const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 stats_id = 0;
    uint32_t index = 0;
    sai_object_id_t counter_obj_id = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    const sai_attribute_value_t *attr_value;

    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    CTC_SAI_PTR_VALID_CHECK(counter_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_counter_create_attr_check(lchip, attr_count, attr_list));
    
    CTC_SAI_DB_LOCK(lchip);
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COUNTER, &stats_id), status, out);
    
    counter_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_COUNTER, lchip, 0, 0, stats_id);
    
    CTC_SAI_LOG_INFO(SAI_API_COUNTER, "create counter_id = 0x%"PRIx64"\n", counter_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_counter_build_db(lchip, counter_obj_id, &p_counter_info), status, error1);

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_COUNTER_ATTR_TYPE, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        p_counter_info->counter_type = attr_value->u32;
    }

    p_counter_info->ctc_sai_counter_type = CTC_SAI_COUNTER_TYPE_MAX;

    *counter_id = counter_obj_id;

    goto out;

error1:
    CTC_SAI_LOG_ERROR(SAI_API_COUNTER, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COUNTER, stats_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
    
}

sai_status_t ctc_sai_counter_remove_counter(
        sai_object_id_t counter_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    uint32 cnt_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_counter_info->ctc_sai_counter_type != CTC_SAI_COUNTER_TYPE_MAX)
    {        
        return SAI_STATUS_OBJECT_IN_USE;
    }

    //CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_remove(counter_id, p_counter_info->counter_type), status, out);
    ctc_sai_oid_get_counter_id(counter_id, &cnt_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COUNTER, cnt_id), status, out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_counter_remove_db(lchip, counter_id), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t ctc_sai_counter_set_counter_attribute(
        sai_object_id_t counter_id,
        const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    CTC_SAI_LOG_INFO(SAI_API_COUNTER, "counter_id = 0x%llx\n", counter_id);
    key.key.object_id = counter_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_COUNTER,  counter_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);  
    return status;
}

sai_status_t ctc_sai_counter_get_counter_attribute (
        sai_object_id_t counter_id,
        uint32_t attr_count,
        sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    CTC_SAI_LOG_INFO(SAI_API_COUNTER, "counter_id = 0x%llx\n", counter_id);
    key.key.object_id = counter_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_COUNTER, loop, counter_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


sai_status_t ctc_sai_counter_get_counter_stats (
        sai_object_id_t counter_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        uint64_t *counters)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    ctc_stats_basic_t ctc_stats;
    ctc_qos_queue_stats_t queue_stats;
    uint32 loop_i = 0;
    uint64 packet_count = 0, byte_count = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    sal_memset(&ctc_stats, 0, sizeof(ctc_stats));
    sal_memset(&queue_stats, 0, sizeof(queue_stats));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_counter_info->ctc_sai_counter_type < CTC_SAI_COUNTER_TYPE_HOSTIF) 
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_stats(lchip, p_counter_info->statsinfo.stats_id, &ctc_stats));
        packet_count = ctc_stats.packet_count;
        byte_count = ctc_stats.byte_count;
    }
    else if(p_counter_info->ctc_sai_counter_type == CTC_SAI_COUNTER_TYPE_HOSTIF)
    {
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
        queue_stats.queue.queue_id = p_counter_info->statsinfo.hostif_queue.queue_id;
        queue_stats.queue.cpu_reason = p_counter_info->statsinfo.hostif_queue.cpu_reason;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_queue_stats(lchip, &queue_stats));
        packet_count = queue_stats.stats.deq_packets;
        byte_count = queue_stats.stats.deq_bytes;
    }
    else
    {
        status = SAI_STATUS_NOT_SUPPORTED;
        goto out;
    }

    for(loop_i = 0;loop_i < number_of_counters;loop_i++)
    {
        if(SAI_COUNTER_STAT_PACKETS == counter_ids[loop_i])
        {
            counters[loop_i] = packet_count;
        }
        else if(SAI_COUNTER_STAT_BYTES == counter_ids[loop_i])
        {
            counters[loop_i] = byte_count;
        }
        else
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
        CTC_SAI_LOG_INFO(SAI_API_COUNTER, "counters[%d] = %llu\n", loop_i, counters[loop_i]);
    }
    

out:
    return status;

}
        
sai_status_t ctc_sai_counter_get_counter_stats_ext (
        sai_object_id_t counter_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids,
        sai_stats_mode_t mode,
        uint64_t *counters)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    ctc_stats_basic_t ctc_stats;
    ctc_qos_queue_stats_t queue_stats;
    uint32 loop_i = 0;
    uint64 packet_count = 0, byte_count = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    sal_memset(&ctc_stats, 0, sizeof(ctc_stats));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);

    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(SAI_STATS_MODE_READ == mode)
    {
        status = SAI_STATUS_NOT_SUPPORTED;
        goto out;
    }
    if(p_counter_info->ctc_sai_counter_type < CTC_SAI_COUNTER_TYPE_HOSTIF)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_get_stats(lchip, p_counter_info->statsinfo.stats_id, &ctc_stats));
        packet_count = ctc_stats.packet_count;
        byte_count = ctc_stats.byte_count;
        CTC_SAI_LOG_INFO(SAI_API_COUNTER, "Route/NextHop Counter.\n");
    }
    else if(p_counter_info->ctc_sai_counter_type == CTC_SAI_COUNTER_TYPE_HOSTIF)
    {
        queue_stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
        queue_stats.queue.queue_id = p_counter_info->statsinfo.hostif_queue.queue_id;
        queue_stats.queue.cpu_reason = p_counter_info->statsinfo.hostif_queue.cpu_reason;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_query_queue_stats(lchip, &queue_stats));
        packet_count = queue_stats.stats.deq_packets;
        byte_count = queue_stats.stats.deq_bytes;
        CTC_SAI_LOG_INFO(SAI_API_COUNTER, "Hostif Trap Counter.\n");
    }
    else
    {
        status = SAI_STATUS_NOT_SUPPORTED;
        goto out;
    }

    for(loop_i = 0;loop_i < number_of_counters;loop_i++)
    {
        if(SAI_COUNTER_STAT_PACKETS == counter_ids[loop_i])
        {
            counters[loop_i] = packet_count;
        }
        else if(SAI_COUNTER_STAT_BYTES == counter_ids[loop_i])
        {
            counters[loop_i] = byte_count;
        }
        else
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
        CTC_SAI_LOG_INFO(SAI_API_COUNTER, "counters[%d] = %llu\n", loop_i, counters[loop_i]);
    }

out:
    return status;

}

        
sai_status_t ctc_sai_counter_clear_counter_stats (
        sai_object_id_t counter_id,
        uint32_t number_of_counters,
        const sai_stat_id_t *counter_ids)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_counter_t* p_counter_info = NULL;
    ctc_qos_queue_stats_t queue_stats;
    uint32 loop_i = 0;
    uint8 pkt_clear = 0, byte_clear = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(counter_id, &lchip));
    CTC_SAI_LOG_ENTER(SAI_API_COUNTER);
    p_counter_info = ctc_sai_db_get_object_property(lchip, counter_id);
    if (NULL == p_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    for(loop_i = 0;loop_i < number_of_counters;loop_i++)
    {
        if(SAI_COUNTER_STAT_PACKETS == counter_ids[loop_i])
        {
            pkt_clear = 1;
        }
        else if(SAI_COUNTER_STAT_BYTES == counter_ids[loop_i])
        {
            byte_clear = 1;
        }
        else
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }
    
    if(pkt_clear && byte_clear)
    {
        if((p_counter_info->ctc_sai_counter_type == CTC_SAI_COUNTER_TYPE_ROUTE) || (p_counter_info->ctc_sai_counter_type == CTC_SAI_COUNTER_TYPE_NEXTHOP))
        {           
            CTC_SAI_LOG_INFO(SAI_OBJECT_TYPE_COUNTER, "clear route/nexthop stats_id = 0x%"PRIx64"\n", p_counter_info->statsinfo.stats_id);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_stats_clear_stats(lchip, p_counter_info->statsinfo.stats_id));
        }
        else if(p_counter_info->ctc_sai_counter_type == CTC_SAI_COUNTER_TYPE_HOSTIF)
        {
            queue_stats.queue.queue_type = CTC_QUEUE_TYPE_EXCP_CPU;
            queue_stats.queue.queue_id = p_counter_info->statsinfo.hostif_queue.queue_id;
            queue_stats.queue.cpu_reason = p_counter_info->statsinfo.hostif_queue.cpu_reason;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_clear_queue_stats(lchip, &queue_stats));
        }
    }
    else
    {
        CTC_SAI_LOG_INFO(SAI_OBJECT_TYPE_COUNTER, "Only support clear both packets and bytes.\n");
        status = SAI_STATUS_NOT_SUPPORTED;
    }
    
out:    
    return status;

}


sai_counter_api_t g_ctc_sai_counter_api = {
    ctc_sai_counter_create_counter,
    ctc_sai_counter_remove_counter,
    ctc_sai_counter_set_counter_attribute,
    ctc_sai_counter_get_counter_attribute,
    ctc_sai_counter_get_counter_stats,
    ctc_sai_counter_get_counter_stats_ext,
    ctc_sai_counter_clear_counter_stats,
};


sai_status_t
ctc_sai_counter_api_init()
{
    ctc_sai_register_module_api(SAI_API_COUNTER, (void*)&g_ctc_sai_counter_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_counter_db_init(uint8 lchip)
{
    /*warmboot start */
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_COUNTER;
    wb_info.data_len = sizeof(ctc_sai_counter_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_counter_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_COUNTER, (void*)(&wb_info));
    /*warmboot end */
    
    return SAI_STATUS_SUCCESS;
}


