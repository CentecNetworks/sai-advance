/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_route.h"
#include "ctc_sai_counter.h"

/*sdk include file*/
#include "ctcs_api.h"

static sai_status_t
_ctc_sai_route_mapping_ipuc_key(const sai_route_entry_t *route_entry, ctc_ipuc_param_t* ipuc_info)
{
    ipv6_addr_t ipv6_mask;
    ctc_sai_oid_get_vrf_id(route_entry->vr_id, &(ipuc_info->vrf_id));
    ipuc_info->ip_ver = (SAI_IP_ADDR_FAMILY_IPV4 == route_entry->destination.addr_family)?
                           CTC_IP_VER_4 : CTC_IP_VER_6;
    sal_memcpy(&(ipuc_info->ip), &(route_entry->destination.addr), sizeof(ipv6_addr_t));
    sal_memcpy(ipv6_mask, &(route_entry->destination.mask), sizeof(ipv6_addr_t));
    CTC_SAI_NTOH_V6(ipuc_info->ip.ipv6);
    CTC_SAI_NTOH_V6(ipv6_mask);
    if (CTC_IP_VER_4 == ipuc_info->ip_ver)
    {
        IPV4_MASK_TO_LEN(ipv6_mask[0], ipuc_info->masklen);
    }
    else
    {
        IPV6_MASK_TO_LEN(ipv6_mask, ipuc_info->masklen);
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_route_mapping_ipuc_action(ctc_ipuc_param_t* ipuc_info, sai_packet_action_t action, sai_object_id_t nh_obj_id, uint16 cid, sai_object_id_t counter_obj_id)
{
    uint32 ctc_nh_id = 0;
    ctc_object_id_t ctc_object_id;

    if ((SAI_PACKET_ACTION_FORWARD == action) || (SAI_PACKET_ACTION_COPY == action)
        || (SAI_PACKET_ACTION_LOG == action) || (SAI_PACKET_ACTION_TRANSIT == action))
    {
        if (nh_obj_id != SAI_NULL_OBJECT_ID)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, nh_obj_id, &ctc_object_id);
            if ((SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type) || (SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type))
            {
                ctc_sai_oid_get_nexthop_id(nh_obj_id, &ctc_nh_id);
            }
            else if((SAI_OBJECT_TYPE_PORT == ctc_object_id.type)||(SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type))/*ip2me*/
            {
                ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_TOCPU;
                CTC_SET_FLAG(ipuc_info->route_flag, CTC_IPUC_FLAG_PROTOCOL_ENTRY);
            }
            else
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
        }
        else
        {
            ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
        }
    }

    CTC_SET_FLAG(ipuc_info->route_flag, CTC_IPUC_FLAG_TTL_CHECK);
    CTC_UNSET_FLAG(ipuc_info->route_flag, CTC_IPUC_FLAG_CPU);

    switch (action)
    {
        case SAI_PACKET_ACTION_DROP:
        case SAI_PACKET_ACTION_DENY:
            ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
            break;
        case SAI_PACKET_ACTION_COPY:
        case SAI_PACKET_ACTION_LOG:
            CTC_SET_FLAG(ipuc_info->route_flag, CTC_IPUC_FLAG_CPU);
            break;
        case SAI_PACKET_ACTION_TRAP:
            CTC_SET_FLAG(ipuc_info->route_flag, CTC_IPUC_FLAG_CPU);
            ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
            break;
        case SAI_PACKET_ACTION_FORWARD:
        case SAI_PACKET_ACTION_TRANSIT:
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }

    if (counter_obj_id != SAI_NULL_OBJECT_ID)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_create(counter_obj_id, CTC_SAI_COUNTER_TYPE_ROUTE, &ipuc_info->stats_id));
        ipuc_info->route_flag |= CTC_IPUC_FLAG_STATS_EN;
    }

    ipuc_info->nh_id = ctc_nh_id;
    ipuc_info->cid = cid;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_route_build_db(uint8 lchip, const sai_route_entry_t *route_entry, ctc_sai_route_t** route_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_route_t* p_route_info = NULL;
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (p_route_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    p_route_info = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_route_t));
    if (NULL == p_route_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTE, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(p_route_info, 0, sizeof(ctc_sai_route_t));
    status = ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry, (void*)p_route_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_route_info);
    }
    *route_property = p_route_info;
    return status;
}

