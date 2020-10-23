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
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_policer.h"

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
_ctc_sai_mpls_remove_db(uint8 lchip, const sai_inseg_entry_t *inseg_entry)
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
ctc_sai_mpls_db_op(uint8 lchip, uint8 db_op, const sai_inseg_entry_t *inseg_entry,  ctc_sai_mpls_t** mpls_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    if(SAI_MPLS_DB_OP_DEL == db_op)
    {
        status = _ctc_sai_mpls_remove_db(lchip, inseg_entry);
    }
    else
    {
        status = _ctc_sai_mpls_build_db(lchip, inseg_entry, mpls_property);
    }
    return status;
}

static sai_status_t
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
_ctc_sai_mpls_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint32 invalid_nh_id[64] = {0};
    const sai_inseg_entry_t* inseg_entry = &(key->key.inseg_entry);
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    sai_packet_action_t action = SAI_PACKET_ACTION_FORWARD;
    uint8 pop = 1;
    sai_object_id_t nexthop_oid = 0;
    uint32 ctc_nh_id = 0, policer_id = 0;
    ctc_object_id_t ctc_object_id;
    ctc_object_id_t ctc_object_id_old;
    ctc_sai_router_interface_t* p_route_interface = NULL;
    ctc_sai_counter_t* p_counter_info = NULL;
    uint8 ilm_update = 0;
    uint32 psc_type = SAI_INSEG_ENTRY_PSC_TYPE_ELSP;
    uint8 qos_tc = 0, enable = 0;;
    uint32 exp_to_tc_map_id = 0, exp_to_color_map_id = 0;
    ctc_mpls_property_t mpls_pro;
    ctc_mpls_ilm_qos_map_t ilm_qos_map;
    uint16 service_id = 0, old_service_id = 0, service_id_update = 0xff;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_sai_next_hop_grp_t* p_nhp_grp_frr = NULL;
    
    
    sal_memset(&ilm_qos_map, 0, sizeof(ilm_qos_map));
    sal_memset(&mpls_pro, 0, sizeof(mpls_pro));

    sal_memset(&ctc_mpls_ilm, 0, sizeof(ctc_mpls_ilm_t));

    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_mpls_info->is_es)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    action = p_mpls_info->action;
    nexthop_oid = p_mpls_info->nexthop_oid;
    psc_type = p_mpls_info->psc_type;
    qos_tc = p_mpls_info->qos_tc;
    exp_to_tc_map_id = p_mpls_info->exp_to_tc_map_id;
    exp_to_color_map_id = p_mpls_info->exp_to_color_map_id;
    policer_id = p_mpls_info->policer_id;
    service_id = p_mpls_info->service_id;

    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_get_ilm(lchip, invalid_nh_id, &ctc_mpls_ilm));

    switch (attr->id)
    {
        case SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
            pop = attr->value.u8;
            ilm_update = 1;
            break;
        case SAI_INSEG_ENTRY_ATTR_PACKET_ACTION:
            action = attr->value.s32;
            ilm_update = 1;
            break;
        case SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID:
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INSEG_ENTRY, attr->value.oid, &ctc_object_id);
            if(SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type)
            {
                p_route_interface = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if(SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER != ctc_object_id.sub_type)
                {
                    return SAI_STATUS_INVALID_PARAMETER;
                }
                else if(0 != p_route_interface->dot1d_bridge_id)
                {
                    return SAI_STATUS_NOT_SUPPORTED;
                }
            }
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, nexthop_oid, &ctc_object_id_old);
            if(ctc_object_id_old.type != ctc_object_id.type)
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
            nexthop_oid = attr->value.oid;
            ilm_update = 1;
            break;
        case SAI_INSEG_ENTRY_ATTR_PSC_TYPE:
            psc_type = attr->value.s32;

            if(SAI_INSEG_ENTRY_PSC_TYPE_LLSP == psc_type)
            {                    
                /*Change from ELSP, need clear exp to tc qosmap */
                if(p_mpls_info->psc_type == SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
                {
                    if(p_mpls_info->exp_to_tc_map_id)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, qos_tc,
                                                    p_mpls_info->exp_to_tc_map_id,
                                                    SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, 0));
                        p_mpls_info->exp_to_tc_map_id = 0;
                        exp_to_tc_map_id = 0;
                    }
                }
                
                ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_LLSP;
                ilm_qos_map.priority = qos_tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
                ilm_qos_map.exp_domain = p_mpls_info->qos_domain_id;
                mpls_pro.label = inseg_entry->label;
                mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
                mpls_pro.value = &ilm_qos_map;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_set_ilm_property(lchip, &mpls_pro));
            }
            else if(SAI_INSEG_ENTRY_PSC_TYPE_ELSP == psc_type)
            {
                ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_ELSP;
                ilm_qos_map.exp_domain = p_mpls_info->qos_domain_id;
                mpls_pro.label = inseg_entry->label;
                mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
                mpls_pro.value = &ilm_qos_map;       
                CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_set_ilm_property(lchip, &mpls_pro));
            }
            else
            {
                         
                /*Change from ELSP, need clear exp to tc qosmap & exp to color qosmap */
                if(p_mpls_info->psc_type == SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
                {
                    if(p_mpls_info->exp_to_tc_map_id)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, qos_tc,
                                                p_mpls_info->exp_to_tc_map_id,
                                                SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, 0));
                        p_mpls_info->exp_to_tc_map_id = 0;
                        exp_to_tc_map_id = 0;
                    }
                    if(p_mpls_info->exp_to_color_map_id)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, qos_tc,
                                                    p_mpls_info->exp_to_color_map_id,
                                                    SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, 0));
                        p_mpls_info->exp_to_color_map_id = 0;
                        
                        exp_to_color_map_id = 0;
                    }
                }
                /*Change from LLSP, need clear exp to color qosmap */
                else if(p_mpls_info->psc_type == SAI_INSEG_ENTRY_PSC_TYPE_LLSP)
                {
                    if(p_mpls_info->exp_to_color_map_id)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, qos_tc,
                                                    p_mpls_info->exp_to_color_map_id,
                                                    SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, 0));
                        p_mpls_info->exp_to_color_map_id = 0;
                        
                        exp_to_color_map_id = 0;
                    }
                }

                ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_DISABLE;
                mpls_pro.label = inseg_entry->label;
                mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
                mpls_pro.value = &ilm_qos_map; 
                
                CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_set_ilm_property(lchip, &mpls_pro));
                
            }

            
            break;
        case SAI_INSEG_ENTRY_ATTR_QOS_TC:
            if(p_mpls_info->psc_type != SAI_INSEG_ENTRY_PSC_TYPE_LLSP)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            qos_tc = attr->value.u8;

            ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_LLSP;
            ilm_qos_map.priority = qos_tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
            ilm_qos_map.exp_domain = p_mpls_info->qos_domain_id;
            mpls_pro.label = inseg_entry->label;
            mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
            mpls_pro.value = &ilm_qos_map;

            CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_set_ilm_property(lchip, &mpls_pro));
            break;
        case SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP:
            if(p_mpls_info->psc_type != SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            ctc_sai_oid_get_value(attr->value.oid, &exp_to_tc_map_id);
            if(exp_to_tc_map_id == p_mpls_info->exp_to_tc_map_id)
            {
                return SAI_STATUS_SUCCESS;
            }
            if (SAI_NULL_OBJECT_ID != attr->value.oid)
            {
                enable = TRUE;
            }

            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, psc_type, qos_tc,
                                                enable ? exp_to_tc_map_id : p_mpls_info->exp_to_tc_map_id,
                                                SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, enable));
            break;
        case SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP:
            if(p_mpls_info->psc_type == SAI_INSEG_ENTRY_PSC_TYPE_NONE)
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            
            ctc_sai_oid_get_value(attr->value.oid, &exp_to_color_map_id);

            if(exp_to_color_map_id == p_mpls_info->exp_to_color_map_id)
            {
                return SAI_STATUS_SUCCESS;
            }

            if (SAI_NULL_OBJECT_ID != attr->value.oid)
            {
                enable = TRUE;
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, psc_type, qos_tc,
                                                enable ? exp_to_color_map_id : p_mpls_info->exp_to_color_map_id,
                                                SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, enable));
            break;
        case SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
            if (SAI_NULL_OBJECT_ID != attr->value.oid)
            {
                p_counter_info = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if (NULL == p_counter_info)
                {
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                if (attr->value.oid == p_mpls_info->counter_oid)
                {
                    break;
                }
                if (SAI_NULL_OBJECT_ID != p_mpls_info->counter_oid)
                {
                    if (SAI_NULL_OBJECT_ID != p_mpls_info->decap_tunnel_oid)
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW));
                    }
                    else
                    {
                        CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP));
                    }
                }

                if (SAI_NULL_OBJECT_ID != p_mpls_info->decap_tunnel_oid)
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_create(attr->value.oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW, &ctc_mpls_ilm.stats_id));
                }
                else
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_create(attr->value.oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP, &ctc_mpls_ilm.stats_id));
                }
                p_mpls_info->counter_oid = attr->value.oid;
            }
            else
            {
                if (SAI_NULL_OBJECT_ID != p_mpls_info->decap_tunnel_oid)
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW));
                }
                else
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP));
                }
                p_mpls_info->counter_oid = SAI_NULL_OBJECT_ID;
            }
            break;
        case SAI_INSEG_ENTRY_ATTR_POLICER_ID: 
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr->value.oid, &ctc_object_id);
            if(SAI_NULL_OBJECT_ID != attr->value.oid)
            {
                CTC_SAI_CTC_ERROR_RETURN(ctc_sai_policer_mpls_set_policer(lchip, inseg_entry->label, ctc_object_id.value, true));
            }
            //revert old policer oid
            if (p_mpls_info->policer_id && ctc_object_id.value && (p_mpls_info->policer_id != ctc_object_id.value) )
            {
                CTC_SAI_CTC_ERROR_RETURN(ctc_sai_policer_mpls_set_policer(lchip, inseg_entry->label, p_mpls_info->policer_id, false));
            }
            policer_id = ctc_object_id.value;
            ilm_update = 1;
            break;
        case SAI_INSEG_ENTRY_ATTR_SERVICE_ID:
            old_service_id = p_mpls_info->service_id;
            if(attr->value.u16)
            {
                service_id = attr->value.u16;
                
                service_id_update = 1;
            }
            else
            {
                service_id_update = 0;
            }
            ilm_update = 1;
            break;
        default:
            break;
    }

    if(ilm_update)
    {
        _ctc_sai_mpls_get_ctc_nh_id(action, nexthop_oid, &ctc_nh_id, &ctc_mpls_ilm);

        ctc_mpls_ilm.nh_id = ctc_nh_id;
        ctc_mpls_ilm.policer_id = policer_id;

        if(1 == service_id_update)
        {
            ctc_mpls_ilm.id_type = CTC_MPLS_ID_SERVICE;
            ctc_mpls_ilm.flw_vrf_srv_aps.service_id = service_id;
            if(0 == old_service_id) //first set, may need set pwid for vpws or l3vpn
            {
                if(p_mpls_info->decap_tunnel_oid)
                {
                    p_tunnel = ctc_sai_db_get_object_property(lchip, p_mpls_info->decap_tunnel_oid);
                    ctc_mpls_ilm.pwid = p_tunnel->logic_port;
                }
                if(p_mpls_info->frr_nhp_grp_oid)
                {
                    p_nhp_grp_frr = ctc_sai_db_get_object_property(lchip, p_mpls_info->frr_nhp_grp_oid);
                    ctc_mpls_ilm.pwid = p_nhp_grp_frr->logic_port;
                }
            }
        }
        else if(0 == service_id_update)
        {
            CTC_UNSET_FLAG(ctc_mpls_ilm.id_type, CTC_MPLS_ID_SERVICE);
        }
        else
        {
            //keep
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_update_ilm(lchip, &ctc_mpls_ilm));
        p_mpls_info->pop = pop;
        p_mpls_info->action = action;
        p_mpls_info->nexthop_oid = nexthop_oid;
        p_mpls_info->policer_id = policer_id;
        p_mpls_info->service_id = service_id;
    }
    else
    {
        p_mpls_info->psc_type = psc_type;
        p_mpls_info->qos_tc = qos_tc;
        p_mpls_info->exp_to_tc_map_id = exp_to_tc_map_id;
        p_mpls_info->exp_to_color_map_id = exp_to_color_map_id;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mpls_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    const sai_inseg_entry_t *inseg_entry = &(key->key.inseg_entry);
    uint8 lchip = 0;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_sai_next_hop_grp_t* p_frr_nhp_grp = NULL;
    ctc_object_id_t ctc_object_id;
    bool protecting = false;

    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_mpls_info->is_es)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
            attr->value.u8 = 1;
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
        case SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID:
            attr->value.oid = p_mpls_info->decap_tunnel_oid;
            break;
        case SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP:
            attr->value.oid = p_mpls_info->frr_nhp_grp_oid;
            break;
        case SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE:
            attr->value.u8 = p_mpls_info->frr_configured_role;
            break;
        case SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD:
            attr->value.booldata = p_mpls_info->frr_rx_discard;
            break;
        case SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE:
            p_frr_nhp_grp = ctc_sai_db_get_object_property(lchip, p_mpls_info->frr_nhp_grp_oid);
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, p_mpls_info->frr_nhp_grp_oid, &ctc_object_id);
            ctcs_aps_get_aps_bridge(lchip, ctc_object_id.value2, &protecting);

            if(((SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY == p_mpls_info->frr_configured_role) && protecting) ||
                ((SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY == p_mpls_info->frr_configured_role) && !protecting))
            {
                attr->value.u8 = SAI_INSEG_ENTRY_OBSERVED_ROLE_INACTIVE;
            }
            else
            {
                attr->value.u8 = SAI_INSEG_ENTRY_OBSERVED_ROLE_ACTIVE;
            }
            break;
        case SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE:
            attr->value.s32 = p_mpls_info->pop_ttl_mode;
            break;
        case SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE:
            attr->value.s32 = p_mpls_info->pop_qos_mode;
            break;
        case SAI_INSEG_ENTRY_ATTR_PSC_TYPE:
            attr->value.s32 = p_mpls_info->psc_type;
            break;
        case SAI_INSEG_ENTRY_ATTR_QOS_TC:
            attr->value.u8 = p_mpls_info->qos_tc;
            break;
        case SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, p_mpls_info->exp_to_tc_map_id);
            break;
        case SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, p_mpls_info->exp_to_color_map_id);
            break;
        case SAI_INSEG_ENTRY_ATTR_COUNTER_ID:
            attr->value.oid = p_mpls_info->counter_oid;
            break;
        case SAI_INSEG_ENTRY_ATTR_POLICER_ID: 
            if (!p_mpls_info->policer_id)
            {
                attr->value.oid = SAI_NULL_OBJECT_ID;
            }
            else
            {
                attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, p_mpls_info->policer_id);
            }
            break;
        case SAI_INSEG_ENTRY_ATTR_SERVICE_ID: 
            attr->value.u16 = p_mpls_info->service_id;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }

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
    sai_object_id_t nexthop_oid = SAI_NULL_OBJECT_ID;
    sai_object_id_t tunnel_oid = SAI_NULL_OBJECT_ID;
    sai_object_id_t counter_oid = SAI_NULL_OBJECT_ID;
    sai_object_id_t frr_oid = SAI_NULL_OBJECT_ID;
    uint32 ctc_nh_id = 0;
    ctc_sai_router_interface_t* p_route_interface = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_sai_counter_t* p_sai_counter = NULL;
    ctc_sai_next_hop_grp_t* p_nhp_grp_frr = NULL;
    ctc_object_id_t ctc_object_id;
    ctc_object_id_t ctc_object_id_br;
    sai_object_id_t bridge_oid = 0;
    ctc_object_id_t ctc_object_id_frr;
    uint8 frr_configured_role = 0;
    bool frr_rx_discard = false;
    uint8 pop_ttl_mode = 0, pop_qos_mode = 0;
    sai_object_key_t key;
    sai_attribute_t set_attr;
    uint32 policer_id = 0;
    uint16 service_id = 0;

    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));
    sal_memset(&key, 0, sizeof(key));
    sal_memset(&set_attr, 0, sizeof(set_attr));

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
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       tunnel_oid = attr_value->oid;
       p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_oid);
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_COUNTER_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        counter_oid = attr_value->oid;
        p_sai_counter = ctc_sai_db_get_object_property(lchip, counter_oid);
        if (NULL == p_sai_counter)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       pop_ttl_mode = attr_value->s32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       pop_qos_mode = attr_value->s32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       frr_oid = attr_value->oid;
       p_nhp_grp_frr = ctc_sai_db_get_object_property(lchip, frr_oid);
       ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, attr_value->oid, &ctc_object_id_frr);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_SERVICE_ID, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
       service_id = attr_value->u16;
    }

    _ctc_sai_mpls_get_ctc_nh_id(action, nexthop_oid, &ctc_nh_id, &ctc_mpls_ilm);
    ctc_mpls_ilm.nh_id = ctc_nh_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_INSEG_ENTRY, nexthop_oid, &ctc_object_id);
    if(NULL != p_nhp_grp_frr)
    {
        p_nhp_grp_frr = ctc_sai_db_get_object_property(lchip, frr_oid);
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
           frr_configured_role = attr_value->s32;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            if(attr_value->booldata)
            {
                frr_rx_discard = true;
                ctc_mpls_ilm.id_type |= CTC_MPLS_ID_APS_SELECT;
                ctc_mpls_ilm.aps_select_grp_id = ctc_object_id_frr.value2;
                ctc_mpls_ilm.aps_select_protect_path = frr_configured_role;
            }
        }
    }
    if(SAI_OBJECT_TYPE_ROUTER_INTERFACE == ctc_object_id.type)
    {
        p_route_interface = ctc_sai_db_get_object_property(lchip, nexthop_oid);
        if((NULL == p_route_interface) || (SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER != ctc_object_id.sub_type))
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }
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
                if(NULL != p_nhp_grp_frr)
                {
                    if(0 != p_nhp_grp_frr->logic_port)
                    {
                        ctc_mpls_ilm.pwid = p_nhp_grp_frr->logic_port;
                    }
                }

                if(service_id)
                {
                    ctc_mpls_ilm.id_type = CTC_MPLS_ID_SERVICE;
                    ctc_mpls_ilm.flw_vrf_srv_aps.service_id = service_id;
                }
            }
            else
            {
                ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_VPWS;
                ctc_mpls_ilm.nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;

                if(service_id)
                {
                    ctc_mpls_ilm.id_type = CTC_MPLS_ID_SERVICE;
                    ctc_mpls_ilm.flw_vrf_srv_aps.service_id = service_id;

                    if(NULL != p_tunnel)
                    {
                        ctc_mpls_ilm.pwid = p_tunnel->logic_port;
                    }
                    if(NULL != p_nhp_grp_frr)
                    {
                        if(0 != p_nhp_grp_frr->logic_port)
                        {
                            ctc_mpls_ilm.pwid = p_nhp_grp_frr->logic_port;
                        }
                    }
                }
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
                if(p_tunnel->split_horizon_valid)
                {
                    ctc_mpls_ilm.logic_port_type = 1;
                }
                else
                {
                    ctc_mpls_ilm.logic_port_type = 0;
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
        else
        {
            if(NULL != p_tunnel)
            {
                if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
                {
                    ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_L3VPN;
                    ctc_mpls_ilm.vrf_id = p_route_interface->vrf_id;
                    //ctc_mpls_ilm.flw_vrf_srv_aps.vrf_id = p_route_interface->vrf_id;
                    //ctc_mpls_ilm.id_type |= CTC_MPLS_ID_VRF;
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

                    if(service_id)
                    {
                        ctc_mpls_ilm.id_type = CTC_MPLS_ID_SERVICE;
                        ctc_mpls_ilm.flw_vrf_srv_aps.service_id = service_id;

                        if(NULL != p_tunnel)
                        {
                            ctc_mpls_ilm.pwid = p_tunnel->logic_port;
                        }
                        if(NULL != p_nhp_grp_frr)
                        {
                            if(0 != p_nhp_grp_frr->logic_port)
                            {
                                ctc_mpls_ilm.pwid = p_nhp_grp_frr->logic_port;
                            }
                        }
                    }
                    
                }
            }
            else
            {
                //pop
                ctc_mpls_ilm.type = CTC_MPLS_LABEL_TYPE_NORMAL;
                if(SAI_INSEG_ENTRY_POP_TTL_MODE_UNIFORM == pop_ttl_mode)
                {
                   ctc_mpls_ilm.model = CTC_MPLS_TUNNEL_MODE_UNIFORM;
                }
                else if(SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE == pop_ttl_mode)
                {
                    ctc_mpls_ilm.model = CTC_MPLS_TUNNEL_MODE_PIPE;
                }
                if(SAI_INSEG_ENTRY_POP_QOS_MODE_UNIFORM == pop_qos_mode)
                {
                    ctc_mpls_ilm.trust_outer_exp = 1;
                }
                else if(SAI_INSEG_ENTRY_POP_QOS_MODE_PIPE == pop_qos_mode)
                {
                    ctc_mpls_ilm.trust_outer_exp = 0;
                }
            }
        }
    }
    else
    {
        ctc_mpls_ilm.pop = 0;
    }

    if (NULL != p_tunnel)
    {
        if(p_tunnel->decap_acl_use_outer && (SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type))
        {
            CTC_SET_FLAG(ctc_mpls_ilm.flag, CTC_MPLS_ILM_FLAG_ACL_USE_OUTER_INFO);
        }
    }
    ctc_mpls_ilm.label = inseg_entry->label;

    if (NULL != p_sai_counter)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(counter_oid, p_tunnel?CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW:CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP, &ctc_mpls_ilm.stats_id), status, out);
        ctc_mpls_ilm.id_type |= CTC_MPLS_ID_STATS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_POLICER_ID, &attr_value, &index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if(SAI_NULL_OBJECT_ID != attr_value->oid)
        {        
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr_value->oid, &ctc_object_id);
            
            CTC_SAI_ERROR_GOTO(ctc_sai_policer_mpls_set_policer(lchip, inseg_entry->label, ctc_object_id.value, 1), status, error1);
            
            policer_id = ctc_object_id.value;
            ctc_mpls_ilm.policer_id = policer_id;
        }
    }    
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_mpls_add_ilm(lchip, &ctc_mpls_ilm), status, error2);


    // build mpls inseg db
    
    CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_build_db(lchip, inseg_entry, &p_mpls_info), status, error3);
    if(NULL != p_tunnel)
    {
        p_tunnel->inseg_label = inseg_entry->label;
        p_tunnel->ref_cnt++;
    }

    
    p_mpls_info->action = action;
    p_mpls_info->nexthop_oid = nexthop_oid;
    p_mpls_info->decap_tunnel_oid = tunnel_oid;
    p_mpls_info->pop_ttl_mode = pop_ttl_mode;
    p_mpls_info->pop_qos_mode = pop_qos_mode;
    p_mpls_info->policer_id = policer_id;
    p_mpls_info->service_id = service_id;
    

    //update ilm qos map

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
        set_attr.id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP;
        set_attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_set_attr(&key, &set_attr), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
        set_attr.id = SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP;
        set_attr.value.oid = attr_value->oid;
        CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_set_attr(&key, &set_attr), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_QOS_TC, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
        set_attr.id = SAI_INSEG_ENTRY_ATTR_QOS_TC;
        set_attr.value.u8 = attr_value->u8;
        CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_set_attr(&key, &set_attr), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_INSEG_ENTRY_ATTR_PSC_TYPE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&key.key.inseg_entry, inseg_entry, sizeof(sai_inseg_entry_t));
        set_attr.id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE;
        set_attr.value.s32 = attr_value->s32;
        CTC_SAI_ERROR_GOTO(_ctc_sai_mpls_set_attr(&key, &set_attr), status, error4);
    }


    if (SAI_NULL_OBJECT_ID != counter_oid)
    {
        p_mpls_info->counter_oid = counter_oid;
    }

    if(NULL != p_nhp_grp_frr)
    {
        p_mpls_info->frr_nhp_grp_oid = frr_oid;
        p_mpls_info->frr_configured_role = frr_configured_role;
        p_mpls_info->frr_rx_discard = frr_rx_discard;
        if(SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY == frr_configured_role)
        {
            p_nhp_grp_frr->rx_label_primary = inseg_entry->label;
        }
        if(SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY == frr_configured_role)
        {
            p_nhp_grp_frr->rx_label_standby = inseg_entry->label;
        }
    }

    return SAI_STATUS_SUCCESS;

