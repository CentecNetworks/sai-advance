/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_route.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_nat.h"
#include "ctc_sai_next_hop.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_vlan.h"
#include "ctcs_api.h"


static sai_status_t _ctc_sai_nat_map_natsa_key (const sai_nat_entry_t *nat_entry, ctc_ipuc_nat_sa_param_t* ip_tunnel_natsa_param, 
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint16 vrf_id = 0;
    sai_ip4_t ipmask = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    ip_tunnel_natsa_param->ip_ver = CTC_IP_VER_4;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
    ip_tunnel_natsa_param->vrf_id = vrf_id;

    sal_memcpy(&(ip_tunnel_natsa_param->ipsa.ipv4), &(nat_entry->data.key.src_ip), sizeof(sai_ip4_t));
    CTC_SAI_NTOH_V4(ip_tunnel_natsa_param->ipsa.ipv4);
    ip_tunnel_natsa_param->l4_src_port = nat_entry->data.key.l4_src_port;

    if(6 == nat_entry->data.key.proto)
    {
        ip_tunnel_natsa_param->flag |= CTC_IPUC_NAT_FLAG_USE_TCP_PORT;
    }
    else if (17 == nat_entry->data.key.proto)
    {
        ip_tunnel_natsa_param->flag = 0;
    }
    else
    {
        
    }
    
    /* Edit info */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_SRC_IP, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&(ip_tunnel_natsa_param->new_ipsa.ipv4), &(attr_value->ip4), sizeof(sai_ip4_t));
        CTC_SAI_NTOH_V4(ip_tunnel_natsa_param->new_ipsa.ipv4);
    }    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_SRC_IP_MASK, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        sal_memcpy(&ipmask, &(attr_value->ip4), sizeof(sai_ip4_t));
        CTC_SAI_NTOH_V4(ipmask);
        ip_tunnel_natsa_param->new_ipsa.ipv4 = ip_tunnel_natsa_param->new_ipsa.ipv4 & ipmask;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_L4_SRC_PORT, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        ip_tunnel_natsa_param->new_l4_src_port = attr_value->u16;
    }    
        
    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_nat_map_natda_key (const sai_nat_entry_t *nat_entry, ctc_ipuc_param_t* ipuc_param, 
        uint32_t attr_count,
        const sai_attribute_t *attr_list, 
        uint8 is_add)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint16 vrf_id = 0;
    uint8 lchip = 0;
    uint32 nh_id = 0;
    uint8 dnat_reroute = 0, mask_len = 0;
    sai_ip4_t ipmask = 0, reroute_ipv4 = 0;
    ctc_ip_tunnel_nh_param_t nh_param;
    ctc_sai_nat_t* p_nat_info = NULL;
    sai_route_entry_t route_entry;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_route_t* p_route_info = NULL;
    ctc_sai_next_hop_t* p_next_hop_info = NULL;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    uint8 if_type = 0;
    uint32 if_gport = 0;
    uint16 if_vlan = 0;

    sal_memset(&nh_param, 0, sizeof(ctc_ip_tunnel_nh_param_t));
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    
    ipuc_param->ip_ver = CTC_IP_VER_4;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
    ipuc_param->vrf_id = vrf_id;

    sal_memcpy(&(ipuc_param->ip.ipv4), &(nat_entry->data.key.dst_ip), sizeof(sai_ip4_t));
    CTC_SAI_NTOH_V4(ipuc_param->ip.ipv4);
    
    sal_memcpy(&(ipmask), &(nat_entry->data.mask.dst_ip), sizeof(sai_ip4_t));
    CTC_SAI_NTOH_V4(ipmask);
    IPV4_MASK_TO_LEN(ipmask, mask_len);
    ipuc_param->masklen = mask_len;
    
    ipuc_param->l4_dst_port = nat_entry->data.key.l4_dst_port;

    if(6 == nat_entry->data.key.proto)
    {
        ipuc_param->is_tcp_port = 1;
    }
    else if (17 == nat_entry->data.key.proto)
    {
        ipuc_param->is_tcp_port = 0;
    }
    else
    {
        
    }
    
    ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip);    

    if(is_add)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id));
        
        /* Edit info */
        nh_param.tunnel_info.tunnel_type = CTC_TUNNEL_TYPE_IPV4_NAT;
        
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_DST_IP, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            sal_memcpy(&(reroute_ipv4), &(attr_value->ip4), sizeof(sai_ip4_t));
            sal_memcpy(&(nh_param.tunnel_info.ip_da.ipv4), &(attr_value->ip4), sizeof(sai_ip4_t));
            CTC_SAI_NTOH_V4(nh_param.tunnel_info.ip_da.ipv4);
            nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_NAT_REPLACE_IP;
        }
        else
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_DST_IP_MASK, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            sal_memcpy(&ipmask, &(attr_value->ip4), sizeof(sai_ip4_t));
            CTC_SAI_NTOH_V4(ipmask);
            nh_param.tunnel_info.ip_da.ipv4 = nh_param.tunnel_info.ip_da.ipv4 & ipmask;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_L4_DST_PORT, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            nh_param.tunnel_info.l4_dst_port = attr_value->u16;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_CUSTOM_DNAT_REROUTE, &attr_value, &index);
        if (SAI_STATUS_SUCCESS == status)
        {
            dnat_reroute = attr_value->booldata;
        }

        if(!dnat_reroute)
        {
            /*Get out rif and mac info */
            route_entry.switch_id = nat_entry->switch_id;
            route_entry.vr_id = nat_entry->vr_id;
            route_entry.destination.addr_family = SAI_IP_ADDR_FAMILY_IPV4;
            sal_memcpy(&(route_entry.destination.addr.ip4), &(reroute_ipv4), sizeof(sai_ip4_t));
            route_entry.destination.mask.ip4 = sal_htonl(ipmask);
            
            p_route_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ROUTE, (void*)&route_entry);
            if(!p_route_info)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            p_next_hop_info = ctc_sai_db_get_object_property(lchip, p_route_info->nh_obj_id);
            if(!p_next_hop_info)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }        

            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(p_next_hop_info->rif_id, &if_type, NULL, &if_gport, &if_vlan));
            if (SAI_ROUTER_INTERFACE_TYPE_PORT == if_type)
            {
                nh_param.oif.gport = if_gport;
            }
            else if ((SAI_ROUTER_INTERFACE_TYPE_VLAN == if_type) || (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == if_type))
            {
                nh_param.oif.gport = if_gport;
                nh_param.oif.vid = if_vlan;
            }

            neighbor_entry.switch_id = nat_entry->switch_id;
            neighbor_entry.rif_id = p_next_hop_info->rif_id;
            neighbor_entry.ip_address.addr_family = SAI_IP_ADDR_FAMILY_IPV4;            
            sal_memcpy(&(neighbor_entry.ip_address.addr.ip4), &(reroute_ipv4), sizeof(sai_ip4_t));
            p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
            if(!p_neighbor_info)
            {
                return SAI_STATUS_ITEM_NOT_FOUND;
            }

            sal_memcpy(&(nh_param.mac), &(p_neighbor_info->dest_mac), sizeof(sai_mac_t));
        }
        else
        {
            nh_param.tunnel_info.flag |= CTC_IP_NH_TUNNEL_FLAG_REROUTE_WITH_TUNNEL_HDR;
        }
                
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_add_ip_tunnel(lchip, nh_id, &nh_param));

        ipuc_param->nh_id = nh_id;
    }
    else
    {
        p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
        if (!p_nat_info)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_ip_tunnel(lchip, p_nat_info->nh_id));
    }
        
    return SAI_STATUS_SUCCESS;
}
        

