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

/*sdk include file*/
#include "ctcs_api.h"

typedef struct  ctc_sai_next_hop_grp_s
{
    sai_object_id_t w_nh_oid;/*member nexthop id*/
    sai_object_id_t p_nh_oid;/*member nexthop id*/
    sai_object_id_t counter_oid;
}ctc_sai_next_hop_grp_t;

typedef struct  ctc_sai_next_hop_grp_member_s
{
    sai_object_id_t nh_grp_oid;/*group nexthop id*/
}ctc_sai_next_hop_grp_member_t;

static sai_status_t
_ctc_sai_next_hop_group_create_aps_nh(uint8 lchip, uint16 aps_group_id, uint32 nh_id,
                                      sai_object_id_t w_nh_oid, sai_object_id_t p_nh_oid)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_aps_bridge_group_t aps_group;
    ctc_object_id_t w_nh;
    ctc_object_id_t p_nh;
    ctc_nh_info_t w_nh_info;
    ctc_nh_info_t p_nh_info;
    uint32 member_nh_id = 0;
    ctc_sai_next_hop_t* p_next_hop_info = 0;

    ctc_sai_get_ctc_object_id(SAI_API_NEXT_HOP, w_nh_oid, &w_nh);
    ctc_sai_get_ctc_object_id(SAI_API_NEXT_HOP, p_nh_oid, &p_nh);
    if (w_nh.sub_type != p_nh.sub_type)
    {
        return  SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&aps_group, 0, sizeof(aps_group));
    sal_memset(&w_nh_info, 0, sizeof(w_nh_info));
    sal_memset(&p_nh_info, 0, sizeof(p_nh_info));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_nexthop_id(w_nh_oid, &member_nh_id));
    CTC_SAI_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, member_nh_id, &w_nh_info));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_nexthop_id(p_nh_oid, &member_nh_id));
    CTC_SAI_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, member_nh_id, &p_nh_info));

    aps_group.working_gport = w_nh_info.gport;
    aps_group.protection_gport = p_nh_info.gport;
    
    p_next_hop_info = ctc_sai_db_get_object_property(lchip, w_nh_oid);
    if (NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_l3if_id(p_next_hop_info->rif_id, &aps_group.w_l3if_id));

    p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_nh_oid);
    if (NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_l3if_id(p_next_hop_info->rif_id, &aps_group.p_l3if_id));
    
    CTC_SAI_CTC_ERROR_RETURN(ctcs_aps_create_aps_bridge_group(lchip, aps_group_id, &aps_group));

    if (SAI_NEXT_HOP_TYPE_IP == w_nh.sub_type)
    {
        ctc_ip_nh_param_t nh_param;
        sal_memset(&nh_param, 0, sizeof(nh_param));
        nh_param.aps_en = 1;
        nh_param.aps_bridge_group_id = aps_group_id;
        status |= ctc_sai_next_hop_get_arp_id(w_nh_oid, &nh_param.arp_id);
        status |= ctc_sai_next_hop_get_arp_id(p_nh_oid, &nh_param.p_arp_id);
        status |= ctcs_nh_add_ipuc(lchip, nh_id, &nh_param);
        if (CTC_SAI_ERROR(status))
        {
            status = ctc_sai_mapping_error_ctc(status);
            goto error1;
        }
    }
    else if(SAI_NEXT_HOP_TYPE_MPLS == w_nh.sub_type)
    {
        ctc_sai_next_hop_t* w_next_hop_info = 0;
        ctc_sai_next_hop_t* p_next_hop_info = 0;
        ctc_mpls_nexthop_param_t nh_param;

        w_next_hop_info = ctc_sai_db_get_object_property(lchip, w_nh_oid);
        if (NULL == w_next_hop_info)
        {
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error1;
        }
        p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_nh_oid);
        if (NULL == p_next_hop_info)
        {
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error1;
        }
        if (w_next_hop_info->label.count != p_next_hop_info->label.count)
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error1;
        }

        sal_memset(&nh_param, 0, sizeof(nh_param));
        nh_param.nh_prop = CTC_MPLS_NH_PUSH_TYPE;
        nh_param.aps_en = 1;
        nh_param.aps_bridge_group_id = aps_group_id;
        /* Working PW */
        nh_param.nh_para.nh_param_push.tunnel_id = w_next_hop_info->ctc_mpls_tunnel_id;
        nh_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
        if (3 == w_next_hop_info->label.count)
        {
            nh_param.nh_para.nh_param_push.label_num = 1;
            nh_param.nh_para.nh_param_push.push_label[0].ttl = (w_next_hop_info->label.list[2])&0xFF;
            nh_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_param.nh_para.nh_param_push.push_label[0].exp = ((w_next_hop_info->label.list[2]) >> 9)&0x7;
            nh_param.nh_para.nh_param_push.push_label[0].label = ((w_next_hop_info->label.list[2]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);

        }
        /* Protection PW */
        nh_param.nh_p_para.nh_p_param_push.tunnel_id = p_next_hop_info->ctc_mpls_tunnel_id;
        nh_param.nh_p_para.nh_p_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
        if (p_next_hop_info->label.count > 1)
        {
            nh_param.nh_para.nh_param_push.label_num = 1;
            nh_param.nh_para.nh_param_push.push_label[0].ttl = (p_next_hop_info->label.list[2])&0xFF;
            nh_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_param.nh_para.nh_param_push.push_label[0].exp = ((p_next_hop_info->label.list[2]) >> 9)&0x7;
            nh_param.nh_para.nh_param_push.push_label[0].label = ((p_next_hop_info->label.list[2]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        }
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, nh_id, &nh_param), status, error1);
    }

    return SAI_STATUS_SUCCESS;
