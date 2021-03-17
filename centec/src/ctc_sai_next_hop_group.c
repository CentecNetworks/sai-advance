/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_bridge.h"

/*sdk include file*/
#include "ctcs_api.h"


static sai_status_t
_ctc_sai_next_hop_group_create_aps_nh(uint8 lchip, uint16 aps_group_id, uint32 nh_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_aps_bridge_group_t aps_bridge;

    sal_memset(&aps_bridge, 0, sizeof(ctc_aps_bridge_group_t));

    CTC_SAI_CTC_ERROR_RETURN(ctcs_aps_create_aps_bridge_group(lchip, aps_group_id, &aps_bridge));

    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_remove_aps_nh(uint8 lchip, uint16 aps_group_id, uint32 nh_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    
    ctcs_aps_destroy_aps_bridge_group(lchip, aps_group_id);
    
    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_update_aps_nh(uint8 lchip, sai_object_id_t nh_group_id, sai_object_id_t member_nexthop_oid, uint8 role)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_nh_grp_obj_id, ctc_nh_obj_id;
    ctc_sai_next_hop_grp_t* p_nh_group_id = NULL;
    ctc_sai_next_hop_t* p_nh_db = NULL;
    ctc_sai_next_hop_t* p_nh_tmp = NULL;
    ctc_sai_bridge_port_t* p_bp_db = NULL;
    ctc_nh_aps_param_t p_nh_param;
    uint32 aps_nh_or_tunnel_id = 0, member_nh_or_tunnel_id = 0;
    uint8 is_add_rw = 0, is_mpls_aps = 0, is_l2_aps = 0;
    ctc_mpls_nexthop_param_t nh_mpls_param;
    uint32 cfg_nh_id = CTC_NH_RESERVED_NHID_FOR_DROP;
    uint32 gport = 0;
    sai_object_type_t oid_type = SAI_OBJECT_TYPE_NULL;

    sal_memset(&nh_mpls_param, 0, sizeof(nh_mpls_param));

    p_nh_group_id = ctc_sai_db_get_object_property(lchip, nh_group_id);
    if(NULL == p_nh_group_id)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        return status;
    }
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, nh_group_id, &ctc_nh_grp_obj_id);
    sal_memset(&p_nh_param, 0, sizeof(p_nh_param));
    
    //ctc_nh_obj_id.value = CTC_NH_RESERVED_NHID_FOR_DROP;
    if(member_nexthop_oid)
    {
        is_add_rw = 1;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, member_nexthop_oid, &ctc_nh_obj_id);

        if(SAI_OBJECT_TYPE_NEXT_HOP == ctc_nh_obj_id.type)
        {
            p_nh_db = ctc_sai_db_get_object_property(lchip, member_nexthop_oid);
            if(NULL == p_nh_db)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                return status;
            }
            cfg_nh_id = ctc_nh_obj_id.value;
            is_mpls_aps = 1;
        }
        else if(SAI_OBJECT_TYPE_BRIDGE_PORT == ctc_nh_obj_id.type)
        {
            p_bp_db = ctc_sai_db_get_object_property(lchip, member_nexthop_oid);
            if(NULL == p_bp_db)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                return status;
            }

            if(ctc_nh_obj_id.sub_type == SAI_BRIDGE_PORT_TYPE_PORT)
            {                
                CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_l2uc(lchip, ctc_nh_obj_id.value, CTC_NH_PARAM_BRGUC_SUB_TYPE_BASIC, &cfg_nh_id));
            }
            else
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                return status;
            }
            is_l2_aps = 1;
        }
    }
    else
    {
        is_add_rw = 0;
    }
    
      
    //confirm aps type
    if(CTC_NH_APS_TYPE_MAX == p_nh_group_id->aps_nh_type)
    {          
        if(is_add_rw)
        {
            if(is_mpls_aps)
            {
                if(p_nh_db->ctc_mpls_tunnel_id)
                {
                    p_nh_param.type = CTC_NH_APS_TYPE_TUNNEL;
                }
                else
                {
                    p_nh_param.type = CTC_NH_APS_TYPE_NH;
                }
            }
            else if(is_l2_aps)
            {
                p_nh_param.type = CTC_NH_APS_TYPE_NH;
            }
        }
    }
    else
    {
        if(is_add_rw)
        {
            if(is_mpls_aps)
            {
                if((p_nh_db->ctc_mpls_tunnel_id && (p_nh_group_id->aps_nh_type != CTC_NH_APS_TYPE_TUNNEL))
                  || (!p_nh_db->ctc_mpls_tunnel_id && (p_nh_group_id->aps_nh_type != CTC_NH_APS_TYPE_NH)))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "member aps type is not equal to group aps type!\n");
                    status = SAI_STATUS_INVALID_OBJECT_ID;
                    return status;        
                }
            }
        }
          
        p_nh_param.type = p_nh_group_id->aps_nh_type;
    }

    //aps is created, do update
    if(p_nh_group_id->aps_nh_created)
    {
        if(p_nh_group_id->aps_tunnel_id) //must be mpls aps
        {
            aps_nh_or_tunnel_id = p_nh_group_id->aps_tunnel_id;
            if(is_add_rw)
            {
                member_nh_or_tunnel_id = p_nh_db->ctc_mpls_tunnel_id;
            }
            else
            {

            }
        
            if(p_nh_group_id->p_nh_oid)
            {
                p_nh_tmp = ctc_sai_db_get_object_property(lchip, p_nh_group_id->p_nh_oid);
                if(NULL == p_nh_tmp)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }
                p_nh_param.p_nhid = p_nh_tmp->ctc_mpls_tunnel_id;
            }
            if(p_nh_group_id->w_nh_oid)
            {
                p_nh_tmp = ctc_sai_db_get_object_property(lchip, p_nh_group_id->w_nh_oid);
                if(NULL == p_nh_tmp)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }
                p_nh_param.w_nhid = p_nh_tmp->ctc_mpls_tunnel_id;
            }
        }
        else
        {
            aps_nh_or_tunnel_id = ctc_nh_grp_obj_id.value;
            member_nh_or_tunnel_id = cfg_nh_id;

            ctc_sai_oid_get_type(p_nh_group_id->w_nh_oid, &oid_type);
            if(( SAI_OBJECT_TYPE_NEXT_HOP == oid_type) || (SAI_NULL_OBJECT_ID == p_nh_group_id->w_nh_oid))
            {
                ctc_sai_oid_get_value(p_nh_group_id->w_nh_oid, &p_nh_param.w_nhid);
            }
            else if( SAI_OBJECT_TYPE_BRIDGE_PORT == oid_type)
            {
                ctc_sai_oid_get_value(p_nh_group_id->w_nh_oid, &gport);
                ctcs_nh_get_l2uc(lchip, gport, CTC_NH_PARAM_BRGUC_SUB_TYPE_BASIC, &p_nh_param.w_nhid);
            }

            ctc_sai_oid_get_type(p_nh_group_id->p_nh_oid, &oid_type);
            if(( SAI_OBJECT_TYPE_NEXT_HOP == oid_type) || (SAI_NULL_OBJECT_ID == p_nh_group_id->p_nh_oid))
            {
                ctc_sai_oid_get_value(p_nh_group_id->p_nh_oid, &p_nh_param.p_nhid);
            }
            else if( SAI_OBJECT_TYPE_BRIDGE_PORT == oid_type)
            {
                ctc_sai_oid_get_value(p_nh_group_id->p_nh_oid, &gport);
                ctcs_nh_get_l2uc(lchip, gport, CTC_NH_PARAM_BRGUC_SUB_TYPE_BASIC, &p_nh_param.p_nhid);
            }            
        }
        
        p_nh_param.aps_group_id = ctc_nh_grp_obj_id.value2;
        

        if(SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY == role)
        {
            if(is_add_rw)
            {
                p_nh_param.w_nhid = member_nh_or_tunnel_id;   
            
                //if p nh is NULL, indicate p nh is not set, set to same nh in ASIC
                if(SAI_NULL_OBJECT_ID == p_nh_group_id->p_nh_oid)
                {
                    p_nh_param.p_nhid = member_nh_or_tunnel_id;
                }
                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, out);
            }
            else
            {
                if(SAI_NULL_OBJECT_ID != p_nh_group_id->p_nh_oid)
                {
                    p_nh_param.w_nhid = p_nh_param.p_nhid;

                    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, out);
                }                
            }
            
            p_nh_group_id->w_nh_oid = member_nexthop_oid;
        }
        else if(SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY == role)
        {
            if(is_add_rw)
            {
                p_nh_param.p_nhid = member_nh_or_tunnel_id;
                //if w nh is NULL, indicate w nh is not set, set to same nh in ASIC
                if(SAI_NULL_OBJECT_ID == p_nh_group_id->w_nh_oid)
                {
                    p_nh_param.w_nhid = member_nh_or_tunnel_id;
                }
                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, out);
            }
            else
            {
                if(SAI_NULL_OBJECT_ID != p_nh_group_id->w_nh_oid)
                {
                    p_nh_param.p_nhid = p_nh_param.w_nhid;

                    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, out);
                }                
            }
            p_nh_group_id->p_nh_oid = member_nexthop_oid;
        }

        //if working & protection nh are both NULL, del aps nh
        if(( SAI_NULL_OBJECT_ID == p_nh_group_id->w_nh_oid) && ( SAI_NULL_OBJECT_ID == p_nh_group_id->p_nh_oid))
        {
            if(CTC_NH_APS_TYPE_TUNNEL == p_nh_group_id->aps_nh_type)
            {
                ctcs_nh_remove_mpls(lchip, ctc_nh_grp_obj_id.value);
            }
            ctcs_nh_remove_aps(lchip, aps_nh_or_tunnel_id, p_nh_group_id->aps_nh_type);
            p_nh_group_id->aps_nh_created = 0;
            if(CTC_NH_APS_TYPE_TUNNEL == p_nh_group_id->aps_nh_type)
            {
                ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, p_nh_group_id->aps_tunnel_id);
                p_nh_group_id->aps_tunnel_id = 0;
            }
            p_nh_group_id->aps_nh_type = CTC_NH_APS_TYPE_MAX;
        }
    }
    else //do aps create
    {        
        
        if(is_mpls_aps && p_nh_db->ctc_mpls_tunnel_id)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, &aps_nh_or_tunnel_id));
            member_nh_or_tunnel_id = p_nh_db->ctc_mpls_tunnel_id;
        }
        else
        {
            aps_nh_or_tunnel_id = ctc_nh_grp_obj_id.value;
            member_nh_or_tunnel_id = cfg_nh_id;
        }        
                
        p_nh_param.aps_group_id = ctc_nh_grp_obj_id.value2;

        if(SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY == role)
        {
            p_nh_param.w_nhid = member_nh_or_tunnel_id;
            p_nh_param.p_nhid = member_nh_or_tunnel_id;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, error1);
            
            if(is_mpls_aps && p_nh_db->ctc_mpls_tunnel_id)
            {
                nh_mpls_param.nh_prop = CTC_MPLS_NH_PUSH_TYPE;
                if(SAI_OUTSEG_TYPE_PUSH == p_nh_db->outseg_type)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
                }
                else if(SAI_OUTSEG_TYPE_SWAP == p_nh_db->outseg_type)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_NONE;
                }
                nh_mpls_param.nh_para.nh_param_push.tunnel_id = aps_nh_or_tunnel_id;
                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, ctc_nh_grp_obj_id.value, &nh_mpls_param), status, error2);
            }
            p_nh_group_id->w_nh_oid = member_nexthop_oid;
            p_nh_group_id->p_nh_oid = SAI_NULL_OBJECT_ID;
        }
        else if(SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY == role)
        {
            p_nh_param.w_nhid = member_nh_or_tunnel_id;
            p_nh_param.p_nhid = member_nh_or_tunnel_id;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_aps(lchip, aps_nh_or_tunnel_id, &p_nh_param), status, error1);

            if(is_mpls_aps && p_nh_db->ctc_mpls_tunnel_id)
            {
                nh_mpls_param.nh_prop = CTC_MPLS_NH_PUSH_TYPE;
                if(SAI_OUTSEG_TYPE_PUSH == p_nh_db->outseg_type)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
                }
                else if(SAI_OUTSEG_TYPE_SWAP == p_nh_db->outseg_type)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_NONE;
                }
                nh_mpls_param.nh_para.nh_param_push.tunnel_id = aps_nh_or_tunnel_id;
                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, ctc_nh_grp_obj_id.value, &nh_mpls_param), status, error2);
            }
            p_nh_group_id->w_nh_oid = SAI_NULL_OBJECT_ID;
            p_nh_group_id->p_nh_oid = member_nexthop_oid;
        }

        if(is_mpls_aps && p_nh_db->ctc_mpls_tunnel_id)
        {
            p_nh_group_id->aps_nh_type = CTC_NH_APS_TYPE_TUNNEL;
            p_nh_group_id->aps_tunnel_id = aps_nh_or_tunnel_id;
        }
        else
        {
            p_nh_group_id->aps_nh_type = CTC_NH_APS_TYPE_NH;
        }
        
        p_nh_group_id->aps_nh_created = 1;
        
        
    }

    goto out;
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "update aps nh rollback to error2\n");
    ctcs_nh_remove_aps(lchip, aps_nh_or_tunnel_id, p_nh_param.type);