static sai_status_t
_ctc_sai_nat_entry_create_attr_check(uint8 lchip, const sai_nat_entry_t *nat_entry, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    sai_nat_type_t nat_type = SAI_NAT_TYPE_NONE;
    uint32_t index = 0;
    ctc_sai_oid_property_t* p_oid_property = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_NAT_TYPE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        nat_type = attr_value->s32;
        if((SAI_NAT_TYPE_DOUBLE_NAT == nat_type) || (SAI_NAT_TYPE_DESTINATION_NAT_POOL == nat_type))
        {
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
        }
    }    

    if(SAI_NAT_TYPE_SOURCE_NAT == nat_type)
    {        
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_DST_IP, &attr_value, &index);
        if(!CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_DST_IP_MASK, &attr_value, &index);
        if(!CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }
    else if(SAI_NAT_TYPE_DESTINATION_NAT == nat_type)
    {
        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_SRC_IP, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }

        status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_SRC_IP_MASK, &attr_value, &index);
        if (!CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + index;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_VR_ID, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
        
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_PACKET_COUNT, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_BYTE_COUNT, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_HIT_BIT_COR, &attr_value, &index);
    if(!CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + index;
    }

    p_oid_property = ctc_sai_db_get_object_property(lchip, nat_entry->vr_id);
    if (NULL == p_oid_property)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if((nat_entry->data.mask.src_ip != 0xFFFFFFFF) || (nat_entry->data.mask.dst_ip != 0xFFFFFFFF) || (nat_entry->data.mask.proto != 0xFF)
        || (nat_entry->data.mask.l4_src_port != 0xFFFF) || (nat_entry->data.mask.l4_dst_port != 0xFFFF))
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }

    
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_nat_build_db(uint8 lchip, const sai_nat_entry_t *nat_entry, ctc_sai_nat_t** nat_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_nat_t* p_nat_info = NULL;
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (p_nat_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }
    p_nat_info = mem_malloc(MEM_IPUC_MODULE, sizeof(ctc_sai_nat_t));
    if (NULL == p_nat_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NAT, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(p_nat_info, 0, sizeof(ctc_sai_nat_t));
    status = ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry, (void*)p_nat_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_nat_info);
    }
    *nat_property = p_nat_info;
    return status;
}

