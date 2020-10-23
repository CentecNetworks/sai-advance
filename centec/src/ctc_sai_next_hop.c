/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_tunnel.h"
#include "ctc_sai_counter.h"
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_qosmap.h"


/*sdk include file*/
#include "ctcs_api.h"


typedef struct  ctc_sai_next_hop_wb_s
{
    /*key*/
    sai_object_id_t oid;
    uint32 index;
    uint32 calc_key_len[0];
    /*data*/
    uint32_t label;
}ctc_sai_next_hop_wb_t;

static sai_status_t
_ctc_sai_next_hop_gen_mpls_push_para(ctc_mpls_nexthop_push_param_t* nh_param_push, ctc_sai_tunnel_t* p_tunnel, sai_u32_list_t* label, uint8 exp_domain)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    /*pipeline*/
    nh_param_push->push_label[0].ttl = (label->list[0])&0xFF;
    nh_param_push->push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
    nh_param_push->push_label[0].exp = ((label->list[0]) >> 9)&0x7;
    nh_param_push->push_label[0].label = ((label->list[0]) >> 12)&0xFFFFF;

    nh_param_push->label_num++;
    if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
    {
        nh_param_push->nh_com.opcode = CTC_MPLS_NH_PUSH_OP_L2VPN;

        if(p_tunnel->encap_cw_en)
        {
            nh_param_push->martini_encap_valid = TRUE;
            nh_param_push->martini_encap_type = 1;
        }
        if(SAI_TUNNEL_MPLS_PW_MODE_TAGGED == p_tunnel->encap_pw_mode)
        {
            nh_param_push->nh_com.vlan_info.cvlan_edit_type = 1;
            nh_param_push->nh_com.vlan_info.svlan_edit_type = 3;
            nh_param_push->nh_com.vlan_info.output_svid = p_tunnel->encap_tagged_vlan;
            nh_param_push->nh_com.vlan_info.output_cvid = 1;
            CTC_SET_FLAG(nh_param_push->nh_com.vlan_info.edit_flag, CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID);
        }
        else if(SAI_TUNNEL_MPLS_PW_MODE_RAW == p_tunnel->encap_pw_mode)
        {
            nh_param_push->nh_com.vlan_info.cvlan_edit_type = 1;
            nh_param_push->nh_com.vlan_info.svlan_edit_type = 4;
            nh_param_push->nh_com.vlan_info.output_svid = 1;
            nh_param_push->nh_com.vlan_info.output_cvid = 1;
            CTC_UNSET_FLAG(nh_param_push->nh_com.vlan_info.edit_flag, CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID);
        }
        nh_param_push->eslb_en= p_tunnel->encap_esi_label_valid;

        if(SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL == p_tunnel->encap_exp_mode)
        {
            nh_param_push->push_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
            nh_param_push->push_label[0].exp_domain = exp_domain;
        }
        else if(SAI_TUNNEL_EXP_MODE_PIPE_MODEL == p_tunnel->encap_exp_mode)
        {
            nh_param_push->push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_param_push->push_label[0].exp = p_tunnel->encap_exp_val;
        }

        
    }
    else
    {
        nh_param_push->nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
        /*ttl and exp process needed here*/
        if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
        {
            if(SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL == p_tunnel->encap_ttl_mode)
            {
                nh_param_push->push_label[0].ttl = 0;
                CTC_SET_FLAG(nh_param_push->push_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
                CTC_SET_FLAG(nh_param_push->push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            }
            else if(SAI_TUNNEL_TTL_MODE_PIPE_MODEL == p_tunnel->encap_ttl_mode)
            {
                nh_param_push->push_label[0].ttl = p_tunnel->encap_ttl_val;
                CTC_UNSET_FLAG(nh_param_push->push_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
                CTC_SET_FLAG(nh_param_push->push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            }
            if(SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL == p_tunnel->encap_exp_mode)
            {
                nh_param_push->push_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
                nh_param_push->push_label[0].exp_domain = exp_domain;
            }
            else if(SAI_TUNNEL_EXP_MODE_PIPE_MODEL == p_tunnel->encap_exp_mode)
            {
                nh_param_push->push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
                nh_param_push->push_label[0].exp = p_tunnel->encap_exp_val;
            }
        }
    }
    return status;
}

static sai_status_t
_ctc_sai_next_hop_add_mpls(uint8 lchip, uint32 nh_id, sai_u32_list_t label, ctc_sai_next_hop_t* p_next_hop_info)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_tunnel_id = 0, stats_id = 0;
    uint16 arp_id;
    uint32 gport = 0;
    uint16 vlan = 0;
    sai_mac_t mac = {0};
    ctc_mpls_nexthop_tunnel_param_t nh_tunnel_param;
    ctc_mpls_nexthop_tunnel_param_t next_level_nh_tunnel_param;
    ctc_mpls_nexthop_param_t nh_mpls_param;
    uint8 chip_type = 0, num = 0;
    ctc_sai_next_hop_t* p_next_hop_info_next_level = NULL;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info_next_level = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t next_hop_obj_id;
    uint8 set_exp_domain = 0;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    uint8 adjust_length = 0,is_l2vpn;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    sal_memset(&nh_tunnel_param, 0, sizeof(nh_tunnel_param));
    sal_memset(&next_level_nh_tunnel_param, 0, sizeof(next_level_nh_tunnel_param));
    sal_memset(&nh_mpls_param, 0, sizeof(nh_mpls_param));
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));

    chip_type = ctcs_get_chip_type(lchip);
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        neighbor_entry.rif_id = p_next_hop_info->rif_id;
        sal_memcpy(&neighbor_entry.ip_address, &(p_next_hop_info->ip_address), sizeof(sai_ip_address_t));
        p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
        if (NULL == p_neighbor_info)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_get_arp_id(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), &arp_id));
        CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_get_outgoing_param(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), &gport, mac));
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(p_next_hop_info->rif_id, NULL, NULL,  NULL, &vlan));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, &ctc_tunnel_id));
    }
    else
    {
        p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
        if (NULL == p_tunnel)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_next_hop_info->next_level_nexthop_id, &ctc_object_id);
        if(SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
        {
            if(SAI_NEXT_HOP_GROUP_TYPE_PROTECTION != ctc_object_id.sub_type)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                goto error1;
            }

            p_next_hop_grp_info_next_level = ctc_sai_db_get_object_property(lchip, p_next_hop_info->next_level_nexthop_id);
            if (NULL == p_next_hop_grp_info_next_level)
            {
                return SAI_STATUS_INVALID_OBJECT_ID;
            }
            if( CTC_NH_APS_TYPE_TUNNEL != p_next_hop_grp_info_next_level->aps_nh_type)
            {
                status = SAI_STATUS_INVALID_OBJECT_ID;
                goto error1;
            }
            adjust_length += 4; // not accurate value
        }
        else
        {
            p_next_hop_info_next_level = ctc_sai_db_get_object_property(lchip, p_next_hop_info->next_level_nexthop_id);
            if(NULL == p_next_hop_info_next_level)
            {
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error1;
            }
            if(0 == p_next_hop_info_next_level->ctc_mpls_tunnel_id)
            {
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error1;
            }
            adjust_length += p_next_hop_info_next_level->label.count << 2;
        }
    }

    //qos map process
    if(p_next_hop_info->tc_color_to_exp_map_id)
    {
        if(p_next_hop_info->tunnel_id)
        {
            next_hop_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP, lchip, SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP, 0, nh_id);
        }
        else
        {
            next_hop_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP, lchip, SAI_NEXT_HOP_TYPE_MPLS, 0, nh_id);
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_mpls_nh_set_map(next_hop_obj_id, p_next_hop_info->tc_color_to_exp_map_id,
            SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP, 1, &set_exp_domain));
    }
    if(0 < label.count)
    {
        p_next_hop_info->label.list = mem_malloc(MEM_NEXTHOP_MODULE, sizeof(uint32_t)*label.count);
        if (NULL == p_next_hop_info->label.list)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto error1;
        }
    }
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        if ((chip_type == CTC_CHIP_GOLDENGATE)
            || (chip_type == CTC_CHIP_GREATBELT))
        {
            sal_memcpy(nh_tunnel_param.nh_param.mac, mac, sizeof(sai_mac_t));
            nh_tunnel_param.nh_param.oif.gport = gport;
            nh_tunnel_param.nh_param.oif.vid = vlan;
        }
        else
        {
            nh_tunnel_param.nh_param.arp_id = arp_id;
        }
        if (0 == label.count)
        {
            if(SAI_OUTSEG_TYPE_PHP == p_next_hop_info->outseg_type)
            {
                nh_mpls_param.nh_prop = CTC_MPLS_NH_POP_TYPE;
                nh_mpls_param.nh_para.nh_param_pop.nh_com.opcode = CTC_MPLS_NH_PHP;
                nh_mpls_param.nh_para.nh_param_pop.arp_id = arp_id;
                if(SAI_OUTSEG_TTL_MODE_UNIFORM == p_next_hop_info->outseg_ttl_mode)
                {
                    nh_mpls_param.nh_para.nh_param_pop.ttl_mode = CTC_MPLS_TUNNEL_MODE_UNIFORM;
                }
                else if(SAI_OUTSEG_TTL_MODE_PIPE == p_next_hop_info->outseg_ttl_mode)
                {
                    nh_mpls_param.nh_para.nh_param_pop.ttl_mode = CTC_MPLS_TUNNEL_MODE_SHORT_PIPE;
                }
                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, nh_id, &nh_mpls_param), status, error2);
                return SAI_STATUS_SUCCESS;
            }
        }
    }
    else
    {
        if(0 == label.count)
        {
            goto error3;
        }
    }
    adjust_length += label.count << 2;
    if (1 == label.count)
    {
        if(0 == p_next_hop_info->next_level_nexthop_id)
        {
            /*lsp*/
            nh_tunnel_param.nh_param.tunnel_label[0].label = ((label.list[0]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            nh_tunnel_param.nh_param.label_num++;
            if(SAI_OUTSEG_TTL_MODE_UNIFORM == p_next_hop_info->outseg_ttl_mode)
            {
                if(SAI_OUTSEG_TYPE_PUSH == p_next_hop_info->outseg_type)
                {
                    nh_tunnel_param.nh_param.tunnel_label[0].ttl = 0;
                }
                else if(SAI_OUTSEG_TYPE_SWAP == p_next_hop_info->outseg_type)
                {
                    nh_tunnel_param.nh_param.tunnel_label[0].ttl = 1;
                }

                CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            }
            else if(SAI_OUTSEG_TTL_MODE_PIPE == p_next_hop_info->outseg_ttl_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[0].ttl = (label.list[0])&0xFF;
                CTC_UNSET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            }
            if(SAI_OUTSEG_EXP_MODE_UNIFORM == p_next_hop_info->outseg_exp_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
                nh_tunnel_param.nh_param.tunnel_label[0].exp = 0;
                nh_tunnel_param.nh_param.tunnel_label[0].exp_domain = set_exp_domain;
            }
            else if(SAI_OUTSEG_EXP_MODE_PIPE == p_next_hop_info->outseg_exp_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
                nh_tunnel_param.nh_param.tunnel_label[0].exp = ((label.list[0]) >> 9)&0x7;
            }
        }
        else
        {
            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
            {
                nh_mpls_param.logic_port_valid = 1;
                nh_mpls_param.logic_port = p_tunnel->logic_port;
                is_l2vpn = 1;
            }
            _ctc_sai_next_hop_gen_mpls_push_para(&nh_mpls_param.nh_para.nh_param_push,p_tunnel,&label, set_exp_domain);
        }

        if(SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id)
        {
            if(0 == p_next_hop_info->next_level_nexthop_id)
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP, &stats_id), status, error3);
                nh_tunnel_param.nh_param.stats_valid = 1;
                nh_tunnel_param.nh_param.stats_id = stats_id;
            }
            else
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW, &stats_id), status, error3);
                nh_mpls_param.nh_para.nh_param_push.stats_valid = 1;
                nh_mpls_param.nh_para.nh_param_push.stats_id = stats_id;
            }
        }
    }
    else if(2 == label.count)
    {
        /*lsp*/
        nh_tunnel_param.nh_param.tunnel_label[0].label = ((label.list[1]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        /*spme*/
        nh_tunnel_param.nh_param.label_num++;
        nh_tunnel_param.nh_param.tunnel_label[1].label = ((label.list[0]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[1].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        nh_tunnel_param.nh_param.label_num++;
        if(SAI_OUTSEG_TTL_MODE_UNIFORM == p_next_hop_info->outseg_ttl_mode)
        {
            if(SAI_OUTSEG_TYPE_PUSH == p_next_hop_info->outseg_type)
            {
                nh_tunnel_param.nh_param.tunnel_label[0].ttl = 0;
                nh_tunnel_param.nh_param.tunnel_label[1].ttl = 0;
            }
            else if(SAI_OUTSEG_TYPE_SWAP == p_next_hop_info->outseg_type)
            {
                nh_tunnel_param.nh_param.tunnel_label[0].ttl = 1;
                nh_tunnel_param.nh_param.tunnel_label[1].ttl = 1;
            }
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[1].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
        }
        else if(SAI_OUTSEG_TTL_MODE_PIPE == p_next_hop_info->outseg_ttl_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].ttl = (label.list[1])&0xFF;
            CTC_UNSET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            nh_tunnel_param.nh_param.tunnel_label[1].ttl = (label.list[0])&0xFF;
            CTC_UNSET_FLAG(nh_tunnel_param.nh_param.tunnel_label[1].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
        }
        if(SAI_OUTSEG_EXP_MODE_UNIFORM == p_next_hop_info->outseg_exp_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
            nh_tunnel_param.nh_param.tunnel_label[0].exp = 0;
            nh_tunnel_param.nh_param.tunnel_label[0].exp_domain = set_exp_domain;
            nh_tunnel_param.nh_param.tunnel_label[1].exp_type = CTC_NH_EXP_SELECT_MAP;
            nh_tunnel_param.nh_param.tunnel_label[1].exp = 0;
            nh_tunnel_param.nh_param.tunnel_label[1].exp_domain = set_exp_domain;
        }
        else if(SAI_OUTSEG_EXP_MODE_PIPE == p_next_hop_info->outseg_exp_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[0].exp = ((label.list[1]) >> 9)&0x7;
            nh_tunnel_param.nh_param.tunnel_label[1].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[1].exp = ((label.list[0]) >> 9)&0x7;
        }

        if((2 == label.count) && (SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id))
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP, &stats_id), status, error3);
            nh_tunnel_param.nh_param.stats_valid = 1;
            nh_tunnel_param.nh_param.stats_id = stats_id;
        }
    }
    else if((3 <= label.count) && (10 >= label.count) && (CTC_CHIP_TSINGMA <= ctcs_get_chip_type(lchip)))
    {
        nh_tunnel_param.nh_param.is_sr = 1;
        for(num = 0;num < label.count;num++)
        {
            nh_tunnel_param.nh_param.tunnel_label[num].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[num].exp = ((label.list[num]) >> 9)&0x7;
            nh_tunnel_param.nh_param.tunnel_label[num].label = ((label.list[num]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[num].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            nh_tunnel_param.nh_param.label_num++;
            if(SAI_OUTSEG_TTL_MODE_UNIFORM == p_next_hop_info->outseg_ttl_mode)
            {
                if(SAI_OUTSEG_TYPE_PUSH == p_next_hop_info->outseg_type)
                {
                    nh_tunnel_param.nh_param.tunnel_label[num].ttl = 0;
                }
                else if(SAI_OUTSEG_TYPE_SWAP == p_next_hop_info->outseg_type)
                {
                    nh_tunnel_param.nh_param.tunnel_label[num].ttl = 1;
                }
                CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[num].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            }
            else if(SAI_OUTSEG_TTL_MODE_PIPE == p_next_hop_info->outseg_ttl_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[num].ttl = (label.list[num])&0xFF;
                CTC_UNSET_FLAG(nh_tunnel_param.nh_param.tunnel_label[num].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
            }
            if(SAI_OUTSEG_EXP_MODE_UNIFORM == p_next_hop_info->outseg_exp_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[num].exp_type = CTC_NH_EXP_SELECT_MAP;
                nh_tunnel_param.nh_param.tunnel_label[num].exp = 0;
                nh_tunnel_param.nh_param.tunnel_label[num].exp_domain = set_exp_domain;
            }
            else if(SAI_OUTSEG_EXP_MODE_PIPE == p_next_hop_info->outseg_exp_mode)
            {
                nh_tunnel_param.nh_param.tunnel_label[num].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
                nh_tunnel_param.nh_param.tunnel_label[num].exp = ((label.list[num]) >> 9)&0x7;
            }
        }
    }

    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls_tunnel_label(lchip, ctc_tunnel_id, &nh_tunnel_param), status, error2);
        p_neighbor_info->ref_cnt++;
    }

    if (3 == label.count && (CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
    {
        nh_mpls_param.nh_para.nh_param_push.push_label[0].label = ((label.list[2]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_mpls_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        nh_mpls_param.nh_para.nh_param_push.label_num++;
        if(SAI_OUTSEG_TTL_MODE_UNIFORM == p_next_hop_info->outseg_ttl_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].ttl = 0;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
        }
        else if(SAI_OUTSEG_TTL_MODE_PIPE == p_next_hop_info->outseg_ttl_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].ttl = (label.list[2])&0xFF;
            CTC_UNSET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
        }
        if(SAI_OUTSEG_EXP_MODE_UNIFORM == p_next_hop_info->outseg_exp_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
            nh_tunnel_param.nh_param.tunnel_label[0].exp = 0;
            nh_tunnel_param.nh_param.tunnel_label[0].exp_domain = set_exp_domain;
        }
        else if(SAI_OUTSEG_EXP_MODE_PIPE == p_next_hop_info->outseg_exp_mode)
        {
            nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[0].exp = ((label.list[2]) >> 9)&0x7;
        }
        if(SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id)
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW, &stats_id), status, error3);
            nh_mpls_param.nh_para.nh_param_push.stats_valid = 1;
            nh_mpls_param.nh_para.nh_param_push.stats_id = stats_id;
        }
    }

    nh_mpls_param.nh_prop = CTC_MPLS_NH_PUSH_TYPE;
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        if(SAI_OUTSEG_TYPE_PUSH == p_next_hop_info->outseg_type)
        {
            nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
        }
        else if(SAI_OUTSEG_TYPE_SWAP == p_next_hop_info->outseg_type)
        {
            nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_NONE;
        }
        nh_mpls_param.nh_para.nh_param_push.tunnel_id = ctc_tunnel_id;
    }
    else if(SAI_OBJECT_TYPE_NEXT_HOP_GROUP != ctc_object_id.type)
    {
        ctcs_nh_get_mpls_tunnel_label(lchip, p_next_hop_info_next_level->ctc_mpls_tunnel_id, &next_level_nh_tunnel_param);
        if(next_level_nh_tunnel_param.nh_param.is_sr)
        {
            nh_mpls_param.nh_para.nh_param_push.loop_nhid = ctc_object_id.value;
        }
        else
        {
            nh_mpls_param.nh_para.nh_param_push.tunnel_id = p_next_hop_info_next_level->ctc_mpls_tunnel_id;
        }
    }
    else if(SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
    {
        nh_mpls_param.nh_para.nh_param_push.tunnel_id = p_next_hop_grp_info_next_level->aps_tunnel_id;  //lsp aps tunnel id
    }
    nh_mpls_param.adjust_length = is_l2vpn ? adjust_length + 14 : adjust_length;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, nh_id, &nh_mpls_param), status, error4);
    p_next_hop_info->label.count = label.count;
    sal_memcpy(p_next_hop_info->label.list, label.list, sizeof(uint32_t)*label.count);
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        p_next_hop_info->ctc_mpls_tunnel_id = ctc_tunnel_id;
    }
    else if(SAI_OBJECT_TYPE_NEXT_HOP_GROUP != ctc_object_id.type)
    {
        p_next_hop_info_next_level->ref_cnt++;
    }
    else if(SAI_OBJECT_TYPE_NEXT_HOP_GROUP == ctc_object_id.type)
    {
        //TODO
    }

    return SAI_STATUS_SUCCESS;

