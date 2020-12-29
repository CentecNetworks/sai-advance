#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_route.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_next_hop_group.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_bfd.h"

typedef struct ctc_sai_bfd_master_s
{
    uint16 reroute_inner_port;
    uint32 reroute_l3if;
    uint32 reroute_iloop_nhid;
    uint8 use_global_res_info;
    
} ctc_sai_bfd_master_t;

ctc_sai_bfd_master_t* p_ctc_sai_bfd[CTC_MAX_LOCAL_CHIP_NUM] = {NULL};

typedef struct  ctc_sai_bfd_master_wb_s
{
    /*key*/
    uint32 lchip;
    uint32 calc_key_len[0];
    
    /*data*/    
    uint32 reroute_l3if;
    uint32 reroute_iloop_nhid;
    uint16 reroute_inner_port;
    uint8 use_global_res_info;
    
}ctc_sai_bfd_master_wb_t;
    

static sai_status_t
_ctc_sai_bfd_build_db(uint8 lchip, sai_object_id_t bfd_session_id, ctc_sai_bfd_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_bfd_t* p_bfd_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    p_bfd_info = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_bfd_t));
    if (NULL == p_bfd_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset((void*)p_bfd_info, 0, sizeof(ctc_sai_bfd_t));
    status = ctc_sai_db_add_object_property(lchip, bfd_session_id, (void*)p_bfd_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_bfd_info);
        return status;
    }

    *oid_property = p_bfd_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bfd_remove_db(uint8 lchip, sai_object_id_t bfd_session_id)
{
    ctc_sai_bfd_t* p_bfd_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    p_bfd_info = ctc_sai_db_get_object_property(lchip, bfd_session_id);
    if (NULL == p_bfd_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, bfd_session_id);
    mem_free(p_bfd_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bfd_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint8 hw_lkp_valid = 0, vlan_hdr_valid = 0, ach_header_valid = 0;
    sai_bfd_encapsulation_type_t bfd_encap_type = SAI_BFD_ENCAPSULATION_TYPE_NONE;
    sai_bfd_mpls_type_t mpls_bfd_type = SAI_BFD_MPLS_TYPE_NORMAL;
    sai_bfd_ach_channel_type_t ach_type = 0;
    sai_object_id_t def_vr_obj_id = 0;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    sai_inseg_entry_t inseg_entry;
    uint8 is_mpls_tp_section_bfd = 0;

    sal_memset(&inseg_entry, 0, sizeof(sai_inseg_entry_t));

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TYPE, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    else
    {
        if( SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE != attr_value->s32)
        {
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MIN_TX, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MIN_RX, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MULTIPLIER, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    else
    {
        if((SAI_BFD_ENCAPSULATION_TYPE_IP_IN_IP == attr_value->s32) || (SAI_BFD_ENCAPSULATION_TYPE_L3_GRE_TUNNEL == attr_value->s32))
        {
            return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
        }
        else
        {
            bfd_encap_type = attr_value->s32;
        }
    }

    if( SAI_BFD_ENCAPSULATION_TYPE_NONE == bfd_encap_type)
    {

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {
            hw_lkp_valid = attr_value->booldata;
        }
        else
        {
            /*default value */
            hw_lkp_valid = true;
        }
       
        if(hw_lkp_valid)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER, &attr_value, &index);
            if (CTC_SAI_ERROR(status))
            {
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
            }

            //TsingMa global res mode, only support default vr_id
            if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && p_ctc_sai_bfd[lchip]->use_global_res_info)
            {
                def_vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, 0);
                if(attr_value->oid != def_vr_obj_id)
                {
                    return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
                }
            }

        }
        else
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_NEXT_HOP_ID, &attr_value, &index);
            if (CTC_SAI_ERROR(status))
            {        
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS, &attr_value, &index);
                if (CTC_SAI_ERROR(status))
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
                }
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS, &attr_value, &index);
                if (CTC_SAI_ERROR(status))
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
                }
                status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_PORT, &attr_value, &index);
                if (CTC_SAI_ERROR(status))
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
                }                
            }           
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_IPHDR_VERSION, &attr_value, &index);
        if (CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS, &attr_value, &index);
        if (CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS, &attr_value, &index);
        if (CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_UDP_SRC_PORT, &attr_value, &index);
        if (CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }
    
    if( SAI_BFD_ENCAPSULATION_TYPE_MPLS == bfd_encap_type)
    {

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {        
            ach_header_valid = attr_value->booldata;
        }

        if(ach_header_valid)
        {
            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_ACH_CHANNEL_TYPE, &attr_value, &index);
            if (CTC_SAI_ERROR(status))
            {        
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
            }
            else
            {
                ach_type = attr_value->s32;
            }
        }    
            
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_MPLS_TYPE, &attr_value, &index);
        if (CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
        else
        {
            mpls_bfd_type =  attr_value->s32;
        }
        
        if(mpls_bfd_type == SAI_BFD_MPLS_TYPE_TP)
        {

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {        
                is_mpls_tp_section_bfd = 1;
            }

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_CV_ENABLE, &attr_value, &index);
            if (!CTC_SAI_ERROR(status))
            {        
                if( SAI_BFD_ACH_CHANNEL_TYPE_TP != ach_type)
                {
                    return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
                }
            }   

        }

        if(!is_mpls_tp_section_bfd)
        {

            status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL, &attr_value, &index);
            if (CTC_SAI_ERROR(status))
            {        
                return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
            }
            else
            {
                inseg_entry.switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, lchip);
                inseg_entry.label = attr_value->u32;
                p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)&inseg_entry);
                if (NULL == p_mpls_info)
                {
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
            }   


        }      
             
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
    }

    if(!vlan_hdr_valid)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VLAN_TPID, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VLAN_ID, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VLAN_PRI, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VLAN_CFI, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {        
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TUNNEL_TOS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TUNNEL_TTL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_ATTR_NOT_IMPLEMENTED_0 + index;
    }    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_STATE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_NEGOTIATED_TX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_NEGOTIATED_RX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_LOCAL_DIAG, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_DIAG, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {        
        return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
    }
    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bfd_build_ipbfd_nh(uint8 lchip, ctc_sai_bfd_t* p_bfd_info, uint32* nh_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 gport = 0;
    ctc_ip_nh_param_t  nh_param;
    ctc_ip_tunnel_nh_param_t tunnel_nh_param;
    uint32 nhid = 0, l3if_id = 0;
    uint8 gchip = 0;
    ctc_l3if_t l3if;
    ctc_l3if_property_t l3if_prop;
    uint16 ctc_vrf_id = 0;

    ctc_internal_port_assign_para_t port_assign;
    ctc_loopback_nexthop_param_t iloop_nh;

    sai_ip_address_t ip_address;

    sal_memset(&nh_param, 0, sizeof(ctc_ip_nh_param_t));
    sal_memset(&tunnel_nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));
    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    sal_memset(&l3if_prop, 0, sizeof(ctc_l3if_property_t));
    sal_memset(&port_assign, 0, sizeof(ctc_internal_port_assign_para_t));
    sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));

    sal_memset(&ip_address, 0, sizeof(sai_ip_address_t));
        
    if( SAI_BFD_ENCAPSULATION_TYPE_NONE == p_bfd_info->encap_type)
    {
        /*Micro BFD nh */
        if(!p_bfd_info->hw_lookup_valid && (SAI_NULL_OBJECT_ID != p_bfd_info->dst_port_oid))
        {
            ctc_sai_oid_get_gport(p_bfd_info->dst_port_oid, &gport);
            if(4 == p_bfd_info->ip_hdr_ver)
            {
                nh_param.oif.gport = gport;
                nh_param.oif.is_l2_port = 1;

                sal_memcpy(nh_param.mac, p_bfd_info->dst_mac, sizeof(sai_mac_t));
                sal_memcpy(nh_param.mac_sa, p_bfd_info->src_mac, sizeof(sai_mac_t));

                CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_add_ipuc(lchip, nhid, &nh_param));

                *nh_id = nhid;

                p_bfd_info->inner_nh_type = CTC_SAI_BFD_NH_TYPE_IPUC;
                p_bfd_info->inner_nhid = nhid;
            }
            else if(6 == p_bfd_info->ip_hdr_ver)
            {
                /*tunnel nh direct to outport */
                CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid), status, out);

                tunnel_nh_param.oif.gport = gport;
                tunnel_nh_param.oif.is_l2_port = 1;

                sal_memcpy(tunnel_nh_param.mac, p_bfd_info->dst_mac, sizeof(sai_mac_t));
                sal_memcpy(tunnel_nh_param.mac_sa, p_bfd_info->src_mac, sizeof(sai_mac_t));

                tunnel_nh_param.tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_IPV4_IN6;
                
                sal_memcpy(&(tunnel_nh_param.tunnel_info.ip_sa.ipv6), &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(ipv6_addr_t));
                CTC_SAI_NTOH_V6(tunnel_nh_param.tunnel_info.ip_sa.ipv6);
                sal_memcpy(&(tunnel_nh_param.tunnel_info.ip_da.ipv6), &(p_bfd_info->dst_ip_addr.addr.ip6), sizeof(ipv6_addr_t));
                CTC_SAI_NTOH_V6(tunnel_nh_param.tunnel_info.ip_da.ipv6);
                
                tunnel_nh_param.tunnel_info.ttl = p_bfd_info->ip_ttl;                

                tunnel_nh_param.tunnel_info.dscp_select = CTC_NH_DSCP_SELECT_ASSIGN;
                tunnel_nh_param.tunnel_info.dscp_or_tos = p_bfd_info->ip_tos;

                //tunnel_nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_REROUTE_WITH_TUNNEL_HDR;
                tunnel_nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_IP_BFD;

                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_ip_tunnel(lchip, nhid, &tunnel_nh_param), status, error6);

                *nh_id = nhid;
                p_bfd_info->inner_nh_type = CTC_SAI_BFD_NH_TYPE_IP_TUNNEL;
                p_bfd_info->inner_nhid = nhid;

                goto out;

                error6:
                    CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error6\n");
                    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nhid);            
            }
            
            goto out;
        }
        else if(p_bfd_info->hw_lookup_valid)  /*IP UC reroute nh */
        {            
            if(4 == p_bfd_info->ip_hdr_ver)
            {
                //ASIC Reroute, TsingMa, only support default vr id
                if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && p_ctc_sai_bfd[lchip]->use_global_res_info)
                {
                    *nh_id = p_ctc_sai_bfd[lchip]->reroute_iloop_nhid;

                    p_bfd_info->inner_l3if = p_ctc_sai_bfd[lchip]->reroute_l3if;
                    p_bfd_info->inner_nh_type = CTC_SAI_BFD_NH_TYPE_ILOOP;
                    p_bfd_info->inner_nhid = *nh_id;
                    p_bfd_info->inner_gport = p_ctc_sai_bfd[lchip]->reroute_inner_port;
                }
                else
                {                
                    /*alloc iloop port */
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
                    port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
                    port_assign.gchip = gchip;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_alloc_internal_port(lchip, &port_assign));

                    /*config inner l3if */
                    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
                    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, error1);

                    l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
                    l3if.gport = port_assign.inter_port;
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_l3if_create(lchip, l3if_id, &l3if), status, error2);

                    CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_vrf_id(p_bfd_info->vr_oid, &ctc_vrf_id), status, error3);

                    l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_IPV6_MCAST;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_VRF_EN;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
                    l3if_prop = CTC_L3IF_PROP_VRF_ID;
                    ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, ctc_vrf_id);                

                    ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);

                    /*iloop nh */
                    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid), status, error3);
                    iloop_nh.lpbk_lport = port_assign.inter_port;
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_iloop(lchip, nhid, &iloop_nh), status, error4);
                    *nh_id = nhid;

                    p_bfd_info->inner_l3if = l3if_id;
                    p_bfd_info->inner_nh_type = CTC_SAI_BFD_NH_TYPE_ILOOP;
                    p_bfd_info->inner_nhid = nhid;
                    p_bfd_info->inner_gport = port_assign.inter_port;

                    goto out;
                    
                    error4:
                        CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error4\n");
                        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nhid);
                    error3:
                        CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error3\n");
                        ctcs_l3if_destory(lchip, l3if_id, &l3if);
                        
                    error2:
                        CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error2\n");
                        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);

                    error1:
                        CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error1\n");
                        ctcs_free_internal_port(lchip, &port_assign);
                }


                goto out;

            }
            else if(6 == p_bfd_info->ip_hdr_ver)
            {
                /*tunnel reroute nh */
                CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid), status, out);

                tunnel_nh_param.tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_IPV4_IN6;
                
                sal_memcpy(&(tunnel_nh_param.tunnel_info.ip_sa.ipv6), &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(ipv6_addr_t));
                CTC_SAI_NTOH_V6(tunnel_nh_param.tunnel_info.ip_sa.ipv6);
                sal_memcpy(&(tunnel_nh_param.tunnel_info.ip_da.ipv6), &(p_bfd_info->dst_ip_addr.addr.ip6), sizeof(ipv6_addr_t));
                CTC_SAI_NTOH_V6(tunnel_nh_param.tunnel_info.ip_da.ipv6);
                
                tunnel_nh_param.tunnel_info.ttl = p_bfd_info->ip_ttl;                

                tunnel_nh_param.tunnel_info.dscp_select = CTC_NH_DSCP_SELECT_ASSIGN;
                tunnel_nh_param.tunnel_info.dscp_or_tos = p_bfd_info->ip_tos;

                tunnel_nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_REROUTE_WITH_TUNNEL_HDR;
                tunnel_nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_IP_BFD;

                CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_ip_tunnel(lchip, nhid, &tunnel_nh_param), status, error5);

                *nh_id = nhid;
                p_bfd_info->inner_nh_type = CTC_SAI_BFD_NH_TYPE_IP_TUNNEL;
                p_bfd_info->inner_nhid = nhid;

                goto out;

                error5:
                    CTC_SAI_LOG_ERROR(SAI_API_BFD, "build ipbfd nexthop rollback to error5\n");
                    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nhid);
                    
                goto out;
            }
            
        }

    }