static sai_status_t
_ctc_sai_nat_remove_db(uint8 lchip, const sai_nat_entry_t *nat_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_nat_t* p_nat_info = NULL;
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (NULL == p_nat_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    status = ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTE, "_ctc_sai_route_remove_db error!\n");
        return status;
    }
    mem_free(p_nat_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_create_nat_entry (
        const sai_nat_entry_t *nat_entry,
        uint32_t attr_count,
        const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint32_t nh_id = 0;
    ctc_sai_nat_t* p_nat_info = NULL;
    ctc_ipuc_nat_sa_param_t ip_tunnel_natsa_param;
    ctc_ipuc_param_t ipuc_param;
    sai_nat_type_t nat_type = SAI_NAT_TYPE_NONE;

    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    sal_memset(&ip_tunnel_natsa_param, 0, sizeof(ip_tunnel_natsa_param));
    sal_memset(&ipuc_param, 0, sizeof(ipuc_param));
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    
    ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip);
    CTC_SAI_ERROR_RETURN(_ctc_sai_nat_entry_create_attr_check(lchip, nat_entry, attr_count, attr_list));
    
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (p_nat_info)
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_NAT_TYPE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        nat_type = attr_value->s32;
    }    

    if(SAI_NAT_TYPE_SOURCE_NAT == nat_type)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_nat_map_natsa_key(nat_entry, &ip_tunnel_natsa_param, attr_count, attr_list));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_add_nat_sa(lchip, &ip_tunnel_natsa_param));
    }

    if(SAI_NAT_TYPE_DESTINATION_NAT == nat_type)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_nat_map_natda_key(nat_entry, &ipuc_param, attr_count, attr_list, 1));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_add(lchip, &ipuc_param));
        nh_id = ipuc_param.nh_id;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_nat_build_db(lchip, nat_entry, &p_nat_info));

    /* update db */
    if(SAI_NAT_TYPE_SOURCE_NAT == nat_type)
    {
        sal_memcpy(&(p_nat_info->new_ipsa), &(ip_tunnel_natsa_param.new_ipsa.ipv4), sizeof(ip_addr_t));
        p_nat_info->new_l4_src_port = ip_tunnel_natsa_param.new_l4_src_port;
        
    }
    p_nat_info->nat_type = nat_type;
    p_nat_info->nh_id = nh_id;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NAT_ENTRY_ATTR_CUSTOM_DNAT_REROUTE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_nat_info->dnat_reroute = attr_value->booldata;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_nat_remove_nat_entry(const sai_nat_entry_t *nat_entry)
{
    uint8 lchip = 0;
    ctc_ipuc_param_t ipuc_info;
    ctc_sai_nat_t* p_nat_info = NULL;
    ctc_ipuc_nat_sa_param_t ip_tunnel_natsa_param;
    ctc_ipuc_param_t ipuc_param;
    
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (NULL == p_nat_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&ipuc_info, 0, sizeof(ipuc_info));
    sal_memset(&ipuc_param, 0, sizeof(ctc_ipuc_param_t));
    sal_memset(&ip_tunnel_natsa_param, 0, sizeof(ctc_ipuc_nat_sa_param_t));

    if(SAI_NAT_TYPE_SOURCE_NAT == p_nat_info->nat_type)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_nat_map_natsa_key(nat_entry, &ip_tunnel_natsa_param, 0, NULL));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_remove_nat_sa(lchip, &ip_tunnel_natsa_param));
    }
    if(SAI_NAT_TYPE_DESTINATION_NAT == p_nat_info->nat_type)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_nat_map_natda_key(nat_entry, &ipuc_param, 0, NULL, 0));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_remove(lchip, &ipuc_param));
    }

    _ctc_sai_nat_remove_db(lchip, nat_entry);

    return SAI_STATUS_SUCCESS;

}