error4:
    ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW);
error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error3\n");
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        ctcs_nh_remove_mpls_tunnel_label(lchip, ctc_tunnel_id);
    }
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error2\n");
    if (label.count)
    {
        mem_free(p_next_hop_info->label.list);
    }
error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error1\n");
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, ctc_tunnel_id);
    }
    return status;
}

static sai_status_t
_ctc_sai_next_hop_remove_mpls(uint8 lchip, uint32 nh_id, ctc_sai_next_hop_t* p_next_hop_info)
{
    ctc_sai_next_hop_t* p_next_hop_info_next_level = 0;
    sai_object_type_t obj_type = 0;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    
                
    if(0 != p_next_hop_info->next_level_nexthop_id)
    {
        ctc_sai_oid_get_type(p_next_hop_info->next_level_nexthop_id, &obj_type);
        if (SAI_OBJECT_TYPE_NEXT_HOP_GROUP != obj_type)
        {
            p_next_hop_info_next_level = ctc_sai_db_get_object_property(lchip, p_next_hop_info->next_level_nexthop_id);

            p_next_hop_info_next_level->ref_cnt--;
        }

        ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP);
        ctcs_nh_remove_mpls(lchip, nh_id);
        mem_free(p_next_hop_info->label.list);
    }
    else
    {
        neighbor_entry.rif_id = p_next_hop_info->rif_id;
        sal_memcpy(&neighbor_entry.ip_address, &(p_next_hop_info->ip_address), sizeof(sai_ip_address_t));
        p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
        if (NULL == p_neighbor_info)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        if(0 == p_next_hop_info->ref_cnt)
        {
            if(0 < p_next_hop_info->label.count)
            {
                ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP);
                ctcs_nh_remove_mpls(lchip, nh_id);
                mem_free(p_next_hop_info->label.list);
                ctcs_nh_remove_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id);
                p_neighbor_info->ref_cnt--;
                ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, p_next_hop_info->ctc_mpls_tunnel_id);
            }
            else
            {
                ctcs_nh_remove_mpls(lchip, nh_id);
            }
        }
        else
        {
            CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "nexthop in use by high level\n");
            return SAI_STATUS_OBJECT_IN_USE;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t/*only for gg*/
