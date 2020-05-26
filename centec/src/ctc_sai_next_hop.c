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
    uint8 chip_type = 0;
    ctc_sai_next_hop_t* p_next_hop_info_next_level = 0;
    ctc_sai_tunnel_t* p_tunnel = NULL;
    int num = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    chip_type = ctcs_get_chip_type(lchip);
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
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
        
    }
    sal_memset(&nh_tunnel_param, 0, sizeof(nh_tunnel_param));
    sal_memset(&nh_mpls_param, 0, sizeof(nh_mpls_param));
    p_next_hop_info->label.list = mem_malloc(MEM_NEXTHOP_MODULE, sizeof(uint32_t)*label.count);
    if (NULL == p_next_hop_info->label.list)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
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
            if(SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id)
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP, &stats_id), status, error3);
                nh_tunnel_param.nh_param.stats_valid = 1;
                nh_tunnel_param.nh_param.stats_id = stats_id;
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

    if (1 == label.count)
    {
        if(0 == p_next_hop_info->next_level_nexthop_id)
        {
            /*lsp*/
            nh_tunnel_param.nh_param.tunnel_label[0].ttl = (label.list[0])&0xFF;
            nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[0].exp = ((label.list[0]) >> 9)&0x7;
            nh_tunnel_param.nh_param.tunnel_label[0].label = ((label.list[0]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            nh_tunnel_param.nh_param.label_num++;
        }
        else
        {
            /*pipeline*/
            nh_mpls_param.nh_para.nh_param_push.push_label[0].ttl = (label.list[0])&0xFF;
            nh_mpls_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_mpls_param.nh_para.nh_param_push.push_label[0].exp = ((label.list[0]) >> 9)&0x7;
            nh_mpls_param.nh_para.nh_param_push.push_label[0].label = ((label.list[0]) >> 12)&0xFFFFF;
            
            nh_mpls_param.nh_para.nh_param_push.label_num++;
            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
            {
                nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_L2VPN;
            
                if(p_tunnel->encap_cw_en)
                {
                    nh_mpls_param.nh_para.nh_param_push.martini_encap_valid = TRUE;
                    nh_mpls_param.nh_para.nh_param_push.martini_encap_type = 1;
                }
                if(SAI_TUNNEL_MPLS_PW_MODE_TAGGED == p_tunnel->encap_pw_mode)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.cvlan_edit_type = 1;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.svlan_edit_type = 3;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.output_svid = p_tunnel->encap_tagged_vlan;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.output_cvid = 1;
                    CTC_SET_FLAG(nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.edit_flag, CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID);
                }
                else if(SAI_TUNNEL_MPLS_PW_MODE_RAW == p_tunnel->encap_pw_mode)
                {
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.cvlan_edit_type = 1;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.svlan_edit_type = 4;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.output_svid = 1;
                    nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.output_cvid = 1;
                    CTC_UNSET_FLAG(nh_mpls_param.nh_para.nh_param_push.nh_com.vlan_info.edit_flag, CTC_VLAN_EGRESS_EDIT_OUPUT_SVID_VALID);
                }
                nh_mpls_param.nh_para.nh_param_push.eslb_en= p_tunnel->encap_esi_label_valid;
                nh_mpls_param.logic_port_valid= 1;
                nh_mpls_param.logic_port= p_tunnel->logic_port;                
            }
            else
            {
                nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
                /*ttl and exp process needed here*/
                if(SAI_TUNNEL_TYPE_MPLS == p_tunnel->tunnel_type)
                {
                    if(SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL == p_tunnel->encap_ttl_mode)
                    {
                        nh_mpls_param.nh_para.nh_param_push.push_label[0].ttl = 0;
                        CTC_SET_FLAG(nh_mpls_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
                    }
                    else if(SAI_TUNNEL_TTL_MODE_PIPE_MODEL == p_tunnel->encap_ttl_mode)
                    {
                        nh_mpls_param.nh_para.nh_param_push.push_label[0].ttl = p_tunnel->encap_ttl_val;
                        CTC_UNSET_FLAG(nh_mpls_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_MAP_TTL);
                    }
                    if(SAI_TUNNEL_EXP_MODE_UNIFORM_MODEL == p_tunnel->encap_exp_mode)
                    {
                        nh_mpls_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_MAP;
                    }
                    else if(SAI_TUNNEL_EXP_MODE_PIPE_MODEL == p_tunnel->encap_exp_mode)
                    {
                        nh_mpls_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
                        nh_mpls_param.nh_para.nh_param_push.push_label[0].exp = p_tunnel->encap_exp_val;
                    }
                }
            }
        }
        
    
        if(SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id)
        {
            if(0 == p_next_hop_info->next_level_nexthop_id)
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP, &stats_id), status, error3);
            }
            else
            {
                CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_PW, &stats_id), status, error3);
            }
            nh_tunnel_param.nh_param.stats_valid = 1;
            nh_tunnel_param.nh_param.stats_id = stats_id;
            
        }
    }
    else if(2 == label.count)
    {
        /*lsp*/
        nh_tunnel_param.nh_param.tunnel_label[0].ttl = (label.list[1])&0xFF;
        nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
        nh_tunnel_param.nh_param.tunnel_label[0].exp = ((label.list[1]) >> 9)&0x7;
        nh_tunnel_param.nh_param.tunnel_label[0].label = ((label.list[1]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        /*spme*/
        nh_tunnel_param.nh_param.label_num++;
        nh_tunnel_param.nh_param.tunnel_label[1].ttl = (label.list[0])&0xFF;
        nh_tunnel_param.nh_param.tunnel_label[1].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
        nh_tunnel_param.nh_param.tunnel_label[1].exp = ((label.list[0]) >> 9)&0x7;
        nh_tunnel_param.nh_param.tunnel_label[1].label = ((label.list[0]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[1].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        nh_tunnel_param.nh_param.label_num++;
    
        if((2 == label.count) && (SAI_NULL_OBJECT_ID != p_next_hop_info->counter_obj_id))
        {
            CTC_SAI_ERROR_GOTO(ctc_sai_counter_id_create(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP_MPLS_LSP, &stats_id), status, error3);
            nh_tunnel_param.nh_param.stats_valid = 1;
            nh_tunnel_param.nh_param.stats_id = stats_id;
        }
    }
    else if(3 <= label.count && 10 >= label.count && CTC_CHIP_TSINGMA <= ctcs_get_chip_type(lchip))
    {
        nh_tunnel_param.nh_param.is_sr = 1;
        for(num = 0;num < label.count;num++)
        {
            nh_tunnel_param.nh_param.tunnel_label[num].ttl = (label.list[num])&0xFF;
            nh_tunnel_param.nh_param.tunnel_label[num].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[num].exp = ((label.list[num]) >> 9)&0x7;
            nh_tunnel_param.nh_param.tunnel_label[num].label = ((label.list[num]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[num].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            nh_tunnel_param.nh_param.label_num++;
        }
    }
    
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls_tunnel_label(lchip, ctc_tunnel_id, &nh_tunnel_param), status, error2);
    }
    else
    {
        p_next_hop_info_next_level = ctc_sai_db_get_object_property(lchip, p_next_hop_info->next_level_nexthop_id);
        if(0 == p_next_hop_info_next_level->ctc_mpls_tunnel_id)
        {
            goto error2;
        }
    }
    
    if (3 == label.count && CTC_CHIP_TSINGMA > ctcs_get_chip_type(lchip))
    {
        nh_mpls_param.nh_para.nh_param_push.push_label[0].ttl = (label.list[2])&0xFF;
        nh_mpls_param.nh_para.nh_param_push.push_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
        nh_mpls_param.nh_para.nh_param_push.push_label[0].exp = ((label.list[2]) >> 9)&0x7;
        nh_mpls_param.nh_para.nh_param_push.push_label[0].label = ((label.list[2]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_mpls_param.nh_para.nh_param_push.push_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        nh_mpls_param.nh_para.nh_param_push.label_num++;
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
        nh_mpls_param.nh_para.nh_param_push.nh_com.opcode = CTC_MPLS_NH_PUSH_OP_ROUTE;
        nh_mpls_param.nh_para.nh_param_push.tunnel_id = ctc_tunnel_id;
    }
    else
    {
        ctcs_nh_get_mpls_tunnel_label(lchip, p_next_hop_info_next_level->ctc_mpls_tunnel_id, &next_level_nh_tunnel_param);
        if(next_level_nh_tunnel_param.nh_param.is_sr)
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_next_hop_info->next_level_nexthop_id, &ctc_object_id);
            nh_mpls_param.nh_para.nh_param_push.loop_nhid = ctc_object_id.value;
        }
        else
        {
            nh_mpls_param.nh_para.nh_param_push.tunnel_id = p_next_hop_info_next_level->ctc_mpls_tunnel_id;
        }
    }
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mpls(lchip, nh_id, &nh_mpls_param), status, error4);
    p_next_hop_info->label.count = label.count;
    sal_memcpy(p_next_hop_info->label.list, label.list, sizeof(uint32_t)*label.count);
    if(0 == p_next_hop_info->next_level_nexthop_id)
    {
        p_next_hop_info->ctc_mpls_tunnel_id = ctc_tunnel_id;
    }
    
    return SAI_STATUS_SUCCESS;

error4:
    ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP);
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
    ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP);
    ctcs_nh_remove_mpls(lchip, nh_id);
    ctcs_nh_remove_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id);
    if (p_next_hop_info->label.count)
    {
        mem_free(p_next_hop_info->label.list);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_TUNNEL_ID, p_next_hop_info->ctc_mpls_tunnel_id);
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
    ctc_mpls_nexthop_param_t nh_mpls_param;

    CTC_SAI_LOG_ENTER(SAI_API_NEXT_HOP);
    CTC_SAI_ERROR_RETURN(ctc_sai_neighbor_get_outgoing_param(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), &gport, mac));
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(p_next_hop_info->rif_id, NULL, NULL,  NULL, &vlan));

    sal_memset(&nh_tunnel_param, 0, sizeof(nh_tunnel_param));
    sal_memset(&nh_mpls_param, 0, sizeof(nh_mpls_param));
    if (0 == p_next_hop_info->label.count)/*php*/
    {
        nh_mpls_param.upd_type = CTC_NH_UPD_FWD_ATTR;
        sal_memcpy(nh_mpls_param.nh_para.nh_param_pop.nh_com.mac, mac, sizeof(sai_mac_t));
        nh_mpls_param.nh_para.nh_param_pop.nh_com.oif.gport = gport;
        nh_mpls_param.nh_para.nh_param_pop.nh_com.oif.vid = vlan;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_add_mpls(lchip, nh_id, &nh_mpls_param));
    }
    else
    {
        sal_memcpy(nh_tunnel_param.nh_param.mac, mac, sizeof(sai_mac_t));
        nh_tunnel_param.nh_param.oif.gport = gport;
        nh_tunnel_param.nh_param.oif.vid = vlan;
        nh_tunnel_param.nh_param.tunnel_label[0].ttl = (p_next_hop_info->label.list[0])&0xFF;
        nh_tunnel_param.nh_param.tunnel_label[0].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
        nh_tunnel_param.nh_param.tunnel_label[0].exp = ((p_next_hop_info->label.list[0]) >> 9)&0x7;
        nh_tunnel_param.nh_param.tunnel_label[0].label = ((p_next_hop_info->label.list[0]) >> 12)&0xFFFFF;
        CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[0].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
        nh_tunnel_param.nh_param.label_num++;
        if (p_next_hop_info->label.count > 1)
        {
            nh_tunnel_param.nh_param.tunnel_label[1].ttl = (p_next_hop_info->label.list[0])&0xFF;
            nh_tunnel_param.nh_param.tunnel_label[1].exp_type = CTC_NH_EXP_SELECT_ASSIGN;
            nh_tunnel_param.nh_param.tunnel_label[1].exp = ((p_next_hop_info->label.list[0]) >> 9)&0x7;
            nh_tunnel_param.nh_param.tunnel_label[1].label = ((p_next_hop_info->label.list[0]) >> 12)&0xFFFFF;
            CTC_SET_FLAG(nh_tunnel_param.nh_param.tunnel_label[1].lable_flag, CTC_MPLS_NH_LABEL_IS_VALID);
            nh_tunnel_param.nh_param.label_num++;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mpls_tunnel_label(lchip, p_next_hop_info->ctc_mpls_tunnel_id, &nh_tunnel_param));
    }
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
    ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP);    
    return status;
}