out:
    return status;
}

static sai_status_t
_ctc_sai_bfd_remove_ipbfd_nh(uint8 lchip, ctc_sai_bfd_t* p_bfd_info)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 gchip = 0;
    ctc_l3if_t l3if;
    ctc_internal_port_assign_para_t port_assign;

    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    sal_memset(&port_assign, 0, sizeof(ctc_internal_port_assign_para_t));
    
    if(CTC_SAI_BFD_NH_TYPE_NONE != p_bfd_info->inner_nh_type)
    {
        if(CTC_SAI_BFD_NH_TYPE_IPUC == p_bfd_info->inner_nh_type)
        {
            ctcs_nh_remove_ipuc(lchip, p_bfd_info->inner_nhid);
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bfd_info->inner_nhid);
        }
        else if(CTC_SAI_BFD_NH_TYPE_IP_TUNNEL == p_bfd_info->inner_nh_type)
        {
            ctcs_nh_remove_ip_tunnel(lchip, p_bfd_info->inner_nhid);
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bfd_info->inner_nhid);
        }
        else if(CTC_SAI_BFD_NH_TYPE_ILOOP == p_bfd_info->inner_nh_type)
        {
            if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && p_ctc_sai_bfd[lchip]->use_global_res_info)
            {
                //Do not del nh info
            }
            else
            {
                ctcs_nh_remove_iloop(lchip, p_bfd_info->inner_nhid);
                ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bfd_info->inner_nhid);

                l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
                l3if.gport = p_bfd_info->inner_gport;
                ctcs_l3if_destory(lchip, p_bfd_info->inner_l3if, &l3if);
                ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_bfd_info->inner_l3if);

                CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
                port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
                port_assign.gchip = gchip;
                port_assign.inter_port = p_bfd_info->inner_gport;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_free_internal_port(lchip, &port_assign));  
            }
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_bfd_lkup_key_gen(uint8 lchip, ctc_sai_bfd_t* p_bfd_info, ctc_oam_lmep_t* lmep, ctc_oam_rmep_t* rmep)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_oam_mep_info_t  mep_info;
    uint16 l3if_id = 0;

    sal_memset(&mep_info, 0, sizeof(ctc_oam_mep_info_t));
    
    mep_info.mep_index = p_bfd_info->remote_mep_index;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info(lchip, &mep_info),status, out);

    if( SAI_BFD_ENCAPSULATION_TYPE_NONE == p_bfd_info->encap_type)
    {
        if(!p_bfd_info->hw_lookup_valid && (SAI_NULL_OBJECT_ID != p_bfd_info->dst_port_oid))
        {
            lmep->key.mep_type = CTC_OAM_MEP_TYPE_MICRO_BFD;
            rmep->key.mep_type = CTC_OAM_MEP_TYPE_MICRO_BFD;
        }
        else
        {
            lmep->key.mep_type = CTC_OAM_MEP_TYPE_IP_BFD;
            rmep->key.mep_type = CTC_OAM_MEP_TYPE_IP_BFD;   
        }
        lmep->key.u.bfd.discr = mep_info.lmep.bfd_lmep.local_discr;
        rmep->key.u.bfd.discr = mep_info.lmep.bfd_lmep.local_discr;
    }
    else if ( SAI_BFD_ENCAPSULATION_TYPE_MPLS == p_bfd_info->encap_type)
    {
        /*MPLS BFD */
        if( SAI_BFD_MPLS_TYPE_NORMAL == p_bfd_info->mpls_bfd_type)
        {
            lmep->key.mep_type = CTC_OAM_MEP_TYPE_MPLS_BFD;
            lmep->key.u.bfd.discr = mep_info.lmep.bfd_lmep.local_discr;

            rmep->key.mep_type = CTC_OAM_MEP_TYPE_MPLS_BFD;
            rmep->key.u.bfd.discr = mep_info.lmep.bfd_lmep.local_discr;
        }
        else if( SAI_BFD_MPLS_TYPE_TP == p_bfd_info->mpls_bfd_type) /*TP BFD */
        {
            lmep->key.mep_type = CTC_OAM_MEP_TYPE_MPLS_TP_BFD;
            rmep->key.mep_type = CTC_OAM_MEP_TYPE_MPLS_TP_BFD;
            
            if(SAI_NULL_OBJECT_ID != p_bfd_info->section_rif_oid)
            {
                ctc_sai_oid_get_l3if_id(p_bfd_info->section_rif_oid, &l3if_id);
                
                CTC_SET_FLAG(lmep->key.flag, CTC_OAM_KEY_FLAG_LINK_SECTION_OAM);
                lmep->key.u.tp.gport_or_l3if_id = l3if_id;

                CTC_SET_FLAG(rmep->key.flag, CTC_OAM_KEY_FLAG_LINK_SECTION_OAM);
                rmep->key.u.tp.gport_or_l3if_id = l3if_id;
            }
            else
            {                
                lmep->key.u.tp.label = p_bfd_info->mpls_in_label;
                rmep->key.u.tp.label = p_bfd_info->mpls_in_label;
            }
        }

    }
    
out:
    return status;
}

static int32
_ctc_sai_bfd_traverse_get_session_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t* user_data)
{
    ctc_sai_bfd_t* p_bfd_info = bucket_data->data;
    uint8 is_remote = 0;

    is_remote = *(uint8*)(user_data->value1);

    if ((!is_remote && (p_bfd_info->local_mep_index == *(uint32*)user_data->value0))
        || (is_remote && (p_bfd_info->remote_mep_index == *(uint32*)user_data->value0)))
    {
        *(uint64*)(user_data->value4) = bucket_data->oid;

        return -1;
    }

    return 0;
}

