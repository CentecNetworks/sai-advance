/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_debug_counter.h"
#include "ctc_sai_port.h"

/*sdk include file*/
#include "ctcs_api.h"


static sai_status_t
_ctc_sai_debug_counter_build_db(uint8 lchip, sai_object_id_t stats_id, ctc_sai_debug_counter_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_debug_counter_t* p_dbg_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    p_dbg_counter_info = mem_malloc(MEM_STATS_MODULE, sizeof(ctc_sai_debug_counter_t));
    if (NULL == p_dbg_counter_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_DEBUG_COUNTER, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_dbg_counter_info, 0, sizeof(ctc_sai_debug_counter_t));
    status = ctc_sai_db_add_object_property(lchip, stats_id, (void*)p_dbg_counter_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_dbg_counter_info);
        return status;
    }

    *oid_property = p_dbg_counter_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_remove_db(uint8 lchip, sai_object_id_t dbgcounter_id)
{
    ctc_sai_debug_counter_t* p_dbg_counter_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    p_dbg_counter_info = ctc_sai_db_get_object_property(lchip, dbgcounter_id);
    if (NULL == p_dbg_counter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, dbgcounter_id);
    mem_free(p_dbg_counter_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_drop_reason_map(uint32 sai_drop_reason, uint8 dir, uint32* ctc_drop_reason)
{
    if(DROP_REASON_IN == dir)
    {
        #if SDK_TM_BRANCH
        switch(sai_drop_reason)
        {
            case SAI_IN_DROP_REASON_SMAC_MULTICAST:
            case SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC:    
                *ctc_drop_reason = IPE_L2_ILLEGAL_PKT_DIS;
                break;
            case SAI_IN_DROP_REASON_DMAC_RESERVED:    
                *ctc_drop_reason = IPE_EXCEP2_DIS;
                break;
            case SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED:    
                *ctc_drop_reason = IPE_AFT_DIS;
                break;
            case SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER:    
                *ctc_drop_reason = IPE_VLAN_FILTER_DIS;
                break;
            case SAI_IN_DROP_REASON_INGRESS_STP_FILTER:    
                *ctc_drop_reason = IPE_STP_DIS;
                break;
            case SAI_IN_DROP_REASON_FDB_UC_DISCARD:    
                *ctc_drop_reason = IPE_IS_DIS_FORWARDING_PTR;
                break;
            case SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER:    
                *ctc_drop_reason = IPE_SECURITY_CHK_DIS;
                break;
            case SAI_IN_DROP_REASON_EXCEEDS_L3_MTU:
                *ctc_drop_reason = EPE_INTERF_MTU_CHK_DIS;
                break;
            case SAI_IN_DROP_REASON_IP_HEADER_ERROR:
                *ctc_drop_reason = IPE_PARSER_LEN_ERR;
                break;
            case SAI_IN_DROP_REASON_UC_DIP_MC_DMAC:
                *ctc_drop_reason = IPE_ROUTE_ERROR_PKT_DIS;
                break;
            case SAI_IN_DROP_REASON_DIP_LOOPBACK:
            case SAI_IN_DROP_REASON_SIP_LOOPBACK:
            case SAI_IN_DROP_REASON_SIP_MC:
            case SAI_IN_DROP_REASON_SIP_CLASS_E:    
            case SAI_IN_DROP_REASON_SIP_UNSPECIFIED:  
            case SAI_IN_DROP_REASON_MC_DMAC_MISMATCH:    
                *ctc_drop_reason = IPE_FATAL_EXCEP_DIS;
                break;
            case SAI_IN_DROP_REASON_SIP_EQUALS_DIP:
            case SAI_IN_DROP_REASON_SIP_BC:    
                *ctc_drop_reason = IPE_ROUTE_ERROR_PKT_DIS;
                break;
            case SAI_IN_DROP_REASON_DIP_LOCAL:
            case SAI_IN_DROP_REASON_DIP_LINK_LOCAL:
            case SAI_IN_DROP_REASON_SIP_LINK_LOCAL:
            case SAI_IN_DROP_REASON_IPV6_MC_SCOPE0:    
            case SAI_IN_DROP_REASON_IPV6_MC_SCOPE1:    
                *ctc_drop_reason = IPE_FATAL_EXCEP_DIS;
                break;
            case SAI_IN_DROP_REASON_BLACKHOLE_ROUTE:    
                *ctc_drop_reason = IPE_IS_DIS_FORWARDING_PTR;
                break;
            case SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP:    
                *ctc_drop_reason = IPE_NO_FORWARDING_PTR;
                break;
            case SAI_IN_DROP_REASON_ACL_ANY:    
                *ctc_drop_reason = IPE_DS_ACL_DIS;
                break;
            case SAI_IN_DROP_REASON_L2_ANY:
            case SAI_IN_DROP_REASON_FDB_MC_DISCARD:
            case SAI_IN_DROP_REASON_EXCEEDS_L2_MTU:
            case SAI_IN_DROP_REASON_L3_ANY:    
            case SAI_IN_DROP_REASON_TTL:
            case SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER:
            case SAI_IN_DROP_REASON_NON_ROUTABLE:
            case SAI_IN_DROP_REASON_NO_L3_HEADER:    
            case SAI_IN_DROP_REASON_IRIF_DISABLED:
            case SAI_IN_DROP_REASON_ERIF_DISABLED:
            case SAI_IN_DROP_REASON_LPM4_MISS:
            case SAI_IN_DROP_REASON_LPM6_MISS:    
            case SAI_IN_DROP_REASON_BLACKHOLE_ARP:   
            case SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN:
            case SAI_IN_DROP_REASON_DECAP_ERROR:
            case SAI_IN_DROP_REASON_ACL_INGRESS_PORT:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_LAG:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_VLAN:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_RIF:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_PORT:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_LAG:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_VLAN:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_RIF:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH:   
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            default:
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;

        }
        #else
        switch(sai_drop_reason)
        {
            case SAI_IN_DROP_REASON_SMAC_MULTICAST:
            case SAI_IN_DROP_REASON_SMAC_EQUALS_DMAC:    
                *ctc_drop_reason = CTC_DROP_PKT_ERR;
                break;
            case SAI_IN_DROP_REASON_DMAC_RESERVED:    
                *ctc_drop_reason = CTC_DROP_EXCP;
                break;
            case SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED:    
            case SAI_IN_DROP_REASON_INGRESS_VLAN_FILTER:    
                *ctc_drop_reason = CTC_DROP_VLAN_FILTER;
                break;
            case SAI_IN_DROP_REASON_INGRESS_STP_FILTER:    
                *ctc_drop_reason = CTC_DROP_STP_CHK;
                break;
            case SAI_IN_DROP_REASON_FDB_UC_DISCARD:    
                *ctc_drop_reason = CTC_DROP_FWD_ERR;
                break;
            case SAI_IN_DROP_REASON_L2_LOOPBACK_FILTER:    
                *ctc_drop_reason = CTC_DROP_SECURITY_CHK;
                break;
            case SAI_IN_DROP_REASON_EXCEEDS_L3_MTU:
                *ctc_drop_reason = CTC_DROP_MTU_CHK;
                break;
            case SAI_IN_DROP_REASON_IP_HEADER_ERROR:
                *ctc_drop_reason = CTC_DROP_PARSER_ERR;
                break;
            case SAI_IN_DROP_REASON_UC_DIP_MC_DMAC:
                *ctc_drop_reason = CTC_DROP_IP_CHK;
                break;
            case SAI_IN_DROP_REASON_DIP_LOOPBACK:
            case SAI_IN_DROP_REASON_SIP_LOOPBACK:
            case SAI_IN_DROP_REASON_SIP_MC:
            case SAI_IN_DROP_REASON_SIP_CLASS_E:    
            case SAI_IN_DROP_REASON_SIP_UNSPECIFIED:  
            case SAI_IN_DROP_REASON_MC_DMAC_MISMATCH:    
                *ctc_drop_reason = CTC_DROP_EXCP;
                break;
            case SAI_IN_DROP_REASON_SIP_EQUALS_DIP:
            case SAI_IN_DROP_REASON_SIP_BC:    
                *ctc_drop_reason = CTC_DROP_IP_CHK;
                break;
            case SAI_IN_DROP_REASON_DIP_LOCAL:
            case SAI_IN_DROP_REASON_DIP_LINK_LOCAL:
            case SAI_IN_DROP_REASON_SIP_LINK_LOCAL:
            case SAI_IN_DROP_REASON_IPV6_MC_SCOPE0:    
            case SAI_IN_DROP_REASON_IPV6_MC_SCOPE1:    
                *ctc_drop_reason = CTC_DROP_EXCP;
                break;
            case SAI_IN_DROP_REASON_BLACKHOLE_ROUTE:    
                *ctc_drop_reason = CTC_DROP_FWD_ERR;
                break;
            case SAI_IN_DROP_REASON_UNRESOLVED_NEXT_HOP:    
                *ctc_drop_reason = CTC_DROP_FWD_ERR;
                break;
            case SAI_IN_DROP_REASON_ACL_ANY:    
                *ctc_drop_reason = CTC_DROP_ACL_DENY;
                break;
            case SAI_IN_DROP_REASON_L2_ANY:
            case SAI_IN_DROP_REASON_FDB_MC_DISCARD:
            case SAI_IN_DROP_REASON_EXCEEDS_L2_MTU:
            case SAI_IN_DROP_REASON_L3_ANY:    
            case SAI_IN_DROP_REASON_TTL:
            case SAI_IN_DROP_REASON_L3_LOOPBACK_FILTER:
            case SAI_IN_DROP_REASON_NON_ROUTABLE:
            case SAI_IN_DROP_REASON_NO_L3_HEADER:    
            case SAI_IN_DROP_REASON_IRIF_DISABLED:
            case SAI_IN_DROP_REASON_ERIF_DISABLED:
            case SAI_IN_DROP_REASON_LPM4_MISS:
            case SAI_IN_DROP_REASON_LPM6_MISS:    
            case SAI_IN_DROP_REASON_BLACKHOLE_ARP:   
            case SAI_IN_DROP_REASON_L3_EGRESS_LINK_DOWN:
            case SAI_IN_DROP_REASON_DECAP_ERROR:
            case SAI_IN_DROP_REASON_ACL_INGRESS_PORT:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_LAG:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_VLAN:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_RIF:    
            case SAI_IN_DROP_REASON_ACL_INGRESS_SWITCH:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_PORT:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_LAG:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_VLAN:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_RIF:    
            case SAI_IN_DROP_REASON_ACL_EGRESS_SWITCH:   
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            default:
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;

        }
        #endif
    }
    else if (DROP_REASON_OUT == dir)
    {
        #if SDK_TM_BRANCH
        switch(sai_drop_reason)
        {
            case SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER:    
                *ctc_drop_reason = EPE_VLAN_FILTER_DIS;
                break;
            case SAI_OUT_DROP_REASON_L2_ANY:   
            case SAI_OUT_DROP_REASON_L3_ANY:       
            case SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN:    
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            default:
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
        }
        #else
        switch(sai_drop_reason)
        {
            case SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER:    
                *ctc_drop_reason = CTC_DROP_VLAN_FILTER;
                break;
            case SAI_OUT_DROP_REASON_L2_ANY:
            case SAI_OUT_DROP_REASON_L3_ANY:       
            case SAI_OUT_DROP_REASON_L3_EGRESS_LINK_DOWN:    
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
            default:
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                break;
        }
        #endif
    }
    else
    {
        return SAI_STATUS_FAILURE;
    }
        

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32 index = 0, loop_i = 0;
    uint32 debug_counter_type = 0;
    uint32 ctc_drop_reason = 0;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_INDEX, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {       
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_TYPE, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {       
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    else
    {
        debug_counter_type = attr_value->s32;
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {       
        if((debug_counter_type != SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS)
            && (debug_counter_type != SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }         
        for(loop_i = 0; loop_i < attr_value->s32list.count; loop_i++)
        {    
            status = _ctc_sai_debug_counter_drop_reason_map(attr_value->s32list.list[loop_i], DROP_REASON_IN, &ctc_drop_reason);
            if(SAI_STATUS_ATTR_NOT_SUPPORTED_0 == status)
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
            }
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {       
        if((debug_counter_type != SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS)
            && (debug_counter_type != SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
        for(loop_i = 0; loop_i < attr_value->s32list.count; loop_i++)
        {    
            status = _ctc_sai_debug_counter_drop_reason_map(attr_value->s32list.list[loop_i], DROP_REASON_OUT, &ctc_drop_reason);
            if(SAI_STATUS_ATTR_NOT_SUPPORTED_0 == status)
            {
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
            }
        }
    }
        
    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    uint32 loop_i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_dbgcounter_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_dbgcounter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
    case SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST:
        {
            if(DROP_REASON_IN == p_dbgcounter_info->dir)
            {
                p_dbgcounter_info->drop_reason_list_bitmap[0] = 0;
                p_dbgcounter_info->drop_reason_list_bitmap[1] = 0;
                for(loop_i = 0; loop_i < attr->value.s32list.count; loop_i++)
                {            
                    if(attr->value.s32list.list[loop_i] < 32)
                    {
                        SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[0], attr->value.s32list.list[loop_i]);
                    }
                    else
                    {
                        SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[1], attr->value.s32list.list[loop_i]-32);
                    }
                }
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0;
            }
        }
        break;
    case SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST:
        {
            if(DROP_REASON_OUT == p_dbgcounter_info->dir)
            {
                p_dbgcounter_info->drop_reason_list_bitmap[0] = 0;
                p_dbgcounter_info->drop_reason_list_bitmap[1] = 0;
                for(loop_i = 0; loop_i < attr->value.s32list.count; loop_i++)
                {            
                    if(attr->value.s32list.list[loop_i] < 32)
                    {
                        SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[0], attr->value.s32list.list[loop_i]);
                    }
                    else
                    {
                        SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[1], attr->value.s32list.list[loop_i]-32);
                    }
                }
            }
            else
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0;
            }
        }
        break;
    default:
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    uint32 loop_i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_dbgcounter_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_dbgcounter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
    case SAI_DEBUG_COUNTER_ATTR_INDEX:
        {
            attr->value.u32 = p_dbgcounter_info->debug_counter_index;
        }
        break;
    case SAI_DEBUG_COUNTER_ATTR_TYPE:
        {
            attr->value.s32 = p_dbgcounter_info->debug_counter_type;
        }
        break;
    case SAI_DEBUG_COUNTER_ATTR_BIND_METHOD:
        {
            attr->value.s32 = p_dbgcounter_info->bind_method;
        }
        break;
    case SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST:
        {
            if (p_dbgcounter_info->dir == DROP_REASON_IN)
            {
                attr->value.s32list.count = 0;
                for(loop_i = 0; loop_i < SAI_IN_DROP_REASON_END; loop_i++)
                {
                    if(loop_i < 32)
                    {
                        if(IS_BIT_SET(p_dbgcounter_info->drop_reason_list_bitmap[0], loop_i))
                        {
                            attr->value.s32list.list[attr->value.s32list.count] = loop_i;
                            attr->value.s32list.count++;
                        }
                    }
                    else
                    {
                        if(IS_BIT_SET(p_dbgcounter_info->drop_reason_list_bitmap[1], loop_i-32))
                        {
                            attr->value.s32list.list[attr->value.s32list.count] = loop_i;
                            attr->value.s32list.count++;
                        }
                    }
                }            
            }
            else
            {
                attr->value.s32list.count = 0;
            }
        }
        break;
    case SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST:
        {
            if (p_dbgcounter_info->dir == DROP_REASON_OUT)
            {
                attr->value.s32list.count = 0;
                for(loop_i = 0; loop_i < SAI_OUT_DROP_REASON_END; loop_i++)
                {
                    if(loop_i < 32)
                    {
                        if(IS_BIT_SET(p_dbgcounter_info->drop_reason_list_bitmap[0], loop_i))
                        {
                            attr->value.s32list.list[attr->value.s32list.count] = loop_i;
                            attr->value.s32list.count++;
                        }
                    }
                    else
                    {
                        if(IS_BIT_SET(p_dbgcounter_info->drop_reason_list_bitmap[1], loop_i-32))
                        {
                            attr->value.s32list.list[attr->value.s32list.count] = loop_i;
                            attr->value.s32list.count++;
                        }
                    }
                }
            }
            else
            {
                attr->value.s32list.count = 0;
            }
        }
        break;
    default:
        return SAI_STATUS_NOT_SUPPORTED;
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t debug_counter_attr_fn_entries[] = {
    { SAI_DEBUG_COUNTER_ATTR_INDEX,
      _ctc_sai_debug_counter_get_attr,
      NULL},
    { SAI_DEBUG_COUNTER_ATTR_TYPE,
      _ctc_sai_debug_counter_get_attr,
      NULL},
    { SAI_DEBUG_COUNTER_ATTR_BIND_METHOD,
      _ctc_sai_debug_counter_get_attr,
      NULL},  
    { SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST,
      _ctc_sai_debug_counter_get_attr,
      _ctc_sai_debug_counter_set_attr},
    { SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST,
      _ctc_sai_debug_counter_get_attr,
      _ctc_sai_debug_counter_set_attr},  
};

static sai_status_t 
_ctc_sai_debug_counter_get_port_reason_stats(uint8 lchip, uint16 portid, uint16 reason, uint32 with_clear, uint32* count)
{
    ctc_diag_drop_t diag_drop;
    ctc_diag_drop_info_buffer_t buffer[5];
    uint32 buffer_count = 5;

    sal_memset(buffer, 0, buffer_count * sizeof(ctc_diag_drop_info_buffer_t));
    sal_memset(&diag_drop, 0, sizeof(ctc_diag_drop_t));

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    diag_drop.oper_type = CTC_DIAG_DROP_OPER_TYPE_GET_DETAIL_INFO;
    diag_drop.reason = reason;
    diag_drop.lport = portid;
    diag_drop.u.info.count = 0;
    diag_drop.with_clear = with_clear;
    
    ctcs_diag_get_drop_info(lchip, &diag_drop);

    *count = diag_drop.u.info.count;
    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_debug_counter_find_stat_index(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    ctc_sai_debug_counter_t* p_dbgcounter_info = bucket_data->data;
    sai_debug_counter_type_t* type = (sai_debug_counter_type_t*)user_data->value0;
    uint32* index_offset = (uint32*)user_data->value1;
    sai_object_id_t* dbg_counter_obj_id = (sai_object_id_t*)user_data->value2;
    
    if((p_dbgcounter_info->debug_counter_type == *type) && (p_dbgcounter_info->debug_counter_index == *index_offset))
    {
        *dbg_counter_obj_id = bucket_data->oid;
        return SAI_STATUS_FAILURE;
    }

    return SAI_STATUS_SUCCESS;
    
}

static sai_status_t
_ctc_sai_debug_counter_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t counter_obj_id = *(sai_object_id_t*)key;

    ctc_sai_debug_counter_t* p_dbgcounter_info = (ctc_sai_debug_counter_t*)data;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, counter_obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER, ctc_object_id.value)); 

    if(p_dbgcounter_info->debug_counter_index)
    {
        if(DROP_REASON_IN == p_dbgcounter_info->dir)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_IN_INDEX, p_dbgcounter_info->debug_counter_index)); 
        }
        else if(DROP_REASON_OUT == p_dbgcounter_info->dir)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_OUT_INDEX, p_dbgcounter_info->debug_counter_index)); 
        }
    }

    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_debug_counter_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  dbgcounter_oid_cur = 0;
    ctc_sai_debug_counter_t    ctc_sai_dbgcounter_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char dir[64] = {'-'};

    sal_memset(&ctc_sai_dbgcounter_cur, 0, sizeof(ctc_sai_debug_counter_t));

    dbgcounter_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_debug_counter_t*)(&ctc_sai_dbgcounter_cur), bucket_data->data, sizeof(ctc_sai_debug_counter_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (dbgcounter_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    if( DROP_REASON_IN == ctc_sai_dbgcounter_cur.dir)
    {
        sal_sprintf(dir,"%s", "IN");
    }
    else
    {
        sal_sprintf(dir,"%s", "OUT");
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d  0x%016"PRIx64 "  %-12d  %-12d  %-12s  %-12d  0x%-22x  0x%-22x\n",\
        num_cnt, dbgcounter_oid_cur, ctc_sai_dbgcounter_cur.debug_counter_type, ctc_sai_dbgcounter_cur.bind_method, dir, ctc_sai_dbgcounter_cur.debug_counter_index, \
        ctc_sai_dbgcounter_cur.drop_reason_list_bitmap[0], ctc_sai_dbgcounter_cur.drop_reason_list_bitmap[1]);
    
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
sai_status_t ctc_sai_debug_counter_get_port_stats(uint8 lchip, uint16 portid, uint32 drop_index, uint32 with_clear, uint64* count)
{
    sai_object_id_t dbg_counter_obj_id = 0;
    ctc_sai_db_traverse_param_t traverse_param;
    uint32 type = 0, index_offset = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    uint32 loop_i = 0, tmp_count = 0, total_count = 0;
    ctc_drop_reason_id_t ctc_drop_reason = CTC_SAI_DROP_REASON_MAX;
    uint32 tmp_drop_reason_list_bitmap = 0;


    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    if((drop_index > SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE) && (drop_index < SAI_PORT_STAT_IN_DROP_REASON_RANGE_END))
    {
        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS;
        index_offset = drop_index - SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE;
    }
    else if((drop_index > SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE) && (drop_index < SAI_PORT_STAT_OUT_DROP_REASON_RANGE_END))
    {
        type = SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS;
        index_offset = drop_index - SAI_PORT_STAT_OUT_DROP_REASON_RANGE_BASE;
    }

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.lchip = lchip;
    traverse_param.value0 = (void*)&type;
    traverse_param.value1 = (void*)&index_offset;
    traverse_param.value2 = (void*)&dbg_counter_obj_id;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_DEBUG_COUNTER, (hash_traversal_fn)_ctc_sai_debug_counter_find_stat_index, (void*)&traverse_param);

    if(dbg_counter_obj_id == SAI_NULL_OBJECT_ID)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_dbgcounter_info = ctc_sai_db_get_object_property(lchip, dbg_counter_obj_id);
    
    if(NULL == p_dbgcounter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(DROP_REASON_IN == p_dbgcounter_info->dir)
    {
        for(loop_i = 0; loop_i < SAI_IN_DROP_REASON_END; loop_i++)
        {
            if(loop_i < 32)
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[0];
            }
            else
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[1];
            }
            if(IS_BIT_SET(tmp_drop_reason_list_bitmap, loop_i))
            {
                _ctc_sai_debug_counter_drop_reason_map(loop_i, DROP_REASON_IN, &ctc_drop_reason);
                CTC_SAI_ERROR_RETURN(_ctc_sai_debug_counter_get_port_reason_stats(lchip, portid, ctc_drop_reason, with_clear, &tmp_count));
                total_count = total_count + tmp_count;
            }
        }                
    }
    else if(DROP_REASON_OUT == p_dbgcounter_info->dir)
    {
        for(loop_i = 0; loop_i < SAI_OUT_DROP_REASON_END; loop_i++)
        {
            if(loop_i < 32)
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[0];
            }
            else
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[1];
            }
            if(IS_BIT_SET(tmp_drop_reason_list_bitmap, loop_i))
            {
                _ctc_sai_debug_counter_drop_reason_map(loop_i, DROP_REASON_OUT, &ctc_drop_reason);
                CTC_SAI_ERROR_RETURN(_ctc_sai_debug_counter_get_port_reason_stats(lchip, portid, ctc_drop_reason, with_clear, &tmp_count));
                total_count = total_count + tmp_count;
            }
        }
    }
    *count = total_count;

    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "Debug counter get port stats:portid = %d, count:%d, drop index = %d, reason bitmap0 = 0x%x, reason bitmap1 = 0x%x \n", 
        portid, total_count, index_offset, p_dbgcounter_info->drop_reason_list_bitmap[0], p_dbgcounter_info->drop_reason_list_bitmap[1]);
        
    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_debug_counter_get_switch_stats(uint8 lchip, uint32 drop_index, uint32 with_clear, uint64* count)
{
    sai_object_id_t dbg_counter_obj_id = 0;
    ctc_sai_db_traverse_param_t traverse_param;
    uint32 type = 0, index_offset = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    uint32 loop_i = 0, tmp_count = 0, total_count = 0, num = 0;
    ctc_drop_reason_id_t ctc_drop_reason = CTC_SAI_DROP_REASON_MAX;
    ctc_global_panel_ports_t local_panel_ports;
    sai_object_id_t port_obj = 0;
    uint8 gchip = 0;
    ctc_sai_port_db_t* p_port_db = NULL;
    uint32 tmp_drop_reason_list_bitmap = 0;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);

    sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));
    
    if((drop_index > SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE) && (drop_index < SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_END))
    {
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS;
        index_offset = drop_index - SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE;
    }
    else if((drop_index > SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE) && (drop_index < SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_END))
    {
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS;
        index_offset = drop_index - SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE;
    }

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.lchip = lchip;
    traverse_param.value0 = (void*)&type;
    traverse_param.value1 = (void*)&index_offset;
    traverse_param.value2 = (void*)&dbg_counter_obj_id;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_DEBUG_COUNTER, (hash_traversal_fn)_ctc_sai_debug_counter_find_stat_index, (void*)&traverse_param);
    if(dbg_counter_obj_id == SAI_NULL_OBJECT_ID)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_dbgcounter_info = ctc_sai_db_get_object_property(lchip, dbg_counter_obj_id);
    
    if(NULL == p_dbgcounter_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if(DROP_REASON_IN == p_dbgcounter_info->dir)
    {
        for(loop_i = 0; loop_i < SAI_IN_DROP_REASON_END; loop_i++)
        {
            if(loop_i < 32)
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[0];
            }
            else
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[1];
            }
            if(IS_BIT_SET(tmp_drop_reason_list_bitmap, loop_i))
            {
                _ctc_sai_debug_counter_drop_reason_map(loop_i, DROP_REASON_IN, &ctc_drop_reason);
                for(num = 0; num < local_panel_ports.count; num ++)
                {
                    port_obj = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]));
                    p_port_db = ctc_sai_db_get_object_property(lchip, port_obj);
                    if (NULL == p_port_db)
                    {
                        continue;
                    }
                    CTC_SAI_ERROR_RETURN(_ctc_sai_debug_counter_get_port_reason_stats(lchip, local_panel_ports.lport[num], ctc_drop_reason, with_clear, &tmp_count));
                    total_count = total_count + tmp_count;
                }
            }
        }                
    }
    else if(DROP_REASON_OUT == p_dbgcounter_info->dir)
    {
        for(loop_i = 0; loop_i < SAI_OUT_DROP_REASON_END; loop_i++)
        {
            if(loop_i < 32)
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[0];
            }
            else
            {
                tmp_drop_reason_list_bitmap = p_dbgcounter_info->drop_reason_list_bitmap[1];
            }
            if(IS_BIT_SET(tmp_drop_reason_list_bitmap, loop_i))
            {
                _ctc_sai_debug_counter_drop_reason_map(loop_i, DROP_REASON_OUT, &ctc_drop_reason);
                for(num = 0; num < local_panel_ports.count; num ++)
                {
                    port_obj = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]));
                    p_port_db = ctc_sai_db_get_object_property(lchip, port_obj);
                    if (NULL == p_port_db)
                    {
                        continue;
                    }
                    CTC_SAI_ERROR_RETURN(_ctc_sai_debug_counter_get_port_reason_stats(lchip, local_panel_ports.lport[num], ctc_drop_reason, with_clear, &tmp_count));
                    total_count = total_count + tmp_count;
                }
            }
        }
    }
    *count = total_count;

    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "Debug counter get switch stats: count:%d, drop index = %d, reason bitmap0 = 0x%x, reason bitmap1 = 0x%x\n", 
        total_count, index_offset, p_dbgcounter_info->drop_reason_list_bitmap[0], p_dbgcounter_info->drop_reason_list_bitmap[1]);
        
    return SAI_STATUS_SUCCESS;
}