_ctc_sai_next_hop_update_mpls(uint8 lchip, uint32 nh_id, ctc_sai_next_hop_t* p_next_hop_info)
{
    uint32 gport = 0;
    uint16 vlan = 0;
    sai_mac_t mac ={0};
    ctc_mpls_nexthop_tunnel_param_t nh_tunnel_param;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_get_outgoing_param(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), &gport, mac));
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(p_next_hop_info->rif_id, NULL, NULL,  NULL, &vlan));

    sal_memset(&nh_tunnel_param,0,sizeof(nh_tunnel_param));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id,&nh_tunnel_param));
    sal_memcpy(nh_tunnel_param.nh_param.mac, mac, sizeof(sai_mac_t));
    nh_tunnel_param.nh_param.oif.gport = gport;
    nh_tunnel_param.nh_param.oif.vid = vlan;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id, &nh_tunnel_param));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_add_ip_tunnel(uint8 lchip, uint32 nh_id, ctc_sai_next_hop_t* p_next_hop_info)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_ip_tunnel_nh_param_t nh_param;
    uint32 stats_id = 0;

    sal_memset(&nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_tunnel_map_to_nh_ip_tunnel(lchip, p_next_hop_info->tunnel_id, nh_id, &p_next_hop_info->ip_address, &nh_param));
    if (p_next_hop_info->dest_vni)
    {
        CTC_SET_FLAG(nh_param.tunnel_info.flag, CTC_IP_NH_TUNNEL_FLAG_OVERLAY_CROSS_VNI);
        nh_param.tunnel_info.vn_id = p_next_hop_info->dest_vni;
        sal_memcpy(nh_param.tunnel_info.inner_macda, p_next_hop_info->tunnel_mac, sizeof(mac_addr_t));
    }
    if(SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_TUNNEL_EGS, &stats_id));
        nh_param.tunnel_info.stats_id = stats_id;
    }
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_ip_tunnel(lchip, nh_id, &nh_param), status, error0);

    return SAI_STATUS_SUCCESS;