static sai_status_t
_ctc_sai_bfd_add_local_ipuc(uint8 lchip, ctc_sai_bfd_t* p_bfd_info)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint16 ctc_vrf_id = 0;
    ctc_ipuc_param_t ipuc_info;
    int32 ret = 0;

    sal_memset(&ipuc_info, 0, sizeof(ctc_ipuc_param_t));

    if(SAI_NULL_OBJECT_ID != p_bfd_info->vr_oid)
    {
        ctc_sai_oid_get_vrf_id(p_bfd_info->vr_oid, &ctc_vrf_id);
    }
    ipuc_info.vrf_id = ctc_vrf_id;

    if(4 == p_bfd_info->ip_hdr_ver)
    {
        sal_memcpy(&ipuc_info.ip.ipv4, &(p_bfd_info->src_ip_addr.addr.ip4), sizeof(sai_ip4_t));
        CTC_SAI_NTOH_V4(ipuc_info.ip.ipv4);
        ipuc_info.masklen = 32;
        ipuc_info.ip_ver = CTC_IP_VER_4;
    }
    else
    {
        sal_memcpy(&ipuc_info.ip.ipv6, &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(ipuc_info.ip.ipv6);
        ipuc_info.masklen = 128;
        ipuc_info.ip_ver = CTC_IP_VER_6;
    }

    ipuc_info.nh_id = 2; //SDK reserverd to CPU nexthop
    ipuc_info.route_flag |= CTC_IPUC_FLAG_SELF_ADDRESS;
    ipuc_info.route_flag |= CTC_IPUC_FLAG_NEIGHBOR;

    ret = ctcs_ipuc_get(lchip, &ipuc_info);
    if(ret < 0)
    {
        p_bfd_info->add_self_route_by_bfd = 1;
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_add(lchip, &ipuc_info));

    return status;

}

static sai_status_t
_ctc_sai_bfd_remove_local_ipuc(uint8 lchip, ctc_sai_bfd_t* p_bfd_info)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint16 ctc_vrf_id = 0;
    ctc_ipuc_param_t ipuc_info;
    int32 ret = 0;

    sal_memset(&ipuc_info, 0, sizeof(ctc_ipuc_param_t));
    
    if( SAI_BFD_ENCAPSULATION_TYPE_NONE != p_bfd_info->encap_type)
    {
        return status;
    }

    if(SAI_NULL_OBJECT_ID != p_bfd_info->vr_oid)
    {
        ctc_sai_oid_get_vrf_id(p_bfd_info->vr_oid, &ctc_vrf_id);
    }
    ipuc_info.vrf_id = ctc_vrf_id;

    if(4 == p_bfd_info->ip_hdr_ver)
    {
        sal_memcpy(&ipuc_info.ip.ipv4, &(p_bfd_info->src_ip_addr.addr.ip4), sizeof(sai_ip4_t));
        CTC_SAI_NTOH_V4(ipuc_info.ip.ipv4);
        ipuc_info.masklen = 32;       
    }
    else
    {
        sal_memcpy(&ipuc_info.ip.ipv6, &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(ipuc_info.ip.ipv6);
        ipuc_info.masklen = 128;
    }

    ipuc_info.nh_id = 2; //SDK reserverd to CPU nexthop
    //ipuc_info.route_flag |= CTC_IPUC_FLAG_SELF_ADDRESS;
    //ipuc_info.route_flag |= CTC_IPUC_FLAG_NEIGHBOR;

    ret = ctcs_ipuc_get(lchip, &ipuc_info);
    if(ret < 0)
    {
        //TBD, just return
        return status;
    }

    if(p_bfd_info->add_self_route_by_bfd)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_remove(lchip, &ipuc_info));
    }
    else
    {
        //Clear self address flag
        CTC_UNSET_FLAG(ipuc_info.route_flag, CTC_IPUC_FLAG_SELF_ADDRESS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_add(lchip, &ipuc_info));
    }

    return status;
}

static sai_status_t
_ctc_sai_bfd_wb_sync_cb1(uint8 lchip)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_status_t ret = 0;
    ctc_wb_data_t wb_data;
    ctc_sai_bfd_master_wb_t bfd_master_wb;
    
    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    
    CTC_WB_INIT_DATA_T((&wb_data),ctc_sai_bfd_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_BFD_GLOBAL);
    bfd_master_wb.lchip = lchip;
    bfd_master_wb.reroute_iloop_nhid = p_ctc_sai_bfd[lchip]->reroute_iloop_nhid;
    bfd_master_wb.reroute_l3if = p_ctc_sai_bfd[lchip]->reroute_l3if;
    bfd_master_wb.reroute_inner_port = p_ctc_sai_bfd[lchip]->reroute_inner_port;
    bfd_master_wb.use_global_res_info = p_ctc_sai_bfd[lchip]->use_global_res_info;

    sal_memcpy((uint8*)wb_data.buffer, (uint8*)&bfd_master_wb, sizeof(ctc_sai_bfd_master_wb_t));

    wb_data.valid_cnt = 1;
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);

done:
out:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return status;
}


static sai_status_t
_ctc_sai_bfd_wb_reload_cb1(uint8 lchip)
{
    sai_status_t ret = 0;
    ctc_wb_query_t wb_query;
    ctc_sai_bfd_master_wb_t bfd_master_wb;
    uint32 entry_cnt = 0;

    sal_memset(&bfd_master_wb, 0, sizeof(ctc_sai_bfd_master_wb_t));

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_bfd_master_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_BFD_GLOBAL);
    CTC_SAI_CTC_ERROR_GOTO(ctc_wb_query_entry(&wb_query), ret, out);

    if (wb_query.valid_cnt != 0)
    {
        sal_memcpy((uint8*)&bfd_master_wb, (uint8*)(wb_query.buffer)+entry_cnt*(wb_query.key_len + wb_query.data_len),
            (wb_query.key_len+wb_query.data_len));

        p_ctc_sai_bfd[lchip]->reroute_inner_port = bfd_master_wb.reroute_inner_port;
        p_ctc_sai_bfd[lchip]->reroute_l3if = bfd_master_wb.reroute_l3if;
        p_ctc_sai_bfd[lchip]->reroute_iloop_nhid = bfd_master_wb.reroute_iloop_nhid;
        p_ctc_sai_bfd[lchip]->use_global_res_info = bfd_master_wb.use_global_res_info;       
    }

    if(p_ctc_sai_bfd[lchip]->use_global_res_info)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_ctc_sai_bfd[lchip]->reroute_iloop_nhid));
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_ctc_sai_bfd[lchip]->reroute_l3if));
    }