error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "update aps nh rollback to error1\n");
    if(p_nh_db->ctc_mpls_tunnel_id)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, aps_nh_or_tunnel_id);
    }
out:    
    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_create_member(sai_object_id_t *next_hop_group_member_id, sai_object_id_t switch_id,
                                                                    uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    sai_object_id_t nh_grp_obj_id = 0;
    ctc_object_id_t ctc_nh_grp_obj_id;
    ctc_object_id_t ctc_mem_nh_obj_id;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = NULL;
    sai_object_id_t nh_obj_id = 0;
    uint32 nh_id = 0;//member nexthop id
    sai_object_id_t nh_grp_member_obj_id = 0;
    uint32 nh_member_id = 0;
    sai_object_id_t original_nh_id = 0;
    uint8 is_working = 1, is_standby = 0, mem_exist = 0;

    ctc_sai_oid_get_lchip(switch_id, &lchip);
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    nh_grp_obj_id = attr_value->oid;
    p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, nh_grp_obj_id);
    if(NULL == p_next_hop_grp_info)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    nh_obj_id = attr_value->oid;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, nh_obj_id, &ctc_mem_nh_obj_id);
    if(SAI_OBJECT_TYPE_NEXT_HOP == ctc_mem_nh_obj_id.type) 
    {        
        CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_nexthop_id(nh_obj_id, &nh_id), status, out);
    }
    else if (SAI_OBJECT_TYPE_BRIDGE_PORT == ctc_mem_nh_obj_id.type)
    {
        //get nh_id from bridge port 
    }
    else
    {
        //ERROR
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, nh_grp_obj_id, &ctc_nh_grp_obj_id);

    p_next_hop_member_info = mem_malloc(MEM_NEXTHOP_MODULE, sizeof(ctc_sai_next_hop_grp_member_t));
    if (NULL == p_next_hop_member_info)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto out;
    }
    sal_memset(p_next_hop_member_info, 0, sizeof(ctc_sai_next_hop_grp_member_t));
    p_next_hop_member_info->nh_grp_oid = nh_grp_obj_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER, &nh_member_id), status, error1);

    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_nh_grp_obj_id.sub_type)
    {
        ctc_nh_ecmp_nh_param_t nh_param;
        sal_memset(&nh_param, 0, sizeof(ctc_nh_ecmp_nh_param_t));
        nh_param.upd_type = CTC_NH_ECMP_ADD_MEMBER;
        nh_param.nh_num = 1;
        nh_param.nhid[0] = nh_id;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_ecmp(lchip, ctc_nh_grp_obj_id.value, &nh_param), status, error2);
    }
    if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_nh_grp_obj_id.sub_type)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto error2;
        }
        is_working = (SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY == attr_value->s32);
        is_standby = (SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY == attr_value->s32);
        mem_exist = is_standby ?  (0 != p_next_hop_grp_info->p_nh_oid) : (0 != p_next_hop_grp_info->w_nh_oid);
        if(mem_exist)
        {
            status = SAI_STATUS_ITEM_ALREADY_EXISTS;
            goto error2;
        }
        if(is_standby)
        {
            original_nh_id = p_next_hop_grp_info->p_nh_oid;
        }
        else
        {
            original_nh_id = p_next_hop_grp_info->w_nh_oid;
        }
        CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_next_hop_group_update_aps_nh(lchip, nh_grp_obj_id, nh_obj_id, is_standby), status, error2);

    }
    nh_grp_member_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, lchip, is_working, nh_member_id, nh_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, nh_grp_member_obj_id, (void*)p_next_hop_member_info), status, error3);
    *next_hop_group_member_id = nh_grp_member_obj_id;
    if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_nh_grp_obj_id.sub_type)
    {
        if(is_standby)
        {
            p_next_hop_grp_info->p_member_oid = nh_grp_member_obj_id;
        }
        else
        {
            p_next_hop_grp_info->w_member_oid = nh_grp_member_obj_id;
        }
    }
    goto out;