static sai_status_t
_ctc_sai_nat_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    const sai_nat_entry_t *nat_entry = &(key->key.nat_entry);
    ctc_sai_nat_t* p_nat_info = NULL;
    ctc_ipuc_nat_sa_param_t ip_tunnel_natsa_param;
    ctc_ipuc_param_t ipuc_param;
    uint16 vrf_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (NULL == p_nat_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {         
        case SAI_NAT_ENTRY_ATTR_HIT_BIT:
            if(SAI_NAT_TYPE_SOURCE_NAT == p_nat_info->nat_type)
            {
                sal_memset(&ip_tunnel_natsa_param, 0, sizeof(ctc_ipuc_nat_sa_param_t));
                ip_tunnel_natsa_param.ip_ver = CTC_IP_VER_4;
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
                ip_tunnel_natsa_param.vrf_id = vrf_id;
                sal_memcpy(&(ip_tunnel_natsa_param.ipsa.ipv4), &(nat_entry->data.key.src_ip), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(ip_tunnel_natsa_param.ipsa.ipv4);
                ip_tunnel_natsa_param.l4_src_port = nat_entry->data.key.l4_src_port;
                if(6 == nat_entry->data.key.proto)
                {
                    ip_tunnel_natsa_param.flag |= CTC_IPUC_NAT_FLAG_USE_TCP_PORT;
                }
                else if (17 == nat_entry->data.key.proto)
                {
                    ip_tunnel_natsa_param.flag = 0;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_set_natsa_entry_hit(lchip, &ip_tunnel_natsa_param, attr->value.booldata));
            }
            else if (SAI_NAT_TYPE_DESTINATION_NAT == p_nat_info->nat_type)
            {
                ipuc_param.ip_ver = CTC_IP_VER_4;
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
                ipuc_param.vrf_id = vrf_id;

                sal_memcpy(&(ipuc_param.ip.ipv4), &(nat_entry->data.key.dst_ip), sizeof(sai_ip4_t));
                ipuc_param.l4_dst_port = nat_entry->data.key.l4_dst_port;

                if(6 == nat_entry->data.key.proto)
                {
                    ipuc_param.is_tcp_port = 1;
                }
                else if (17 == nat_entry->data.key.proto)
                {
                    ipuc_param.is_tcp_port = 0;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_set_entry_hit(lchip, &ipuc_param, attr->value.booldata));
            }
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
            break;
    }
    
    return status;
}

static sai_status_t
_ctc_sai_nat_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    const sai_nat_entry_t *nat_entry = &(key->key.nat_entry);
    uint8 lchip = 0;
    ctc_sai_nat_t* p_nat_info = NULL;
    ctc_nh_info_t nh_info;
    ctc_ip_tunnel_nh_param_t ip_tunnel;
    ctc_ipuc_nat_sa_param_t ip_tunnel_natsa_param;
    ctc_ipuc_param_t ipuc_param;
    uint16 vrf_id = 0;
    uint8 hit = 0, mask_len = 0;
    sai_ip4_t ipmask = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    if (NULL == p_nat_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset(&nh_info, 0, sizeof(ctc_nh_info_t));
    sal_memset(&ip_tunnel, 0, sizeof(ctc_ip_tunnel_nh_param_t));
    sal_memset(&ip_tunnel_natsa_param, 0, sizeof(ctc_ipuc_nat_sa_param_t));
    sal_memset(&ipuc_param, 0, sizeof(ctc_ipuc_param_t));
    
    if(p_nat_info->nh_id != 0)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_nh_info(lchip, p_nat_info->nh_id, &nh_info));
        if (nh_info.nh_type == CTC_NH_TYPE_IP_TUNNEL)
        {
            nh_info.p_nh_param = &ip_tunnel;
            ctcs_nh_get_nh_info(lchip, p_nat_info->nh_id, &nh_info);
        }
        else
        {
            return SAI_STATUS_INVALID_ATTRIBUTE_0 + attr_idx;
        }
    }
    
    switch (attr->id)
    {
        case SAI_NAT_ENTRY_ATTR_NAT_TYPE:
            attr->value.s32 = p_nat_info->nat_type;
            break;
        case SAI_NAT_ENTRY_ATTR_SRC_IP:
            sal_memcpy(&(attr->value.ip4), &(p_nat_info->new_ipsa), sizeof(sai_ip4_t));
            break;
        case SAI_NAT_ENTRY_ATTR_L4_SRC_PORT:
            attr->value.u16 = p_nat_info->new_l4_src_port;
            break;
        case SAI_NAT_ENTRY_ATTR_DST_IP:            
            sal_memcpy(&(attr->value.ip4), &(ip_tunnel.tunnel_info.ip_da.ipv4), sizeof(sai_ip4_t));
            break;
        case SAI_NAT_ENTRY_ATTR_L4_DST_PORT:
            attr->value.u16 = ip_tunnel.tunnel_info.l4_dst_port;
            break;
        case SAI_NAT_ENTRY_ATTR_HIT_BIT:
            if(SAI_NAT_TYPE_SOURCE_NAT == p_nat_info->nat_type)
            {
                ip_tunnel_natsa_param.ip_ver = CTC_IP_VER_4;
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
                ip_tunnel_natsa_param.vrf_id = vrf_id;
                sal_memcpy(&(ip_tunnel_natsa_param.ipsa.ipv4), &(nat_entry->data.key.src_ip), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(ip_tunnel_natsa_param.ipsa.ipv4);
                ip_tunnel_natsa_param.l4_src_port = nat_entry->data.key.l4_src_port;
                if(6 == nat_entry->data.key.proto)
                {
                    ip_tunnel_natsa_param.flag |= CTC_IPUC_NAT_FLAG_USE_TCP_PORT;
                }
                else if (17 == nat_entry->data.key.proto)
                {
                    ip_tunnel_natsa_param.flag = 0;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_get_natsa_entry_hit(lchip, &ip_tunnel_natsa_param, &hit));
            }
            else if (SAI_NAT_TYPE_DESTINATION_NAT == p_nat_info->nat_type)
            {
                ipuc_param.ip_ver = CTC_IP_VER_4;
                CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vrf_id(nat_entry->vr_id, &vrf_id));
                ipuc_param.vrf_id = vrf_id;

                sal_memcpy(&(ipuc_param.ip.ipv4), &(nat_entry->data.key.dst_ip), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(ipuc_param.ip.ipv4);

                sal_memcpy(&(ipmask), &(nat_entry->data.mask.dst_ip), sizeof(sai_ip4_t));
                CTC_SAI_NTOH_V4(ipmask);
                IPV4_MASK_TO_LEN(ipmask, mask_len);
                ipuc_param.masklen = mask_len;
    
                ipuc_param.l4_dst_port = nat_entry->data.key.l4_dst_port;

                if(6 == nat_entry->data.key.proto)
                {
                    ipuc_param.is_tcp_port = 1;
                }
                else if (17 == nat_entry->data.key.proto)
                {
                    ipuc_param.is_tcp_port = 0;
                }
                CTC_SAI_CTC_ERROR_RETURN(ctcs_ipuc_get_entry_hit(lchip, &ipuc_param, &hit));
            }
            attr->value.booldata = hit;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t nat_attr_fn_entries[] = {
    { SAI_NAT_ENTRY_ATTR_NAT_TYPE,
      _ctc_sai_nat_get_attr,
      NULL},
    { SAI_NAT_ENTRY_ATTR_SRC_IP,
      _ctc_sai_nat_get_attr,
      NULL},
    { SAI_NAT_ENTRY_ATTR_SRC_IP_MASK,
      NULL,
      NULL},
    { SAI_NAT_ENTRY_ATTR_VR_ID,
      NULL,
      NULL},
    { SAI_NAT_ENTRY_ATTR_DST_IP,
      _ctc_sai_nat_get_attr,
      NULL},
    { SAI_NAT_ENTRY_ATTR_DST_IP_MASK,
      NULL,
      NULL},
    { SAI_NAT_ENTRY_ATTR_L4_SRC_PORT,
      _ctc_sai_nat_get_attr,
      NULL},
    { SAI_NAT_ENTRY_ATTR_L4_DST_PORT,
      _ctc_sai_nat_get_attr,
      NULL},  
    { SAI_NAT_ENTRY_ATTR_ENABLE_PACKET_COUNT,
      NULL,
      NULL}, 
    { SAI_NAT_ENTRY_ATTR_PACKET_COUNT,
      NULL,
      NULL}, 
    { SAI_NAT_ENTRY_ATTR_ENABLE_BYTE_COUNT,
      NULL,
      NULL},  
    { SAI_NAT_ENTRY_ATTR_BYTE_COUNT,
      NULL,
      NULL},
    { SAI_NAT_ENTRY_ATTR_HIT_BIT_COR,
      NULL,
      NULL},
    { SAI_NAT_ENTRY_ATTR_HIT_BIT,
      _ctc_sai_nat_get_attr,
      _ctc_sai_nat_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};
      

static sai_status_t
_ctc_sai_nat_set_nat_attr(const sai_nat_entry_t *nat_entry, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    sal_memcpy(&key.key.nat_entry, nat_entry, sizeof(sai_nat_entry_t));
    status = ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_NAT_ENTRY,  nat_attr_fn_entries, attr);
    return status;
}

static sai_status_t
_ctc_sai_nat_get_nat_attr(const sai_nat_entry_t *nat_entry,
                                                uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8          loop = 0;
    sai_object_key_t key;
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    sal_memcpy(&key.key.nat_entry, nat_entry, sizeof(sai_nat_entry_t));
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_NAT_ENTRY, loop, nat_attr_fn_entries, &attr_list[loop]));
        loop++;
    }
    return status;
}