out:    
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
            
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_bfd_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t sai_bfd_id = *(sai_object_id_t*)key;
    ctc_sai_bfd_t* p_bfd_info = (ctc_sai_bfd_t*)data;
    
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, sai_bfd_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_BFD, ctc_object_id.value));

    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && (p_bfd_info->hw_lookup_valid) && (4 == p_bfd_info->ip_hdr_ver))
    {
        /*do not need reload nexthop & l3if, use global */
    }
    else
    {
        if(p_bfd_info->inner_nhid)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_bfd_info->inner_nhid));
        }

        if(p_bfd_info->inner_l3if)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_bfd_info->inner_l3if));
        }
    }

    return SAI_STATUS_SUCCESS;
}


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_bfd_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  bfd_oid_cur = 0;
    ctc_sai_bfd_t    ctc_sai_bfd_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;

    char srcip[64] = {'-'};
    char dstip[64] = {'-'};
    char ip_mask[64] = {'-'};
    sai_ip_address_t ip_addr;
    char srcmac_buf[20] ={0};
    char dstmac_buf[20] ={0};

    sal_memset(&ctc_sai_bfd_cur, 0, sizeof(ctc_sai_bfd_t));

    bfd_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_bfd_t*)(&ctc_sai_bfd_cur), bucket_data->data, sizeof(ctc_sai_bfd_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bfd_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    if((*((sai_bfd_encapsulation_type_t*)p_cb_data->value3) == ctc_sai_bfd_cur.encap_type)
         && ( SAI_BFD_ENCAPSULATION_TYPE_NONE == ctc_sai_bfd_cur.encap_type))
    {
        //IP BFD
        sal_memset(&ip_addr, 0, sizeof(sai_ip_address_t));
        sal_memcpy(&(ip_addr), &(ctc_sai_bfd_cur.src_ip_addr), sizeof(sai_ip_address_t));
        ctc_sai_get_ip_str(&ip_addr, srcip);
        sal_sprintf(ip_mask, "/%d", 32);
        sal_strcat(srcip, ip_mask);

        sal_memset(&ip_addr, 0, sizeof(sai_ip_address_t));
        sal_memcpy(&(ip_addr), &(ctc_sai_bfd_cur.src_ip_addr), sizeof(sai_ip_address_t));
        ctc_sai_get_ip_str(&ip_addr, dstip);
        sal_sprintf(ip_mask, "/%d", 32);
        sal_strcat(dstip, ip_mask);

        ctc_sai_get_mac_str(ctc_sai_bfd_cur.src_mac, srcmac_buf);
        ctc_sai_get_mac_str(ctc_sai_bfd_cur.dst_mac, dstmac_buf);
    
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-12d %-12d %-12d %-12d 0x%016"PRIx64 " %-12d %-12d %-12d %-12d %-12d %-22s %-22s 0x%016"PRIx64 "  %-20s %-20s\n",\
            num_cnt, bfd_oid_cur, ctc_sai_bfd_cur.session_type, ctc_sai_bfd_cur.offload_type, ctc_sai_bfd_cur.local_mep_index, ctc_sai_bfd_cur.remote_mep_index,
            ctc_sai_bfd_cur.hw_lookup_valid, ctc_sai_bfd_cur.vr_oid, ctc_sai_bfd_cur.udp_src_port, ctc_sai_bfd_cur.echo_en, ctc_sai_bfd_cur.ip_hdr_ver,
            ctc_sai_bfd_cur.ip_tos, ctc_sai_bfd_cur.ip_ttl, srcip, dstip, ctc_sai_bfd_cur.dst_port_oid, srcmac_buf, dstmac_buf);
    }

    if((*((sai_bfd_encapsulation_type_t*)p_cb_data->value3) == ctc_sai_bfd_cur.encap_type)
         && ( SAI_BFD_ENCAPSULATION_TYPE_MPLS == ctc_sai_bfd_cur.encap_type))
    {
        //IP BFD
        sal_memset(&ip_addr, 0, sizeof(sai_ip_address_t));
        sal_memcpy(&(ip_addr), &(ctc_sai_bfd_cur.src_ip_addr), sizeof(sai_ip_address_t));
        ctc_sai_get_ip_str(&ip_addr, srcip);
        sal_sprintf(ip_mask, "/%d", 32);
        sal_strcat(srcip, ip_mask);

        sal_memset(&ip_addr, 0, sizeof(sai_ip_address_t));
        sal_memcpy(&(ip_addr), &(ctc_sai_bfd_cur.src_ip_addr), sizeof(sai_ip_address_t));
        ctc_sai_get_ip_str(&ip_addr, dstip);
        sal_sprintf(ip_mask, "/%d", 32);
        sal_strcat(dstip, ip_mask);

        ctc_sai_get_mac_str(ctc_sai_bfd_cur.src_mac, srcmac_buf);
        ctc_sai_get_mac_str(ctc_sai_bfd_cur.dst_mac, dstmac_buf);
    
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d %-12d 0x%016"PRIx64 " 0x%016"PRIx64 "\n",\
            num_cnt, bfd_oid_cur, ctc_sai_bfd_cur.session_type, ctc_sai_bfd_cur.offload_type, ctc_sai_bfd_cur.local_mep_index, ctc_sai_bfd_cur.remote_mep_index,
            ctc_sai_bfd_cur.udp_src_port, ctc_sai_bfd_cur.echo_en, ctc_sai_bfd_cur.mpls_bfd_type, ctc_sai_bfd_cur.ach_header_valid, ctc_sai_bfd_cur.ach_channel_type,
            ctc_sai_bfd_cur.mpls_in_label, ctc_sai_bfd_cur.cv_en, ctc_sai_bfd_cur.section_rif_oid, ctc_sai_bfd_cur.nh_tunnel_oid);
    }

    

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________
void ctc_sai_bfd_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sai_bfd_encapsulation_type_t bfd_encap_type = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI BFD MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_BFD_SESSION))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "BFD");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_bfd_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------- IP BFD ----------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-12s %-12s %-12s %-12s %-18s %-12s %-12s %-12s %-12s %-12s %-22s %-22s %-18s %-20s %-20s \n", \
            "No.", "Bfd_oid", "Session Type", "OffloadType", "lmepIndex", "rmepIndex", "hwlookup", "vr_oid", "udpsrcport", \
            "echo en", "iphdrver", "iptos", "ipttl", "srcip", "dstip", "dstportoid", "srcmac", "dstmac");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        bfd_encap_type = SAI_BFD_ENCAPSULATION_TYPE_NONE;
        sai_cb_data.value3 = &bfd_encap_type;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BFD_SESSION,
                                            (hash_traversal_fn)_ctc_sai_bfd_dump_print_cb, (void*)(&sai_cb_data));


        CTC_SAI_LOG_DUMP(p_file, "%s\n", "------------------------------------------- MPLS/TP BFD ----------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-18s %-18s \n", \
            "No.", "Bfd_oid", "Session Type", "OffloadType", "lmepIndex", "rmepIndex", "udpsrcport", \
            "echo en", "mplsbfdtype", "achvalid", "achchantype", "mplsinlabel", "cven", "sectionrif", "nh_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        bfd_encap_type = SAI_BFD_ENCAPSULATION_TYPE_MPLS;
        sai_cb_data.value3 = &bfd_encap_type;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BFD_SESSION,
                                            (hash_traversal_fn)_ctc_sai_bfd_dump_print_cb, (void*)(&sai_cb_data));
    }
}

sai_status_t
ctc_sai_bfd_traverse_get_session_by_mepindex(uint8 lchip, uint32 mepindex, uint8 isremote, sai_object_id_t* session_id)
{
    ctc_sai_db_traverse_param_t bfd_cb;

    sal_memset(&bfd_cb, 0, sizeof(ctc_sai_db_traverse_param_t));

    bfd_cb.lchip = lchip;
    bfd_cb.value0 = (void*)&mepindex;
    bfd_cb.value1 = (void*)&isremote;
    bfd_cb.value4 = (void*)session_id;

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_BFD_SESSION, (hash_traversal_fn)_ctc_sai_bfd_traverse_get_session_cb, (void*)&bfd_cb);
    return SAI_STATUS_SUCCESS;
}



sai_status_t
ctc_sai_bfd_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_id_t bfd_session_id = 0;
    ctc_sai_bfd_t* p_bfd_info = NULL;
    ctc_object_id_t ctc_object_id;
    
    ctc_oam_mep_info_t  mep_info;
    ctc_oam_lmep_t lmep;
    ctc_oam_rmep_t rmep;
    ctc_oam_update_t  update_lmep;
    uint8 lmep_upd_en = 0, rmep_upd_en = 0;
    ctc_oam_bfd_timer_t oam_bfd_timer;
    ctc_oam_hw_aps_t  oam_aps;

    ctc_sai_virtual_router_t* p_vr_info = NULL;
    uint16 ctc_vrf_id = 0;
    ctc_l3if_property_t l3if_prop;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&mep_info, 0, sizeof(ctc_oam_mep_info_t));
    sal_memset(&lmep, 0, sizeof(ctc_oam_lmep_t));
    sal_memset(&rmep, 0, sizeof(ctc_oam_rmep_t));
    sal_memset(&update_lmep, 0, sizeof(ctc_oam_update_t));
    sal_memset(&oam_bfd_timer, 0, sizeof(ctc_oam_bfd_timer_t));
    sal_memset(&oam_aps, 0, sizeof(ctc_oam_hw_aps_t));

    bfd_session_id = key->key.object_id;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(key->key.object_id, &lchip));

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    CTC_SAI_LOG_INFO(SAI_API_BFD, "bfd_session_id = %llu\n", bfd_session_id);

    p_bfd_info = ctc_sai_db_get_object_property(lchip, bfd_session_id);
    if (NULL == p_bfd_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "Failed to set bfd session, invalid bfd_session_id %d!\n", bfd_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    mep_info.mep_index = p_bfd_info->remote_mep_index;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info(lchip, &mep_info), status, out); 

    CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_bfd_lkup_key_gen(lchip, p_bfd_info, &lmep, &rmep), status, out);

    sal_memcpy(&(update_lmep.key), &(lmep.key), sizeof(ctc_oam_key_t));

    switch(attr->id)
    {
        case SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER:
            if(!p_bfd_info->hw_lookup_valid)
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                goto out;
            }
            else
            {
                //Not suport set, only create
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                
                p_vr_info = ctc_sai_db_get_object_property(lchip, p_bfd_info->vr_oid);
                if (NULL == p_vr_info)
                {
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                ctc_sai_oid_get_vrf_id(p_bfd_info->vr_oid, &ctc_vrf_id);
                if(CTC_SAI_BFD_NH_TYPE_ILOOP == p_bfd_info->inner_nh_type)
                {
                    l3if_prop = CTC_L3IF_PROP_VRF_ID;
                    ctcs_l3if_set_property(lchip, p_bfd_info->inner_l3if, l3if_prop, (uint32)ctc_vrf_id);
                }
                else if(CTC_SAI_BFD_NH_TYPE_IP_TUNNEL == p_bfd_info->inner_nh_type)
                {
                    return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
                }
            }
            break;
        case SAI_BFD_SESSION_ATTR_PORT:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BFD_SESSION_ATTR_TC:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BFD_SESSION_ATTR_STATE:
            if(attr->value.s32 > SAI_BFD_SESSION_STATE_UP) 
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_STATE;
            update_lmep.update_value = attr->value.s32;
            lmep_upd_en = 1;
            break;
        case SAI_BFD_SESSION_ATTR_TOS:
            p_bfd_info->ip_tos = attr->value.u8;
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TX_COS_EXP;
            update_lmep.update_value = attr->value.u8 >> 3 ;
            lmep_upd_en = 1;
            break;
        case SAI_BFD_SESSION_ATTR_MPLS_EXP:
            p_bfd_info->mpls_exp = attr->value.u8;
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TX_COS_EXP;
            update_lmep.update_value = attr->value.u8;
            lmep_upd_en = 1;
            break;    
        case SAI_BFD_SESSION_ATTR_TTL:
            p_bfd_info->ip_ttl = attr->value.u8;
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TTL;
            update_lmep.update_value = attr->value.u8;
            lmep_upd_en = 1;
        case SAI_BFD_SESSION_ATTR_MPLS_TTL:
            p_bfd_info->mpls_ttl = attr->value.u8;
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TTL;
            update_lmep.update_value = attr->value.u8;
            lmep_upd_en = 1;
            break;   
        case SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS:
            //TODO
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS:
            //TODO
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;
        case SAI_BFD_SESSION_ATTR_MIN_TX:
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TX_TIMER;
            oam_bfd_timer.min_interval = attr->value.u32 & 0xFF;
            oam_bfd_timer.detect_mult = mep_info.lmep.bfd_lmep.local_detect_mult;
            update_lmep.p_update_value = &oam_bfd_timer;
            
            lmep_upd_en = 1;
            break;
        case SAI_BFD_SESSION_ATTR_MIN_RX:
            update_lmep.is_local = 0;
            update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_RX_TIMER;
            oam_bfd_timer.min_interval = attr->value.u32 & 0xFF;
            oam_bfd_timer.detect_mult = mep_info.rmep.bfd_rmep.remote_detect_mult;
            update_lmep.p_update_value = &oam_bfd_timer;
            
            rmep_upd_en = 1;
            break;    
        case SAI_BFD_SESSION_ATTR_MULTIPLIER:
            update_lmep.is_local = 1;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_TX_TIMER;
            oam_bfd_timer.min_interval = mep_info.lmep.bfd_lmep.desired_min_tx_interval;
            oam_bfd_timer.detect_mult = attr->value.u8;     
            update_lmep.p_update_value = &oam_bfd_timer;
            
            lmep_upd_en = 1;
            break;   
        case SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
            update_lmep.is_local = 1;
            p_bfd_info->cv_en = attr->value.booldata;
            update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_CV_EN;
            update_lmep.update_value = attr->value.booldata;
            lmep_upd_en = 1;
            break;     
        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
            if(SAI_NULL_OBJECT_ID == attr->value.oid)
            {
                //enable hw aps
                update_lmep.is_local = 0;
                update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS_EN;
                update_lmep.p_update_value = NULL;
                update_lmep.update_value = 0;

                rmep_upd_en = 1;

                p_bfd_info->hw_binding_aps_en = 0;
                p_bfd_info->hw_binding_aps_group = SAI_NULL_OBJECT_ID;
            }
            else
            {
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, attr->value.oid, &ctc_object_id);
                if( SAI_NEXT_HOP_GROUP_TYPE_PROTECTION != ctc_object_id.sub_type)
                {
                    status = SAI_STATUS_INVALID_OBJECT_TYPE;
                    goto out;
                }
                p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, attr->value.oid);
                if(NULL == p_next_hop_grp_info)
                {
                    status = SAI_STATUS_ITEM_NOT_FOUND;
                    goto out;
                }
            
                p_bfd_info->hw_binding_aps_group = attr->value.oid;
                
                update_lmep.is_local = 0;
                update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS;
                            
                ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, p_bfd_info->hw_binding_aps_group, &ctc_object_id);
                oam_aps.aps_group_id = ctc_object_id.value2;
                oam_aps.protection_path = p_bfd_info->hw_binding_is_protecting_path;
                update_lmep.p_update_value = &oam_aps;
                                
                rmep_upd_en = 1;
                
            }
            break;
        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:   
            if( SAI_NULL_OBJECT_ID == p_bfd_info->hw_binding_aps_group)
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                goto out;
            }
            p_bfd_info->hw_binding_is_protecting_path = attr->value.booldata;
            
            update_lmep.is_local = 0;
            update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS;
                        
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, p_bfd_info->hw_binding_aps_group, &ctc_object_id);
            oam_aps.aps_group_id = ctc_object_id.value2;
            oam_aps.protection_path = p_bfd_info->hw_binding_is_protecting_path;
            update_lmep.p_update_value = &oam_aps;
            rmep_upd_en = 1;
            break;

        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:   
            if( SAI_NULL_OBJECT_ID == p_bfd_info->hw_binding_aps_group)
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0;
                goto out;
            }
            p_bfd_info->hw_binding_aps_en = attr->value.booldata;
            
            //enable hw aps
            update_lmep.is_local = 0;
            update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS_EN;
            update_lmep.p_update_value = NULL;
            update_lmep.update_value = p_bfd_info->hw_binding_aps_en;
            
            rmep_upd_en = 1;
            break;
        
        default:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            break;

    }

    if(lmep_upd_en)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, out);
    }
    else if(rmep_upd_en)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_rmep(lchip, &update_lmep), status, out);
    }
    