error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error3\n");
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_nh_grp_obj_id.sub_type)
    {
        ctc_nh_ecmp_nh_param_t nh_param;
        sal_memset(&nh_param, 0, sizeof(ctc_nh_ecmp_nh_param_t));
        ctc_sai_oid_get_nexthop_id(nh_obj_id, &nh_id);
        nh_param.upd_type = CTC_NH_ECMP_REMOVE_MEMBER;
        nh_param.nh_num = 1;
        nh_param.nhid[0] = nh_id;
        ctcs_nh_update_ecmp(lchip, ctc_nh_grp_obj_id.value, &nh_param);
    }
    if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_nh_grp_obj_id.sub_type)
    {
        _ctc_sai_next_hop_group_update_aps_nh(lchip, nh_grp_obj_id, original_nh_id, is_standby);
    }
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error2\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER, nh_member_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error1\n");
    mem_free(p_next_hop_member_info);
out:
    return status;
}
                                                                    
static sai_status_t
_ctc_sai_next_hop_group_remove_member(sai_object_id_t next_hop_group_member_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = NULL;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    ctc_object_id_t ctc_nh_grp_oid;
    ctc_object_id_t ctc_nh_grp_member_oid;
    //sai_object_id_t nh_oid_old;

    ctc_sai_oid_get_lchip(next_hop_group_member_id, &lchip);
    p_next_hop_member_info = ctc_sai_db_get_object_property(lchip, next_hop_group_member_id);
    if(NULL == p_next_hop_member_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, p_next_hop_member_info->nh_grp_oid);
    if(NULL == p_next_hop_grp_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, p_next_hop_member_info->nh_grp_oid, &ctc_nh_grp_oid);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, next_hop_group_member_id, &ctc_nh_grp_member_oid);
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_nh_grp_oid.sub_type)
    {
        ctc_nh_ecmp_nh_param_t nh_param;
        sal_memset(&nh_param, 0, sizeof(ctc_nh_ecmp_nh_param_t));
        nh_param.upd_type = CTC_NH_ECMP_REMOVE_MEMBER;
        nh_param.nh_num = 1;
        nh_param.nhid[0] = ctc_nh_grp_member_oid.value;
        status = ctcs_nh_update_ecmp(lchip, ctc_nh_grp_oid.value, &nh_param);
        if (status && (CTC_E_NH_NOT_EXIST != status) && (CTC_E_NOT_EXIST != status))
        {
            status = ctc_sai_mapping_error_ctc(status);
            goto out;
        }
    }
    if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_nh_grp_oid.sub_type)
    {
        _ctc_sai_next_hop_group_update_aps_nh(lchip, p_next_hop_member_info->nh_grp_oid, 0, !ctc_nh_grp_member_oid.sub_type);
        if(ctc_nh_grp_member_oid.sub_type)
        {
            p_next_hop_grp_info->w_member_oid = SAI_NULL_OBJECT_ID;
        }
        else
        {
            p_next_hop_grp_info->p_member_oid = SAI_NULL_OBJECT_ID;
        }
    }
    
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER, ctc_nh_grp_member_oid.value2);
    ctc_sai_db_remove_object_property(lchip, next_hop_group_member_id);
    mem_free(p_next_hop_member_info);
