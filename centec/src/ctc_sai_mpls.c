/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_tunnel.h"

/*sdk include file*/
#include "ctcs_api.h"
#include "ctc_sai_db.h"
#include "ctc_init.h"



static sai_status_t
_ctc_sai_mpls_attr_param_chk(uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_NUM_OF_POP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        if(attr_value->u8 >1)
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0 + index;
        }
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        if ((SAI_PACKET_ACTION_LOG == attr_value->s32) || (SAI_PACKET_ACTION_COPY == attr_value->s32))
        {
            return SAI_STATUS_INVALID_ATTR_VALUE_0 + index;
        }
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        return SAI_STATUS_SUCCESS;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mpls_build_db(uint8 lchip, const sai_inseg_entry_t *inseg_entry, ctc_sai_mpls_t** mpls_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (p_mpls_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    p_mpls_info = mem_malloc(MEM_MPLS_MODULE, sizeof(ctc_sai_mpls_t));
    if (NULL == p_mpls_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MPLS, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(p_mpls_info, 0, sizeof(ctc_sai_mpls_t));
    status = ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry, (void*)p_mpls_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_mpls_info);
    }
    *mpls_property = p_mpls_info;
    return status;
}

static sai_status_t
_ctc_sai_mpls_remove_db(uint8 lchip, sai_inseg_entry_t *inseg_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mpls_t* p_mpls_info = NULL;

    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    status = ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_MPLS, "_ctc_sai_mpls_remove_db error!\n");
        return status;
    }
    mem_free(p_mpls_info);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_mpls_get_ctc_nh_id(sai_packet_action_t action, sai_object_id_t nexthop_oid, uint32* p_ctc_nh_id, ctc_mpls_ilm_t* p_ctc_mpls_ilm)
{
    uint32 ctc_nh_id = 0;
    ctc_object_id_t ctc_object_id;
    
    sal_memset(&ctc_object_id,0,sizeof(ctc_object_id_t));
    if ((SAI_PACKET_ACTION_DROP == action)
        || (SAI_PACKET_ACTION_DENY == action))
    {
        ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
    }
    else if(SAI_PACKET_ACTION_TRAP == action)
    {
        ctc_nh_id = CTC_NH_RESERVED_NHID_FOR_TOCPU;
    }
    else
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INSEG_ENTRY, nexthop_oid, &ctc_object_id);
        if (SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type && SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER == ctc_object_id.sub_type)
        {
            p_ctc_mpls_ilm->pop = 1;
            p_ctc_mpls_ilm->decap = 1;
        }
        else if((SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type) || (SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type))
        {
            ctc_sai_oid_get_nexthop_id(nexthop_oid, &ctc_nh_id);
        }
    }
    *p_ctc_nh_id = ctc_nh_id;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mpls_create_inseg_entry(const sai_inseg_entry_t *inseg_entry,
                                             uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32_t index = 0;
    const sai_attribute_value_t *attr_value;
    sai_packet_action_t action = SAI_PACKET_ACTION_FORWARD;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    sai_object_id_t nexthop_oid = 0;
    sai_object_id_t tunnel_oid = 0;
    uint32 ctc_nh_id = 0;
    ctc_sai_router_interface_t* p_route_interface = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_object_id_t ctc_object_id;
    ctc_object_id_t ctc_object_id_br;
    sai_object_id_t bridge_oid = 0;
    ctc_mpls_ilm_qos_map_t ilm_qos_map;
    
    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));
    sal_memset(&ilm_qos_map, 0, sizeof(ctc_mpls_ilm_qos_map_t));
    
    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (p_mpls_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_NUM_OF_POP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        ctc_mpls_ilm.pop = attr_value->u8;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        action = attr_value->s32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       nexthop_oid = attr_value->oid;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_TUNNEL_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       tunnel_oid = attr_value->oid;
       p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_oid);
    }
    _ctc_sai_mpls_get_ctc_nh_id(action, nexthop_oid, &ctc_nh_id, &ctc_mpls_ilm);
    ctc_mpls_ilm.nh_id = ctc_nh_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INSEG_ENTRY, nexthop_oid, &ctc_object_id);
    if(SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type)
    {
        p_route_interface = ctc_sai_db_get_object_property(lchip, nexthop_oid);
        if(0 != p_route_interface->dot1d_bridge_id)
        {
            bridge_oid = p_route_interface->dot1d_bridge_id;
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE, bridge_oid, &ctc_object_id_br);
            if(SAI_BRIDGE_TYPE_CROSS_CONNECT != ctc_object_id_br.sub_type)
            {
                ctc_mpls_ilm.fid = ctc_object_id_br.value;
                ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_VPLS;
                ctc_mpls_ilm.logic_port_type = TRUE;

                if(NULL != p_tunnel)
                {
                    ctc_mpls_ilm.pwid = p_tunnel->logic_port;
                }
            }
            else
            {
                ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_VPWS;
                ctc_mpls_ilm.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
            }
            if(NULL != p_tunnel)
            {
                ctc_mpls_ilm.cwen = p_tunnel->decap_cw_en;
                ctc_mpls_ilm.pw_mode = p_tunnel->decap_pw_mode;
                /* need update sdk api to set DsMpls.metadata for tm1.1 and DsMpls.ttlThresholdIndex for tm2 */
                //ctc_mpls_ilm.??metadata/ttlThresholdIndex?? = p_tunnel->decap_esi_label_valid;
                if(p_tunnel->decap_esi_label_valid)
                {
                    CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ESLB_EXIST);
                }
            }
        }
        else
        {
            if(NULL != p_tunnel)
            {
                if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
                {
                    ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_L3VPN;
                    ctc_mpls_ilm.flw_vrf_srv_aps.vrf_id = p_route_interface->vrf_id;
                    ctc_mpls_ilm.id_type |= CTC_MPLS_ID_VRF;
                    if(SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL == p_tunnel->decap_ttl_mode)
                    {
                        ctc_mpls_ilm.model = CTC_MPLS_TUNNEL_MODE_UNIFORM;
                    }
                    else if(SAI_TUNNEL_TTL_MODE_PIPE_MODEL == p_tunnel->decap_ttl_mode)
                    {
                        ctc_mpls_ilm.model = CTC_MPLS_TUNNEL_MODE_PIPE;
                    }
                    if(SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL == p_tunnel->decap_exp_mode)
                    {
                        ctc_mpls_ilm.trust_outer_exp = 1;
                    }
                    else if(SAI_TUNNEL_EXP_MODE_PIPE_MODEL == p_tunnel->decap_exp_mode)
                    {
                        ctc_mpls_ilm.trust_outer_exp = 0;
                    }
                }
            }
        }
    }
    
    if(NULL != p_tunnel )
    {
        if(p_tunnel->decap_acl_use_outer && (SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type))
        {
            CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ACL_USE_OUTER_INFO);
        }
    }
    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_mpls_add_ilm(lchip, &ctc_mpls_ilm), status, out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_build_db(lchip, inseg_entry, &p_mpls_info), status, error1);
    if(NULL != p_tunnel)
    {
        p_tunnel->inseg_label = inseg_entry->label;
    }
    p_mpls_info->action = action;
    p_mpls_info->nexthop_oid = nexthop_oid;
    return SAI_STATUS_SUCCESS;