void ctc_sai_debug_counter_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Debug Counter MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_DEBUG_COUNTER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Debug Counter");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_counter_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s  %-18s  %-12s  %-12s  %-12s  %-12s  %-24s  %-24s\n", \
            "No.", "DbgCounter_oid", "Counter Type", "Bind Method", "Direction", "Stats Index", "Drop Reason List(Low)", "Drop Reason List(High)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_DEBUG_COUNTER,
                                            (hash_traversal_fn)_ctc_sai_debug_counter_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________DebugCounter______

sai_status_t ctc_sai_debug_counter_create_debug_counter (
         sai_object_id_t *debug_counter_id,
         sai_object_id_t switch_id,
         uint32_t attr_count,
         const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 dbgcnt_id = 0, dbgcnt_index = 0;
    uint32_t index = 0;
    sai_object_id_t dbg_counter_obj_id = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    const sai_attribute_value_t *attr_value;
    uint32 loop_i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    CTC_SAI_PTR_VALID_CHECK(debug_counter_id);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_debug_counter_create_attr_check(lchip, attr_count, attr_list));
    
    CTC_SAI_DB_LOCK(lchip);
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER, &dbgcnt_id), status, out);
    
    dbg_counter_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_DEBUG_COUNTER, lchip, 0, 0, dbgcnt_id);
    
    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "create debug counter id = 0x%"PRIx64"\n", dbg_counter_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_debug_counter_build_db(lchip, dbg_counter_obj_id, &p_dbgcounter_info), status, error1);

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_TYPE, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        p_dbgcounter_info->debug_counter_type = attr_value->s32;

        if((SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS == p_dbgcounter_info->debug_counter_type) ||
            (SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS == p_dbgcounter_info->debug_counter_type))
        {
            p_dbgcounter_info->dir = DROP_REASON_IN;
        }
        else if ((SAI_DEBUG_COUNTER_TYPE_PORT_OUT_DROP_REASONS == p_dbgcounter_info->debug_counter_type) ||
            (SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS == p_dbgcounter_info->debug_counter_type))
        {
            p_dbgcounter_info->dir = DROP_REASON_OUT;
        }
        else
        {
            p_dbgcounter_info->dir = DROP_REASON_MAX;
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_IN_DROP_REASON_LIST, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        for(loop_i = 0; loop_i < attr_value->s32list.count; loop_i++)
        {            
            if(attr_value->s32list.list[loop_i] < 32)
            {
                SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[0], attr_value->s32list.list[loop_i]);
            }
            else
            {
                SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[1], attr_value->s32list.list[loop_i]-32);
            }
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_OUT_DROP_REASON_LIST, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        for(loop_i = 0; loop_i < attr_value->s32list.count; loop_i++)
        {            
            if(attr_value->s32list.list[loop_i] < 32)
            {
                SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[0], attr_value->s32list.list[loop_i]);
            }
            else
            {
                SET_BIT(p_dbgcounter_info->drop_reason_list_bitmap[1], attr_value->s32list.list[loop_i]-32);
            }
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_DEBUG_COUNTER_ATTR_BIND_METHOD, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        p_dbgcounter_info->bind_method = attr_value->s32;
    }

    if(DROP_REASON_IN == p_dbgcounter_info->dir)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_IN_INDEX, &dbgcnt_index), status, error2);        
    }
    else if(DROP_REASON_OUT == p_dbgcounter_info->dir)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_OUT_INDEX, &dbgcnt_index), status, error2);        
    }

    p_dbgcounter_info->debug_counter_index = dbgcnt_index;
    
    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "create debug counter drop index = 0x%x, type:%d\n", dbgcnt_index, p_dbgcounter_info->debug_counter_type);

    *debug_counter_id = dbg_counter_obj_id;

    goto out;
    