out:
    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_get_members_from_db(ctc_sai_oid_property_t* bucket_data, sai_object_list_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = (ctc_sai_next_hop_grp_member_t*)(bucket_data->data);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, bucket_data->oid, &ctc_object_id);
    if (p_next_hop_member_info->nh_grp_oid == user_data->list[0])
    {
        user_data->list[user_data->count++] = bucket_data->oid;
    }
    return status;
}
static sai_status_t
_ctc_sai_next_hop_group_set_grp_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;

    if (SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER == attr->id)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, key->key.object_id, &ctc_object_id);
        if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION != ctc_object_id.sub_type)
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_aps_set_aps_bridge(ctc_object_id.lchip, ctc_object_id.value2, attr->value.booldata));
    }
    else
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    return status;
}
static sai_status_t
_ctc_sai_next_hop_group_get_grp_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    uint32 nh_id = 0;
    uint8 group_type = 0;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    group_type = ctc_object_id.sub_type;
    nh_id = ctc_object_id.value;

    if (SAI_NEXT_HOP_GROUP_ATTR_TYPE == attr->id)
    {
        attr->value.s32 = group_type;
    }
    else if(SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER == attr->id)
    {
        ctcs_aps_get_aps_bridge(lchip, ctc_object_id.value2, &attr->value.booldata);
    }
    else if(SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID == attr->id)
    {
        p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
        if (NULL == p_next_hop_grp_info)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if(SAI_NEXT_HOP_GROUP_TYPE_ECMP == group_type)
        {
            attr->value.oid = p_next_hop_grp_info->counter_oid;
        }
        else
        {
            attr->value.oid = SAI_NULL_OBJECT_ID;
        }
    }
    else
    {
        if(SAI_NEXT_HOP_GROUP_TYPE_ECMP == group_type)
        {
            ctc_nh_info_t nh_info;
            sal_memset(&nh_info, 0, sizeof(nh_info));
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, nh_id, &nh_info));
            if (!CTC_FLAG_ISSET(nh_info.flag, CTC_NH_INFO_FLAG_IS_ECMP))
            {
                return SAI_STATUS_FAILURE;
            }
            if (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT == attr->id)
            {
                attr->value.u32 = nh_info.ecmp_cnt;
            }
            else if (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST == attr->id)
            {
                attr->value.objlist.count = 1;
                attr->value.objlist.list[0] = key->key.object_id;/*the first member used as param when traverser*/
                ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER,
                                                         (hash_traversal_fn)_ctc_sai_next_hop_group_get_members_from_db, (void*)(&(attr->value.objlist)));
                if (attr->value.objlist.count > 1)
                {
                    attr->value.objlist.list[0] = attr->value.objlist.list[--attr->value.objlist.count];
                }
                else
                {
                    attr->value.objlist.count = 0;
                    attr->value.objlist.list[0] = SAI_NULL_OBJECT_ID;
                }
            }
        }
        else if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == group_type)
        {
            p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
            if (NULL == p_next_hop_grp_info)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            if (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT == attr->id)
            {
                attr->value.u32 = (p_next_hop_grp_info->w_nh_oid != 0) + (p_next_hop_grp_info->p_nh_oid != 0);
            }
            else if (SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST == attr->id)
            {
                attr->value.objlist.count = 0;
                if (p_next_hop_grp_info->w_nh_oid != 0)
                {
                    attr->value.objlist.list[attr->value.objlist.count++] = p_next_hop_grp_info->w_member_oid;
                }
                if (p_next_hop_grp_info->p_nh_oid != 0)
                {
                    attr->value.objlist.list[attr->value.objlist.count++] = p_next_hop_grp_info->p_member_oid;
                }
            }
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_get_member_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = NULL;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    ctc_object_id_t ctc_nh_grp_member_oid;
    ctc_object_id_t ctc_nh_grp_oid;
    sai_object_id_t nh_oid;
    uint8 is_working = 0;
    uint16 aps_bridge_id = 0;
    bool protect_en = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_next_hop_member_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_next_hop_member_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, p_next_hop_member_info->nh_grp_oid);
    if (NULL == p_next_hop_grp_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, key->key.object_id, &ctc_nh_grp_member_oid);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, p_next_hop_member_info->nh_grp_oid, &ctc_nh_grp_oid);
    nh_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP, lchip, 0, 0, ctc_nh_grp_member_oid.value);
    if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_nh_grp_oid.sub_type)
    {
        aps_bridge_id = ctc_nh_grp_oid.value2;
        if (nh_oid == p_next_hop_grp_info->w_nh_oid)
        {
            is_working = 1;
        }
    }

    if (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID == attr->id)
    {
        attr->value.oid = p_next_hop_member_info->nh_grp_oid;
    }
    else if (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID == attr->id)
    {
        attr->value.oid = nh_oid;
    }
    else if (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE == attr->id)
    {
        if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_nh_grp_oid.sub_type)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.s32 = is_working? SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY
                                        : SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY;
    }
    else if (SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE == attr->id)
    {
        if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_nh_grp_oid.sub_type)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        ctcs_aps_get_aps_bridge(lchip, aps_bridge_id, & protect_en);
        if (is_working)
        {
            attr->value.s32 = protect_en? SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE
                                             : SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE;
        }
        else
        {
            attr->value.s32 = protect_en? SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE
                                             : SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE;
        }
    }
    else
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_next_hop_group_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = (ctc_sai_next_hop_grp_t*)(bucket_data->data);;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    ctc_object_id_t ctc_object_id;
    uint32 num_cnt = 0;
    char nh_grp_oid[64] = {'-'};
    char w_nh_oid[64] = {'-'};
    char p_nh_oid[64] = {'-'};
    char* type = "-";

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(nh_grp_oid, "0x%016"PRIx64, bucket_data->oid);
    if (p_next_hop_grp_info->w_nh_oid)
    {
        sal_sprintf(w_nh_oid, "0x%016"PRIx64, p_next_hop_grp_info->w_nh_oid);
    }
    if (p_next_hop_grp_info->p_nh_oid)
    {
        sal_sprintf(p_nh_oid, "0x%016"PRIx64, p_next_hop_grp_info->p_nh_oid);
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, bucket_data->oid, &ctc_object_id);
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_object_id.sub_type)
    {
        type = "ECMP";
    }
    else if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_object_id.sub_type)
    {
        type = "PROTECTION";
    }

    CTC_SAI_LOG_DUMP(p_file, "%-8d%-24s%-24s%-10d%-24s%-24s\n", num_cnt, nh_grp_oid, type, ctc_object_id.value, w_nh_oid, p_nh_oid);
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_group_member_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = (ctc_sai_next_hop_grp_member_t*)(bucket_data->data);;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    ctc_object_id_t ctc_object_id;
    uint32 num_cnt = 0;
    char nh_grp_oid[64] = {'-'};
    char nh_grp_mem_oid[64] = {'-'};

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(nh_grp_mem_oid, "0x%016"PRIx64, bucket_data->oid);
    sal_sprintf(nh_grp_oid, "0x%016"PRIx64, p_next_hop_member_info->nh_grp_oid);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, bucket_data->oid, &ctc_object_id);
    CTC_SAI_LOG_DUMP(p_file, "%-8d%-32s%-24s%-10d\n", num_cnt, nh_grp_mem_oid, nh_grp_oid, ctc_object_id.value);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}