error0:
    ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_TUNNEL_EGS);
    return status;
}

static sai_status_t
_ctc_sai_next_hop_remove_ip_tunnel(uint8 lchip, uint32 nh_id, ctc_sai_next_hop_t* p_next_hop_info)
{
    ctc_ip_tunnel_nh_param_t nh_param;

    sal_memset(&nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_TUNNEL_EGS));
    CTC_SAI_ERROR_RETURN(ctc_sai_tunnel_unmap_to_nh_ip_tunnel(lchip, p_next_hop_info->tunnel_id, nh_id));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_ip_tunnel(lchip, nh_id));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value = NULL;
    uint32_t index = 0;
    uint8 label_cnt = 0;
    ctc_sai_oid_property_t* p_oid_property = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;

    CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TYPE, &attr_value, &index), status, error);
    if (SAI_NEXT_HOP_TYPE_IP == attr_value->s32)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_IP, &attr_value, &index), status, error);
        CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, &attr_value, &index), status, error);
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_COUNTER_ID, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
    }
    else if(SAI_NEXT_HOP_TYPE_MPLS == attr_value->s32)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID, &attr_value, &index);
        if(SAI_STATUS_SUCCESS != status)
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_IP, &attr_value, &index), status, error);
            CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, &attr_value, &index), status, error);
        }
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_LABELSTACK, &attr_value, &index), status, error);
        if (attr_value->u32list.count > 10 || (attr_value->u32list.count > 3 && CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip)))
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        label_cnt = attr_value->u32list.count;
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_COUNTER_ID, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if (NULL == p_oid_property)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
        }
        /* MPLS L3VPN */
        ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);
            p_tunnel = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if(NULL != p_tunnel && SAI_TUNNEL_TYPE_MPLS !=p_tunnel->tunnel_type)
            {
                goto error;
            }
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_TYPE, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            if ((SAI_OUTSEG_TYPE_PHP < attr_value->s32)||((SAI_OUTSEG_TYPE_PHP == attr_value->s32) && label_cnt > 0)||((SAI_OUTSEG_TYPE_PHP != attr_value->s32) && label_cnt == 0))
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
        }
    }
    else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == attr_value->s32)
    {
        ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);
            p_tunnel = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if(NULL == p_tunnel || ((SAI_TUNNEL_TYPE_MPLS_L2 !=p_tunnel->tunnel_type) && (SAI_TUNNEL_TYPE_MPLS !=p_tunnel->tunnel_type)))
            {
                goto error;
            }
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_COUNTER_ID, &attr_value, &index);
        if(SAI_STATUS_SUCCESS == status)
        {
            p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if (NULL == p_oid_property)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
        }
    }
    else if((SAI_NEXT_HOP_TYPE_SEGMENTROUTE_SIDLIST == attr_value->s32)
        ||(SAI_NEXT_HOP_TYPE_SEGMENTROUTE_ENDPOINT == attr_value->s32))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
error:
    return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
}