error2:
    CTC_SAI_LOG_ERROR(SAI_API_COUNTER, "rollback to error2\n");
    _ctc_sai_debug_counter_remove_db(lchip, dbg_counter_obj_id);
    
error1:
    CTC_SAI_LOG_ERROR(SAI_API_COUNTER, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER, dbgcnt_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
    
    
}

sai_status_t ctc_sai_debug_counter_remove_debug_counter(
        sai_object_id_t dbgcounter_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_debug_counter_t* p_dbgcounter_info = NULL;
    uint32 dbgcnt_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(dbgcounter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    p_dbgcounter_info = ctc_sai_db_get_object_property(lchip, dbgcounter_id);
    
    ctc_sai_oid_get_debug_counter_id(dbgcounter_id, &dbgcnt_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER, dbgcnt_id);

    if(DROP_REASON_IN == p_dbgcounter_info->dir)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_IN_INDEX, p_dbgcounter_info->debug_counter_index);
    }
    else if(DROP_REASON_OUT == p_dbgcounter_info->dir)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_DEBUG_COUNTER_OUT_INDEX, p_dbgcounter_info->debug_counter_index);
    }    
    
    CTC_SAI_ERROR_GOTO(_ctc_sai_debug_counter_remove_db(lchip, dbgcounter_id), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t ctc_sai_debug_counter_set_debug_counter_attribute (
        sai_object_id_t debug_counter_id,
        const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    CTC_SAI_PTR_VALID_CHECK(attr);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(debug_counter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "counter_id = 0x%llx\n", debug_counter_id);
    key.key.object_id = debug_counter_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_COUNTER,  debug_counter_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);  
    return status;
}