error1:
    ctcs_aps_destroy_aps_bridge_group(lchip, aps_group_id);
    return status;
}

static sai_status_t
_ctc_sai_next_hop_group_remove_aps_nh(uint8 lchip, uint16 aps_group_id, uint32 nh_id, sai_object_id_t nh_oid)
{
    ctc_object_id_t nh;
    ctc_sai_get_ctc_object_id(SAI_API_NEXT_HOP, nh_oid, &nh);
    if (SAI_NEXT_HOP_TYPE_IP == nh.sub_type)
    {
        ctcs_nh_remove_ipuc(lchip, nh_id);
    }
    else if (SAI_NEXT_HOP_TYPE_MPLS == nh.sub_type)
    {

    }
    ctcs_aps_destroy_aps_bridge_group(lchip, aps_group_id);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_group_create_member(sai_object_id_t *next_hop_group_member_id, sai_object_id_t switch_id,
                                                                    uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;
    ctc_sai_next_hop_grp_member_t* p_next_hop_member_info = NULL;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    ctc_object_id_t ctc_nh_grp_obj_id;
    sai_object_id_t nh_grp_obj_id = 0;
    sai_object_id_t nh_obj_id = 0;
    sai_object_id_t nh_grp_member_obj_id = 0;
    uint32 nh_id = 0;/*member nexthop id*/
    uint32 nh_member_id = 0;
    uint8 lchip = 0;
    uint16 aps_group_id = 0 ;
    uint8 is_working = 0;
    sai_object_id_t w_nh_oid = 0;
    sai_object_id_t p_nh_oid = 0;


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
    ctc_sai_oid_get_nexthop_id(nh_obj_id, &nh_id);
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
    else
    {
        aps_group_id = ctc_nh_grp_obj_id.value2;
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
            goto error2;
        }
        w_nh_oid = p_next_hop_grp_info->w_nh_oid;
        p_nh_oid = p_next_hop_grp_info->p_nh_oid;
        if (SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY == attr_value->s32)
        {
            w_nh_oid = nh_obj_id;
            is_working = 1;
        }
        else
        {
            p_nh_oid = nh_obj_id;
        }
        if (w_nh_oid && p_nh_oid)/* w and p are all collected, create hw*/
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_group_create_aps_nh(lchip, aps_group_id, ctc_nh_grp_obj_id.value,
                                                                     w_nh_oid, p_nh_oid), status, error2);
        }
        p_next_hop_grp_info->w_nh_oid = w_nh_oid;
        p_next_hop_grp_info->p_nh_oid = p_nh_oid;
    }

    nh_grp_member_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP_MEMBER, lchip, is_working, nh_member_id, nh_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, nh_grp_member_obj_id, (void*)p_next_hop_member_info), status, error3);
    *next_hop_group_member_id = nh_grp_member_obj_id;
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
    else if (w_nh_oid && p_nh_oid)
    {
        _ctc_sai_next_hop_group_remove_aps_nh(lchip, aps_group_id, ctc_nh_grp_obj_id.value, w_nh_oid);
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
    sai_object_id_t nh_oid_old;

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
    else
    {
        if (1 == ctc_nh_grp_member_oid.sub_type)/*working path*/
        {
        nh_oid_old = p_next_hop_grp_info->w_nh_oid;
            p_next_hop_grp_info->w_nh_oid = 0;
        }
        else
        {
            nh_oid_old = p_next_hop_grp_info->p_nh_oid;
            p_next_hop_grp_info->p_nh_oid = 0;
        }
        if (0 == (p_next_hop_grp_info->w_nh_oid + p_next_hop_grp_info->p_nh_oid))
        {
             _ctc_sai_next_hop_group_remove_aps_nh(lchip, ctc_nh_grp_oid.value2, ctc_nh_grp_oid.value, nh_oid_old);
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
            return SAI_STATUS_NOT_SUPPORTED;
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
                    attr->value.objlist.list[attr->value.objlist.count++] = p_next_hop_grp_info->w_nh_oid;
                }
                if (p_next_hop_grp_info->p_nh_oid != 0)
                {
                    attr->value.objlist.list[attr->value.objlist.count++] = p_next_hop_grp_info->p_nh_oid;
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
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, next_hop_group_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_object_id.value));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_APS, ctc_object_id.value2));
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
            CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_create(counter_oid, CTC_SAI_COUNTER_TYPE_ECMP, &stats_id));
            nh_param.stats_id = stats_id;
        }
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_ecmp(lchip, nh_id, &nh_param), status, error1);
        nh_param.upd_type = CTC_NH_ECMP_REMOVE_MEMBER;
        ctcs_nh_update_ecmp(lchip, nh_id, &nh_param);
    }
    else if (SAI_NEXT_HOP_GROUP_TYPE_PROTECTION == group_type)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_APS, &aps_group_id), status, error1);
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
        goto error2;
    }
    sal_memset(p_next_hop_grp_info, 0, sizeof(ctc_sai_next_hop_grp_t));
    p_next_hop_grp_info->counter_oid = counter_oid;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, nh_grp_obj_id, p_next_hop_grp_info), status, error3);
    *next_hop_group_id = nh_grp_obj_id;
    goto out;

error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP_GROUP, "rollback to error3\n");
    mem_free(p_next_hop_grp_info);
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
        ctcs_nh_remove_ipuc(lchip, ctc_object_id.value);
        ctcs_aps_destroy_aps_bridge_group(lchip, ctc_object_id.value2);
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
    CTC_SAI_DB_LOCK(lchip);
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_lchip(object_id[i], &lchip), status, out);
        object_statuses[i] = _ctc_sai_next_hop_group_remove_member(object_id[i]);
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