out:    
    return status;
}

sai_status_t
ctc_sai_bfd_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_bfd_t* p_bfd_info = NULL;
    ctc_oam_mep_info_t  mep_info;

    sai_object_id_t vr_obj_id = 0;
    uint32 ctc_vrf_id = 0;
    ctc_l3if_property_t l3if_prop;

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BFD_SESSION, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;

    p_bfd_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_bfd_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset((void*)&mep_info, 0, sizeof(ctc_oam_mep_info_t));
    mep_info.mep_index = p_bfd_info->remote_mep_index;
    //mep_info.is_rmep = 1;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_get_mep_info(lchip, &mep_info), status, out);    

    switch(attr->id)
    {
        case SAI_BFD_SESSION_ATTR_TYPE:
            attr->value.s32 = p_bfd_info->session_type;
            break;
        case SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
            attr->value.booldata = p_bfd_info->hw_lookup_valid;
            break;
        case SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER:
            if(!p_bfd_info->hw_lookup_valid)
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
                goto out;
            }
            else
            {
                if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && p_ctc_sai_bfd[lchip]->use_global_res_info)
                {
                    attr->value.oid = p_bfd_info->vr_oid;
                }
                else
                {
                    if(CTC_SAI_BFD_NH_TYPE_ILOOP == p_bfd_info->inner_nh_type)
                    {
                        l3if_prop = CTC_L3IF_PROP_VRF_ID;
                        ctcs_l3if_get_property(lchip, p_bfd_info->inner_l3if, l3if_prop, &ctc_vrf_id);
                        vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, ctc_vrf_id);
                        attr->value.oid = vr_obj_id;
                    }
                    else if(CTC_SAI_BFD_NH_TYPE_IP_TUNNEL == p_bfd_info->inner_nh_type)
                    {
                        status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
                    }
                }
            }
            break;
        case SAI_BFD_SESSION_ATTR_PORT:
            attr->value.oid = p_bfd_info->dst_port_oid;
            break;
        case SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
            attr->value.u32 = mep_info.lmep.bfd_lmep.local_discr;
            break;
        case SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
            attr->value.u32 = mep_info.rmep.bfd_rmep.remote_discr;
            break;
        case SAI_BFD_SESSION_ATTR_UDP_SRC_PORT:
            attr->value.u32 = p_bfd_info->udp_src_port;
            break;
        case SAI_BFD_SESSION_ATTR_TC:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
        case SAI_BFD_SESSION_ATTR_TOS:
            attr->value.u8 = p_bfd_info->ip_tos;
            break;
        case SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE:
            attr->value.s32 = p_bfd_info->encap_type;
            break;
        case SAI_BFD_SESSION_ATTR_IPHDR_VERSION:
            attr->value.u8 = p_bfd_info->ip_hdr_ver;
            break;
        case SAI_BFD_SESSION_ATTR_TTL:
            attr->value.u8 = p_bfd_info->ip_ttl;
            break;
        case SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS:
            sal_memcpy(&(attr->value.ipaddr), &(p_bfd_info->src_ip_addr), sizeof(sai_ip_address_t));
            break;
        case SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS:
            sal_memcpy(&(attr->value.ipaddr), &(p_bfd_info->dst_ip_addr), sizeof(sai_ip_address_t));
            break;
        case SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS:
            sal_memcpy(&(attr->value.mac), &(p_bfd_info->src_mac), sizeof(sai_mac_t));
            break;
        case SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS:
            sal_memcpy(&(attr->value.mac), &(p_bfd_info->dst_mac), sizeof(sai_mac_t));
            break;
        case SAI_BFD_SESSION_ATTR_MULTIHOP:
            attr->value.booldata = !mep_info.lmep.bfd_lmep.single_hop;
            break;
        case SAI_BFD_SESSION_ATTR_MIN_TX:
            attr->value.u32 = mep_info.lmep.bfd_lmep.desired_min_tx_interval;
            break;
        case SAI_BFD_SESSION_ATTR_MIN_RX:
            attr->value.u32 = mep_info.rmep.bfd_rmep.required_min_rx_interval;
            break;
        case SAI_BFD_SESSION_ATTR_MULTIPLIER:
            attr->value.u8 = mep_info.lmep.bfd_lmep.local_detect_mult;
            break;
        case SAI_BFD_SESSION_ATTR_STATE:
            if ( CTC_OAM_BFD_STATE_DOWN == mep_info.lmep.bfd_lmep.loacl_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_DOWN;
            }
            else if ( CTC_OAM_BFD_STATE_INIT == mep_info.lmep.bfd_lmep.loacl_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_INIT;
            }
            else if ( CTC_OAM_BFD_STATE_UP == mep_info.lmep.bfd_lmep.loacl_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_UP;
            }
            else if ( CTC_OAM_BFD_STATE_ADMIN_DOWN == mep_info.lmep.bfd_lmep.loacl_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_ADMIN_DOWN;
            }            
            
            break;
        case SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE:
            attr->value.s32 = p_bfd_info->offload_type;
            break;
        case SAI_BFD_SESSION_ATTR_NEGOTIATED_TX:
            attr->value.u32 = mep_info.lmep.bfd_lmep.actual_tx_interval;
            break;
        case SAI_BFD_SESSION_ATTR_NEGOTIATED_RX:
            attr->value.u32 = mep_info.rmep.bfd_rmep.actual_rx_interval;
            break;
        case SAI_BFD_SESSION_ATTR_LOCAL_DIAG:
            attr->value.u8 = mep_info.lmep.bfd_lmep.local_diag;
            break;
        case SAI_BFD_SESSION_ATTR_REMOTE_DIAG:
            attr->value.u8 = mep_info.rmep.bfd_rmep.remote_diag;
            break;
        case SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER:
            attr->value.u8 = mep_info.rmep.bfd_rmep.remote_detect_mult;
            break;
        case SAI_BFD_SESSION_ATTR_BFD_MPLS_TYPE:
            attr->value.s32 = p_bfd_info->mpls_bfd_type;
            break;
        case SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
            attr->value.booldata = p_bfd_info->ach_header_valid;
            break;
        case SAI_BFD_SESSION_ATTR_BFD_ACH_CHANNEL_TYPE:
            if (p_bfd_info->ach_header_valid)
            {
                attr->value.s32 = p_bfd_info->ach_channel_type;
            }
            else
            {
                status = SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
            }
            break;
        case SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
            attr->value.u32 = p_bfd_info->mpls_in_label;
            break;
        case SAI_BFD_SESSION_ATTR_MPLS_TTL:
            attr->value.u8 = p_bfd_info->mpls_ttl;
            break;
        case SAI_BFD_SESSION_ATTR_MPLS_EXP:
            attr->value.u8 = p_bfd_info->mpls_exp;
            break;
        case SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
            attr->value.booldata = p_bfd_info->cv_en;
            break;
        case SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID:
            sal_memcpy(attr->value.chardata, mep_info.lmep.bfd_lmep.mep_id, p_bfd_info->mep_id_len);
            break;
        case SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID:
            attr->value.oid = p_bfd_info->section_rif_oid;
            break;
        case SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
            attr->value.booldata = p_bfd_info->without_gal;
            break;
        case SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
            attr->value.oid = p_bfd_info->nh_tunnel_oid;
            break;
        case SAI_BFD_SESSION_ATTR_REMOTE_STATE:
            if ( CTC_OAM_BFD_STATE_DOWN == mep_info.rmep.bfd_rmep.remote_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_DOWN;
            }
            else if ( CTC_OAM_BFD_STATE_INIT == mep_info.rmep.bfd_rmep.remote_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_INIT;
            }
            else if ( CTC_OAM_BFD_STATE_UP == mep_info.rmep.bfd_rmep.remote_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_UP;
            }
            else if ( CTC_OAM_BFD_STATE_ADMIN_DOWN == mep_info.rmep.bfd_rmep.remote_state)
            {
                attr->value.s32 = SAI_BFD_SESSION_STATE_ADMIN_DOWN;
            }    
            break;
        case SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX:
        case SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
            attr->value.oid = p_bfd_info->hw_binding_aps_group;
            break;
        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
            attr->value.booldata = p_bfd_info->hw_binding_is_protecting_path;
            break;
        case SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
            attr->value.booldata = p_bfd_info->hw_binding_aps_en;
            break;
        default:
            status = SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;

    }

