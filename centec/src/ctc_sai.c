#include "ctcs_api.h"
#include "ctc_sai.h"
#include "ctc_sai_db.h"
#include "ctc_sai_oid.h"

#include "ctc_sai_switch.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_port.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_route.h"
#include "ctc_sai_mcast.h"
#include "ctc_sai_policer.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_wred.h"
#include "ctc_sai_queue.h"
#include "ctc_sai_ld_hash.h"
#include "ctc_sai_udf.h"
#include "ctc_sai_mirror.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_stp.h"
#include "ctc_sai_hostif.h"
#include "ctc_sai_samplepacket.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_scheduler.h"
#include "ctc_sai_scheduler_group.h"
#include "ctc_sai_buffer.h"
#include "ctc_sai_tunnel.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_isolation_group.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_debug_counter.h"
#include "ctc_sai_nat.h"
#include "ctc_sai_twamp.h"
#include "ctc_sai_bfd.h"
#include "ctc_sai_npm.h"
#include "ctc_sai_y1731.h"
#include "ctc_sai_ptp.h"
#include "ctc_sai_es.h"
#include "ctc_sai_synce.h"
#include "ctc_sai_monitor.h"

extern ctc_sai_db_t* g_sai_db[CTC_SAI_MAX_CHIP_NUM];

#define CTC_SAI_API_INIT_CHECK                                          \
    do {                                                                \
        if (!g_api_master.api_status){                                  \
            return SAI_STATUS_UNINITIALIZED; }                          \
    } while(0)

sai_api_master_t g_api_master;

sai_status_t
ctc_sai_mapping_error_ctc(int32 error)
{
    switch(error)
    {
        case CTC_E_NONE:
            return SAI_STATUS_SUCCESS;
        case CTC_E_INVALID_PTR:
            return SAI_STATUS_INVALID_PARAMETER;
        case CTC_E_INVALID_PORT:
            return SAI_STATUS_INVALID_PORT_NUMBER;
        case CTC_E_INVALID_PARAM:
        case CTC_E_BADID:
        case CTC_E_INVALID_CHIP_ID:
        case CTC_E_INVALID_CONFIG:
            return SAI_STATUS_INVALID_PARAMETER;
        case CTC_E_EXIST:
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        case CTC_E_NOT_EXIST:
            return SAI_STATUS_ITEM_NOT_FOUND;
        case CTC_E_NOT_READY:
            return SAI_STATUS_INSUFFICIENT_RESOURCES;
        case CTC_E_IN_USE:
            return SAI_STATUS_OBJECT_IN_USE;
        case CTC_E_NOT_SUPPORT:
            return SAI_STATUS_NOT_SUPPORTED;
        case CTC_E_NO_RESOURCE:
        case CTC_E_PROFILE_NO_RESOURCE:
            return SAI_STATUS_INSUFFICIENT_RESOURCES;
        case CTC_E_NO_MEMORY:
            return SAI_STATUS_NO_MEMORY;
        case CTC_E_HASH_CONFLICT:
            return SAI_STATUS_FAILURE;
        case CTC_E_NOT_INIT:
            return SAI_STATUS_UNINITIALIZED;
        case CTC_E_INIT_FAIL:
        case CTC_E_DMA:
        case CTC_E_HW_TIME_OUT:
        case CTC_E_HW_BUSY:
        case CTC_E_HW_INVALID_INDEX:
        case CTC_E_HW_NOT_LOCK:
        case CTC_E_HW_FAIL:
            return SAI_STATUS_FAILURE;
        case CTC_E_VERSION_MISMATCH:
            return SAI_STATUS_SW_UPGRADE_VERSION_MISMATCH;
        case CTC_E_PARAM_CONFLICT:
            return SAI_STATUS_FAILURE;
        case CTC_E_TOO_MANY_FRAGMENT:
            return SAI_STATUS_FAILURE;
        case CTC_E_WB_BUSY:
            return SAI_STATUS_NOT_EXECUTED;
        default:
            return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_FAILURE;
}

sai_status_t ctc_sai_fill_object_list(uint32_t element_size, void *data, uint32_t count, void *list)
{
    sai_object_list_t *objlist = list;
    sai_status_t       status = SAI_STATUS_SUCCESS;

    if ((NULL == data) || (NULL == objlist))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "NULL ptr\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }


    if (0 == element_size)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Zero element size\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (count > objlist->count)
    {
        status = SAI_STATUS_BUFFER_OVERFLOW;
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "buffer size error. Allocated %u needed %u\n", objlist->count, count);
        objlist->count = count;
        return status;
    }

    objlist->count = count;
    sal_memcpy(objlist->list, data, count * element_size);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_find_attrib_in_list(uint32_t       attr_count,
                                 const sai_attribute_t        *attr_list,
                                 sai_attr_id_t          attrib_id,
                                 const sai_attribute_value_t **attr_value,
                                 uint32_t              *index)
{
    uint32 loop;

    if ((attr_count) && (NULL == attr_list))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (NULL == attr_value)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (NULL == index)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    for (loop = 0; loop < attr_count; loop++) {
        if (attr_list[loop].id == attrib_id) {
            *attr_value = &(attr_list[loop].value);
            *index      = loop;
            return SAI_STATUS_SUCCESS;
        }
    }
    return SAI_STATUS_ITEM_NOT_FOUND;
}


sai_status_t
 _ctc_sai_find_attribute_fn( sai_attr_id_t          attr_id,
                            ctc_sai_attr_fn_entry_t *attr_func_list,
                            uint16              *index)
{
    uint16 loop;

    CTC_SAI_LOG_ENTER(SAI_API_UNSPECIFIED);

    if (NULL == index) {

        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (NULL == attr_func_list) {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"NULL value attr_func_lists\n");

        return SAI_STATUS_INVALID_PARAMETER;
    }

    for (loop = 0; CTC_SAI_FUNC_ATTR_END_ID != attr_func_list[loop].id; loop++) {
        if (attr_id == attr_func_list[loop].id) {
            *index = loop;

            return SAI_STATUS_SUCCESS;
        }
    }

    return SAI_STATUS_ITEM_NOT_FOUND;
}


sai_status_t
ctc_sai_check_attr_metadata( uint32_t         attr_count,
                                     const sai_attribute_t      *attr_list,
                                     sai_object_type_t     object_type,
                                     ctc_sai_attr_fn_entry_t *attr_func_list,
                                     sai_common_api_t      oper)
{
    sai_status_t               status = SAI_STATUS_SUCCESS;

     CTC_SAI_LOG_ENTER(SAI_API_UNSPECIFIED);

    if ((attr_count) && (NULL == attr_list)) {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"NULL value attr list\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }

    if (NULL == attr_func_list) {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"NULL value functionality vendor attrib\n");
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }

    if (SAI_COMMON_API_MAX <= oper) {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"Invalid operation %d\n", oper);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }

    if (SAI_COMMON_API_REMOVE == oper) {
        /* No attributes expected for remove at this point */
        status = SAI_STATUS_NOT_IMPLEMENTED;
        goto out;
    }

    if (SAI_COMMON_API_SET == oper) {
        if (1 != attr_count) {
            CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"Set operation supports only single attribute\n");
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    if (!ctc_sai_is_object_type_valid(object_type))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED,"Invalid object type (%d)\n", object_type);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }
    /* more check   TBD.....*/

out:

    return status;
}