error4:
    CTC_SAI_LOG_ERROR(SAI_API_MPLS, "rollback to error4\n");
    _ctc_sai_mpls_remove_db(lchip, inseg_entry);   
error3:
    CTC_SAI_LOG_ERROR(SAI_API_MPLS, "rollback to error3\n");
    ctcs_mpls_del_ilm(lchip, &ctc_mpls_ilm);
error2:
    CTC_SAI_LOG_ERROR(SAI_API_MPLS, "rollback to error2\n");
    if(policer_id)
    {
        ctc_sai_policer_mpls_set_policer(lchip, inseg_entry->label, policer_id, 0);
    }
error1:
    CTC_SAI_LOG_ERROR(SAI_API_MPLS, "rollback to error1\n");    
    ctc_sai_counter_id_remove(counter_oid, p_tunnel?CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW:CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP);

out:
    return status;
}

static sai_status_t
_ctc_sai_mpls_remove_inseg_entry(const sai_inseg_entry_t *inseg_entry)
{
    uint8 lchip = 0;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_mpls_ilm_t ctc_mpls_ilm;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_sai_next_hop_grp_t* p_nhp_grp_frr = NULL;

    sal_memset(&ctc_mpls_ilm,0,sizeof(ctc_mpls_ilm_t));

    CTC_SAI_PTR_VALID_CHECK(inseg_entry);
    ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip);
    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if(p_mpls_info->is_es)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(p_mpls_info->exp_to_tc_map_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, p_mpls_info->qos_tc,
                                                p_mpls_info->exp_to_tc_map_id,
                                                SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC, 0));
        p_mpls_info->exp_to_tc_map_id = 0;

    }
    if(p_mpls_info->exp_to_color_map_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_inseg_set_map(inseg_entry, p_mpls_info->psc_type, p_mpls_info->qos_tc,
                                                p_mpls_info->exp_to_color_map_id,
                                                SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR, 0));
        p_mpls_info->exp_to_color_map_id = 0;
    }

    if (SAI_NULL_OBJECT_ID != p_mpls_info->counter_oid)
    {
        if (SAI_NULL_OBJECT_ID != p_mpls_info->decap_tunnel_oid)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_PW));
        }
        else
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_mpls_info->counter_oid, CTC_SAI_COUNTER_TYPE_INSEG_MPLS_LSP));
        }
    }

    ctc_mpls_ilm.label = inseg_entry->label;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_del_ilm(lchip, &ctc_mpls_ilm));
    if(p_mpls_info->decap_tunnel_oid)
    {
        p_tunnel = ctc_sai_db_get_object_property(lchip, p_mpls_info->decap_tunnel_oid);
        if(NULL != p_tunnel)
        {
            p_tunnel->ref_cnt--;
            p_tunnel->inseg_label = 0;
        }
    }

    if(p_mpls_info->frr_nhp_grp_oid)
    {
        p_nhp_grp_frr = ctc_sai_db_get_object_property(lchip, p_mpls_info->frr_nhp_grp_oid);

        if(p_nhp_grp_frr)
        {
            if(SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY == p_mpls_info->frr_configured_role)
            {
                p_nhp_grp_frr->rx_label_primary = 0;
            }
            else if(SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY == p_mpls_info->frr_configured_role)
            {
                p_nhp_grp_frr->rx_label_standby = 0;
            }
        }
    }

    if (p_mpls_info->policer_id)
    {
        ctc_sai_policer_mpls_set_policer(lchip, (uint32)inseg_entry->label, p_mpls_info->policer_id, 0);
    }

    _ctc_sai_mpls_remove_db(lchip, inseg_entry);
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
    { SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_FRR_NHP_GRP,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_FRR_CONFIGURED_ROLE,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_FRR_OBSERVED_ROLE,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_FRR_INACTIVE_RX_DISCARD,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_POP_TTL_MODE,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_POP_QOS_MODE,
      _ctc_sai_mpls_get_attr,
      NULL},
    { SAI_INSEG_ENTRY_ATTR_PSC_TYPE,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_QOS_TC,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_TC_MAP,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_MPLS_EXP_TO_COLOR_MAP,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_COUNTER_ID,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_POLICER_ID,
      _ctc_sai_mpls_get_attr,
      _ctc_sai_mpls_set_attr},
    { SAI_INSEG_ENTRY_ATTR_SERVICE_ID,
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