out:
    return status;
}


static ctc_sai_attr_fn_entry_t  bfd_attr_fn_entries[] =
{
    { SAI_BFD_SESSION_ATTR_TYPE,
      ctc_sai_bfd_get_info,
      NULL},
    { SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info},
    { SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_PORT,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info }, 
    { SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_UDP_SRC_PORT,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TC,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_VLAN_TPID,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_VLAN_ID,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_VLAN_PRI,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_VLAN_CFI,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_VLAN_HEADER_VALID,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_IPHDR_VERSION,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TOS,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TTL,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_TUNNEL_TOS,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_TUNNEL_TTL,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_TUNNEL_SRC_IP_ADDRESS,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_TUNNEL_DST_IP_ADDRESS,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_ECHO_ENABLE,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_MULTIHOP,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_CBIT,
      NULL,
      NULL },
    { SAI_BFD_SESSION_ATTR_MIN_TX,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_MIN_RX,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_MULTIPLIER,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_REMOTE_MIN_TX,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_REMOTE_MIN_RX,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_STATE,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_NEGOTIATED_TX,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_NEGOTIATED_RX,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_LOCAL_DIAG,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_REMOTE_DIAG,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_REMOTE_STATE,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_BFD_MPLS_TYPE,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_BFD_ACH_CHANNEL_TYPE,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_MPLS_TTL,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_MPLS_EXP,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TP_CV_ENABLE,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID,
      ctc_sai_bfd_get_info,
      NULL },
    { SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL,
      ctc_sai_bfd_get_info,
      NULL },  
    { SAI_BFD_SESSION_ATTR_NEXT_HOP_ID,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },
    { SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN,
      ctc_sai_bfd_get_info,
      ctc_sai_bfd_set_info },      
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};


#define ________SAI_API________