sai_status_t
ctc_sai_set_attribute(sai_object_key_t   *key,
                                  char                *key_str,
                                  sai_object_type_t   object_type,
                                 ctc_sai_attr_fn_entry_t *attr_func_list,
                                const  sai_attribute_t       *attr)
{
    uint16_t index;

    CTC_SAI_ERROR_RETURN(ctc_sai_check_attr_metadata( 1, attr, object_type, attr_func_list, SAI_COMMON_API_SET));
    CTC_SAI_ERROR_RETURN(_ctc_sai_find_attribute_fn(attr->id, attr_func_list, &index));

    if (attr_func_list[index].set)
    {
        return attr_func_list[index].set(key, attr);
    }
    else
    {
        return SAI_STATUS_INVALID_ATTRIBUTE_0;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_get_attribute( sai_object_key_t   *key,
                                  char                *key_str,
                                  sai_object_type_t   object_type,
                                  uint32 attr_index,
                                 ctc_sai_attr_fn_entry_t *attr_func_list,
                                  sai_attribute_t       *attr)
{
    uint16_t index;

    CTC_SAI_ERROR_RETURN(ctc_sai_check_attr_metadata( 1, attr, object_type, attr_func_list, SAI_COMMON_API_GET));
    CTC_SAI_ERROR_RETURN(_ctc_sai_find_attribute_fn(attr->id, attr_func_list, &index));

    if (attr_func_list[index].get)
    {
        return attr_func_list[index].get(key, attr, attr_index);
    }
    else
    {
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_index;
    }

    return SAI_STATUS_SUCCESS;
}

char ctc_sai_log_buffer[1024] = {0};
#define CTC_SAI_LOG_BUFFER_SIZE 1023

char *ctc_sai_module_str[] = {
    "Common",
    "Switch",
    "Port",
    "FDB",
    "VLAN",
    "VRoute",
    "Route",
    "Nexthop",
    "NexthopGroup",
    "RIF",
    "Neighbor",
    "Acl",
    "HostIf",
    "Mirror",
    "SamplePacket",
    "STP",
    "LAG",
    "Policer",
    "WRED",
    "QosMap",
    "Queue",
    "Scheduler",
    "SchedulerGroup",
    "Buffer",
    "Hash",
    "UDF",
    "Tunnel",
    "L2MC",
    "IPMC",
    "RPF Group",
    "L2MC Group",
    "IPMC Group",
    "Mcast FDB",
    "Bridge",
    "TAM",
    "SR",
    "MPLS",
    "uBrust",
    "BFD",
    "IsolationGroup",
    "NAT",
    "Counter",
    "DebugCounter",
    "TWAMP",
    "NPM",
    "ES",
    "Y1731",
    "PTP",
    "SYNCE"
};

#define SAI_LOG_MODE 0

void ctc_sai_log(int level, sai_api_t api, char *fmt, ...)
{
    va_list args;
    // compare if level of each API here?
    if (level < g_api_master.log_level[api]) {
        return;
    }
    va_start(args, fmt);
    vsnprintf(ctc_sai_log_buffer, CTC_SAI_LOG_BUFFER_SIZE, fmt, args);
    va_end(args);
//SONiC use syslog, uml use printf
#if (1 == SDK_WORK_PLATFORM) || (1 == SAI_LOG_MODE)
    printf("%s: %s\n", ctc_sai_module_str[api], ctc_sai_log_buffer);
#else
#include <stdio.h>
#include <stdlib.h>
#include <syslog.h>
    {
        int   syslog_level;
        char *level_str;

        /* translate SDK log level to syslog level */
        switch (level) {
        case SAI_LOG_LEVEL_NOTICE:
            syslog_level     = LOG_NOTICE;
            level_str = "NOTICE";
            break;

        case SAI_LOG_LEVEL_INFO:
            syslog_level     = LOG_INFO;
            level_str = "INFO";
            break;

        case SAI_LOG_LEVEL_ERROR:
            syslog_level     = LOG_ERR;
            level_str = "ERR";
            break;

        case SAI_LOG_LEVEL_WARN:
            syslog_level     = LOG_WARNING;
            level_str = "WARNING";
            break;

        case SAI_LOG_LEVEL_DEBUG:
            syslog_level     = LOG_DEBUG;
            level_str = "DEBUG";
            break;

        case SAI_LOG_LEVEL_CRITICAL:
            syslog_level     = LOG_CRIT;
            level_str = "CRITICAL";
            break;
        
        default:
            syslog_level     = LOG_DEBUG;
            level_str = "DEBUG";
            break;
        }

        syslog(syslog_level, "%s: %s", level_str, ctc_sai_log_buffer);
    }
#endif
}

sai_status_t
ctc_sai_register_module_api( sai_api_t sai_api_id,   void* module_api)
{
    g_api_master.module_api[sai_api_id] = module_api;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_get_services_fn(sai_service_method_table_t** p_service_method)
{

    *p_service_method = &g_api_master.services;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_object_traversal_fn(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    uint32* cnt = (uint32*)(user_data->value0);
    sai_object_key_t* object_list = (sai_object_key_t*)(user_data->value1);
    object_list[(*cnt)++].key.object_id = bucket_data->oid;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_entry_traversal_fn(ctc_sai_entry_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    uint32* cnt = (uint32*)(user_data->value0);
    sai_object_key_t* object_list = (sai_object_key_t*)(user_data->value1);
    ctc_sai_db_entry_type_t* type = (ctc_sai_db_entry_type_t*)(user_data->value2);
    ctc_sai_db_entry_unmapping_key(user_data->lchip, *type, bucket_data, &(object_list[(*cnt)++].key));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_get_single_attribute(sai_object_type_t object_type, sai_object_key_t key, sai_attribute_t* attr_tmp)
{
    switch (object_type)
    {
        /*entry*/
        case SAI_OBJECT_TYPE_FDB_ENTRY:
            return ((sai_fdb_api_t*)g_api_master.module_api[SAI_API_FDB])->get_fdb_entry_attribute(&(key.key.fdb_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_NEIGHBOR_ENTRY:
            return ((sai_neighbor_api_t*)g_api_master.module_api[SAI_API_NEIGHBOR])->get_neighbor_entry_attribute(&(key.key.neighbor_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_ROUTE_ENTRY:
            return ((sai_route_api_t*)g_api_master.module_api[SAI_API_ROUTE])->get_route_entry_attribute(&(key.key.route_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_L2MC_ENTRY:
            return ((sai_l2mc_api_t*)g_api_master.module_api[SAI_API_L2MC])->get_l2mc_entry_attribute(&(key.key.l2mc_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_IPMC_ENTRY:
            return ((sai_ipmc_api_t*)g_api_master.module_api[SAI_API_IPMC])->get_ipmc_entry_attribute(&(key.key.ipmc_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_MCAST_FDB_ENTRY:
            return ((sai_mcast_fdb_api_t*)g_api_master.module_api[SAI_API_MCAST_FDB])->get_mcast_fdb_entry_attribute(&(key.key.mcast_fdb_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_INSEG_ENTRY:
            return ((sai_mpls_api_t*)g_api_master.module_api[SAI_API_MPLS])->get_inseg_entry_attribute(&(key.key.inseg_entry), 1, attr_tmp);
        case SAI_OBJECT_TYPE_NAT_ENTRY:
            return ((sai_nat_api_t*)g_api_master.module_api[SAI_API_NAT])->get_nat_entry_attribute(&(key.key.nat_entry), 1, attr_tmp);    
        /*object*/
        case SAI_OBJECT_TYPE_PORT:
            return ((sai_port_api_t*)g_api_master.module_api[SAI_API_PORT])->get_port_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_LAG:
            return ((sai_lag_api_t*)g_api_master.module_api[SAI_API_LAG])->get_lag_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_VIRTUAL_ROUTER:
            return ((sai_virtual_router_api_t*)g_api_master.module_api[SAI_API_VIRTUAL_ROUTER])->get_virtual_router_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_NEXT_HOP:
            return ((sai_next_hop_api_t*)g_api_master.module_api[SAI_API_NEXT_HOP])->get_next_hop_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_NEXT_HOP_GROUP:
            return ((sai_next_hop_group_api_t*)g_api_master.module_api[SAI_API_NEXT_HOP_GROUP])->get_next_hop_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ROUTER_INTERFACE:
            return ((sai_router_interface_api_t*)g_api_master.module_api[SAI_API_ROUTER_INTERFACE])->get_router_interface_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_TABLE:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_table_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_ENTRY:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_entry_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_COUNTER:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_counter_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_RANGE:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_range_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_TABLE_GROUP:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_table_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER:
            return ((sai_acl_api_t*)g_api_master.module_api[SAI_API_ACL])->get_acl_table_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_MIRROR_SESSION:
            return ((sai_mirror_api_t*)g_api_master.module_api[SAI_API_MIRROR])->get_mirror_session_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_SAMPLEPACKET:
            return ((sai_samplepacket_api_t*)g_api_master.module_api[SAI_API_SAMPLEPACKET])->get_samplepacket_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_STP:
            return ((sai_stp_api_t*)g_api_master.module_api[SAI_API_STP])->get_stp_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_trap_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_POLICER:
            return ((sai_policer_api_t*)g_api_master.module_api[SAI_API_POLICER])->get_policer_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_WRED:
            return ((sai_wred_api_t*)g_api_master.module_api[SAI_API_WRED])->get_wred_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_QOS_MAP:
            return ((sai_qos_map_api_t*)g_api_master.module_api[SAI_API_QOS_MAP])->get_qos_map_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_QUEUE:
            return ((sai_queue_api_t*)g_api_master.module_api[SAI_API_QUEUE])->get_queue_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_SCHEDULER:
            return ((sai_scheduler_api_t*)g_api_master.module_api[SAI_API_SCHEDULER])->get_scheduler_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_SCHEDULER_GROUP:
            return ((sai_scheduler_group_api_t*)g_api_master.module_api[SAI_API_SCHEDULER_GROUP])->get_scheduler_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_BUFFER_POOL:
            return ((sai_buffer_api_t*)g_api_master.module_api[SAI_API_BUFFER])->get_buffer_pool_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_BUFFER_PROFILE:
            return ((sai_buffer_api_t*)g_api_master.module_api[SAI_API_BUFFER])->get_buffer_profile_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP:
            return ((sai_buffer_api_t*)g_api_master.module_api[SAI_API_BUFFER])->get_ingress_priority_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_LAG_MEMBER:
            return ((sai_lag_api_t*)g_api_master.module_api[SAI_API_LAG])->get_lag_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HASH:
            return ((sai_hash_api_t*)g_api_master.module_api[SAI_API_HASH])->get_hash_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_UDF:
            return ((sai_udf_api_t*)g_api_master.module_api[SAI_API_UDF])->get_udf_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_UDF_MATCH:
            return ((sai_udf_api_t*)g_api_master.module_api[SAI_API_UDF])->get_udf_match_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_UDF_GROUP:
            return ((sai_udf_api_t*)g_api_master.module_api[SAI_API_UDF])->get_udf_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_SWITCH:
            return ((sai_switch_api_t*)g_api_master.module_api[SAI_API_SWITCH])->get_switch_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF_TRAP:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_trap_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_table_entry_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_VLAN:
            return ((sai_vlan_api_t*)g_api_master.module_api[SAI_API_VLAN])->get_vlan_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_VLAN_MEMBER:
            return ((sai_vlan_api_t*)g_api_master.module_api[SAI_API_VLAN])->get_vlan_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF_PACKET:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TUNNEL_MAP:
            return ((sai_tunnel_api_t*)g_api_master.module_api[SAI_API_TUNNEL])->get_tunnel_map_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TUNNEL:
            return ((sai_tunnel_api_t*)g_api_master.module_api[SAI_API_TUNNEL])->get_tunnel_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY:
            return ((sai_tunnel_api_t*)g_api_master.module_api[SAI_API_TUNNEL])->get_tunnel_term_table_entry_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_FDB_FLUSH : /*???*/
            return SAI_STATUS_NOT_IMPLEMENTED;
        case SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER:
            return ((sai_next_hop_group_api_t*)g_api_master.module_api[SAI_API_NEXT_HOP_GROUP])->get_next_hop_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_STP_PORT:
            return ((sai_stp_api_t*)g_api_master.module_api[SAI_API_STP])->get_stp_port_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_RPF_GROUP:
            return ((sai_rpf_group_api_t*)g_api_master.module_api[SAI_API_RPF_GROUP])->get_rpf_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_RPF_GROUP_MEMBER:
            return ((sai_rpf_group_api_t*)g_api_master.module_api[SAI_API_RPF_GROUP])->get_rpf_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_L2MC_GROUP:
            return ((sai_l2mc_group_api_t*)g_api_master.module_api[SAI_API_L2MC])->get_l2mc_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER:
            return ((sai_l2mc_group_api_t*)g_api_master.module_api[SAI_API_L2MC])->get_l2mc_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_IPMC_GROUP:
            return ((sai_ipmc_group_api_t*)g_api_master.module_api[SAI_API_IPMC])->get_ipmc_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER:
            return ((sai_ipmc_group_api_t*)g_api_master.module_api[SAI_API_IPMC])->get_ipmc_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP:
            return ((sai_hostif_api_t*)g_api_master.module_api[SAI_API_HOSTIF])->get_hostif_user_defined_trap_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_BRIDGE:
            return ((sai_bridge_api_t*)g_api_master.module_api[SAI_API_BRIDGE])->get_bridge_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_BRIDGE_PORT:
            return ((sai_bridge_api_t*)g_api_master.module_api[SAI_API_BRIDGE])->get_bridge_port_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY:
            return ((sai_tunnel_api_t*)g_api_master.module_api[SAI_API_TUNNEL])->get_tunnel_map_entry_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_SEGMENTROUTE_SIDLIST:
            return ((sai_segmentroute_api_t*)g_api_master.module_api[SAI_API_SEGMENTROUTE])->get_segmentroute_sidlist_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_PORT_POOL:
            return ((sai_port_api_t*)g_api_master.module_api[SAI_API_PORT])->get_port_pool_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_DTEL:
            return ((sai_dtel_api_t*)g_api_master.module_api[SAI_API_DTEL])->get_dtel_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_DTEL_QUEUE_REPORT:
            return ((sai_dtel_api_t*)g_api_master.module_api[SAI_API_DTEL])->get_dtel_queue_report_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_DTEL_INT_SESSION:
            return ((sai_dtel_api_t*)g_api_master.module_api[SAI_API_DTEL])->get_dtel_int_session_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_DTEL_REPORT_SESSION:
            return ((sai_dtel_api_t*)g_api_master.module_api[SAI_API_DTEL])->get_dtel_report_session_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_DTEL_EVENT:
            return ((sai_dtel_api_t*)g_api_master.module_api[SAI_API_DTEL])->get_dtel_event_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_BFD_SESSION:
            return ((sai_bfd_api_t*)g_api_master.module_api[SAI_API_BFD])->get_bfd_session_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ISOLATION_GROUP:
            return ((sai_isolation_group_api_t*)g_api_master.module_api[SAI_API_ISOLATION_GROUP])->get_isolation_group_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER:
            return ((sai_isolation_group_api_t*)g_api_master.module_api[SAI_API_ISOLATION_GROUP])->get_isolation_group_member_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_MATH_FUNC:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_math_func_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_REPORT:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_report_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_event_threshold_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_TEL_TYPE:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_tel_type_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_TRANSPORT:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_transport_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_TELEMETRY:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_telemetry_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_COLLECTOR:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_collector_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_EVENT_ACTION:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_event_action_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_TAM_EVENT:
            return ((sai_tam_api_t*)g_api_master.module_api[SAI_API_TAM])->get_tam_event_attribute(key.key.object_id, 1, attr_tmp);
        case SAI_OBJECT_TYPE_NAT_ZONE_COUNTER:
            return ((sai_nat_api_t*)g_api_master.module_api[SAI_API_NAT])->get_nat_zone_counter_attribute(key.key.object_id, 1, attr_tmp);    
        case SAI_OBJECT_TYPE_COUNTER:
            return ((sai_counter_api_t*)g_api_master.module_api[SAI_API_COUNTER])->get_counter_attribute(key.key.object_id, 1, attr_tmp);    

        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_dbg_sdk_dump(sal_file_t p_file, uint8 lchip)
{
    CTC_SAI_LOG_DUMP(p_file, "%s %s\n", "SDK Version:", CTC_SDK_VERSION_STR);
    CTC_SAI_LOG_DUMP(p_file, "%s %s\n", "SDK Release Date:", CTC_SDK_RELEASE_DATE);
    CTC_SAI_LOG_DUMP(p_file, "%s %s\n", "SDK Copyright Time:", CTC_SDK_COPYRIGHT_TIME);

    CTC_SAI_LOG_DUMP(p_file, "%s %s\n", "CHIP NAME:", ctcs_get_chip_name(lchip));

    return SAI_STATUS_SUCCESS;
}
#define ________INTERNAL_API________

/* char ip_buf[CTC_IPV6_ADDR_STR_LEN] = {0};  ip_str_buf memery must big enough, CTC_IPV6_ADDR_STR_LEN */
sai_status_t
ctc_sai_get_ip_str(sai_ip_address_t* ip_addr, char* ip_str_buf)
{
    uint32 ip4_addr = 0;
    uint32 ip6_addr[4] = {0};

    CTC_SAI_PTR_VALID_CHECK(ip_addr);
    CTC_SAI_PTR_VALID_CHECK(ip_str_buf);

    if (SAI_IP_ADDR_FAMILY_IPV4 == ip_addr->addr_family)
    {
        if (0 == ip_addr->addr.ip4)
        {
            sal_strcpy(ip_str_buf, "-");
        }
        else
        {
            ip4_addr = sal_ntohl(ip_addr->addr.ip4);
            sal_inet_ntop(AF_INET, &ip4_addr, ip_str_buf, CTC_IPV6_ADDR_STR_LEN);
        }
    }
    else if (SAI_IP_ADDR_FAMILY_IPV6 == ip_addr->addr_family)
    {
        if (0 == sal_memcmp(ip6_addr, ip_addr->addr.ip6, 16))
        {
            sal_strcpy(ip_str_buf, "-");
        }
        else
        {
            ip6_addr[0] = sal_ntohl(*((uint32*)ip_addr->addr.ip6));
            ip6_addr[1] = sal_ntohl(*((uint32*)ip_addr->addr.ip6 + 1));
            ip6_addr[2] = sal_ntohl(*((uint32*)ip_addr->addr.ip6 + 2));
            ip6_addr[3] = sal_ntohl(*((uint32*)ip_addr->addr.ip6 + 3));
            sal_inet_ntop(AF_INET6, ip6_addr, ip_str_buf, CTC_IPV6_ADDR_STR_LEN);
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_get_ipv4_str(sai_ip4_t* ip_addr, char* ip_str_buf)
{
    uint32 ip4_addr = 0;

    CTC_SAI_PTR_VALID_CHECK(ip_addr);
    CTC_SAI_PTR_VALID_CHECK(ip_str_buf);

    if (0 == *ip_addr)
    {
        sal_strcpy(ip_str_buf, "-");
    }
    else
    {
        ip4_addr = sal_ntohl(*ip_addr);
        sal_inet_ntop(AF_INET, &ip4_addr, ip_str_buf, CTC_IPV6_ADDR_STR_LEN);
    }

    return SAI_STATUS_SUCCESS;
    
}

sai_status_t
ctc_sai_get_mac_str(sai_mac_t in_mac, char out_mac[])
{
    sai_mac_t mac_addr = {0};

    CTC_SAI_PTR_VALID_CHECK(in_mac);
    CTC_SAI_PTR_VALID_CHECK(out_mac);

    if (0 == sal_memcmp(mac_addr, in_mac, 6))
    {
        sal_strcpy(out_mac, "-");
    }
    else
    {
        sal_sprintf(out_mac, "%.2x%.2x.%.2x%.2x.%.2x%.2x", in_mac[0], in_mac[1], in_mac[2], in_mac[3], in_mac[4], in_mac[5]);
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_get_packet_action_desc(uint8 action_type, char *action_str)
{
    CTC_SAI_PTR_VALID_CHECK(action_str);
    switch (action_type)
    {
        case SAI_PACKET_ACTION_DROP:
            sal_strcpy(action_str, "DROP");
            break;
        case SAI_PACKET_ACTION_FORWARD:
            sal_strcpy(action_str, "FORWARD");
            break;
        case SAI_PACKET_ACTION_COPY:
            sal_strcpy(action_str, "COPY");
            break;
        case SAI_PACKET_ACTION_COPY_CANCEL:
            sal_strcpy(action_str, "COPY_CANCEL");
            break;
        case SAI_PACKET_ACTION_TRAP:
            sal_strcpy(action_str, "TRAP");
            break;
        case SAI_PACKET_ACTION_LOG:
            sal_strcpy(action_str, "LOG");
            break;
        case SAI_PACKET_ACTION_DENY:
            sal_strcpy(action_str, "DENY");
            break;
        case SAI_PACKET_ACTION_TRANSIT:
            sal_strcpy(action_str, "TRANSIT");
            break;
        default:
            sal_strcpy(action_str, "Error action_type");
            break;
    }
    return SAI_STATUS_SUCCESS;
}

#define ________API________
/*
 * Routine Description:
 *     Adapter module initialization call. This is NOT for SDK initialization.
 *
 * Arguments:
 *     [in] flags - reserved for future use, must be zero
 *     [in] services - methods table with services provided by adapter host
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
sai_status_t
sai_api_initialize( uint64_t flags,  const sai_service_method_table_t* services)
{
    sai_api_t api =0;
    sai_status_t ret = SAI_STATUS_SUCCESS;

    sal_memset(&g_api_master, 0, sizeof(sai_api_master_t));
    /* init global resource sdk module */
    ret = mem_mgr_init();
    if (ret != 0)
    {
        return ret;
    }
    ret = ctc_debug_init();
    if (ret != 0)
    {
        return ret;
    }

    ret = sal_init();
    if (ret != 0)
    {
        return ret;
    }


    if ((NULL == services) || (NULL == services->profile_get_next_value) || (NULL == services->profile_get_value)) 
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Invalid services handle passed to SAI API initialize\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    
    sal_memcpy(&g_api_master.services, services, sizeof(g_api_master.services));

    if (0 != flags) 
    {
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "Invalid flags passed to SAI API initialize\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    ctc_sai_switch_api_init();
    ctc_sai_bridge_api_init();
    ctc_sai_port_api_init();
    ctc_sai_fdb_api_init();
    ctc_sai_vlan_api_init();
    ctc_sai_virtual_router_api_init();
    ctc_sai_router_interface_api_init();
    ctc_sai_neighbor_api_init();
    ctc_sai_next_hop_api_init();
    ctc_sai_next_hop_group_api_init();
    ctc_sai_route_api_init();
    ctc_sai_mcast_api_init();
    ctc_sai_policer_api_init();
    ctc_sai_wred_api_init();
    ctc_sai_qos_map_api_init();
    ctc_sai_queue_api_init();
    ctc_sai_lag_api_init();
    ctc_sai_stp_api_init();
    ctc_sai_ld_hash_api_init();
    ctc_sai_udf_api_init();
    ctc_sai_mirror_api_init();
    ctc_sai_mpls_api_init();
    ctc_sai_hostif_api_init();
    ctc_sai_samplepacket_api_init();
    ctc_sai_acl_api_init();
    ctc_sai_tunnel_api_init();
    ctc_sai_scheduler_api_init();
    ctc_sai_scheduler_group_api_init();
    ctc_sai_buffer_api_init();
    ctc_sai_isolation_group_api_init();
    ctc_sai_counter_api_init();
    ctc_sai_debug_counter_api_init();
    ctc_sai_nat_api_init();
    ctc_sai_twamp_api_init();
    ctc_sai_bfd_api_init();
    ctc_sai_npm_api_init();
    ctc_sai_ptp_api_init();
    ctc_sai_y1731_api_init();
    ctc_sai_es_api_init();
    ctc_sai_synce_api_init();
    ctc_sai_monitor_api_init();

    g_api_master.api_status = true;
    /*init sai all module*/
    for (api = SAI_API_UNSPECIFIED; api < SAI_API_MAX; api++) 
    {
        sai_log_set(api, SAI_LOG_LEVEL_ERROR);
    }

    return SAI_STATUS_SUCCESS;
}

/*
 * Routine Description:
 *     Retrieve a pointer to the C-style method table for desired SAI
 *     functionality as specified by the given sai_api_id.
 *
 * Arguments:
 *     [in] sai_api_id - SAI api ID
 *     [out] api_method_table - Caller allocated method table
 *           The table must remain valid until the sai_api_uninitialize() is called
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
sai_status_t sai_api_query( sai_api_t sai_api_id, _Out_ void** api_method_table)
{
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_UNSPECIFIED);
    CTC_SAI_API_INIT_CHECK;
    CTC_SAI_API_ID_CHECK(sai_api_id);

    if (!api_method_table)
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, "null api method table");
        return status;
    }

    if (g_api_master.module_api[sai_api_id])
    {
        *api_method_table = g_api_master.module_api[sai_api_id];
    }
    else
    {
        status = SAI_STATUS_NOT_SUPPORTED;
    }

    return status;
}

/*
 * Routine Description:
 *   Uninitialization of the adapter module. SAI functionalities, retrieved via
 *   sai_api_query() cannot be used after this call.
 *
 * Arguments:
 *   None
 *
 * Return Values:
 *   SAI_STATUS_SUCCESS on success
 *   Failure status code on error
 */
sai_status_t sai_api_uninitialize(void)
{
    CTC_SAI_API_INIT_CHECK;
    sal_memset(&g_api_master, 0, sizeof(g_api_master));


    return SAI_STATUS_SUCCESS;
}

/*
 * Routine Description:
 *     Set log level for sai api module. The default log level is SAI_LOG_WARN.
 *
 * Arguments:
 *     [in] sai_api_id - SAI api ID
 *     [in] log_level - log level
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
sai_status_t sai_log_set( sai_api_t sai_api_id,  sai_log_level_t log_level)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 debug_level = CTC_DEBUG_LEVEL_NONE;

/*SYSTEM MODIFIED by xgu for SDK bug, should not check SAI INIT for log module in SAI, 2019-3-4*/
//    CTC_SAI_API_INIT_CHECK;
    CTC_SAI_API_ID_CHECK(sai_api_id);


    g_api_master.log_level[sai_api_id] = log_level;

    switch (log_level)
    {
        case SAI_LOG_LEVEL_DEBUG:
            debug_level |= (CTC_DEBUG_LEVEL_PARAM | CTC_DEBUG_LEVEL_FUNC);
        case SAI_LOG_LEVEL_INFO:
            debug_level |= CTC_DEBUG_LEVEL_INFO;
        case SAI_LOG_LEVEL_NOTICE:
        case SAI_LOG_LEVEL_WARN:
        case SAI_LOG_LEVEL_ERROR:
        case SAI_LOG_LEVEL_CRITICAL:
            debug_level |= CTC_DEBUG_LEVEL_ERROR;
            break;
        default:
            break;
    }

    switch (sai_api_id)
    {
        case SAI_API_SWITCH           :
            ctc_debug_set_flag("chip", "chip", 1, debug_level, TRUE);
            break;
        case SAI_API_PORT             :
        case SAI_API_ISOLATION_GROUP  :
            ctc_debug_set_flag("port", "port", 1, debug_level, TRUE);
            ctc_debug_set_flag("port", "mac", 1, debug_level, TRUE);
            ctc_debug_set_flag("port", "cl73", 1, debug_level, TRUE);
            break;
        case SAI_API_FDB              :
            ctc_debug_set_flag("l2", "fdb", 1, debug_level, TRUE);
            break;
        case SAI_API_VLAN             :
            ctc_debug_set_flag("vlan", "vlan", 1, debug_level, TRUE);
            ctc_debug_set_flag("vlan", "vlan_class", 1, debug_level, TRUE);
            ctc_debug_set_flag("vlan", "vlan_mapping", 1, debug_level, TRUE);
            ctc_debug_set_flag("vlan", "protocol_vlan", 1, debug_level, TRUE);
            break;
        case SAI_API_VIRTUAL_ROUTER   :
            break;
        case SAI_API_ROUTE            :
        case SAI_API_NAT              :
            ctc_debug_set_flag("ip", "ipuc", 1, debug_level, TRUE);
            break;
        case SAI_API_NEXT_HOP         :
            ctc_debug_set_flag("nexthop", "nexthop", 1, debug_level, TRUE);
            break;
        case SAI_API_NEXT_HOP_GROUP   :
            ctc_debug_set_flag("nexthop", "nexthop", 1, debug_level, TRUE);
            ctc_debug_set_flag("aps", "aps", 1, debug_level, TRUE);
            break;
        case SAI_API_ROUTER_INTERFACE :
            ctc_debug_set_flag("l3if", "l3if", 1, debug_level, TRUE);
            break;
        case SAI_API_NEIGHBOR         :
            ctc_debug_set_flag("ip", "ipuc", 1, debug_level, TRUE);
            break;
        case SAI_API_ACL              :
            ctc_debug_set_flag("acl", "acl", 1, debug_level, TRUE);
            break;
        case SAI_API_HOSTIF           :
            ctc_debug_set_flag("acl", "acl", 1, debug_level, TRUE);
            ctc_debug_set_flag("qos", "queue", 1, debug_level, TRUE);
            ctc_debug_set_flag("qos", "policer", 1, debug_level, TRUE);
            break;
        case SAI_API_MIRROR           :
            ctc_debug_set_flag("nexthop", "nexthop", 1, debug_level, TRUE);
            ctc_debug_set_flag("mirror", "mirror", 1, debug_level, TRUE);
            break;
        case SAI_API_SAMPLEPACKET     :
            ctc_debug_set_flag("acl", "acl", 1, debug_level, TRUE);
            ctc_debug_set_flag("mirror", "mirror", 1, debug_level, TRUE);
            break;
        case SAI_API_STP              :
            ctc_debug_set_flag("l2", "stp", 1, debug_level, TRUE);
            break;
        case SAI_API_LAG              :
            ctc_debug_set_flag("linkagg", "linkagg", 1, debug_level, TRUE);
            break;
        case SAI_API_POLICER          :
            ctc_debug_set_flag("security", "security", 1, debug_level, TRUE);
            ctc_debug_set_flag("qos", "policer", 1, debug_level, TRUE);
            break;
        case SAI_API_QOS_MAP          :
            ctc_debug_set_flag("qos", "class", 1, debug_level, TRUE);
            break;
        case SAI_API_WRED             :
        case SAI_API_QUEUE            :
        case SAI_API_SCHEDULER        :
        case SAI_API_SCHEDULER_GROUP  :
        case SAI_API_BUFFER           :
            ctc_debug_set_flag("qos", "queue", 1, debug_level, TRUE);
            break;
        case SAI_API_HASH             :
            ctc_debug_set_flag("parser", "parser", 1, debug_level, TRUE);
            break;
        case SAI_API_UDF              :
            ctc_debug_set_flag("acl", "acl", 1, debug_level, TRUE);
            break;
        case SAI_API_TUNNEL           :
            break;
        case SAI_API_L2MC             :
        case SAI_API_IPMC             :
        case SAI_API_RPF_GROUP        :
        case SAI_API_L2MC_GROUP       :
        case SAI_API_IPMC_GROUP       :
        case SAI_API_MCAST_FDB        :
            ctc_debug_set_flag("nexthop", "nexthop", 1, debug_level, TRUE);
            ctc_debug_set_flag("ip", "ipmc", 1, debug_level, TRUE);
            ctc_debug_set_flag("l2", "fdb", 1, debug_level, TRUE);
            break;
        case SAI_API_BRIDGE           :
            ctc_debug_set_flag("l2", "fdb", 1, debug_level, TRUE);
            ctc_debug_set_flag("security", "security", 1, debug_level, TRUE);
            ctc_debug_set_flag("port", "port", 1, debug_level, TRUE);
            ctc_debug_set_flag("vlan", "vlan", 1, debug_level, TRUE);
            ctc_debug_set_flag("vlan", "vlan_mapping", 1, debug_level, TRUE);
            ctc_debug_set_flag("nexthop", "nexthop", 1, debug_level, TRUE);
            break;
        case SAI_API_TAM              :
            break;
        case SAI_API_SEGMENTROUTE     :
            break;
        case SAI_API_MPLS             :
            ctc_debug_set_flag("mpls", "mpls", 1, debug_level, TRUE);
            break;
        case SAI_API_COUNTER          :
        case SAI_API_DEBUG_COUNTER    :    
            ctc_debug_set_flag("stats", "stats", 1, debug_level, TRUE);
            break;
        case SAI_API_BFD             :
        case SAI_API_Y1731           :
            ctc_debug_set_flag("oam", "oam", 1, debug_level, TRUE);
            break;
        case SAI_API_TWAMP             :
        case SAI_API_NPM           :
            ctc_debug_set_flag("npm", "npm", 1, debug_level, TRUE);
            break;
        case SAI_API_PTP           :
            ctc_debug_set_flag("ptp", "ptp", 1, debug_level, TRUE);
            break;
        case SAI_API_MONITOR           :
            ctc_debug_set_flag("monitor", "monitor", 1, debug_level, TRUE);
            break;
        case SAI_API_SYNCE           :
            ctc_debug_set_flag("sync_ether", "sync_ether", 1, debug_level, TRUE);
            break;
        default:
            break;
    }

    return status;
}

/*
 * Routine Description:
 *     Query sai object type.
 *
 * Arguments:
 *     [in] sai_object_id_t
 *
 * Return Values:
 *    Return SAI_OBJECT_TYPE_NULL when sai_object_id is not valid.
 *    Otherwise, return a valid sai object type SAI_OBJECT_TYPE_XXX
 */
sai_object_type_t
sai_object_type_query( sai_object_id_t sai_object_id)
{
    sai_object_type_t         object_type = SAI_OBJECT_TYPE_NULL;

    object_type = ((ctc_object_id_t*)&sai_object_id)->type;

    return object_type;
}

/**
 * @brief Query sai switch id.
 *
 * @param[in] sai_object_id Object id
 *
 * @return Return #SAI_NULL_OBJECT_ID when sai_object_id is not valid.
 * Otherwise, return a valid SAI_OBJECT_TYPE_SWITCH object on which
 * provided object id belongs. If valid switch id object is provided
 * as input parameter it should returin itself.
 */
sai_object_id_t
sai_switch_id_query(sai_object_id_t sai_object_id)
{
    sai_uint32_t    lchip   = 0;
    CTC_SAI_LOG_ENTER(SAI_API_UNSPECIFIED);

    lchip = ((ctc_object_id_t*)&sai_object_id)->lchip;

    return lchip;
}


/**
 * @brief Generate dump file. The dump file may include SAI state information and vendor SDK information.
 *
 * @param[in] dump_file_name Full path for dump file
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
sai_status_t
sai_dbg_generate_dump(const char *dump_file_name)
{
    sal_file_t p_file = NULL;
    uint8  lchip = 0;
    char line_buf[CTC_SAI_DUMP_LINE_LEN+1] = {0};
    uint16 str_len = 0;
    sai_object_id_t switch_id = 0;
    ctc_sai_dump_grep_param_t dump_grep_param;
	uint8 gchip = 0;

    sal_memset(&dump_grep_param, 0, sizeof(ctc_sai_dump_grep_param_t));
    sal_memset(dump_grep_param.api_bmp, 0xFFFFFFFF, sizeof(uint32)*(SAI_API_MAX - 1) / 32 + 1);
    sal_memset(dump_grep_param.object_bmp, 0xFFFFFFFF, sizeof(uint32)*(SAI_OBJECT_TYPE_MAX - 1) / 32 + 1);

    p_file = sal_fopen(dump_file_name, "w+");
    if (NULL == p_file)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Error opening file %s with write permission\n", dump_file_name);
        return SAI_STATUS_FAILURE;
    }

    for (lchip = 0; lchip < CTC_SAI_MAX_CHIP_NUM; lchip++)
    {
        if (NULL == g_sai_db[lchip])
        {
            continue;
        }
        CTC_SAI_DB_LOCK(lchip);

        str_len += sal_sprintf(line_buf + str_len, "%s", "---------------------------------------------------**** lchip: ");
        str_len += sal_sprintf(line_buf + str_len, "%d", lchip);
        str_len += sal_sprintf(line_buf + str_len, "%s", " ****---------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", line_buf);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "************************************************* CTC SDK DEBUG DUMP ***************************************************");
        _ctc_sai_dbg_sdk_dump(p_file, lchip);
        ctcs_get_gchip_id(lchip, &gchip);
        switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
        CTC_SAI_LOG_DUMP(p_file, "-----------------------------------------**** switch_id:0x%016"PRIx64" ****-----------------------------------------\n",switch_id);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "************************************************* CTC SAI DEBUG DUMP ***************************************************");

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_SWITCH))
        {
            ctc_sai_switch_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_PORT))
        {
            ctc_sai_port_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_FDB))
        {
            ctc_sai_fdb_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_VLAN))
        {
            ctc_sai_vlan_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_VIRTUAL_ROUTER))
        {
            ctc_sai_virtual_router_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_ROUTE))
        {
            ctc_sai_route_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_NEXT_HOP))
        {
            ctc_sai_next_hop_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_NEXT_HOP_GROUP))
        {
            ctc_sai_next_hop_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_ROUTER_INTERFACE))
        {
            ctc_sai_router_interface_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_NEIGHBOR))
        {
            ctc_sai_neighbor_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_ACL))
        {
            ctc_sai_acl_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_HOSTIF))
        {
            ctc_sai_hostif_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_MIRROR))
        {
            ctc_sai_mirror_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_SAMPLEPACKET))
        {
            ctc_sai_samplepacket_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_STP))
        {
            ctc_sai_stp_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_LAG))
        {
            ctc_sai_lag_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_POLICER))
        {
            ctc_sai_policer_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_WRED))
        {
            ctc_sai_wred_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_QOS_MAP))
        {
            ctc_sai_qos_map_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_QUEUE))
        {
            ctc_sai_queue_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_SCHEDULER))
        {
            ctc_sai_scheduler_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_SCHEDULER_GROUP))
        {
            ctc_sai_scheduler_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_BUFFER))
        {
            ctc_sai_buffer_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_HASH))
        {
            ctc_sai_ld_hash_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_UDF))
        {
            ctc_sai_udf_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_TUNNEL))
        {
            ctc_sai_tunnel_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_L2MC))
        {
            ctc_sai_l2mc_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_IPMC))
        {
            ctc_sai_ipmc_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_RPF_GROUP))
        {
            ctc_sai_rpf_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_L2MC_GROUP))
        {
            ctc_sai_l2mc_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_IPMC_GROUP))
        {
            ctc_sai_ipmc_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_MCAST_FDB))
        {
            ctc_sai_mcast_fdb_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_BRIDGE))
        {
            ctc_sai_bridge_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_TAM))
        {
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_SEGMENTROUTE))
        {
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_MPLS))
        {
            ctc_sai_mpls_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_ISOLATION_GROUP))
        {
            ctc_sai_isolation_group_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_NAT))
        {
            ctc_sai_nat_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_COUNTER))
        {
            ctc_sai_counter_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_DEBUG_COUNTER))
        {
            ctc_sai_debug_counter_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_TWAMP))
        {
            ctc_sai_debug_counter_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_BFD))
        {
            ctc_sai_bfd_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_Y1731))
        {
            ctc_sai_y1731_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_PTP))
        {
            ctc_sai_ptp_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_ES))
        {
            ctc_sai_es_dump(lchip, p_file, &dump_grep_param);
        }

        if (CTC_BMP_ISSET(dump_grep_param.api_bmp, SAI_API_MONITOR))
        {
            ctc_sai_monitor_buffer_dump(lchip, p_file, &dump_grep_param);
            ctc_sai_monitor_latency_dump(lchip, p_file, &dump_grep_param);
        }

        CTC_SAI_DB_UNLOCK(lchip);
    }
    sal_fclose(p_file);

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Query an enum attribute (enum or enum list) list of implemented enum values
 *
 * @param[in] switch_id SAI Switch object id
 * @param[in] object_type SAI object type
 * @param[in] attr_id SAI attribute ID
 * @param[inout] enum_values_capability List of implemented enum values
 *
 * @return #SAI_STATUS_SUCCESS on success, #SAI_STATUS_BUFFER_OVERFLOW if list size insufficient, failure status code on error
 */
sai_status_t sai_query_attribute_enum_values_capability(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _In_ sai_attr_id_t attr_id,
        _Inout_ sai_s32_list_t *enum_values_capability)
{
    // TODO: taocy. tmp use here.    
    return SAI_STATUS_NOT_SUPPORTED;
}

sai_status_t
sai_get_maximum_attribute_count(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _Inout_ uint32_t *count)
{
    uint32 cnt[] = {
        0,                                     /*SAI_OBJECT_TYPE_NULL                     =  0*/
        SAI_PORT_ATTR_END,                     /*SAI_OBJECT_TYPE_PORT                     =  1*/
        SAI_LAG_ATTR_END,                      /*SAI_OBJECT_TYPE_LAG                      =  2*/
        SAI_VIRTUAL_ROUTER_ATTR_END,           /*SAI_OBJECT_TYPE_VIRTUAL_ROUTER           =  3*/
        SAI_NEXT_HOP_ATTR_END,                 /*SAI_OBJECT_TYPE_NEXT_HOP                 =  4*/
        SAI_NEXT_HOP_GROUP_ATTR_END,           /*SAI_OBJECT_TYPE_NEXT_HOP_GROUP           =  5*/
        SAI_ROUTER_INTERFACE_ATTR_END,         /*SAI_OBJECT_TYPE_ROUTER_INTERFACE         =  6*/
        SAI_ACL_TABLE_ATTR_END,                /*SAI_OBJECT_TYPE_ACL_TABLE                =  7*/
        SAI_ACL_ENTRY_ATTR_END,                /*SAI_OBJECT_TYPE_ACL_ENTRY                =  8*/
        SAI_ACL_COUNTER_ATTR_END,              /*SAI_OBJECT_TYPE_ACL_COUNTER              =  9*/
        SAI_ACL_RANGE_ATTR_END,                /*SAI_OBJECT_TYPE_ACL_RANGE                = 10*/
        SAI_ACL_TABLE_GROUP_ATTR_END,          /*SAI_OBJECT_TYPE_ACL_TABLE_GROUP          = 11*/
        SAI_ACL_TABLE_GROUP_MEMBER_ATTR_END,   /*SAI_OBJECT_TYPE_ACL_TABLE_GROUP_MEMBER   = 12*/
        SAI_HOSTIF_ATTR_END,                   /*SAI_OBJECT_TYPE_HOSTIF                   = 13*/
        SAI_MIRROR_SESSION_ATTR_END,           /*SAI_OBJECT_TYPE_MIRROR_SESSION           = 14*/
        SAI_SAMPLEPACKET_ATTR_END,             /*SAI_OBJECT_TYPE_SAMPLEPACKET             = 15*/
        SAI_STP_ATTR_END,                      /*SAI_OBJECT_TYPE_STP                      = 16*/
        SAI_HOSTIF_TRAP_GROUP_ATTR_END,        /*SAI_OBJECT_TYPE_HOSTIF_TRAP_GROUP        = 17*/
        SAI_POLICER_ATTR_END,                  /*SAI_OBJECT_TYPE_POLICER                  = 18*/
        SAI_WRED_ATTR_END,                     /*SAI_OBJECT_TYPE_WRED                     = 19*/
        SAI_QOS_MAP_ATTR_END,                  /*SAI_OBJECT_TYPE_QOS_MAP                  = 20*/
        SAI_QUEUE_ATTR_END,                    /*SAI_OBJECT_TYPE_QUEUE                    = 21*/
        SAI_SCHEDULER_ATTR_END,                /*SAI_OBJECT_TYPE_SCHEDULER                = 22*/
        SAI_SCHEDULER_GROUP_ATTR_END,          /*SAI_OBJECT_TYPE_SCHEDULER_GROUP          = 23*/
        SAI_BUFFER_POOL_ATTR_END,              /*SAI_OBJECT_TYPE_BUFFER_POOL              = 24*/
        SAI_BUFFER_PROFILE_ATTR_END,           /*SAI_OBJECT_TYPE_BUFFER_PROFILE           = 25*/
        SAI_INGRESS_PRIORITY_GROUP_ATTR_END,   /*SAI_OBJECT_TYPE_INGRESS_PRIORITY_GROUP   = 26*/
        SAI_LAG_MEMBER_ATTR_END,               /*SAI_OBJECT_TYPE_LAG_MEMBER               = 27*/
        SAI_HASH_ATTR_END,                     /*SAI_OBJECT_TYPE_HASH                     = 28*/
        SAI_UDF_ATTR_END,                      /*SAI_OBJECT_TYPE_UDF                      = 29*/
        SAI_UDF_MATCH_ATTR_END,                /*SAI_OBJECT_TYPE_UDF_MATCH                = 30*/
        SAI_UDF_GROUP_ATTR_END,                /*SAI_OBJECT_TYPE_UDF_GROUP                = 31*/
        SAI_FDB_ENTRY_ATTR_END,                /*SAI_OBJECT_TYPE_FDB_ENTRY                = 32*/
        SAI_SWITCH_ATTR_END,                   /*SAI_OBJECT_TYPE_SWITCH                   = 33*/
        SAI_HOSTIF_TRAP_ATTR_END,              /*SAI_OBJECT_TYPE_HOSTIF_TRAP              = 34*/
        SAI_HOSTIF_TABLE_ENTRY_ATTR_END,       /*SAI_OBJECT_TYPE_HOSTIF_TABLE_ENTRY       = 35*/
        SAI_NEIGHBOR_ENTRY_ATTR_END,           /*SAI_OBJECT_TYPE_NEIGHBOR_ENTRY           = 36*/
        SAI_ROUTE_ENTRY_ATTR_END,              /*SAI_OBJECT_TYPE_ROUTE_ENTRY              = 37*/
        SAI_VLAN_ATTR_END,                     /*SAI_OBJECT_TYPE_VLAN                     = 38*/
        SAI_VLAN_MEMBER_ATTR_END,              /*SAI_OBJECT_TYPE_VLAN_MEMBER              = 39*/
        SAI_HOSTIF_PACKET_ATTR_END,            /*SAI_OBJECT_TYPE_HOSTIF_PACKET            = 40*/
        SAI_TUNNEL_MAP_ATTR_END,               /*SAI_OBJECT_TYPE_TUNNEL_MAP               = 41*/
        SAI_TUNNEL_ATTR_END,                   /*SAI_OBJECT_TYPE_TUNNEL                   = 42*/
        SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_END,  /*SAI_OBJECT_TYPE_TUNNEL_TERM_TABLE_ENTRY  = 43*/
        SAI_FDB_FLUSH_ATTR_END,                /*SAI_OBJECT_TYPE_FDB_FLUSH                = 44*/
        SAI_NEXT_HOP_GROUP_MEMBER_ATTR_END,    /*SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER    = 45*/
        SAI_STP_PORT_ATTR_END,                 /*SAI_OBJECT_TYPE_STP_PORT                 = 46*/
        SAI_RPF_GROUP_ATTR_END,                /*SAI_OBJECT_TYPE_RPF_GROUP                = 47*/
        SAI_RPF_GROUP_MEMBER_ATTR_END,         /*SAI_OBJECT_TYPE_RPF_GROUP_MEMBER         = 48*/
        SAI_L2MC_GROUP_ATTR_END,               /*SAI_OBJECT_TYPE_L2MC_GROUP               = 49*/
        SAI_L2MC_GROUP_MEMBER_ATTR_END,        /*SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER        = 50*/
        SAI_IPMC_GROUP_ATTR_END,               /*SAI_OBJECT_TYPE_IPMC_GROUP               = 51*/
        SAI_IPMC_GROUP_MEMBER_ATTR_END,        /*SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER        = 52*/
        SAI_L2MC_ENTRY_ATTR_END,               /*SAI_OBJECT_TYPE_L2MC_ENTRY               = 53*/
        SAI_IPMC_ENTRY_ATTR_END,               /*SAI_OBJECT_TYPE_IPMC_ENTRY               = 54*/
        SAI_MCAST_FDB_ENTRY_ATTR_END,          /*SAI_OBJECT_TYPE_MCAST_FDB_ENTRY          = 55*/
        SAI_HOSTIF_USER_DEFINED_TRAP_ATTR_END, /*SAI_OBJECT_TYPE_HOSTIF_USER_DEFINED_TRAP = 56*/
        SAI_BRIDGE_ATTR_END,                   /*SAI_OBJECT_TYPE_BRIDGE                   = 57*/
        SAI_BRIDGE_PORT_ATTR_END,              /*SAI_OBJECT_TYPE_BRIDGE_PORT              = 58*/
        SAI_TUNNEL_MAP_ENTRY_ATTR_END,         /*SAI_OBJECT_TYPE_TUNNEL_MAP_ENTRY         = 59*/
        SAI_TAM_ATTR_END,                      /*SAI_OBJECT_TYPE_TAM                      = 60*/
        SAI_SEGMENTROUTE_SIDLIST_ATTR_END,     /*SAI_OBJECT_TYPE_SEGMENTROUTE_SIDLIST     = 61*/
        SAI_PORT_POOL_ATTR_END,                /*SAI_OBJECT_TYPE_PORT_POOL                = 62*/
        SAI_INSEG_ENTRY_ATTR_END,              /*SAI_OBJECT_TYPE_INSEG_ENTRY              = 63*/
        SAI_DTEL_ATTR_END,                     /*SAI_OBJECT_TYPE_DTEL                     = 64*/
        SAI_DTEL_QUEUE_REPORT_ATTR_END,        /*SAI_OBJECT_TYPE_DTEL_QUEUE_REPORT        = 65*/
        SAI_DTEL_INT_SESSION_ATTR_END,         /*SAI_OBJECT_TYPE_DTEL_INT_SESSION         = 66*/
        SAI_DTEL_REPORT_SESSION_ATTR_END,      /*SAI_OBJECT_TYPE_DTEL_REPORT_SESSION      = 67*/
        SAI_DTEL_EVENT_ATTR_END,               /*SAI_OBJECT_TYPE_DTEL_EVENT               = 68*/
        SAI_BFD_SESSION_ATTR_END,              /*SAI_OBJECT_TYPE_BFD_SESSION              = 69*/
        SAI_ISOLATION_GROUP_ATTR_END,          /*SAI_OBJECT_TYPE_ISOLATION_GROUP          = 70*/
        SAI_ISOLATION_GROUP_MEMBER_ATTR_END,   /*SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER   = 71*/
        SAI_TAM_MATH_FUNC_ATTR_END,            /*SAI_OBJECT_TYPE_TAM_MATH_FUNC            = 72*/
        SAI_TAM_REPORT_ATTR_END,               /*SAI_OBJECT_TYPE_TAM_REPORT               = 73*/
        SAI_TAM_EVENT_THRESHOLD_ATTR_END,      /*SAI_OBJECT_TYPE_TAM_EVENT_THRESHOLD      = 74*/
        SAI_TAM_TEL_TYPE_ATTR_END,             /*SAI_OBJECT_TYPE_TAM_TEL_TYPE             = 75*/
        SAI_TAM_TRANSPORT_ATTR_END,            /*SAI_OBJECT_TYPE_TAM_TRANSPORT            = 76*/
        SAI_TAM_TELEMETRY_ATTR_END,            /*SAI_OBJECT_TYPE_TAM_TELEMETRY            = 77*/
        SAI_TAM_COLLECTOR_ATTR_END,            /*SAI_OBJECT_TYPE_TAM_COLLECTOR            = 78*/
        SAI_TAM_EVENT_ACTION_ATTR_END,         /*SAI_OBJECT_TYPE_TAM_EVENT_ACTION         = 79*/
        SAI_TAM_EVENT_ATTR_END,                /*SAI_OBJECT_TYPE_TAM_EVENT                = 80*/
        SAI_NAT_ZONE_COUNTER_ATTR_END,         /*SAI_OBJECT_TYPE_NAT_ZONE_COUNTER         = 81*/
        SAI_NAT_ENTRY_ATTR_END,                /*SAI_OBJECT_TYPE_NAT_ENTRY                = 82*/
        SAI_TAM_INT_ATTR_END,                  /*SAI_OBJECT_TYPE_TAM_INT                  = 83*/
        SAI_COUNTER_ATTR_END,                  /*SAI_OBJECT_TYPE_COUNTER                  = 84*/
        SAI_DEBUG_COUNTER_ATTR_END,            /*SAI_OBJECT_TYPE_DEBUG_COUNTER            = 85*/
        SAI_PORT_SERDES_ATTR_END,              /*SAI_OBJECT_TYPE_PORT_SERDES              = 86*/
        0                                      /*SAI_OBJECT_TYPE_MAX                      = 87*/
    };

    CTC_SAI_PTR_VALID_CHECK(count);
    if (!ctc_sai_is_object_type_valid(object_type)
        ||(object_type > SAI_OBJECT_TYPE_ISOLATION_GROUP_MEMBER))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    *count = cnt[object_type];
    return SAI_STATUS_SUCCESS;
}

sai_status_t
sai_get_object_count(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _Inout_ uint32_t *count)
{
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(count);
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    if (SAI_OBJECT_TYPE_FDB_ENTRY == object_type)
    {
        *count = ctc_sai_fdb_get_fdb_count(lchip);
    }
    else if ((SAI_OBJECT_TYPE_NEIGHBOR_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_ROUTE_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_L2MC_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_IPMC_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_MCAST_FDB_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_INSEG_ENTRY == object_type))
    {
        ctc_sai_db_entry_type_t db_entry_type = 0;
        ctc_sai_db_get_db_entry_type(object_type, &db_entry_type);
        ctc_sai_db_entry_property_get_cnt(lchip, db_entry_type, count);
    }
    else
    {
        ctc_sai_db_get_object_property_count(lchip, object_type, count);
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
sai_get_object_key(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _Inout_ uint32_t *object_count,
        _Inout_ sai_object_key_t *object_list)
{
    uint8 lchip = 0;
    uint32 cnt = 0;
    ctc_sai_db_traverse_param_t traverse_param;
    CTC_SAI_PTR_VALID_CHECK(object_list);
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.lchip = lchip;
    traverse_param.value0 = (void*)&cnt;
    traverse_param.value1 = (void*)object_list;
    if (SAI_OBJECT_TYPE_FDB_ENTRY == object_type)
    {
        cnt = ctc_sai_fdb_get_fdb_count(lchip);
        if (*object_count < cnt)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_BUFFER_OVERFLOW;
        }
        cnt = 0;
        ctc_sai_fdb_dump_fdb_entrys(lchip, *object_count, object_list);
    }
    else if ((SAI_OBJECT_TYPE_NEIGHBOR_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_ROUTE_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_L2MC_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_IPMC_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_MCAST_FDB_ENTRY == object_type)
    || (SAI_OBJECT_TYPE_INSEG_ENTRY == object_type))
    {
        ctc_sai_db_entry_type_t db_entry_type = 0;
        ctc_sai_db_get_db_entry_type(object_type, &db_entry_type);
        ctc_sai_db_entry_property_get_cnt(lchip, db_entry_type, &cnt);
        if (*object_count < cnt)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_BUFFER_OVERFLOW;
        }
        cnt = 0;
        traverse_param.value2 = (void*)(&db_entry_type);
        ctc_sai_db_entry_property_traverse(lchip, db_entry_type, (hash_traversal_fn)_ctc_sai_entry_traversal_fn, (void*)(&traverse_param));
    }
    else
    {
        ctc_sai_db_get_object_property_count(lchip, object_type, &cnt);
        if (*object_count < cnt)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_BUFFER_OVERFLOW;
        }
         cnt = 0;
        ctc_sai_db_traverse_object_property(lchip, object_type, (hash_traversal_fn)_ctc_sai_object_traversal_fn, (void*)(&traverse_param));
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
sai_bulk_get_attribute(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _In_ uint32_t object_count,
        _In_ const sai_object_key_t *object_key,
        _Inout_ uint32_t *attr_count,
        _Inout_ sai_attribute_t **attr_list,
        _Inout_ sai_status_t *object_statuses)
{
    uint8 lchip = 0;
    uint32 i = 0, j = 0;
    uint32 max_count = 0;
    uint32 actual_cnt = 0;
    sai_status_t actual_status = SAI_STATUS_SUCCESS;
    uint32* attr_cnt = NULL;
    sai_object_key_t           key;
    sai_attribute_t* attr = NULL;
    sai_status_t* status = NULL;
    sai_attribute_t attr_tmp;

    CTC_SAI_PTR_VALID_CHECK(object_key);
    CTC_SAI_PTR_VALID_CHECK(attr_count);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_PTR_VALID_CHECK(object_statuses);
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    sai_get_maximum_attribute_count(switch_id, object_type, &max_count);
    for (i = 0; i < object_count; i++)
    {
        actual_cnt = 0;
        attr_cnt = &(attr_count[i]);
        key = object_key[i];
        attr = (sai_attribute_t*)(&(attr_list[i]));
        status = &(object_statuses[i]);
        for (j = 0; j < max_count; j++)
        {
            if (actual_cnt > *attr_cnt)
            {
                *status = SAI_STATUS_BUFFER_OVERFLOW;
                break;
            }
            sal_memset(&attr_tmp, 0, sizeof(sai_attribute_t));
            attr_tmp.id = j;
            actual_status = _ctc_sai_get_single_attribute(object_type, key, &attr_tmp);
            if ((SAI_STATUS_SUCCESS == actual_status)
                ||(SAI_STATUS_BUFFER_OVERFLOW == actual_status))
            {
                sal_memcpy(&(attr[actual_cnt++]), &attr_tmp, sizeof(sai_attribute_t));
                *attr_cnt = actual_cnt;
            }
            else if ((SAI_STATUS_NOT_SUPPORTED == actual_status)
                ||((actual_status>=SAI_STATUS_ATTR_NOT_SUPPORTED_0)&&(actual_status<SAI_STATUS_ATTR_NOT_SUPPORTED_MAX)))
            {
                continue;
            }
            else
            {
                *status = actual_status;
                break;
            }
        }
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t sai_object_type_get_availability(
        _In_ sai_object_id_t switch_id,
        _In_ sai_object_type_t object_type,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list,
        _Out_ uint64_t *count)
{
    uint8 lchip = 0;
    uint32 i = 0, j = 0;   
    uint32 not_match = 0;
    sai_status_t actual_status = SAI_STATUS_SUCCESS;
    uint32 object_count = 0;
    sai_object_key_t *p_object_key_list = NULL;
    sai_attribute_t attr_tmp;
    sai_object_key_t           key;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_PTR_VALID_CHECK(count);
    if (!ctc_sai_is_object_type_valid(object_type))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));    

    sai_get_object_count(switch_id, object_type, &object_count);
    p_object_key_list = mem_malloc(MEM_SYSTEM_MODULE, object_count*sizeof(sai_object_key_t));  
    sai_get_object_key(switch_id, object_type, &object_count, p_object_key_list);
    
    for(i=0; i < object_count;i++ )
    {   
        not_match = 0;
        key = p_object_key_list[i];
        
        for(j=0; j <attr_count;j++ )
        {
            
            attr_tmp.id = attr_list[j].id;
            actual_status = _ctc_sai_get_single_attribute(object_type, key, &attr_tmp);
            if (SAI_STATUS_SUCCESS == actual_status)
            {
                if(sal_memcmp((void*)&(attr_tmp.value), (void*)&(attr_list[j].value), sizeof(sai_attribute_value_t)))
                {
                    continue;
                }
                else
                {
                    not_match = 1;
                    break;
                }
            }
            else
            {
                not_match = 1;
                break;
            }                        
        }
        if (!not_match)
        {
            *count = *count + 1;
        }
        
    }

    return SAI_STATUS_SUCCESS;
}