#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_nat_dump_print_cb(ctc_sai_entry_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_nat_t* p_nat_info = (ctc_sai_nat_t*)(bucket_data->data);;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    char vr_oid[64] = {'-'};
    char srcip[64] = {'-'};
    char srcip_mask[64] = {'-'};
    char dstip[64] = {'-'};
    char dstip_mask[64] = {'-'};
    char new_ipsa[64] = {'-'};
    sai_nat_entry_t         nat_entry;
    uint8 mask_len = 0;
    sai_ip4_t iptmp;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    sal_memset(&nat_entry, 0, sizeof(sai_route_entry_t));
    if (sal_memcmp(&nat_entry, &(p_dmp_grep->key.key.nat_entry), sizeof(ctc_sai_nat_t)))
    {
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_db_entry_unmapping_key(p_cb_data->lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, bucket_data, &nat_entry);
    if (!sal_memcmp(&nat_entry, &p_dmp_grep->key.key.nat_entry, sizeof(ctc_sai_nat_t)))
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memcpy(&iptmp, &nat_entry.data.key.src_ip, sizeof(sai_ip4_t));
    CTC_SAI_NTOH_V4(iptmp);
    ctc_sai_get_ipv4_str(&iptmp, srcip);
    IPV4_MASK_TO_LEN(nat_entry.data.mask.src_ip, mask_len);
    sal_sprintf(srcip_mask, "/%d", mask_len);
    sal_strcat(srcip, srcip_mask);

    sal_memcpy(&iptmp, &nat_entry.data.key.dst_ip, sizeof(sai_ip4_t));
    CTC_SAI_NTOH_V4(iptmp);
    ctc_sai_get_ipv4_str(&iptmp, dstip);
    IPV4_MASK_TO_LEN(nat_entry.data.mask.dst_ip, mask_len);
    sal_sprintf(dstip_mask, "/%d", mask_len);
    sal_strcat(dstip, dstip_mask);
    
    sal_sprintf(vr_oid, "0x%016"PRIx64, nat_entry.vr_id);

    ctc_sai_get_ipv4_str(&p_nat_info->new_ipsa, new_ipsa);   

    CTC_SAI_LOG_DUMP(p_file, "%-6d%-22s%-12d%-20s%-20s%-6d%-10d%-10d%-6d%-20s%-10d\n", num_cnt, vr_oid, p_nat_info->nat_type, srcip, dstip, nat_entry.data.key.proto, 
        nat_entry.data.key.l4_src_port, nat_entry.data.key.l4_dst_port,
        p_nat_info->nh_id, new_ipsa, p_nat_info->new_l4_src_port);
    
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_nat_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_sai_nat_t* p_nat_info = (ctc_sai_nat_t*)data;
    
    if(p_nat_info->nh_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_nat_info->nh_id));
    }

    return SAI_STATUS_SUCCESS;
}