static sai_status_t
_ctc_sai_route_remove_db(uint8 lchip, sai_route_entry_t *route_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_route_t* p_route_info = NULL;
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (NULL == p_route_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    status = ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTE, "_ctc_sai_route_remove_db error!\n");
        return status;
    }
    mem_free(p_route_info);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_route_create_route(const sai_route_entry_t *route_entry,
                                             uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_ipuc_param_t ipuc_info;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    sai_packet_action_t action = SAI_PACKET_ACTION_FORWARD;
    sai_object_id_t nh_obj_id = 0, counter_obj_id = 0;
    uint16 cid = 0;
    ctc_sai_route_t* p_route_info = NULL;

    CTC_SAI_PTR_VALID_CHECK(route_entry);
    ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip);
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (p_route_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        action = attr_value->s32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        nh_obj_id = attr_value->oid;
    }
    if ((SAI_PACKET_ACTION_FORWARD == action)
        || (SAI_PACKET_ACTION_COPY == action)
        || (SAI_PACKET_ACTION_LOG == action)
        || (SAI_PACKET_ACTION_TRANSIT == action))
    {
        if (0 == nh_obj_id)
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTE_ENTRY_ATTR_META_DATA, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        cid = CTC_SAI_META_DATA_SAI_TO_CTC(attr_value->u32);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTE_ENTRY_ATTR_COUNTER_ID, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        counter_obj_id = attr_value->oid;
    }

    sal_memset(&ipuc_info, 0, sizeof(ipuc_info));
    CTC_SAI_ERROR_GOTO(_ctc_sai_route_mapping_ipuc_key(route_entry, &ipuc_info), status, error1);
    CTC_SAI_ERROR_GOTO(_ctc_sai_route_mapping_ipuc_action(&ipuc_info, action, nh_obj_id, cid, counter_obj_id), status, error1);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_ipuc_add(lchip, &ipuc_info), status, error1);
    CTC_SAI_ERROR_GOTO(_ctc_sai_route_build_db(lchip, route_entry, &p_route_info), status, error2);
    p_route_info->action = action;
    p_route_info->nh_obj_id = nh_obj_id;
    p_route_info->cid = cid;
    p_route_info->counter_obj_id = counter_obj_id;
    return SAI_STATUS_SUCCESS;

error2:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTE, "rollback to error2\n");
    ctcs_ipuc_remove(lchip, &ipuc_info);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTE, "rollback to error1\n");

out:
    return status;
}