static  ctc_sai_attr_fn_entry_t nh_grp_attr_fn_entries[] = {
    { SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT,
      _ctc_sai_next_hop_group_get_grp_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST,
      _ctc_sai_next_hop_group_get_grp_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_ATTR_TYPE,
      _ctc_sai_next_hop_group_get_grp_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER,
      _ctc_sai_next_hop_group_get_grp_attr,
      _ctc_sai_next_hop_group_set_grp_attr},
    { SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID,
      _ctc_sai_next_hop_group_get_grp_attr,
      NULL},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

static  ctc_sai_attr_fn_entry_t nh_grp_member_attr_fn_entries[] = {
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_WEIGHT,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    { SAI_NEXT_HOP_GROUP_MEMBER_ATTR_MONITORED_OBJECT,
      _ctc_sai_next_hop_group_get_member_attr,
      NULL},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

#define ________INTERNAL_API________

static sai_status_t
_ctc_sai_next_hop_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_object_id_t next_hop_group_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_grp_t* p_sai_next_hop_grp_info = (ctc_sai_next_hop_grp_t*)data;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, next_hop_group_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_object_id.value));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_APS, ctc_object_id.value2));

    if(p_sai_next_hop_grp_info->aps_tunnel_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, p_sai_next_hop_grp_info->aps_tunnel_id));
    }
    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_group_member_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_object_id_t next_hop_group_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_object_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, next_hop_group_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP_MEMBER, ctc_object_id.value2));
    return SAI_STATUS_SUCCESS;
}