#define ________INTERNAL_API________
void ctc_sai_nat_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.lchip = lchip;
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI NAT MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_NAT_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "NAT");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_nat_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-6s%-22s%-12s%-20s%-20s%-6s%-10s%-10s%-6s%-20s%-10s\n", "No.", "Vr_id", "Nattype", "Srcip", "Dstip", "Proto", "L4srcport", "L4dstport", "Nh_id", "New_ipsa", "Newl4srcport");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT,
                                            (hash_traversal_fn)_ctc_sai_nat_dump_print_cb, (void*)(&sai_cb_data));
    }
}



#define ________NAT______

sai_status_t ctc_sai_nat_create_nat_entry (
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_nat_t* p_nat_info = NULL;
    
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    status = _ctc_sai_create_nat_entry(nat_entry, attr_count, attr_list);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
        if(SAI_NAT_TYPE_SOURCE_NAT == p_nat_info->nat_type)
        {
            p_switch_master->nat_cnt[CTC_SAI_CNT_SNAT]++;
        }
        else if(SAI_NAT_TYPE_DESTINATION_NAT == p_nat_info->nat_type)
        {
            p_switch_master->nat_cnt[CTC_SAI_CNT_DNAT]++;
        }
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t ctc_sai_nat_remove_nat_entry (
        _In_ const sai_nat_entry_t *nat_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_nat_t* p_nat_info = NULL;
    sai_nat_type_t nat_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    p_nat_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)nat_entry);
    nat_type = p_nat_info->nat_type;
    
    status = _ctc_sai_nat_remove_nat_entry(nat_entry);
    if (SAI_STATUS_SUCCESS == status)
    {        
        if(SAI_NAT_TYPE_SOURCE_NAT == nat_type)
        {
            p_switch_master->nat_cnt[CTC_SAI_CNT_SNAT]--;
        }
        else if(SAI_NAT_TYPE_DESTINATION_NAT == nat_type)
        {
            p_switch_master->nat_cnt[CTC_SAI_CNT_DNAT]--;
        }
    }
    
    CTC_SAI_DB_UNLOCK(lchip);
    return status;    
}