static sai_status_t
_ctc_sai_route_remove_route(const sai_route_entry_t *route_entry)
{
    uint8 lchip = 0;
    ctc_ipuc_param_t ipuc_info;
    ctc_sai_route_t* p_route_info = NULL;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip);
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (NULL == p_route_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&ipuc_info, 0, sizeof(ipuc_info));
    CTC_SAI_ERROR_RETURN(_ctc_sai_route_mapping_ipuc_key(route_entry, &ipuc_info));
    CTC_SAI_ERROR_RETURN(_ctc_sai_route_mapping_ipuc_action(&ipuc_info, p_route_info->action, p_route_info->nh_obj_id, p_route_info->cid, SAI_NULL_OBJECT_ID));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_remove(lchip, &ipuc_info));
    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_route_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_ROUTE));
    _ctc_sai_route_remove_db(lchip, (void*)route_entry);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_route_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    const sai_route_entry_t *route_entry = &(key->key.route_entry);
    ctc_sai_route_t* p_route_info = NULL;
    ctc_ipuc_param_t ipuc_info;
    sai_packet_action_t action = 0;
    sai_object_id_t nh_obj_id= 0, counter_obj_id = 0;
    uint16 cid = 0;
    uint8 is_set_counter_oid = 0;

    ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip);
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (NULL == p_route_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    action = p_route_info->action;
    nh_obj_id = p_route_info->nh_obj_id;
    cid = p_route_info->cid;
    counter_obj_id = p_route_info->counter_obj_id;

    sal_memset(&ipuc_info, 0, sizeof(ipuc_info));
    CTC_SAI_ERROR_RETURN(_ctc_sai_route_mapping_ipuc_key(route_entry, &ipuc_info));
    CTC_SAI_ERROR_RETURN(ctcs_ipuc_get(lchip, &ipuc_info));
    CTC_SAI_ERROR_RETURN(_ctc_sai_route_mapping_ipuc_key(route_entry, &ipuc_info));
    switch (attr->id)
    {
        case SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
            action = attr->value.s32;
            break;
        case SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
            nh_obj_id = attr->value.oid;
            break;
        case SAI_ROUTE_ENTRY_ATTR_META_DATA:
            cid = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            break;
        case SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
            counter_obj_id = attr->value.oid;
            /* del old stats id */
            if((p_route_info->counter_obj_id != SAI_NULL_OBJECT_ID) && (p_route_info->counter_obj_id != counter_obj_id))
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_route_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_ROUTE));
            }
            is_set_counter_oid = 1;
            break;
        case SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID:
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    CTC_SAI_ERROR_RETURN(_ctc_sai_route_mapping_ipuc_action(&ipuc_info, action, nh_obj_id, cid, is_set_counter_oid ? counter_obj_id : SAI_NULL_OBJECT_ID));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_add(lchip, &ipuc_info));
    p_route_info->action = action;
    p_route_info->nh_obj_id = nh_obj_id;
    p_route_info->cid = cid;
    p_route_info->counter_obj_id = counter_obj_id;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_route_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    const sai_route_entry_t *route_entry = &(key->key.route_entry);
    uint8 lchip = 0;
    ctc_sai_route_t* p_route_info = NULL;
    ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip);
    p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)route_entry);
    if (NULL == p_route_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
            attr->value.s32 = p_route_info->action;
            break;
        case SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
            attr->value.oid = p_route_info->nh_obj_id;
            break;
        case SAI_ROUTE_ENTRY_ATTR_META_DATA:
            attr->value.u32 = CTC_SAI_META_DATA_CTC_TO_SAI(p_route_info->cid);
            break;
        case SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY:
            attr->value.u32 = route_entry->destination.addr_family;
            break;
        case SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
            attr->value.oid = p_route_info->counter_obj_id;
            break;
        case SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID:
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t route_attr_fn_entries[] = {
    { SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION,
      _ctc_sai_route_get_attr,
      _ctc_sai_route_set_attr},
    { SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID,
      _ctc_sai_route_get_attr,
      _ctc_sai_route_set_attr},
    { SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID,
      _ctc_sai_route_get_attr,
      _ctc_sai_route_set_attr},
    { SAI_ROUTE_ENTRY_ATTR_META_DATA,
      _ctc_sai_route_get_attr,
      _ctc_sai_route_set_attr},
    { SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY,
      _ctc_sai_route_get_attr,
      NULL},
    { SAI_ROUTE_ENTRY_ATTR_COUNTER_ID,
      _ctc_sai_route_get_attr,
      _ctc_sai_route_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

static sai_status_t
_ctc_sai_route_set_route_attr(const sai_route_entry_t *route_entry, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    sal_memset(&key, 0, sizeof(key));
    sal_memcpy(&key.key.route_entry, route_entry, sizeof(sai_route_entry_t));
    status = ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_ROUTE_ENTRY,  route_attr_fn_entries, attr);
    return status;
}

static sai_status_t
_ctc_sai_route_get_route_attr(const sai_route_entry_t *route_entry,
                                                uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8          loop = 0;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    sal_memcpy(&key.key.route_entry, route_entry, sizeof(sai_route_entry_t));
    while(loop < attr_count)
    {

        CTC_SAI_ERROR_RETURN(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_ROUTE_ENTRY, loop, route_attr_fn_entries, &attr_list[loop]));
        loop++;
    }
    return status;
}

static sai_status_t
_ctc_sai_next_route_dump_print_cb(ctc_sai_entry_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_route_t* p_route_info = (ctc_sai_route_t*)(bucket_data->data);;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint8 ip_ver = 0;
    char vr_oid[64] = {'-'};
    char ip[64] = {'-'};
    char ip_mask[64] = {'-'};
    char nh_obj_id[64] = {0 };
    sai_ip_address_t ip_addr;
    sai_route_entry_t         route_entry;

    p_file = (sal_file_t)p_cb_data->value0;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ip_ver = *((uint8 *)(p_cb_data->value3));

    if (bucket_data->key.route.ip_ver != ip_ver)
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_memset(&route_entry, 0, sizeof(sai_route_entry_t));
    if (sal_memcmp(&route_entry, &(p_dmp_grep->key.key.route_entry), sizeof(sai_route_entry_t)))
    {
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_db_entry_unmapping_key(p_cb_data->lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, bucket_data, &route_entry);
    if (!sal_memcmp(&route_entry, &p_dmp_grep->key.key.route_entry, sizeof(sai_route_entry_t)))
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&ip_addr, 0, sizeof(sai_ip_address_t));
    sal_memcpy(&(ip_addr.addr), &(route_entry.destination.addr), sizeof(sai_ip_addr_t));
    ip_addr.addr_family = route_entry.destination.addr_family;
    ctc_sai_get_ip_str(&ip_addr, ip);
    sal_sprintf(ip_mask, "/%d", bucket_data->key.route.mask_len);
    sal_strcat(ip, ip_mask);
    sal_sprintf(vr_oid, "0x%016"PRIx64, route_entry.vr_id);
    sal_sprintf(nh_obj_id, "0x%016"PRIx64, p_route_info->nh_obj_id);
    CTC_SAI_LOG_DUMP(p_file, "%-8s%-22s%-48s%-22s%-8d%-12d\n", "No.", vr_oid, ip, nh_obj_id, p_route_info->cid, p_route_info->action);
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}


#define ________INTERNAL_API________
void ctc_sai_route_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    uint8 ip_ver = SAI_IP_ADDR_FAMILY_IPV4;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.lchip = lchip;
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Route MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ROUTE_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Route");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_route_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-22s%-48s%-22s%-8s%-12s\n", "No.", "vr_id", "ip4", "nh_obj_id", "cid", "action");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        sai_cb_data.value3 = &ip_ver;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE,
                                            (hash_traversal_fn)_ctc_sai_next_route_dump_print_cb, (void*)(&sai_cb_data));
        num_cnt = 1;
        ip_ver = SAI_IP_ADDR_FAMILY_IPV6;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_route_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-22s%-48s%-22s%-8s%-12s\n", "No.", "vr_id", "ip6", "nh_obj_id", "cid", "action");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        sai_cb_data.value3 = &ip_ver;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE,
                                            (hash_traversal_fn)_ctc_sai_next_route_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