void ctc_sai_next_hop_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Next Hop Group MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_NEXT_HOP_GROUP))
    {
        num_cnt = 1;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Next Hop Group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_next_hop_grp_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-24s%-24s%-10s%-24s%-24s\n", "No.", "next_hop_group_id", "type", "nh_id", "w_nh_oid", "p_nh_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP_GROUP,
                                            (hash_traversal_fn)_ctc_sai_next_hop_group_dump_print_cb, (void*)(&sai_cb_data));
    }

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER))
    {
        num_cnt = 1;
        CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "Next Hop Group Member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_next_hop_grp_member_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-32s%-24s%-10s\n", "No.", "next_hop_group_member_id", "next_hop_group_id", "nh_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER,
                                            (hash_traversal_fn)_ctc_sai_next_hop_group_member_dump_print_cb, (void*)(&sai_cb_data));
    }
}


#define ________SAI_API________
static sai_status_t
ctc_sai_next_hop_group_create_nh_grp(sai_object_id_t *next_hop_group_id, sai_object_id_t switch_id,
                                                                   uint32_t attr_count, const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    uint32 nh_id = 0;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    sai_object_id_t nh_grp_obj_id = 0, counter_oid = 0;
    ctc_nh_ecmp_nh_param_t nh_param;
    uint32 aps_group_id = 0;
    uint8 group_type = 0;
    uint32 stats_id = 0;
    ctc_aps_bridge_group_t aps_bridge;

    sal_memset(&aps_bridge, 0, sizeof(ctc_aps_bridge_group_t));

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);
    CTC_SAI_PTR_VALID_CHECK(next_hop_group_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_ATTR_TYPE, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    group_type = attr_value->s32;

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        counter_oid = attr_value->oid;
    }    

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id), status, out);
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == group_type)
    {
        sal_memset(&nh_param, 0, sizeof(nh_param));
        nh_param.type = CTC_NH_ECMP_TYPE_STATIC;
        nh_param.member_num = 64;
        nh_param.nhid[0] = CTC_NH_RESERVED_NHID_FOR_DROP;
        nh_param.nh_num = 1;
        if(SAI_NULL_OBJECT_ID != counter_oid)
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(counter_oid, CTC_SAI_COUNTER_TYPE_ECMP, &stats_id),status,error0);
            nh_param.stats_id = stats_id;
        }
        CTC_SAI_ERROR_GOTO(ctcs_nh_add_ecmp(lchip, nh_id, &nh_param), status, error1);
        nh_param.upd_type = CTC_NH_ECMP_REMOVE_MEMBER;
        ctcs_nh_update_ecmp(lchip, nh_id, &nh_param);
    }
    else if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == group_type)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_APS, &aps_group_id), status, error1);
        CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_group_create_aps_nh(lchip, aps_group_id, nh_id), status, error2);        
    }
    else
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error1;
    }

    nh_grp_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, lchip, group_type, aps_group_id, nh_id);
    p_next_hop_grp_info = mem_malloc(MEM_NEXTHOP_MODULE, sizeof(ctc_sai_next_hop_grp_t));
    if (NULL == p_next_hop_grp_info)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    sal_memset(p_next_hop_grp_info, 0, sizeof(ctc_sai_next_hop_grp_t));
    p_next_hop_grp_info->counter_oid = counter_oid;
    p_next_hop_grp_info->aps_nh_type = CTC_NH_APS_TYPE_MAX;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, nh_grp_obj_id, p_next_hop_grp_info), status, error4);
    *next_hop_group_id = nh_grp_obj_id;
    goto out;