error1:
    CTC_SAI_LOG_ERROR(SAI_API_MPLS, "rollback to error1\n");
    ctcs_mpls_del_ilm(lchip, &ctc_mpls_ilm);
out:
    return status;
}

static sai_status_t
_ctc_sai_mpls_remove_inseg_entry(const sai_inseg_entry_t *inseg_entry)
{
    uint8 lchip = 0;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;

    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));

    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_del_ilm(lchip, &ctc_mpls_ilm));
    _ctc_sai_mpls_remove_db(lchip, (void*)inseg_entry);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_mpls_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 invalid_nh_id[64] = {0};
    const sai_inseg_entry_t* inseg_entry = &(key->key.inseg_entry);
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    //ctc_mpls_ilm_t ctc_mpls_ilm_tmp;
    sai_packet_action_t action = SAI_PACKET_ACTION_FORWARD;
    sai_object_id_t nexthop_oid = 0;
    uint32 ctc_nh_id = 0;

    sal_memset(&ctc_mpls_ilm, 0, sizeof(ctc_mpls_ilm_t));
    //sal_memset(&ctc_mpls_ilm_tmp, 0, sizeof(ctc_mpls_ilm_t));

    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    action = p_mpls_info->action;
    nexthop_oid = p_mpls_info->nexthop_oid;
    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));
    //ctc_mpls_ilm.pop = ctc_mpls_ilm_tmp.pop;

    switch (attr->id)
    {
        case SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
            ctc_mpls_ilm.pop = attr->value.u8;
            break;
        case SAI_INSEG_ENTRY_ATTR_PACKET_ACTION:
            action = attr->value.s32;
            break;
        case SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID:
            nexthop_oid = attr->value.oid;
            break;
        default:
            break;
    }

    _ctc_sai_mpls_get_ctc_nh_id(action, nexthop_oid, &ctc_nh_id, &ctc_mpls_ilm);

    //ctc_mpls_ilm.label = inseg_entry->label;
    ctc_mpls_ilm.nh_id = ctc_nh_id;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
    p_mpls_info->action = action;
    p_mpls_info->nexthop_oid = nexthop_oid;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mpls_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    const sai_inseg_entry_t *inseg_entry = &(key->key.inseg_entry);
    uint8 lchip = 0;
    uint32 invalid_nh_id[64] = {0};
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;

    sal_memset(&ctc_mpls_ilm, 0, sizeof(ctc_mpls_ilm_t));

    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));

    switch (attr->id)
    {
        case SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
            attr->value.u8 = ctc_mpls_ilm.pop;
            break;
        case SAI_INSEG_ENTRY_ATTR_PACKET_ACTION:
            attr->value.s32 = p_mpls_info->action;
            break;
        case SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
        case SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID:
            attr->value.oid = p_mpls_info->nexthop_oid;
            break;
        case SAI_INSEG_ENTRY_ATTR_TUNNEL_ID:
             attr->value.oid = p_mpls_info->decap_tunnel_oid;
             break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t mpls_attr_fn_entries[] = {
    { SAI_INSEG_ENTRY_ATTR_NUM_OF_POP,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_PACKET_ACTION,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_TRAP_PRIORITY,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static sai_status_t
_ctc_sai_mpls_set_inseg_entry_attr(const sai_inseg_entry_t *inseg_entry, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    sal_memset(&key, 0, sizeof(key));
    sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
    status = ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_INSEG_ENTRY,  mpls_attr_fn_entries, attr);
    return status;
}

static sai_status_t
_ctc_sai_mpls_get_inseg_entry_attr(const sai_inseg_entry_t *inseg_entry,
                                                uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8          loop = 0;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_LOG_ENTER(SAI_API_MPLS);
    sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_INSEG_ENTRY, loop, mpls_attr_fn_entries, &attr_list[loop]));
        loop++;
    }
    return status;
}