sai_status_t ctc_sai_nat_set_nat_entry_attribute (
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);   
    status = _ctc_sai_nat_set_nat_attr(nat_entry, attr);
    
    CTC_SAI_DB_UNLOCK(lchip);
    return status;    
}

sai_status_t ctc_sai_nat_get_nat_entry_attribute (
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    status = _ctc_sai_nat_get_nat_attr(nat_entry, attr_count, attr_list);
    
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t ctc_sai_nat_bulk_create_nat_entry (
        _In_ uint32_t object_count,
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ const uint32_t *attr_count,
        _In_ const sai_attribute_t **attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);

        object_statuses[i] = _ctc_sai_create_nat_entry(&(nat_entry[i]), attr_count[i], attr_list[i]);
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return object_statuses[i];
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

sai_status_t ctc_sai_nat_bulk_remove_nat_entry (
        _In_ uint32_t object_count,
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    CTC_SAI_PTR_VALID_CHECK(nat_entry);
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_nat_remove_nat_entry(&(nat_entry[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return object_statuses[i];
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

sai_status_t ctc_sai_nat_bulk_set_nat_entry_attribute (
        _In_ uint32_t object_count,
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ const sai_attribute_t *attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_nat_set_nat_attr(&(nat_entry[i]), &(attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return object_statuses[i];
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;    
}

sai_status_t ctc_sai_nat_bulk_get_nat_entry_attribute (
        _In_ uint32_t object_count,
        _In_ const sai_nat_entry_t *nat_entry,
        _In_ const uint32_t *attr_count,
        _Inout_ sai_attribute_t **attr_list,
        _In_ sai_bulk_op_error_mode_t mode,
        _Out_ sai_status_t *object_statuses)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 i =  0;
    CTC_SAI_LOG_ENTER(SAI_API_NAT);
    for (i = 0; i < object_count; i++)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nat_entry[i].switch_id, &lchip));
        CTC_SAI_DB_LOCK(lchip);
        object_statuses[i] = _ctc_sai_nat_get_nat_attr(&(nat_entry[i]), attr_count[i], (attr_list[i]));
        if (CTC_SAI_ERROR(object_statuses[i]) && (SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode))
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return object_statuses[i];
        }
        CTC_SAI_DB_UNLOCK(lchip);
    }
    return status;
}

sai_status_t ctc_sai_nat_create_nat_zone_counter (
        _Out_ sai_object_id_t *nat_zone_counter_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_SUPPORTED;
}

sai_status_t ctc_sai_nat_remove_nat_zone_counter (
        _In_ sai_object_id_t nat_zone_counter_id)
{
    return SAI_STATUS_NOT_SUPPORTED;
}

sai_status_t ctc_sai_nat_set_zone_counter_attribute (
        _In_ sai_object_id_t nat_zone_counter_id,
        _In_ const sai_attribute_t *attr)
{
    return SAI_STATUS_NOT_SUPPORTED;
}

sai_status_t ctc_sai_nat_get_zone_counter_attribute (
        _In_ sai_object_id_t nat_zone_counter_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    return SAI_STATUS_NOT_SUPPORTED;
}

sai_nat_api_t g_ctc_sai_nat_api = {
    ctc_sai_nat_create_nat_entry,
    ctc_sai_nat_remove_nat_entry,
    ctc_sai_nat_set_nat_entry_attribute,
    ctc_sai_nat_get_nat_entry_attribute,
    ctc_sai_nat_bulk_create_nat_entry,
    ctc_sai_nat_bulk_remove_nat_entry,
    ctc_sai_nat_bulk_set_nat_entry_attribute,
    ctc_sai_nat_bulk_get_nat_entry_attribute,
    ctc_sai_nat_create_nat_zone_counter,
    ctc_sai_nat_remove_nat_zone_counter,
    ctc_sai_nat_set_zone_counter_attribute,
    ctc_sai_nat_get_zone_counter_attribute,
};


sai_status_t
ctc_sai_nat_api_init()
{
    ctc_sai_register_module_api(SAI_API_NAT, (void*)&g_ctc_sai_nat_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_nat_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NAT;
    wb_info.data_len = sizeof(ctc_sai_nat_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_nat_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_NAT, (void*)(&wb_info));
    
    return SAI_STATUS_SUCCESS;   
}