sai_status_t ctc_sai_debug_counter_get_debug_counter_attribute (
        sai_object_id_t debug_counter_id,
        uint32_t attr_count,
        sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    CTC_SAI_PTR_VALID_CHECK(attr_list);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(debug_counter_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_DEBUG_COUNTER);
    CTC_SAI_LOG_INFO(SAI_API_DEBUG_COUNTER, "counter_id = 0x%llx\n", debug_counter_id);
    key.key.object_id = debug_counter_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_COUNTER, loop, debug_counter_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


sai_debug_counter_api_t g_ctc_sai_debug_counter_api = {
    ctc_sai_debug_counter_create_debug_counter,
    ctc_sai_debug_counter_remove_debug_counter,
    ctc_sai_debug_counter_set_debug_counter_attribute,
    ctc_sai_debug_counter_get_debug_counter_attribute,
};


sai_status_t
ctc_sai_debug_counter_api_init()
{
    ctc_sai_register_module_api(SAI_API_DEBUG_COUNTER, (void*)&g_ctc_sai_debug_counter_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_debug_counter_db_init(uint8 lchip)
{
    /*warmboot start */
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_DEBUG_COUNTER;
    wb_info.data_len = sizeof(ctc_sai_debug_counter_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_debug_counter_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_DEBUG_COUNTER, (void*)(&wb_info));
    /*warmboot end */   
    return SAI_STATUS_SUCCESS;
}