static sai_status_t
_ctc_sai_next_hop_set_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value = NULL;
    uint32_t index = 0;
    uint8 i = 0;
    ctc_sai_oid_property_t* p_oid_property = NULL;
    uint32 attrib_id[4] =
    {
        SAI_NEXT_HOP_ATTR_TYPE,
        SAI_NEXT_HOP_ATTR_LABELSTACK,
        SAI_NEXT_HOP_ATTR_TUNNEL_ID,
        SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID
    };
    for (i = 0; i < 4; i++)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, attrib_id[i], &attr_value, &index));
        if (SAI_STATUS_SUCCESS == status)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_TYPE, &attr_value, &index));
    if (SAI_STATUS_SUCCESS == status)
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_POP_TYPE, &attr_value, &index));
    if (SAI_STATUS_SUCCESS == status)
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_COUNTER_ID, &attr_value, &index);
    if(SAI_STATUS_SUCCESS == status)
    {
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint8 rif_type;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_sai_neighbor_t* p_neighbor_info_old = NULL;
    ctc_ip_nh_param_t  nh_param;
    ctc_mpls_nexthop_tunnel_param_t mpls_tunnel_param;

    sal_memset(&nh_param, 0 , sizeof(ctc_ip_nh_param_t));
    sal_memset(&neighbor_entry, 0 , sizeof(sai_neighbor_entry_t));
    sal_memset(&mpls_tunnel_param, 0, sizeof(ctc_mpls_nexthop_tunnel_param_t));
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_next_hop_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_router_interface_get_rif_info(p_next_hop_info->rif_id, &rif_type, NULL, NULL, NULL);
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == rif_type)
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, key->key.object_id, &ctc_object_id);
    if (SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID == attr->id)
    {
        ctc_sai_router_interface_get_rif_info(attr->value.oid, &rif_type, NULL, NULL, NULL);
        if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == rif_type)
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }
        p_next_hop_info->rif_id_temp = attr->value.oid;
        return SAI_STATUS_FAILURE;
    }
    else if (SAI_NEXT_HOP_ATTR_IP == attr->id)
    {
        if (!sal_memcmp(&attr->value.ipaddr, &(p_next_hop_info->ip_address), sizeof(sai_ip_address_t)))
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }

        /*check old neighbor db*/
        neighbor_entry.rif_id = p_next_hop_info->rif_id;
        sal_memcpy(&neighbor_entry.ip_address, &(p_next_hop_info->ip_address), sizeof(sai_ip_address_t));
        p_neighbor_info_old = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
        if ((p_neighbor_info_old == NULL)||(0 == p_neighbor_info_old->neighbor_exists))
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        /*find new neighbor db*/
        neighbor_entry.rif_id = p_next_hop_info->rif_id_temp ? p_next_hop_info->rif_id_temp : p_next_hop_info->rif_id;
        sal_memcpy(&neighbor_entry.ip_address, &(attr->value.ipaddr), sizeof(sai_ip_address_t));
        p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
        if ((p_neighbor_info == NULL)||(0 == p_neighbor_info->neighbor_exists))
        {
            p_next_hop_info->rif_id_temp = 0;
            return SAI_STATUS_FAILURE;
        }

        /*only support ipuc nexthop and mpls tunnel nexthop*/
        if (SAI_NEXT_HOP_TYPE_IP == ctc_object_id.sub_type)
        {
            nh_param.arp_id = p_neighbor_info->arp_id;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_ipuc(lchip, ctc_object_id.value, &nh_param));
        }
        else if (SAI_NEXT_HOP_TYPE_MPLS == ctc_object_id.sub_type)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id, &mpls_tunnel_param));
            mpls_tunnel_param.nh_param.arp_id = p_neighbor_info->arp_id;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id, &mpls_tunnel_param));
        }
        else
        {
            return SAI_STATUS_NOT_SUPPORTED;
        }

        /*modify related db*/
        if (p_next_hop_info->rif_id_temp)
        {
            p_next_hop_info->rif_id = p_next_hop_info->rif_id_temp;
            p_next_hop_info->rif_id_temp = 0;
        }
        p_next_hop_info->ip_address = attr->value.ipaddr;
        p_neighbor_info->ref_cnt++;
        p_neighbor_info_old->ref_cnt--;
        
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_next_hop_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, key->key.object_id, &ctc_object_id);
    switch(attr->id)
    {
    case SAI_NEXT_HOP_ATTR_TYPE:
        attr->value.s32 = ctc_object_id.sub_type;
        break;
    case SAI_NEXT_HOP_ATTR_IP:
        sal_memcpy(&(attr->value.ipaddr), &(p_next_hop_info->ip_address), sizeof(sai_ip_address_t));
        break;
    case SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
        attr->value.oid = p_next_hop_info->rif_id;
        break;
    case SAI_NEXT_HOP_ATTR_TUNNEL_ID:
        attr->value.oid = p_next_hop_info->tunnel_id;
        break;
    case SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID:
        break;
    case SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_TYPE:
        break;
    case SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_POP_TYPE:
        break;
    case SAI_NEXT_HOP_ATTR_LABELSTACK:
        attr->value.u32list.count = p_next_hop_info->label.count;
        CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(uint32_t), p_next_hop_info->label.list, p_next_hop_info->label.count, &attr->value.u32list));
        break;
    case SAI_NEXT_HOP_ATTR_COUNTER_ID:
        attr->value.oid = p_next_hop_info->counter_obj_id;
        break;
    case SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID:
        attr->value.oid = p_next_hop_info->tunnel_id;
        break;
    case SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID:
        attr->value.oid = p_next_hop_info->next_level_nexthop_id;
        break;
    case SAI_NEXT_HOP_ATTR_OUTSEG_TYPE:
        attr->value.s32 = p_next_hop_info->outseg_type;
        break;
    case SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE:
        attr->value.s32 = p_next_hop_info->outseg_ttl_mode;
        break;
    case SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE:
        attr->value.u8 = p_next_hop_info->outseg_ttl_val;
        break;
    case SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE:
        attr->value.s32 = p_next_hop_info->outseg_exp_mode;
        break;
    case SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE:
        attr->value.u8 = p_next_hop_info->outseg_exp_val;
        break;
    case SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP:
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, p_next_hop_info->tc_color_to_exp_map_id);;
        break;
    default:
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    ctc_object_id_t ctc_object_id;
    uint32 num_cnt = 0;
    char nh_oid[64] = {'-'};
    char* type = "-";

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(nh_oid, "0x%016"PRIx64, bucket_data->oid);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, bucket_data->oid, &ctc_object_id);
    if (SAI_NEXT_HOP_TYPE_IP == ctc_object_id.sub_type)
    {
        type = "IP";
    }
    else if (SAI_NEXT_HOP_TYPE_MPLS == ctc_object_id.sub_type)
    {
        type = "MPLS";
    }
    else if (SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == ctc_object_id.sub_type)
    {
        type = "TUNNEL_ENCAP";
    }
    else if (SAI_NEXT_HOP_TYPE_SEGMENTROUTE_SIDLIST == ctc_object_id.sub_type)
    {
        type = "SEGMENTROUTE_SIDLIST";
    }
    else if (SAI_NEXT_HOP_TYPE_SEGMENTROUTE_ENDPOINT == ctc_object_id.sub_type)
    {
        type = "SEGMENTROUTE_ENDPOINT";
    }

    CTC_SAI_LOG_DUMP(p_file, "%-8d%-24s%-26s%-10d\n", num_cnt, nh_oid, type, ctc_object_id.value);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}