static sai_status_t
_ctc_sai_next_hop_remove_ip_tunnel(uint8 lchip, uint32 nh_id, ctc_sai_next_hop_t* p_next_hop_info)
{
    ctc_ip_tunnel_nh_param_t nh_param;

    sal_memset(&nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_counter_id_remove(p_next_hop_info->counter_obj_id, CTC_SAI_COUNTER_TYPE_NEXTHOP));
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
    }
    else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == attr_value->s32)
    {
        ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);
            p_tunnel = ctc_sai_db_get_object_property(lchip, attr_value->oid);
            if(NULL == p_tunnel || SAI_TUNNEL_TYPE_MPLS_L2 !=p_tunnel->tunnel_type)
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
    uint32 attrib_id[6] =
    {
        SAI_NEXT_HOP_ATTR_TYPE,
        SAI_NEXT_HOP_ATTR_IP,
        SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID,
        SAI_NEXT_HOP_ATTR_LABELSTACK,
        SAI_NEXT_HOP_ATTR_TUNNEL_ID,
        SAI_NEXT_HOP_ATTR_SEGMENTROUTE_SIDLIST_ID
    };
    for (i = 0; i < 6; i++)
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
    case SAI_NEXT_HOP_ATTR_MPLS_DECAP_TUNNEL_ID:
        attr->value.oid = p_next_hop_info->decap_tunnel_id;
    case SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID:
        attr->value.oid = p_next_hop_info->next_level_nexthop_id;
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
      NULL},
    { SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},
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
    { SAI_NEXT_HOP_ATTR_MPLS_DECAP_TUNNEL_ID,
      _ctc_sai_next_hop_get_attr,
      NULL},  
    { SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID,
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
    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_alloc_ipuc_nexthop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), &nh_id), status, error1);
    }
    else
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id), status, error1);
        if(SAI_NEXT_HOP_TYPE_MPLS == next_hop_type)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_TUNNEL_ID, &attr_value, &index);
            /*tunnel type*/
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->tunnel_id = attr_value->oid;
                p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
            }
            if (NULL == p_tunnel)
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_MPLS_ENCAP_TUNNEL_ID, &attr_value, &index);
                /*tunnel type*/
                if (!CTC_SAI_ERROR(status))
                {
                    p_next_hop_info->tunnel_id = attr_value->oid;
                    p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
                    if(NULL != p_tunnel && SAI_TUNNEL_TYPE_MPLS !=p_tunnel->tunnel_type)
                    {
                        return SAI_STATUS_INVALID_OBJECT_ID;
                    }
                }
            }
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {
                p_next_hop_info->next_level_nexthop_id = attr_value->oid;
            }
            ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_LABELSTACK, &attr_value, &index);
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
                if(NULL == p_tunnel || SAI_TUNNEL_TYPE_MPLS_L2 !=p_tunnel->tunnel_type)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }
            }

            if(SAI_TUNNEL_TYPE_MPLS_L2 == p_tunnel->tunnel_type)
            {
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID, &attr_value, &index);
                if (!CTC_SAI_ERROR(status))
                {
                    p_next_hop_info->next_level_nexthop_id = attr_value->oid;
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
    status = ctc_sai_db_add_object_property(lchip, next_hop_obj_id, (void*)p_next_hop_info);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error2;
    }
    if (SAI_NEXT_HOP_TYPE_IP == next_hop_type)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        p_switch_master->nexthop_cnt[p_next_hop_info->ip_address.addr_family]++;
    }
    else if((SAI_NEXT_HOP_TYPE_MPLS == next_hop_type) && (0 == p_next_hop_info->next_level_nexthop_id))
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_binding_next_hop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_obj_id), status, error3);
    }
    else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == next_hop_type)
    {
        //CTC_SAI_ERROR_GOTO(ctc_sai_neighbor_binding_next_hop(lchip, p_tunnel->underlay_if, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_obj_id), status, error3);
        p_tunnel->encap_nexthop_sai = next_hop_obj_id;
    }
    *next_hop_id = next_hop_obj_id;
    
    goto out;

error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEXT_HOP, "rollback to error3\n");
    ctc_sai_db_remove_object_property(lchip, next_hop_obj_id);
error2:
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
            _ctc_sai_next_hop_remove_ip_tunnel(lchip, nh_id, p_next_hop_info);
        }
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
            ctc_sai_neighbor_unbinding_next_hop(lchip, p_next_hop_info->rif_id, (sai_ip_address_t*)(&(p_next_hop_info->ip_address)), next_hop_id);
            _ctc_sai_next_hop_remove_mpls(lchip, ctc_object_id.value, p_next_hop_info);
        }
        else if(SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP == ctc_object_id.sub_type)
        {
            p_tunnel = ctc_sai_db_get_object_property(lchip, p_next_hop_info->tunnel_id);
            if(SAI_TUNNEL_TYPE_MPLS_L2 ==p_tunnel->tunnel_type)
            {
                _ctc_sai_next_hop_remove_mpls(lchip, ctc_object_id.value, p_next_hop_info);
            }
            else
            {
                _ctc_sai_next_hop_remove_ip_tunnel(lchip, ctc_object_id.value, p_next_hop_info);
            }
            
        }
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, ctc_object_id.value);
    }
    ctc_sai_db_remove_object_property(lchip, next_hop_id);
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