sai_status_t ctc_sai_bfd_create_bfd_session( sai_object_id_t      * sai_bfd_session_id,
                                      sai_object_id_t        switch_id,
                                      uint32_t               attr_count,
                                      const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_id_t bfd_obj_id = 0;
    ctc_sai_bfd_t* p_bfd_info = NULL;
    uint32 bfd_session_id = 0;
    const sai_attribute_value_t *attr_value;
    uint32 index = 0;
    uint32 local_disc = 0, remote_disc = 0;
    uint32 udp_src_port = 0;
    uint8 is_single_hop = 0;
    char mep_id[SAI_BFD_CV_SIZE] = {0};
    ctc_sai_router_interface_t* p_rif_info = NULL;
    uint16 l3if_id = 0;
    uint32 nh_id = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;
    ctc_sai_next_hop_grp_t* p_next_hop_grp_info = NULL;

    ctc_oam_lmep_t lmep;
    ctc_oam_bfd_lmep_t* p_bfd_lmep  = NULL;
    ctc_oam_rmep_t rmep;
    ctc_oam_bfd_rmep_t* p_bfd_rmep  = NULL;

    ctc_oam_update_t update_lmep;
    ctc_oam_hw_aps_t  oam_aps;
    
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    
    sal_memset(&lmep, 0, sizeof(ctc_oam_lmep_t));
    p_bfd_lmep = &lmep.u.bfd_lmep;
    
    sal_memset(&rmep, 0, sizeof(ctc_oam_rmep_t));
    p_bfd_rmep = &rmep.u.bfd_rmep;

    sal_memset(&update_lmep, 0, sizeof(ctc_oam_update_t));
    sal_memset(&oam_aps, 0, sizeof(ctc_oam_hw_aps_t));

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    CTC_SAI_PTR_VALID_CHECK(sai_bfd_session_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_bfd_create_attr_check(lchip, attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_BFD, &bfd_session_id), status, out);
    
    bfd_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BFD_SESSION, lchip, 0, 0, bfd_session_id);
    CTC_SAI_LOG_INFO(SAI_API_BFD, "create bfd_obj_id = 0x%"PRIx64"\n", bfd_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_bfd_build_db(lchip, bfd_obj_id, &p_bfd_info), status, error1);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->session_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->hw_lookup_valid = attr_value->booldata;
    }
    else
    {
        p_bfd_info->hw_lookup_valid = 1;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->vr_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_PORT, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->dst_port_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        local_disc = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        remote_disc = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_UDP_SRC_PORT, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        udp_src_port = attr_value->u32;
        p_bfd_info->udp_src_port = udp_src_port;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->encap_type = attr_value->s32;
    }

    /*IP hdr */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_IPHDR_VERSION, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->ip_hdr_ver = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TOS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->ip_tos = attr_value->u8;
    }
    else
    {
        /*default 0 */
        p_bfd_info->ip_tos = 0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TTL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->ip_ttl = attr_value->u8;
    }
    else
    {
        /*default 255 */
        p_bfd_info->ip_ttl = 255;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&(p_bfd_info->src_ip_addr), &(attr_value->ipaddr), sizeof(sai_ip_address_t));
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&(p_bfd_info->dst_ip_addr), &(attr_value->ipaddr), sizeof(sai_ip_address_t));
    }

    /*Tunnel header, TBD */

    /*MAC hdr */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&(p_bfd_info->src_mac), &(attr_value->mac), sizeof(sai_mac_t));
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        sal_memcpy(&(p_bfd_info->dst_mac), &(attr_value->mac), sizeof(sai_mac_t));
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_ECHO_ENABLE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->echo_en = attr_value->booldata;
    }

    /*BFD configuration */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->offload_type = attr_value->s32;
    }
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MULTIHOP, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        is_single_hop = !attr_value->booldata;
    }
    else
    {
        is_single_hop = 1;
    }        

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MIN_TX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_lmep->desired_min_tx_interval = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MIN_RX, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_rmep->required_min_rx_interval = attr_value->u32;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MULTIPLIER, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_lmep->local_detect_mult = attr_value->u8;
    }

    /*Encapsulation type */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_MPLS_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->mpls_bfd_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->ach_header_valid = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_BFD_ACH_CHANNEL_TYPE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->ach_channel_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->mpls_in_label = attr_value->u32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MPLS_TTL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->mpls_ttl = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_MPLS_EXP, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->mpls_exp = attr_value->u8;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_CV_ENABLE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->cv_en = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        /*TLV length + Type & Length */
        p_bfd_info->mep_id_len = (attr_value->chardata[3] + 4);
        sal_memcpy(mep_id, attr_value->chardata,  p_bfd_info->mep_id_len);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->section_rif_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->without_gal = attr_value->booldata;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_NEXT_HOP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        p_bfd_info->nh_tunnel_oid = attr_value->oid;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, attr_value->oid, &ctc_object_id);
        if( SAI_NEXT_HOP_GROUP_TYPE_PROTECTION != ctc_object_id.sub_type)
        {
            status = SAI_STATUS_INVALID_OBJECT_TYPE;
            goto error2;
        }
        p_next_hop_grp_info = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if(NULL == p_next_hop_grp_info)
        {
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error2;
        }
        p_bfd_info->hw_binding_aps_group = attr_value->oid;     
    }
    
    if(p_bfd_info->hw_binding_aps_group)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {
            p_bfd_info->hw_binding_is_protecting_path = attr_value->booldata;
        }
        else
        {
            p_bfd_info->hw_binding_is_protecting_path = 0;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {
            p_bfd_info->hw_binding_aps_en = attr_value->booldata;
        }
        else
        {
            p_bfd_info->hw_binding_aps_en = 0;
        }
    }


    /*IP BFD */
    if( SAI_BFD_ENCAPSULATION_TYPE_NONE == p_bfd_info->encap_type)
    {
        /*Micro BFD */
        if(!p_bfd_info->hw_lookup_valid && (SAI_NULL_OBJECT_ID != p_bfd_info->dst_port_oid))
        {
            lmep.key.mep_type = CTC_OAM_MEP_TYPE_MICRO_BFD;
            rmep.key.mep_type = CTC_OAM_MEP_TYPE_MICRO_BFD;
        }
        else
        {
            lmep.key.mep_type = CTC_OAM_MEP_TYPE_IP_BFD;  
            rmep.key.mep_type = CTC_OAM_MEP_TYPE_IP_BFD;
        }
        lmep.key.u.bfd.discr = local_disc;
        rmep.key.u.bfd.discr = local_disc;
        p_bfd_rmep->remote_discr = remote_disc;
        
        if(is_single_hop)
        {
            CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_IP_SINGLE_HOP);
        }

        p_bfd_lmep->bfd_src_port = udp_src_port;
        if(4 == p_bfd_info->ip_hdr_ver)
        {
            CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_IPV4_ENCAP);
            sal_memcpy(&p_bfd_lmep->ip4_sa, &(p_bfd_info->src_ip_addr.addr.ip4), sizeof(sai_ip4_t));
            CTC_SAI_NTOH_V4(p_bfd_lmep->ip4_sa);

            sal_memcpy(&p_bfd_lmep->ip4_da, &(p_bfd_info->dst_ip_addr.addr.ip4), sizeof(sai_ip4_t));
            CTC_SAI_NTOH_V4(p_bfd_lmep->ip4_da);
        }
        else if(6 == p_bfd_info->ip_hdr_ver)
        {
            /* use reroute
            CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_IPV6_ENCAP);
            sal_memcpy(&p_bfd_lmep->ipv6_sa, &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(sai_ip6_t));
            CTC_SAI_NTOH_V6(p_bfd_lmep->ipv6_sa);

            sal_memcpy(&p_bfd_lmep->ipv6_da, &(p_bfd_info->dst_ip_addr.addr.ip6), sizeof(sai_ip6_t));
            CTC_SAI_NTOH_V6(p_bfd_lmep->ipv6_da);
            */
        }

        //do not do rollback, in case del local ipuc as mistake
        CTC_SAI_ERROR_GOTO(_ctc_sai_bfd_add_local_ipuc(lchip, p_bfd_info), status, error2);

        p_bfd_lmep->ttl = p_bfd_info->ip_ttl;
        p_bfd_lmep->tx_cos_exp = (p_bfd_info->ip_tos >> 3);

        if(SAI_NULL_OBJECT_ID != p_bfd_info->nh_tunnel_oid)
        {
            
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_bfd_info->nh_tunnel_oid, &ctc_object_id);
            if( SAI_OBJECT_TYPE_NEXT_HOP != ctc_object_id.type)
            {
                status = SAI_STATUS_INVALID_OBJECT_TYPE;
                goto error2;
            }
            else
            {
                p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_bfd_info->nh_tunnel_oid);
                if(NULL == p_next_hop_info)
                {
                    status = SAI_STATUS_ITEM_NOT_FOUND;
                    goto error2;
                }
                nh_id = ctc_object_id.value;
            }
        }
        else
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_bfd_build_ipbfd_nh(lchip, p_bfd_info, &nh_id), status, error2);
        }

        p_bfd_lmep->nhid = nh_id;

    }
    else if ( SAI_BFD_ENCAPSULATION_TYPE_MPLS == p_bfd_info->encap_type)
    {
        /*MPLS BFD */
        if( SAI_BFD_MPLS_TYPE_NORMAL == p_bfd_info->mpls_bfd_type)
        {
            lmep.key.mep_type = CTC_OAM_MEP_TYPE_MPLS_BFD;
            lmep.key.u.bfd.discr = local_disc;
            rmep.key.mep_type = CTC_OAM_MEP_TYPE_MPLS_BFD;
            rmep.key.u.bfd.discr = local_disc;
            p_bfd_rmep->remote_discr = remote_disc;

            if (p_bfd_info->ach_header_valid)
            {
                if(SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW == p_bfd_info->ach_channel_type)
                {
                    CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_MPLS_PW_VCCV);
                }
                else if(SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4 == p_bfd_info->ach_channel_type)
                {
                    CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_MPLS_PW_VCCV_IPV4);
                }
                else if(SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6 == p_bfd_info->ach_channel_type)
                {
                    CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_MPLS_PW_VCCV_IPV6);
                }
            }
            p_bfd_lmep->mpls_in_label = p_bfd_info->mpls_in_label;
            p_bfd_lmep->bfd_src_port = udp_src_port;

            if(4 == p_bfd_info->ip_hdr_ver)
            {
                CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_IPV4_ENCAP);
                sal_memcpy(&p_bfd_lmep->ip4_sa, &(p_bfd_info->src_ip_addr.addr.ip4), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(p_bfd_lmep->ip4_sa);

                sal_memcpy(&p_bfd_lmep->ip4_da, &(p_bfd_info->dst_ip_addr.addr.ip4), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(p_bfd_lmep->ip4_da);
            }
            else if(6 == p_bfd_info->ip_hdr_ver)
            {                                
                CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_IPV6_ENCAP);
                sal_memcpy(&p_bfd_lmep->ipv6_sa, &(p_bfd_info->src_ip_addr.addr.ip6), sizeof(sai_ip6_t));
                CTC_SAI_NTOH_V6(p_bfd_lmep->ipv6_sa);

                sal_memcpy(&p_bfd_lmep->ipv6_da, &(p_bfd_info->dst_ip_addr.addr.ip6), sizeof(sai_ip6_t));
                CTC_SAI_NTOH_V6(p_bfd_lmep->ipv6_da);
            }

            p_bfd_lmep->ttl = p_bfd_info->mpls_ttl;
            p_bfd_lmep->tx_cos_exp = p_bfd_info->mpls_exp;

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_bfd_info->nh_tunnel_oid, &ctc_object_id);
            if( SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
            {
                p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_bfd_info->nh_tunnel_oid);
                if(NULL == p_next_hop_info)
                {
                    status = SAI_STATUS_ITEM_NOT_FOUND;
                    goto error2;
                }
                p_bfd_lmep->nhid = ctc_object_id.value;
            }
            else if( SAI_OBJECT_TYPE_TUNNEL == ctc_object_id.type)
            {
                /*get nh from tunnel db */
            }
            else
            {
                status = SAI_STATUS_INVALID_OBJECT_TYPE;
                goto error2;
            }
                           
        }
        else if( SAI_BFD_MPLS_TYPE_TP == p_bfd_info->mpls_bfd_type) /*TP BFD */
        {
            lmep.key.mep_type = CTC_OAM_MEP_TYPE_MPLS_TP_BFD;
            rmep.key.mep_type = CTC_OAM_MEP_TYPE_MPLS_TP_BFD;

            if(SAI_NULL_OBJECT_ID != p_bfd_info->section_rif_oid)
            {
                p_rif_info = ctc_sai_db_get_object_property(lchip, p_bfd_info->section_rif_oid);
                if (NULL == p_rif_info)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_BFD, "Failed to get route interface, invalid router_interface_id %d!\n", p_bfd_info->section_rif_oid);
                    status = SAI_STATUS_ITEM_NOT_FOUND;
                    goto error2;
                }
    
                CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_l3if_id(p_bfd_info->section_rif_oid, &l3if_id), status, error2);
                
                CTC_SET_FLAG(lmep.key.flag, CTC_OAM_KEY_FLAG_LINK_SECTION_OAM);                
                lmep.key.u.tp.gport_or_l3if_id = l3if_id;

                CTC_SET_FLAG(rmep.key.flag, CTC_OAM_KEY_FLAG_LINK_SECTION_OAM);
                rmep.key.u.tp.gport_or_l3if_id = l3if_id;
            }
            else
            {
                lmep.key.u.tp.label = p_bfd_info->mpls_in_label;
                rmep.key.u.tp.label = p_bfd_info->mpls_in_label;
            }

            p_bfd_lmep->local_discr = local_disc;
            p_bfd_rmep->remote_discr = remote_disc;

            p_bfd_lmep->ttl = p_bfd_info->mpls_ttl;
            p_bfd_lmep->tx_cos_exp = p_bfd_info->mpls_exp;

            if(p_bfd_info->without_gal)
            {
                CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_WITHOUT_GAL);
            }

            if(p_bfd_info->cv_en)
            {
                CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_TP_WITH_MEP_ID);
                p_bfd_lmep->mep_id_len = p_bfd_info->mep_id_len;
                sal_memcpy(p_bfd_lmep->mep_id, mep_id, p_bfd_info->mep_id_len);

                CTC_SET_FLAG(p_bfd_rmep->flag, CTC_OAM_BFD_RMEP_FLAG_TP_WITH_MEP_ID);
                p_bfd_rmep->mep_id_len = p_bfd_info->mep_id_len;
                sal_memcpy(p_bfd_rmep->mep_id, mep_id, p_bfd_info->mep_id_len);
            }

            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, p_bfd_info->nh_tunnel_oid, &ctc_object_id);
            if( SAI_OBJECT_TYPE_NEXT_HOP == ctc_object_id.type)
            {
                p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_bfd_info->nh_tunnel_oid);
                if(NULL == p_next_hop_info)
                {
                    status = SAI_STATUS_ITEM_NOT_FOUND;
                    goto error2;
                }
                p_bfd_lmep->nhid = ctc_object_id.value;
            }
            else if( SAI_OBJECT_TYPE_TUNNEL == ctc_object_id.type)
            {
                /*get nh from tunnel db */
            }
            else
            {
                status = SAI_STATUS_INVALID_OBJECT_TYPE;
                goto error2;
            }                        
        }
        
    }

    CTC_SET_FLAG(p_bfd_lmep->flag, CTC_OAM_BFD_LMEP_FLAG_MEP_EN);
    CTC_SET_FLAG(p_bfd_rmep->flag, CTC_OAM_BFD_RMEP_FLAG_MEP_EN);
    p_bfd_lmep->local_state = 1; //Down
    p_bfd_lmep->local_diag = 0;

    p_bfd_rmep->remote_state = 1; //Down
    p_bfd_rmep->remote_diag = 0;
    p_bfd_rmep->remote_detect_mult = 3; //by default
    

    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_add_lmep(lchip, &lmep), status, error3);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_add_rmep(lchip, &rmep), status, error4);

    p_bfd_info->local_mep_index = lmep.lmep_index;
    p_bfd_info->remote_mep_index = rmep.rmep_index;

    sal_memcpy(&(update_lmep.key), &(lmep.key), sizeof(ctc_oam_key_t));
    
    update_lmep.is_local = 1;
    update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_CC_EN;
    update_lmep.update_value = 1;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, error5);
    
    if(p_bfd_info->cv_en)
    {
        update_lmep.update_type = CTC_OAM_BFD_LMEP_UPDATE_TYPE_CV_EN;
        update_lmep.update_value = 1;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_lmep(lchip, &update_lmep), status, error5);
    }    

    if(p_bfd_info->hw_binding_aps_group)
    {
        //configure hw aps group and is protecting path
        update_lmep.is_local = 0;
        update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS;
        
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, p_bfd_info->hw_binding_aps_group, &ctc_object_id);
        oam_aps.aps_group_id = ctc_object_id.value2;
        oam_aps.protection_path = p_bfd_info->hw_binding_is_protecting_path;
        update_lmep.p_update_value = &oam_aps;
        
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_rmep(lchip, &update_lmep), status, error5);

        //enable hw aps
        update_lmep.is_local = 0;
        update_lmep.update_type = CTC_OAM_BFD_RMEP_UPDATE_TYPE_HW_APS_EN;
        update_lmep.p_update_value = NULL;
        update_lmep.update_value = p_bfd_info->hw_binding_aps_en;
        
        CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_update_rmep(lchip, &update_lmep), status, error5);
    }

    *sai_bfd_session_id = bfd_obj_id;    

    goto out;