static  ctc_sai_attr_fn_entry_t next_hop_attr_fn_entries[] = {
    { SAI_NEXT_HOP_ATTR_TYPE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_IP,
      _ctc_sai_next_hop_get_attr,
      _ctc_sai_next_hop_set_attr},
    { SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID,
      _ctc_sai_next_hop_get_attr,
      _ctc_sai_next_hop_set_attr},
    { SAI_NEXT_HOP_ATTR_TUNNEL_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_TYPE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_SEGMENTROUTE_ENDPOINT_POP_TYPE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_LABELSTACK,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_COUNTER_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_OUTSEG_TYPE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE,
      _ctc_sai_next_hop_get_attr,
      NULL},
    { SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP,
      _ctc_sai_next_hop_get_attr,
      NULL},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

#define ________INTERNAL_API________
sai_status_t
ctc_sai_next_hop_get_arp_id(sai_object_id_t next_hop_id, uint16* arp_id)
{
    uint8 lchip = 0;
    ctc_sai_next_hop_t* p_next_hop_info = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_id, &lchip));
    p_next_hop_info = ctc_sai_db_get_object_property(lchip, next_hop_id);
    if (NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_get_arp_id(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), arp_id));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_next_hop_update_by_neighbor(sai_object_id_t next_hop_id, sai_object_id_t rif_id, sai_ip_address_t ip_address)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = 0;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, next_hop_id, &ctc_object_id);
    if (SAI_NEXT_HOP_TYPE_IP == ctc_object_id.sub_type)
    {
        return SAI_STATUS_SUCCESS;
    }
    p_next_hop_info = ctc_sai_db_get_object_property(ctc_object_id.lchip, next_hop_id);
    if(NULL == p_next_hop_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (SAI_NEXT_HOP_TYPE_MPLS == ctc_object_id.sub_type)
    {
       CTC_SAI_ERROR_RETURN(_ctc_sai_next_hop_update_mpls(ctc_object_id.lchip, ctc_object_id.value, p_next_hop_info));
    }
    else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == ctc_object_id.sub_type)
    {

    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_cmp_ip_tunnel_info(ctc_sai_oid_property_t* bucket_data, ctc_sai_next_hop_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_next_hop_t* p_ctc_sai_nh = (ctc_sai_next_hop_t*)(bucket_data->data);

    if ((p_ctc_sai_nh->tunnel_id == user_data->tunnel_id)
        && (p_ctc_sai_nh->ip_address.addr_family == user_data->ip_address.addr_family))
    {
        if (((SAI_IP_ADDR_FAMILY_IPV4 == p_ctc_sai_nh->ip_address.addr_family) && (0 == sal_memcmp(&p_ctc_sai_nh->ip_address.addr.ip4, &user_data->ip_address.addr.ip4, sizeof(sai_ip4_t))))
            || ((SAI_IP_ADDR_FAMILY_IPV6 == p_ctc_sai_nh->ip_address.addr_family) && (0 == sal_memcmp(&p_ctc_sai_nh->ip_address.addr.ip6, &user_data->ip_address.addr.ip6, sizeof(sai_ip6_t)))))
        {
            /*get nexthop oid*/
            user_data->rif_id = bucket_data->oid;
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_next_hop_cmp_mpls_tunnel_info(ctc_sai_oid_property_t* bucket_data, ctc_sai_next_hop_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_next_hop_t* p_ctc_sai_nh = (ctc_sai_next_hop_t*)(bucket_data->data);

    if (p_ctc_sai_nh->tunnel_id == user_data->tunnel_id)
    {
        user_data->rif_id = bucket_data->oid;
    }

    return status;
}

sai_status_t
ctc_sai_next_hop_get_tunnel_nh(sai_object_id_t tunnel_id, const sai_ip_address_t* ip_addr, uint32* tunnel_nh_id)
{
    ctc_sai_next_hop_t ctc_sai_nh;
    ctc_object_id_t ctc_oid;
    uint8 lchip = 0;
    ctc_sai_tunnel_t* p_tunnel = NULL;

    sal_memset(&ctc_sai_nh, 0, sizeof(ctc_sai_next_hop_t));
    sal_memset(&ctc_oid, 0, sizeof(ctc_object_id_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(tunnel_id, &lchip));
    ctc_sai_nh.tunnel_id = tunnel_id;
    sal_memcpy(&ctc_sai_nh.ip_address, ip_addr, sizeof(sai_ip_address_t));

    p_tunnel = ctc_sai_db_get_object_property(lchip, tunnel_id);

    if(SAI_TUNNEL_TYPE_IPINIP == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_IPINIP_GRE == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_VXLAN == p_tunnel->tunnel_type)
    {
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP,
                                                         (hash_traversal_fn)_ctc_sai_next_hop_cmp_ip_tunnel_info, (void*)(&ctc_sai_nh));
        if (0 != ctc_sai_nh.rif_id)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, ctc_sai_nh.rif_id, &ctc_oid);
            *tunnel_nh_id = ctc_oid.value;
        }
        else
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }
    else if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
    {
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP,
                                                         (hash_traversal_fn)_ctc_sai_next_hop_cmp_mpls_tunnel_info, (void*)(&ctc_sai_nh));
        if (0 != ctc_sai_nh.rif_id)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, ctc_sai_nh.rif_id, &ctc_oid);
            *tunnel_nh_id = ctc_oid.value;
        }
        else
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t next_hop_id = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_next_hop_t* p_next_hop_info = (ctc_sai_next_hop_t*)data;
    ctc_sai_next_hop_wb_t next_hop_wb;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_next_hop_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NEXT_HOP);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    for (index = 0; index < p_next_hop_info->label.count; index++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        next_hop_wb.oid = next_hop_id;
        next_hop_wb.index = index;
        sal_memcpy(&next_hop_wb.label, &(p_next_hop_info->label.list[index]), sizeof(uint32_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &next_hop_wb, (wb_data.key_len + wb_data.data_len));
        if (++wb_data.valid_cnt == max_entry_cnt)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
            wb_data.valid_cnt = 0;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }


done:
out:
    CTC_WB_FREE_BUFFER(wb_data.buffer);

    return status;
}