#define ________SAI_DUMP________

static
sai_status_t _ctc_sai_mpls_dump_print_cb(ctc_sai_entry_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_mpls_t    mpls_cur;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    sai_label_id_t label_cur = 0;
    char action_str[25] = {0};
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&mpls_cur, 0, sizeof(ctc_sai_mpls_t));

    label_cur = bucket_data->key.mpls.label;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.inseg_entry.switch_id) && (label_cur != p_dmp_grep->key.key.inseg_entry.label))
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memcpy((ctc_sai_mpls_t*)(&mpls_cur), bucket_data->data, sizeof(ctc_sai_mpls_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    ctc_sai_get_packet_action_desc(mpls_cur.action, action_str);

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%05x %-20s 0x%016"PRIx64 "\n", num_cnt, label_cur, action_str, mpls_cur.nexthop_oid);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

void _ctc_sai_mpls_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "MPLS");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mpls_t");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%-4s %-7s %-20s %-18s\n", \
        "No.", "Label", "Packet_action", "Nexthop_oid");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;

    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS,
                                       (hash_traversal_fn) _ctc_sai_mpls_dump_print_cb, (void*)(&sai_cb_data));
}

#define ________INTERNAL_API________

void
ctc_sai_mpls_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    CTC_SAI_LOG_DUMP(p_file, "\n");
    CTC_SAI_LOG_DUMP(p_file, "# SAI MPLS MODULE\n");

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_INSEG_ENTRY))
    {
        _ctc_sai_mpls_dump(lchip, p_file, dump_grep_param);
    }
}

#define ________SAI_API________

static sai_status_t
ctc_sai_mpls_create_inseg_entry(const sai_inseg_entry_t *inseg_entry,
                                             uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_mpls_attr_param_chk(attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    status = _ctc_sai_mpls_create_inseg_entry(inseg_entry, attr_count, attr_list);

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mpls_remove_inseg_entry(const sai_inseg_entry_t *inseg_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    status = _ctc_sai_mpls_remove_inseg_entry(inseg_entry);

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mpls_set_inseg_entry_attr(const sai_inseg_entry_t *inseg_entry, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    CTC_SAI_ERROR_RETURN(_ctc_sai_mpls_attr_param_chk(1, attr));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_MPLS);
    status = _ctc_sai_mpls_set_inseg_entry_attr(inseg_entry, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_mpls_get_inseg_entry_attr(const sai_inseg_entry_t *inseg_entry,
                                                uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_MPLS);
    status = _ctc_sai_mpls_get_inseg_entry_attr(inseg_entry, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_mpls_api_t ctc_sai_mpls_api = {
    ctc_sai_mpls_create_inseg_entry,
    ctc_sai_mpls_remove_inseg_entry,
    ctc_sai_mpls_set_inseg_entry_attr,
    ctc_sai_mpls_get_inseg_entry_attr
};

sai_status_t
ctc_sai_mpls_api_init()
{
    ctc_sai_register_module_api(SAI_API_MPLS, (void*)&ctc_sai_mpls_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_mpls_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_MPLS;
    wb_info.data_len = sizeof(ctc_sai_mpls_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = NULL;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}