error5:
    CTC_SAI_LOG_ERROR(SAI_API_BFD, "rollback to error5\n");
    ctcs_oam_remove_rmep(lchip, &rmep);
error4:
    CTC_SAI_LOG_ERROR(SAI_API_BFD, "rollback to error4\n");
    ctcs_oam_remove_lmep(lchip, &lmep);
error3:
    CTC_SAI_LOG_ERROR(SAI_API_BFD, "rollback to error3\n");
    _ctc_sai_bfd_remove_ipbfd_nh(lchip, p_bfd_info);  
error2:
    CTC_SAI_LOG_ERROR(SAI_API_BFD, "rollback to error2\n");
    _ctc_sai_bfd_remove_db(lchip, bfd_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_BFD, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_BFD, bfd_session_id);    
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;

}

static sai_status_t ctc_sai_bfd_remove_bfd_session( sai_object_id_t sai_bfd_session_id)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_bfd_t* p_bfd_info = NULL;
    uint32 bfd_session_id = 0;
    
    ctc_oam_lmep_t lmep;
    ctc_oam_rmep_t rmep;

    sal_memset(&lmep, 0, sizeof(ctc_oam_lmep_t));    
    sal_memset(&rmep, 0, sizeof(ctc_oam_rmep_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_bfd_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    CTC_SAI_LOG_INFO(SAI_API_BFD, "bfd_session_id = %llu\n", sai_bfd_session_id);
    
    p_bfd_info = ctc_sai_db_get_object_property(lchip, sai_bfd_session_id);
    if (NULL == p_bfd_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "Failed to remove bfd session, invalid bfd_session_id %d!\n", sai_bfd_session_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_bfd_lkup_key_gen(lchip, p_bfd_info, &lmep, &rmep), status, out);    
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_remove_rmep(lchip, &rmep), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_oam_remove_lmep(lchip, &lmep), status, out);

    _ctc_sai_bfd_remove_ipbfd_nh(lchip, p_bfd_info);
    _ctc_sai_bfd_remove_local_ipuc(lchip, p_bfd_info);

    ctc_sai_oid_get_value(sai_bfd_session_id, &bfd_session_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_BFD, bfd_session_id);
    
    _ctc_sai_bfd_remove_db(lchip, sai_bfd_session_id);
    
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;    
}

static sai_status_t ctc_sai_bfd_set_bfd_session_attribute( sai_object_id_t sai_bfd_session_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = sai_bfd_session_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_bfd_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_BFD_SESSION,  bfd_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "Failed to set bfd attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}


static sai_status_t ctc_sai_bfd_get_bfd_session_attribute( 
    sai_object_id_t sai_bfd_session_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = sai_bfd_session_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_BFD);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_bfd_session_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_BFD_SESSION, loop, bfd_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "Failed to get bfd attr:%d, attr_id:%d\n", status, attr_list[loop].id);
    }
    return status;
}


static sai_status_t ctc_sai_bfd_get_bfd_session_stats( sai_object_id_t sai_bfd_session_id,
                                                uint32_t               number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                uint64_t             *counters)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

static sai_status_t
ctc_sai_bfd_get_bfd_session_stats_ext( sai_object_id_t sai_bfd_session_id,
                                                uint32_t               number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                sai_stats_mode_t mode,
                                                uint64_t             *counters)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

static sai_status_t ctc_sai_bfd_clear_bfd_session_stats( sai_object_id_t sai_bfd_session_id,
                                                  uint32_t               number_of_counters,
                                                  const sai_stat_id_t *counter_ids)
{
    return SAI_STATUS_NOT_IMPLEMENTED;
}

const sai_bfd_api_t ctc_sai_bfd_api = {
    ctc_sai_bfd_create_bfd_session,
    ctc_sai_bfd_remove_bfd_session,
    ctc_sai_bfd_set_bfd_session_attribute,
    ctc_sai_bfd_get_bfd_session_attribute,
    ctc_sai_bfd_get_bfd_session_stats,
    ctc_sai_bfd_get_bfd_session_stats_ext,
    ctc_sai_bfd_clear_bfd_session_stats
};

sai_status_t
ctc_sai_bfd_db_init(uint8 lchip)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    
    uint8 gchip = 0;
    ctc_internal_port_assign_para_t port_assign;
    //ctc_port_scl_property_t port_scl_property;
    ctc_l3if_t l3if;
    ctc_l3if_property_t l3if_prop;
    ctc_loopback_nexthop_param_t iloop_nh;
    uint32 nhid = 0, l3if_id = 0;

    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    sal_memset(&l3if_prop, 0, sizeof(ctc_l3if_property_t));
    sal_memset(&port_assign, 0, sizeof(ctc_internal_port_assign_para_t));
    sal_memset(&iloop_nh, 0, sizeof(ctc_loopback_nexthop_param_t));

    /*warmboot start */
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_BFD;
    wb_info.data_len = sizeof(ctc_sai_bfd_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_sync_cb1 = _ctc_sai_bfd_wb_sync_cb1;
    wb_info.wb_reload_cb = _ctc_sai_bfd_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_bfd_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_BFD_SESSION, (void*)(&wb_info));
    /*warmboot end */
        
    if(NULL != p_ctc_sai_bfd[lchip])
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_ctc_sai_bfd[lchip] = mem_malloc(MEM_OAM_MODULE, sizeof(ctc_sai_bfd_master_t));
    if (NULL == p_ctc_sai_bfd[lchip])
    {
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_ctc_sai_bfd[lchip], 0, sizeof(ctc_sai_bfd_master_t));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) || (CTC_CHIP_TSINGMA_MX== ctcs_get_chip_type(lchip))) 
    {
        /*alloc global iloop port */
        
        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
        port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
        port_assign.gchip = gchip;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_alloc_internal_port(lchip, &port_assign));
        
        p_ctc_sai_bfd[lchip]->reroute_inner_port = port_assign.inter_port;

        /*config inner l3if */
        sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, error1);

        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
        l3if.gport = port_assign.inter_port;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l3if_create(lchip, l3if_id, &l3if), status, error2);

        l3if_prop = CTC_L3IF_PROP_ROUTE_EN;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_IPV4_UCAST;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_IPV4_MCAST;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_IPV6_UCAST;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_IPV6_MCAST;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_ROUTE_ALL_PKT;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_VRF_EN;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 1);
        l3if_prop = CTC_L3IF_PROP_VRF_ID;
        ctcs_l3if_set_property(lchip, l3if_id, l3if_prop, 0);   //use default vr id             

        ctcs_port_set_phy_if_en(lchip, port_assign.inter_port, 1);

        p_ctc_sai_bfd[lchip]->reroute_l3if = l3if_id;

        /*iloop nh */
        CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nhid), status, error3);
        iloop_nh.lpbk_lport = port_assign.inter_port;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_iloop(lchip, nhid, &iloop_nh), status, error4);
        p_ctc_sai_bfd[lchip]->reroute_iloop_nhid = nhid;

        p_ctc_sai_bfd[lchip]->use_global_res_info = 1;

        goto out;


    error4:
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "bfd db init nexthop rollback to error4\n");
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nhid);
    error3:
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "bfd db init rollback to error3\n");
        ctcs_l3if_destory(lchip, l3if_id, &l3if);

    error2:
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "bfd db init rollback to error2\n");
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);
        

    error1:
        CTC_SAI_LOG_ERROR(SAI_API_BFD, "bfd db init rollback to error1\n");
        ctcs_free_internal_port(lchip, &port_assign);        

    }
out:        
    return status;
}

sai_status_t
ctc_sai_bfd_db_deinit(uint8 lchip)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;

    /* only free master, do not need deinit sdk resource */
    if(NULL == p_ctc_sai_bfd[lchip])
    {
        return status;
    }
    
    /*
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && p_ctc_sai_bfd[lchip]->use_global_res_info) 
    {
        ctcs_nh_remove_iloop(lchip, p_ctc_sai_bfd[lchip]->reroute_iloop_nhid);
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_ctc_sai_bfd[lchip]->reroute_iloop_nhid);

        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
        l3if.gport = p_ctc_sai_bfd[lchip]->reroute_inner_port;
        ctcs_l3if_destory(lchip, p_ctc_sai_bfd[lchip]->reroute_l3if, &l3if);

        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, p_ctc_sai_bfd[lchip]->reroute_l3if);
        
        port_assign.type = CTC_INTERNAL_PORT_TYPE_ILOOP;
        port_assign.gchip = gchip;
        port_assign.inter_port = p_ctc_sai_bfd[lchip]->reroute_inner_port;
        ctcs_free_internal_port(lchip, &port_assign);        
    }
    */

    if(NULL != p_ctc_sai_bfd[lchip])
    {
        mem_free(p_ctc_sai_bfd[lchip]);
    }

    return status;
}

sai_status_t
ctc_sai_bfd_api_init()
{
    ctc_sai_register_module_api(SAI_API_BFD, (void*)&ctc_sai_bfd_api);

    return SAI_STATUS_SUCCESS;
}