static sai_status_t
_ctc_sai_next_hop_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_object_id_t next_hop_id = *(sai_object_id_t*)key;
    ctc_sai_next_hop_t* p_next_hop_info = (ctc_sai_next_hop_t*)data;
    ctc_object_id_t ctc_oid;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, next_hop_id, &ctc_oid);
    if (SAI_NEXT_HOP_TYPE_IP == ctc_oid.sub_type)
    {
        return SAI_STATUS_SUCCESS;
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_oid.value));
        if (SAI_NEXT_HOP_TYPE_MPLS == ctc_oid.sub_type)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, p_next_hop_info->ctc_mpls_tunnel_id));
            p_next_hop_info->label.list = (uint32_t*)mem_malloc(MEM_QUEUE_MODULE, p_next_hop_info->label.count * sizeof(uint32_t));
            if (NULL == p_next_hop_info->label.list)
            {
                return SAI_STATUS_NO_MEMORY;
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_next_hop_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    ctc_sai_next_hop_wb_t next_hop_wb;
    ctc_wb_query_t wb_query;
    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_next_hop_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NEXT_HOP);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
    offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
    entry_cnt++;
    sal_memcpy(&next_hop_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_next_hop_wb_t));
    p_next_hop_info = ctc_sai_db_get_object_property(lchip, next_hop_wb.oid);
    if ((NULL == p_next_hop_info) || (NULL == p_next_hop_info->label.list))
    {
        continue;
    }

    sal_memcpy(&(p_next_hop_info->label.list[next_hop_wb.index]), &next_hop_wb.label,  sizeof(uint32_t));
    CTC_WB_QUERY_ENTRY_END((&wb_query));
done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
    return ret;
}

void ctc_sai_next_hop_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Next Hop MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_NEXT_HOP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Next Hop");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-24s%-26s%-10s\n", "No.", "next_hop_id", "type", "nh_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_NEXT_HOP,
                                            (hash_traversal_fn)_ctc_sai_next_hop_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
static sai_status_t
ctc_sai_next_hop_create_nh(sai_object_id_t *next_hop_id, sai_object_id_t switch_id,
                                                       uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value = NULL;
    uint32_t index = 0;
    uint32 nh_id = 0;
    sai_object_id_t next_hop_obj_id = 0;
    uint8 next_hop_type = 0;
    ctc_sai_next_hop_t* p_next_hop_info = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
	ctc_sai_tunnel_t* p_tunnel = NULL;
    ctc_sai_qos_map_db_t* p_map_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    CTC_SAI_PTR_VALID_CHECK(next_hop_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_create_attr_check(lchip, attr_count, attr_list), status, out);

    p_next_hop_info = mem_malloc(MEM_NEXTHOP_MODULE, sizeof(ctc_sai_next_hop_t));
    if (NULL == p_next_hop_info)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto out;
    }
    sal_memset(p_next_hop_info, 0, sizeof(ctc_sai_next_hop_t));
    p_next_hop_info->outseg_type = SAI_OUTSEG_TYPE_SWAP;

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_IP, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&(p_next_hop_info->ip_address), &(attr_value->ipaddr), sizeof(sai_ip_address_t));
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_next_hop_info->rif_id = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_COUNTER_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_next_hop_info->counter_obj_id = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TYPE, &attr_value, &index);
    next_hop_type = attr_value->s32;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id), status, error1);
    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_alloc_ipuc_nexthop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), nh_id), status, error1);
    }
    else
    {
        if(SAI_NEXT_HOP_TYPE_MPLS == next_hop_type)
        {
            /*
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);

            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->tunnel_id = attr_value->oid;
                p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
            }
            if (NULL == p_tunnel)
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);

                if (!CTC_SAI_ERROR(status))
                {
                    p_next_hop_info->tunnel_id = attr_value->oid;
                    p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
                    if(NULL != p_tunnel && SAI_TUNNEL_TYPE_MPLS !=p_tunnel->tunnel_type)
                    {
                        status = SAI_STATUS_INVALID_OBJECT_ID;
                        goto error1;
                    }
                }
            }
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->next_level_nexthop_id = attr_value->oid;
            }
            */
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_TYPE, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->outseg_type = attr_value->s32;
            }

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_TTL_MODE, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->outseg_ttl_mode = attr_value->s32;
                if(SAI_OUTSEG_TTL_MODE_PIPE == attr_value->s32)
                {
                    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_TTL_VALUE, &attr_value, &index);
                    if (!CTC_SAI_ERROR(status))
                    {
                        p_next_hop_info->outseg_ttl_val = attr_value->u8;
                    }
                }
            }

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_EXP_MODE, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->outseg_exp_mode = attr_value->s32;
                if(SAI_OUTSEG_EXP_MODE_PIPE == attr_value->s32)
                {
                    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_OUTSEG_EXP_VALUE, &attr_value, &index);
                    if (!CTC_SAI_ERROR(status))
                    {
                        p_next_hop_info->outseg_exp_val = attr_value->u8;
                    }
                }
            }

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                if(SAI_OUTSEG_EXP_MODE_UNIFORM == p_next_hop_info->outseg_exp_mode)
                {
                    ctc_sai_oid_get_value(attr_value->oid, (uint32*)&p_next_hop_info->tc_color_to_exp_map_id);
                    p_map_db = ctc_sai_db_get_object_property(lchip, attr_value->oid);
                    if (NULL == p_map_db)
                    {
                        CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "qos map db not found\n");
                        status = SAI_STATUS_INVALID_OBJECT_ID;
                        goto error2;
                    }
                }
                else
                {
                    status = SAI_STATUS_INVALID_PARAMETER;
                    goto error2;
                }
            }

            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_LABELSTACK, &attr_value, &index);
            if((3<=attr_value->u32list.count)&&(SAI_OUTSEG_TTL_MODE_PIPE!=p_next_hop_info->outseg_ttl_mode))
            {
                status = SAI_STATUS_NOT_SUPPORTED;
                goto error2;
            }
            CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_add_mpls(lchip, nh_id, attr_value->u32list, p_next_hop_info), status, error2);
        }
        else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == next_hop_type)
        {
            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);
            /*tunnel type*/
            p_next_hop_info->tunnel_id = attr_value->oid;
            p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
            if (NULL == p_tunnel)
            {
                ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);
                /*tunnel type*/
                p_next_hop_info->tunnel_id = attr_value->oid;
                p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
                if(NULL == p_tunnel || (SAI_TUNNEL_TYPE_MPLS_L2 !=p_tunnel->tunnel_type && SAI_TUNNEL_TYPE_MPLS !=p_tunnel->tunnel_type))
                {
                    status = SAI_STATUS_INVALID_OBJECT_ID;
                    goto error2;
                }
            }

            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID, &attr_value, &index);
                if (!CTC_SAI_ERROR(status))
                {
                    p_next_hop_info->next_level_nexthop_id = attr_value->oid;
                }

                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_QOS_TC_AND_COLOR_TO_MPLS_EXP_MAP, &attr_value, &index);
                if (!CTC_SAI_ERROR(status))
                {
                    //Note: here use tunnel configure, TBD
                    if(SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL == p_tunnel->encap_exp_mode)
                    {
                        ctc_sai_oid_get_value(attr_value->oid, (uint32*)&p_next_hop_info->tc_color_to_exp_map_id);
                        p_map_db = ctc_sai_db_get_object_property(lchip, attr_value->oid);
                        if (NULL == p_map_db)
                        {
                            CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "qos map db not found\n");
                            return SAI_STATUS_INVALID_OBJECT_ID;
                        }
                    }
                    else
                    {
                        status = SAI_STATUS_INVALID_PARAMETER;
                        goto error2;
                    }
                }

                ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_LABELSTACK, &attr_value, &index);
                CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_add_mpls(lchip, nh_id, attr_value->u32list, p_next_hop_info), status, error2);
            }
            else
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_VNI, &attr_value, &index);
                if (SAI_STATUS_SUCCESS == status)
                {
                    p_next_hop_info->dest_vni = attr_value->u32;
                    if (SAI_STATUS_SUCCESS == ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_MAC, &attr_value, &index))
                    {
                        sal_memcpy(p_next_hop_info->tunnel_mac, attr_value->mac, sizeof(sai_mac_t));
                    }
                    else
                    {
                        if (!p_switch_master->vxlan_default_router_mac)
                        {
                            status = SAI_STATUS_INVALID_PARAMETER;
                            goto error2;
                        }
                        sal_memcpy(p_next_hop_info->tunnel_mac, p_switch_master->vxlan_default_router_mac, sizeof(sai_mac_t));
                    }
                }
                CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_add_ip_tunnel(lchip, nh_id, p_next_hop_info), status, error2);
            }
        }
    }
    next_hop_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_NEXT_HOP, lchip, next_hop_type, 0, nh_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, next_hop_obj_id, (void*)p_next_hop_info), status, error3);

    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        p_switch_master->nexthop_cnt[p_next_hop_info->ip_address.addr_family]++;
    }
    else if((SAI_NEXT_HOP_TYPE_MPLS == next_hop_type) && (0 == p_next_hop_info->next_level_nexthop_id))
    {
        if(CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_binding_next_hop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_obj_id), status, error4);
        }
    }
    else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == next_hop_type)
    {
        //CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_binding_next_hop(lchip, p_tunnel->underlay_if, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_obj_id), status, error3);
        p_tunnel->encap_nexthop_sai = next_hop_obj_id;
    }
    *next_hop_id = next_hop_obj_id;
    if(p_tunnel)
    {
        p_tunnel->ref_cnt++;
    }

    goto out;