error4:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error4\n");
    mem_free(p_next_hop_grp_info);
error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error3\n");
    if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == group_type)
    {
        _ctc_sai_next_hop_group_remove_aps_nh(lchip, aps_group_id, nh_id);
    }    
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error2\n");
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == group_type)
    {
        ctcs_nh_remove_ecmp(lchip, nh_id);
    }
    else if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == group_type)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_APS, aps_group_id);
    }
error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error1\n");
    if ((SAI_NEXT_HOP_GROUP_TYPE_ECMP == group_type)&&(SAI_NULL_OBJECT_ID != counter_oid))
    {
        ctc_sai_counter_id_remove(counter_oid, CTC_SAI_COUNTER_TYPE_ECMP);
    }
error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_remove_nh_grp(sai_object_id_t next_hop_group_id)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);

    p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, next_hop_group_id);
    if (NULL == p_next_hop_grp_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, next_hop_group_id, &ctc_object_id);
    if (SAI_NEXT_HOP_GROUP_TYPE_ECMP == ctc_object_id.sub_type)
    {        
        status = ctcs_nh_remove_ecmp(lchip, ctc_object_id.value);
        if (status)
        {
            status = ctc_sai_mapping_error_ctc(status);
            CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "remove ecmp gourp error\n");
            goto out;
        }

        if(SAI_NULL_OBJECT_ID != p_next_hop_grp_info->counter_oid)
        {
            status = ctc_sai_counter_id_remove(p_next_hop_grp_info->counter_oid, CTC_SAI_COUNTER_TYPE_ECMP);
            if (status)
            {
                CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "remove ecmp stats oid error\n");
                goto out;
            }

        }
    }
    else if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == ctc_object_id.sub_type)
    {
        _ctc_sai_next_hop_group_remove_aps_nh(lchip, ctc_object_id.value2, ctc_object_id.value);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_APS, ctc_object_id.value2);
    }


    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_object_id.value);
    ctc_sai_db_remove_object_property(lchip, next_hop_group_id);
    mem_free(p_next_hop_grp_info);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_set_grp_attr(sai_object_id_t next_hop_group_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);
    key.key.object_id = next_hop_group_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_NEXT_HOP_GROUP,  nh_grp_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_get_grp_attr(sai_object_id_t next_hop_group_id,
                                                                     uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);
    key.key.object_id = next_hop_group_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_NEXT_HOP_GROUP, loop, nh_grp_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_create_member(sai_object_id_t *next_hop_group_member_id, sai_object_id_t switch_id,
                                                                    uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_PTR_VALID_CHECK(next_hop_group_member_id);
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_next_hop_group_create_member(next_hop_group_member_id, switch_id, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_remove_member(sai_object_id_t next_hop_group_member_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_next_hop_group_remove_member(next_hop_group_member_id);
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_set_member_attr(sai_object_id_t next_hop_group_member_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);
    key.key.object_id = next_hop_group_member_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER,  nh_grp_member_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_get_member_attr(sai_object_id_t next_hop_group_member_id,
                                                                       uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP_GROUP);
    key.key.object_id = next_hop_group_member_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, loop, nh_grp_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_bulk_create_members(
         sai_object_id_t switch_id,
         uint32_t object_count,
         const uint32_t *attr_count,
         const sai_attribute_t **attr_list,
         sai_bulk_op_error_mode_t mode,
         sai_object_id_t *object_id,
         sai_status_t *object_statuses)
{
    uint8 lchip = 0;
    uint32 i =  0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (i = 0; i < object_count; i++)
    {
        object_statuses[i] = _ctc_sai_next_hop_group_create_member(&(object_id[i]), switch_id,
                                                                   attr_count[i], attr_list[i]);
        if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
            if (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode)
            {
                goto out;
            }
        }
    }
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_group_bulk_remove_members(
         uint32_t object_count,
         const sai_object_id_t *object_id,
         sai_bulk_op_error_mode_t mode,
         sai_status_t *object_statuses)
{
    uint8 lchip = 0;
    uint32 i =  0;
    sai_status_t           status = SAI_STATUS_SUCCESS;

    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_lchip(object_id[i], &lchip), status, out);
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_next_hop_group_remove_member(object_id[i]);
        if (CTC_SAI_ERROR(object_statuses[i]))
        {
            status = SAI_STATUS_FAILURE;
            if (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode)
            {
                CTC_SAI_DB_UNLOCK(lchip);
                return status;
            }
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
out:
    return status;
}


const sai_next_hop_group_api_t ctc_sai_next_hop_group_api = {
    ctc_sai_next_hop_group_create_nh_grp,
    ctc_sai_next_hop_group_remove_nh_grp,
    ctc_sai_next_hop_group_set_grp_attr,
    ctc_sai_next_hop_group_get_grp_attr,
    ctc_sai_next_hop_group_create_member,
    ctc_sai_next_hop_group_remove_member,
    ctc_sai_next_hop_group_set_member_attr,
    ctc_sai_next_hop_group_get_member_attr,
    ctc_sai_next_hop_group_bulk_create_members,
    ctc_sai_next_hop_group_bulk_remove_members
};

sai_status_t
ctc_sai_next_hop_group_api_init()
{
    ctc_sai_register_module_api(SAI_API_NEXT_HOP_GROUP, (void*)&ctc_sai_next_hop_group_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_next_hop_group_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NEXTHOPGROUP;
    wb_info.data_len = sizeof(ctc_sai_next_hop_grp_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_next_hop_group_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_NEXT_HOP_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NEXTHOPGROUP;
    wb_info.data_len = sizeof(ctc_sai_next_hop_grp_member_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_next_hop_group_member_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