static sai_status_t
ctc_sai_route_create_route(const sai_route_entry_t *route_entry,
                                             uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_PTR_VALID_CHECK(route_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    p_switch_master = ctc_sai_get_switch_property(lchip);
    status = _ctc_sai_route_create_route(route_entry, attr_count, attr_list);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_switch_master->route_cnt[route_entry->destination.addr_family]++;
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_route_remove_route(const sai_route_entry_t *route_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    status = _ctc_sai_route_remove_route(route_entry);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_switch_master->route_cnt[route_entry->destination.addr_family]--;
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_route_set_route_attr(const sai_route_entry_t *route_entry, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    status = _ctc_sai_route_set_route_attr(route_entry, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_route_get_route_attr(const sai_route_entry_t *route_entry,
                                                uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    status = _ctc_sai_route_get_route_attr(route_entry, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_route_bulk_create_route(
         uint32_t object_count,
         const sai_route_entry_t *route_entry,
         const uint32_t *attr_count,
         const sai_attribute_t **attr_list,
         sai_bulk_op_error_mode_t mode,
         sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        p_switch_master = ctc_sai_get_switch_property(lchip);
        object_statuses[i] = _ctc_sai_route_create_route(&(route_entry[i]), attr_count[i], (attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
        }

        if (SAI_STATUS_SUCCESS == object_statuses[i])
        {
            p_switch_master->route_cnt[route_entry[i].destination.addr_family]++;
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_route_bulk_remove_route(
         uint32_t object_count,
         const sai_route_entry_t *route_entry,
         sai_bulk_op_error_mode_t mode,
         sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        p_switch_master = ctc_sai_get_switch_property(lchip);
        object_statuses[i] = _ctc_sai_route_remove_route(&(route_entry[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
        }

        if (SAI_STATUS_SUCCESS == object_statuses[i])
        {
            p_switch_master->route_cnt[route_entry[i].destination.addr_family]--;
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_route_bulk_set_route_attr(
         uint32_t object_count,
         const sai_route_entry_t *route_entry,
         const sai_attribute_t *attr_list,
         sai_bulk_op_error_mode_t mode,
         sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_route_set_route_attr(&(route_entry[i]), &(attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

static sai_status_t
ctc_sai_route_bulk_get_route_attr(
         uint32_t object_count,
         const sai_route_entry_t *route_entry,
         const uint32_t *attr_count,
         sai_attribute_t **attr_list,
         sai_bulk_op_error_mode_t mode,
         sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTE);
    CTC_SAI_PTR_VALID_CHECK(route_entry);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = SAI_STATUS_NOT_EXECUTED;
    }
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(route_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_route_get_route_attr(&(route_entry[i]), attr_count[i], (attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_FAILURE;
        }
        else if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
        }
        
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

const sai_route_api_t ctc_sai_route_api = {
    ctc_sai_route_create_route,
    ctc_sai_route_remove_route,
    ctc_sai_route_set_route_attr,
    ctc_sai_route_get_route_attr,
    ctc_sai_route_bulk_create_route,
    ctc_sai_route_bulk_remove_route,
    ctc_sai_route_bulk_set_route_attr,
    ctc_sai_route_bulk_get_route_attr
};

sai_status_t
ctc_sai_route_api_init()
{
    ctc_sai_register_module_api(SAI_API_ROUTE, (void*)&ctc_sai_route_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_route_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ROUTE;
    wb_info.data_len = sizeof(ctc_sai_route_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