error4:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error3\n");
    ctc_sai_db_remove_object_property(lchip, next_hop_obj_id);
error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error2\n");
    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {
        ctc_sai_neighbor_free_ipuc_nexthop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), nh_id);
    }
    else
    {
        if (SAI_NEXT_HOP_TYPE_MPLS == next_hop_type)
        {
            _ctc_sai_next_hop_remove_mpls(lchip, nh_id, p_next_hop_info);
        }
        else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == next_hop_type)
        {
            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type || SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
            {
                _ctc_sai_next_hop_remove_mpls(lchip, nh_id, p_next_hop_info);
            }
            else
            {
                _ctc_sai_next_hop_remove_ip_tunnel(lchip, nh_id, p_next_hop_info);
            }
        }
    }
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error2\n");
    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {

    }
    else
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
    }
error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error1\n");
    mem_free(p_next_hop_info);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_remove_nh(sai_object_id_t next_hop_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    uint8 set_exp_domain = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    p_next_hop_info = ctc_sai_db_get_object_property(lchip, next_hop_id);
    if(NULL == p_next_hop_info)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, next_hop_id, &ctc_object_id);
    if(SAI_NEXT_HOP_TYPE_IP == ctc_object_id.sub_type)
    {
        ctc_sai_neighbor_free_ipuc_nexthop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), ctc_object_id.value);
        p_switch_master = ctc_sai_get_switch_property(lchip);
        p_switch_master->nexthop_cnt[p_next_hop_info->ip_address.addr_family]--;
    }
    else
    {
        if (SAI_NEXT_HOP_TYPE_MPLS == ctc_object_id.sub_type)
        {
            if(CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip) && (0 == p_next_hop_info->next_level_nexthop_id))
            {
                ctc_sai_neighbor_unbinding_next_hop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_id);
            }
            if(p_next_hop_info->tc_color_to_exp_map_id)
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_qos_map_mpls_nh_set_map(next_hop_id, p_next_hop_info->tc_color_to_exp_map_id,
                    SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP, 0, &set_exp_domain), status, out);
            }

            CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_remove_mpls(lchip, ctc_object_id.value, p_next_hop_info), status, out);
        }
        else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == ctc_object_id.sub_type)
        {
            if(p_next_hop_info->tc_color_to_exp_map_id)
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_qos_map_mpls_nh_set_map(next_hop_id, p_next_hop_info->tc_color_to_exp_map_id,
                    SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP, 0, &set_exp_domain), status, out);
            }

            p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
            if(SAI_TUNNEL_TYPE_MPLS_L2 ==p_tunnel->tunnel_type)
            {
                CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_remove_mpls(lchip, ctc_object_id.value, p_next_hop_info), status, out);
            }
            else if(SAI_TUNNEL_TYPE_MPLS ==p_tunnel->tunnel_type)
            {
                CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_remove_mpls(lchip, ctc_object_id.value, p_next_hop_info), status, out);
            }
            else
            {
                CTC_SAI_ERROR_GOTO(_ctc_sai_next_hop_remove_ip_tunnel(lchip, ctc_object_id.value, p_next_hop_info), status, out);
            }
        }   
    }
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_object_id.value);
    ctc_sai_db_remove_object_property(lchip, next_hop_id);
    if(p_next_hop_info->tunnel_id)
    {
        p_tunnel = NULL;
        p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
        if(NULL != p_tunnel)
        {
            p_tunnel->ref_cnt--;
        }
    }
    mem_free(p_next_hop_info);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_set_nh_attr(sai_object_id_t next_hop_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_next_hop_set_attr_check(lchip, 1, attr));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    key.key.object_id = next_hop_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_API_NEXT_HOP,  next_hop_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_next_hop_get_nh_attr(sai_object_id_t next_hop_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(next_hop_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    key.key.object_id = next_hop_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_API_NEXT_HOP, loop, next_hop_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_next_hop_api_t ctc_sai_next_hop_api = {
     ctc_sai_next_hop_create_nh,
     ctc_sai_next_hop_remove_nh,
     ctc_sai_next_hop_set_nh_attr,
     ctc_sai_next_hop_get_nh_attr
};

sai_status_t
ctc_sai_next_hop_api_init()
{
    ctc_sai_register_module_api(SAI_API_NEXT_HOP, (void*)&ctc_sai_next_hop_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_next_hop_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NEXTHOP;
    wb_info.data_len = sizeof(ctc_sai_next_hop_t);
    wb_info.wb_sync_cb = _ctc_sai_next_hop_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_next_hop_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_next_hop_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_NEXT_HOP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}


