/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_neighbor.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_next_hop.h"

/*sdk include file*/
#include "ctcs_api.h"

typedef struct  ctc_sai_neighbor_nh_node_s
{
   ctc_slistnode_t head;
   sai_object_id_t next_hop_id;
}ctc_sai_neighbor_nh_node_t;

typedef struct  ctc_sai_neighbor_wb_s
{
    /*key*/
    ctc_sai_neighbor_key_t key;
    uint32 index;
    uint32 calc_key_len[0];
    /*data*/
    sai_object_id_t next_hop_id;
}ctc_sai_neighbor_wb_t;

typedef enum ctc_sai_neighbor_trverse_type_e
{
    CTC_SAI_NEIGHBOR_REMOVE_ALL = 0,
    CTC_SAI_NEIGHBOR_CREATE_FDB,
    CTC_SAI_NEIGHBOR_REMOVE_FDB,
    CTC_SAI_NEIGHBOR_FLUSH_FDB,
    CTC_SAI_NEIGHBOR_MAX,
}ctc_sai_neighbor_trvse_type_t;

typedef struct  ctc_sai_neighbor_traverse_param_s
{
    ctc_sai_neighbor_trvse_type_t traverse_type;
    sai_object_id_t switch_id;
    const sai_fdb_entry_t* fdb_entry;
}ctc_sai_neighbor_traverse_param_t;

static sai_status_t
_ctc_sai_neighbor_lookup_fdb(uint8 lchip, sai_object_id_t rif_id, sai_mac_t mac, uint32* gport, uint16* bridge_port_vlan_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_l2_fdb_query_t query;
    ctc_l2_fdb_query_rst_t query_rst;
    ctc_l2_addr_t l2_addr;
    uint32 tmp_port = 0;
    uint16 vlan_id = 0;
    uint16 fid = 0;

    ctc_sai_router_interface_get_vlan_ptr(rif_id, &fid);
    sal_memset(&query, 0, sizeof(query));
    sal_memset(&query_rst, 0, sizeof(query_rst));
    sal_memset(&l2_addr, 0, sizeof(l2_addr));
    query.query_type = CTC_L2_FDB_ENTRY_OP_BY_MAC_VLAN;
    query.query_flag = CTC_L2_FDB_ENTRY_ALL;
    sal_memcpy(query.mac, mac, sizeof(sai_mac_t));
    query.fid = fid;
    query_rst.buffer = &l2_addr;
    query_rst.buffer_len = sizeof(l2_addr);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fdb_entry(lchip, &query, &query_rst));
    if (0 == query.count)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    tmp_port = l2_addr.gport;
    if (l2_addr.is_logic_port)
    {
        status = ctc_sai_bridge_traverse_get_bridge_port_info(lchip, fid, l2_addr.gport, &tmp_port, &vlan_id);
        if (SAI_STATUS_SUCCESS != status)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }


    if (gport)
    {
        *gport = tmp_port;
    }
    if (bridge_port_vlan_id)
    {
        *bridge_port_vlan_id = vlan_id;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_build_db(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address,
                               ctc_sai_neighbor_t** neighbor_property, uint8 by_next_hop)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));

    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (p_neighbor_info)
    {
        *neighbor_property = p_neighbor_info;
        if ((p_neighbor_info->neighbor_exists) && (0 == by_next_hop))/*create neighbor repeat by neighbor module*/
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }
        else if (0 == by_next_hop)
        {
            p_neighbor_info->neighbor_exists = 1;
        }
        return SAI_STATUS_SUCCESS;
    }

    p_neighbor_info = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_neighbor_t));
    if (NULL == p_neighbor_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NEIGHBOR, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(p_neighbor_info, 0, sizeof(ctc_sai_neighbor_t));

    if (!by_next_hop)/*create by neighbor module*/
    {
        p_neighbor_info->neighbor_exists = 1;
    }
    status = ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry, (void*)p_neighbor_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_neighbor_info);
    }
    *neighbor_property = p_neighbor_info;

    return status;
}

static sai_status_t
_ctc_sai_neighbor_remove_db(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, uint8 by_next_hop)
{
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
    ctc_slistnode_t        *ctc_slistnode, *ctc_slistnode_next;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if ((!p_neighbor_info->neighbor_exists) && (!by_next_hop))/* delete by neighbor module*/
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if((p_neighbor_info->neighbor_exists)&&(!by_next_hop))
    {
        p_neighbor_info->neighbor_exists = 0;
    }
    if (1 >= p_neighbor_info->ref_cnt)
    {
        if (p_neighbor_info->nh_list)
        {
            CTC_SLIST_LOOP_DEL(p_neighbor_info->nh_list, ctc_slistnode, ctc_slistnode_next)
            {
                p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
                mem_free(p_neighbor_nh_node);
            }
            mem_free(p_neighbor_info->nh_list);
        }
        ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
        mem_free(p_neighbor_info);
    }
    else
    {
        p_neighbor_info->ref_cnt--;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_add_arp_entry(uint8 lchip, sai_object_id_t rif_id, ctc_sai_neighbor_t* p_neighbor_info)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 rif_type = 0;
    uint32 gport = 0;
    uint16 vlan = 0;
    ctc_nh_nexthop_mac_param_t ctc_nh_mac_param;
    uint32 arp_id = 0;
    uint8 is_add = 0;
    uint8 gchip_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    if (0 == p_neighbor_info->arp_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_ARP, &arp_id));
        p_neighbor_info->arp_id = arp_id;
        CTC_SAI_LOG_INFO(SAI_API_NEIGHBOR, "alloc ctc arp_id = %u\n", arp_id);
        is_add = 1;
    } 
    sal_memset(&ctc_nh_mac_param, 0, sizeof(ctc_nh_mac_param));
    sal_memcpy(ctc_nh_mac_param.mac, p_neighbor_info->dest_mac, sizeof(sai_mac_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, &gport, &vlan), status, error1);

    if (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == rif_type)
    {
        ctc_nh_mac_param.vlan_id = vlan;
        CTC_SET_FLAG(ctc_nh_mac_param.flag, CTC_NH_NEXTHOP_MAC_VLAN_VALID);
    }
    else if (SAI_ROUTER_INTERFACE_TYPE_VLAN == rif_type)
    {
        gport = 0xFFFF;
        status = _ctc_sai_neighbor_lookup_fdb(lchip, rif_id, p_neighbor_info->dest_mac, &gport, NULL);
        if (SAI_STATUS_SUCCESS != status)
        {
            CTC_SET_FLAG(ctc_nh_mac_param.flag, CTC_NH_NEXTHOP_MAC_REDIRECT_TO_CPU);
        }
        CTC_SET_FLAG(ctc_nh_mac_param.flag, CTC_NH_NEXTHOP_MAC_VLAN_VALID);
        ctc_nh_mac_param.vlan_id = vlan;
    }
    ctc_nh_mac_param.gport = gport;
    switch (p_neighbor_info->action)
    {
        case SAI_PACKET_ACTION_COPY:
        case SAI_PACKET_ACTION_TRAP:
            ctcs_get_gchip_id(lchip, &gchip_id);
            CTC_SET_FLAG(ctc_nh_mac_param.flag, CTC_NH_NEXTHOP_MAC_REDIRECT_TO_CPU);
            break;
        case SAI_PACKET_ACTION_DROP:
        case SAI_PACKET_ACTION_DENY:
            CTC_SET_FLAG(ctc_nh_mac_param.flag, CTC_NH_NEXTHOP_MAC_DISCARD);
            break;
        case SAI_PACKET_ACTION_TRANSIT:
        case SAI_PACKET_ACTION_FORWARD:
            break;
        default:
            status = SAI_STATUS_NOT_SUPPORTED;
            goto error1;
            break;
    }
    p_neighbor_info->gport = gport;

    if (is_add)
    {
        status = ctcs_nh_add_nexthop_mac(lchip, p_neighbor_info->arp_id, &ctc_nh_mac_param);
    }
    else
    {
        status = ctcs_nh_update_nexthop_mac(lchip, p_neighbor_info->arp_id, &ctc_nh_mac_param);
    }
    if (CTC_SAI_ERROR(status))
    {
        status = ctc_sai_mapping_error_ctc(status);
        goto error1;
    }
    return SAI_STATUS_SUCCESS;
error1:
    if (is_add)
    {
        CTC_SAI_LOG_ERROR(SAI_API_NEIGHBOR, "rollback to error1\n");
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ARP, arp_id);
    }
    return status;
}

static sai_status_t
_ctc_sai_neighbor_remove_arp_entry(uint8 lchip, ctc_sai_neighbor_t* p_neighbor_info)
{
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_remove_nexthop_mac(lchip, p_neighbor_info->arp_id));
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_ARP, p_neighbor_info->arp_id);
    p_neighbor_info->arp_id = 0;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_add_ipuc_nexthop(uint8 lchip, sai_object_id_t rif_id, ctc_sai_neighbor_t* p_neighbor_info)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 nh_id = 0;
    uint8 rif_type = 0;
    uint16 vlan = 0;
    ctc_ip_nh_param_t  nh_param;
    uint8 chip_type = 0;
    uint8 gchip_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    chip_type = ctcs_get_chip_type(lchip);
    sal_memset(&nh_param, 0 , sizeof(nh_param));


    if ((chip_type == CTC_CHIP_GOLDENGATE)
        || (chip_type == CTC_CHIP_GREATBELT))
    {
        sal_memcpy(nh_param.mac, p_neighbor_info->dest_mac, sizeof(sai_mac_t));
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, NULL, &vlan));
        nh_param.oif.gport = p_neighbor_info->gport;
        nh_param.oif.vid = vlan;
        if ((SAI_PACKET_ACTION_TRAP == p_neighbor_info->action)
            || (SAI_PACKET_ACTION_COPY == p_neighbor_info->action))
        {
            ctcs_get_gchip_id(lchip, &gchip_id);
            nh_param.oif.gport = CTC_MAP_LPORT_TO_GPORT(gchip_id, 0) | (1 << (CTC_LOCAL_PORT_LENGTH + CTC_GCHIP_LENGTH + CTC_EXT_PORT_LENGTH + CTC_RSV_PORT_LENGTH));
            nh_param.oif.is_l2_port = 1;
        }
        else if ((SAI_PACKET_ACTION_DROP == p_neighbor_info->action)
            || (SAI_PACKET_ACTION_DENY == p_neighbor_info->action))
        {
            nh_param.arp_id = p_neighbor_info->arp_id;
        }
    }
    else
    {
        nh_param.arp_id = p_neighbor_info->arp_id;
    }

    if (0 == p_neighbor_info->nh_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id));
        status = ctcs_nh_add_ipuc(lchip, nh_id, &nh_param);
        if (CTC_SAI_ERROR(status))
        {
            ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_neighbor_info->nh_id);
            return ctc_sai_mapping_error_ctc(status);
        }
        CTC_SAI_LOG_INFO(SAI_API_NEIGHBOR, "alloc ctc nh_id = %u\n", nh_id);
        p_neighbor_info->nh_id = nh_id;
    }
    else /*update*/
    {
        nh_param.upd_type = CTC_NH_UPD_FWD_ATTR;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_ipuc(lchip, p_neighbor_info->nh_id, &nh_param));
    }

    return status;
}
static sai_status_t
_ctc_sai_neighbor_remove_ipuc_nexthop(uint8 lchip, ctc_sai_neighbor_t* p_neighbor_info)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    if (p_neighbor_info->nh_id)
    {
        status = ctcs_nh_remove_ipuc(lchip, p_neighbor_info->nh_id);
        if (CTC_SAI_ERROR(status))
        {
            return ctc_sai_mapping_error_ctc(status);
        }
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_neighbor_info->nh_id);
        p_neighbor_info->nh_id = 0;
    }
    return status;
}

static sai_status_t
_ctc_sai_neighbor_add_host_route(uint8 lchip, const sai_neighbor_entry_t* neighbor_entry, ctc_sai_neighbor_t* p_neighbor_info)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_ipuc_param_t ipuc_param;
    uint16 ctc_vrf_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    if (0 == p_neighbor_info->nh_id)
    {
        return SAI_STATUS_FAILURE;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(neighbor_entry->rif_id, NULL, &ctc_vrf_id, NULL, NULL));
    sal_memset(&ipuc_param, 0 , sizeof(ipuc_param));
    ipuc_param.route_flag = CTC_IPUC_FLAG_TTL_CHECK | CTC_IPUC_FLAG_NEIGHBOR;
    ipuc_param.nh_id = p_neighbor_info->nh_id;
    ipuc_param.vrf_id = ctc_vrf_id;
    ipuc_param.ip_ver = CTC_IP_VER_4;
    ipuc_param.masklen = 32;
    if (SAI_IP_ADDR_FAMILY_IPV6 == neighbor_entry->ip_address.addr_family)
    {
        ipuc_param.ip_ver = CTC_IP_VER_6;
        ipuc_param.masklen = 128;
    }
    sal_memcpy(&ipuc_param.ip, &neighbor_entry->ip_address.addr, sizeof(sai_ip6_t));
    CTC_SAI_NTOH_V6(ipuc_param.ip.ipv6);
    status = ctcs_ipuc_add(lchip, &ipuc_param);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_INFO(SAI_API_NEIGHBOR, "ctcs_ipuc_add fail\n");
        return ctc_sai_mapping_error_ctc(status);
    }
    return status;
}

static sai_status_t
_ctc_sai_neighbor_remove_host_route(uint8 lchip, const sai_neighbor_entry_t* neighbor_entry, ctc_sai_neighbor_t* p_neighbor_info)
{
    sai_status_t           status = 0;
    ctc_ipuc_param_t ipuc_param;
    uint16 ctc_vrf_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(neighbor_entry->rif_id, NULL, &ctc_vrf_id, NULL, NULL));
    sal_memset(&ipuc_param, 0 , sizeof(ipuc_param));
    ipuc_param.vrf_id = ctc_vrf_id;
    ipuc_param.ip_ver = CTC_IP_VER_4;
    ipuc_param.masklen = 32;
    ipuc_param.nh_id = p_neighbor_info->nh_id;
    if (SAI_IP_ADDR_FAMILY_IPV6 == neighbor_entry->ip_address.addr_family)
    {
        ipuc_param.ip_ver = CTC_IP_VER_6;
        ipuc_param.masklen = 128;
    }
    sal_memcpy(&ipuc_param.ip, &neighbor_entry->ip_address.addr, sizeof(sai_ip6_t));
    CTC_SAI_NTOH_V6(ipuc_param.ip.ipv6);
    status = ctcs_ipuc_remove(lchip, &ipuc_param);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_INFO(SAI_API_NEIGHBOR, "ctcs_ipuc_remove fail\n");
        return ctc_sai_mapping_error_ctc(status);
    }

    return status;
}

static sai_status_t
_ctc_sai_neighbor_add_nexthop(uint8 lchip, sai_object_id_t rif_id, ctc_sai_neighbor_t* p_neighbor_info, uint8 ip_version)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 rif_type = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, NULL, NULL));
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == rif_type)
    {
        uint32 nh_id = 0;
        ctc_misc_nh_param_t nh_param;
        uint8 gchip_id = 0;
        uint32 gport = 0;
        uint32 cpu_gport = 0;
        uint16 vlan_id = 0;
        uint16 fid = 0;

        ctcs_get_gchip_id(lchip, &gchip_id);
        ctc_sai_router_interface_get_vlan_ptr(rif_id, &fid);
        cpu_gport = CTC_MAP_LPORT_TO_GPORT(gchip_id, 0) | (1 << (CTC_LOCAL_PORT_LENGTH + CTC_GCHIP_LENGTH + CTC_EXT_PORT_LENGTH + CTC_RSV_PORT_LENGTH));
        sal_memset(&nh_param, 0 , sizeof(nh_param));
        status = _ctc_sai_neighbor_lookup_fdb(lchip, rif_id, p_neighbor_info->dest_mac, &gport, &vlan_id);
        if(SAI_STATUS_SUCCESS != status)
        {
            gport = cpu_gport;
        }
        switch (p_neighbor_info->action)
        {
            case SAI_PACKET_ACTION_TRAP:
                gport = cpu_gport;
                break;
            case SAI_PACKET_ACTION_DENY:
                break;
            case SAI_PACKET_ACTION_TRANSIT:
            case SAI_PACKET_ACTION_FORWARD:
                break;
            default:
                status = SAI_STATUS_NOT_SUPPORTED;
                break;
        }

        nh_param.gport = gport;
        nh_param.type = CTC_MISC_NH_TYPE_FLEX_EDIT_HDR;
        nh_param.oif.gport = gport;
        nh_param.oif.vid = fid;
        nh_param.is_oif = CTC_IS_CPU_PORT(gport)? 0 : 1;
        if (!CTC_IS_CPU_PORT(gport))
        {
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_REPLACE_L2_HDR);
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_REPLACE_MACDA);
            sal_memcpy(nh_param.misc_param.flex_edit.mac_da, p_neighbor_info->dest_mac, sizeof(sai_mac_t));
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_REPLACE_MACSA);
            CTC_SAI_CTC_ERROR_RETURN(ctc_sai_router_interface_get_src_mac(rif_id, nh_param.misc_param.flex_edit.mac_sa));
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_REPLACE_VLAN_TAG);
            nh_param.misc_param.flex_edit.stag_op = CTC_VLAN_TAG_OP_REP_OR_ADD;
            nh_param.misc_param.flex_edit.svid_sl = CTC_VLAN_TAG_SL_NEW;
            nh_param.misc_param.flex_edit.scos_sl = CTC_VLAN_TAG_SL_AS_PARSE;
            nh_param.misc_param.flex_edit.new_svid = vlan_id;
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_REPLACE_IP_HDR);
            if (SAI_IP_ADDR_FAMILY_IPV4 == ip_version)
            {
                CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_IPV4);
            }
            CTC_SET_FLAG(nh_param.misc_param.flex_edit.flag, CTC_MISC_NH_FLEX_EDIT_DECREASE_TTL);
            nh_param.misc_param.flex_edit.ttl = 1;
        }
        if (p_neighbor_info->nh_id)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_misc(lchip, p_neighbor_info->nh_id, &nh_param));
        }
        else
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id));
            status = (ctcs_nh_add_misc(lchip, nh_id, &nh_param));
            if(status)
            {
                ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
                return ctc_sai_mapping_error_ctc(status);
            }
            p_neighbor_info->nh_id = nh_id;
        }
        
    }
    else
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_neighbor_add_arp_entry(lchip, rif_id, p_neighbor_info));
    }


    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_remove_nexthop(uint8 lchip, sai_object_id_t rif_id, ctc_sai_neighbor_t* p_neighbor_info)
{
    uint8 rif_type = 0;
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, NULL, NULL));
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == rif_type)
    {
        ctcs_nh_remove_misc(lchip, (p_neighbor_info->nh_id));
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_neighbor_info->nh_id);
        p_neighbor_info->nh_id = 0 ;
    }
    else
    {
        _ctc_sai_neighbor_remove_arp_entry(lchip, p_neighbor_info);
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t           status = 0;
    uint8 lchip = 0;
    sai_neighbor_entry_t *neighbor_entry = &(key->key.neighbor_entry);
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_sai_neighbor_t neighbor_info_old ;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip);
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, neighbor_entry);
    if ((NULL == p_neighbor_info)||(0 == p_neighbor_info->neighbor_exists))
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    sal_memcpy(&neighbor_info_old, p_neighbor_info, sizeof(ctc_sai_neighbor_t));

    if (SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS == attr->id)
    {
        ctc_slistnode_t* ctc_slistnode = NULL;
        sal_memcpy(p_neighbor_info->dest_mac, attr->value.mac, sizeof(sai_mac_t));
        CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info, (uint8)neighbor_entry->ip_address.addr_family), status, error);
        CTC_SLIST_LOOP(p_neighbor_info->nh_list, ctc_slistnode)
        {
            ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
            p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
            if (p_neighbor_nh_node)
            {
                ctc_sai_next_hop_update_by_neighbor(p_neighbor_nh_node->next_hop_id, neighbor_entry->rif_id, neighbor_entry->ip_address);
            }
        }
    }
    else if (SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION == attr->id)
    {
        p_neighbor_info->action = attr->value.s32;
        CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info, (uint8)neighbor_entry->ip_address.addr_family), status, error);
    }
    else if (SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE == attr->id)
    {
        if ((attr->value.booldata)&&(!p_neighbor_info->no_host_route))
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_remove_host_route(lchip, neighbor_entry,  p_neighbor_info), status, error);
        }
        else if ((!attr->value.booldata) && (p_neighbor_info->no_host_route))
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_host_route(lchip, neighbor_entry, p_neighbor_info), status, error);
        }
        p_neighbor_info->no_host_route = attr->value.booldata;
    }
    else
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
    goto out;
error:
    sal_memcpy(p_neighbor_info, &neighbor_info_old, sizeof(ctc_sai_neighbor_t));
out:
    return status;
}

static sai_status_t
_ctc_sai_neighbor_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    sai_status_t           status = 0;
    uint8 lchip = 0;
    sai_neighbor_entry_t *neighbor_entry = &(key->key.neighbor_entry);
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip);
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, neighbor_entry);
    if ((NULL == p_neighbor_info)||(0 == p_neighbor_info->neighbor_exists))
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if (SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS == attr->id)
    {
        sal_memcpy(attr->value.mac, p_neighbor_info->dest_mac, sizeof(sai_mac_t));
    }
    else if (SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION == attr->id)
    {
        attr->value.s32 = p_neighbor_info->action;
    }
    else if (SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE == attr->id)
    {
        attr->value.booldata = p_neighbor_info->no_host_route;
    }
    else
    {
        return SAI_STATUS_NOT_SUPPORTED;
    }
out:
    return status;
}


static sai_status_t
_ctc_sai_neighbor_remove_neighbor(const sai_neighbor_entry_t *neighbor_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    uint8 rif_type;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);

    if (NULL == neighbor_entry)
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }
    ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip);

    ctc_sai_router_interface_get_rif_info(neighbor_entry->rif_id, &rif_type, NULL, NULL, NULL);
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, (void*)neighbor_entry);
    if ((NULL == p_neighbor_info)||(!p_neighbor_info->neighbor_exists))
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (0 == p_neighbor_info->no_host_route)
    {
        _ctc_sai_neighbor_remove_host_route(lchip, neighbor_entry, p_neighbor_info);
        if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
        {
            _ctc_sai_neighbor_remove_ipuc_nexthop(lchip, p_neighbor_info);
        }
    }
    if (1 >= p_neighbor_info->ref_cnt)
    {
        _ctc_sai_neighbor_remove_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info);
    }
    else
    {
        ctc_sai_router_interface_get_miss_action(neighbor_entry->rif_id, &p_neighbor_info->action);
        sal_memset(p_neighbor_info->dest_mac, 0, sizeof(sai_mac_t));
        _ctc_sai_neighbor_add_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info, (uint8)neighbor_entry->ip_address.addr_family);
    }
    _ctc_sai_neighbor_remove_db(lchip, neighbor_entry->rif_id, (sai_ip_address_t*)(&(neighbor_entry->ip_address)), 0);

    return status;
}

static int32
_ctc_sai_neighbor_hash_traverse_fun(void* bucket_data, void* user_data)
{
    uint8 lchip = 0;
    sai_object_id_t rif_id = 0;
    sai_neighbor_entry_t neighbor_entry;
    ctc_slistnode_t* ctc_slistnode = NULL;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_sai_neighbor_traverse_param_t* traverse_param = ((ctc_sai_neighbor_traverse_param_t*)user_data);
    ctc_sai_neighbor_key_t* p_neighbor_key =  &(((ctc_sai_entry_property_t*)bucket_data)->key.neighbor);
    ctc_sai_neighbor_t* p_neighbor_info = (((ctc_sai_entry_property_t*)bucket_data)->data);

    if (NULL == traverse_param)
    {
        return SAI_STATUS_SUCCESS;
    }

    ctc_sai_oid_get_lchip(traverse_param->switch_id, &lchip);
    rif_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, p_neighbor_key->sai_rif_type, 0, p_neighbor_key->l3if_id);

    sal_memset(&neighbor_entry, 0 , sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    neighbor_entry.switch_id = traverse_param->switch_id;
    neighbor_entry.ip_address.addr_family = p_neighbor_key->ip_ver;
    sal_memcpy(&neighbor_entry.ip_address.addr, &(p_neighbor_key->addr) , sizeof(sai_ip6_t));
    if (CTC_SAI_NEIGHBOR_REMOVE_ALL == traverse_param->traverse_type)
    {
        _ctc_sai_neighbor_remove_neighbor(&neighbor_entry);
        
        p_switch_master = ctc_sai_get_switch_property(lchip);
        p_switch_master->neighbor_cnt[neighbor_entry.ip_address.addr_family]--;
        return SAI_STATUS_SUCCESS;
    }

    if ((SAI_ROUTER_INTERFACE_TYPE_VLAN != p_neighbor_key->sai_rif_type)
        &&(SAI_ROUTER_INTERFACE_TYPE_BRIDGE != p_neighbor_key->sai_rif_type))
    {
        return SAI_STATUS_SUCCESS;
    }
    if ((CTC_SAI_NEIGHBOR_CREATE_FDB == traverse_param->traverse_type)
        || (CTC_SAI_NEIGHBOR_REMOVE_FDB == traverse_param->traverse_type))
    {
        ctc_object_id_t ctc_object_id;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, traverse_param->fdb_entry->bv_id, &ctc_object_id);
        if (SAI_OBJECT_TYPE_VLAN == ctc_object_id.type)
        {
            uint16 vlan = 0;
            uint16 vlan_fdb = 0;
            ctc_sai_router_interface_get_rif_info(rif_id, NULL, NULL, NULL, &vlan);
            ctc_sai_vlan_get_vlan_id(traverse_param->fdb_entry->bv_id, &vlan_fdb);
            if ((vlan != vlan_fdb)
                || (0 != sal_memcmp(p_neighbor_info->dest_mac, traverse_param->fdb_entry->mac_address, sizeof(sai_mac_t))))
            {
                return SAI_STATUS_SUCCESS;
            }
        }
        else if (SAI_OBJECT_TYPE_BRIDGE == ctc_object_id.type)
        {
            uint16 fid;
            uint16 fid_fdb;
            ctc_sai_bridge_get_fid(traverse_param->fdb_entry->bv_id, &fid_fdb);
            ctc_sai_router_interface_get_vlan_ptr(rif_id, &fid);
            if ((fid != fid_fdb)
                || (0 != sal_memcmp(p_neighbor_info->dest_mac, traverse_param->fdb_entry->mac_address, sizeof(sai_mac_t))))
            {
                return SAI_STATUS_SUCCESS;
            }
        }
        else
        {
            return SAI_STATUS_SUCCESS;
        }
    }
    _ctc_sai_neighbor_add_nexthop(lchip, rif_id, p_neighbor_info, p_neighbor_key->ip_ver);/*lookup fdb again*/

    CTC_SLIST_LOOP(p_neighbor_info->nh_list, ctc_slistnode)
    {
        ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
        p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
        if (p_neighbor_nh_node)
        {
            ctc_sai_next_hop_update_by_neighbor(p_neighbor_nh_node->next_hop_id, rif_id, neighbor_entry.ip_address);
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_dump_print_cb(ctc_sai_entry_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_neighbor_t* p_neighbor_info = (ctc_sai_neighbor_t*)(bucket_data->data);;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint8 ip_ver = 0;
    char rif_id[64] = {'-'};
    char ip[64] = {'-'};
    char gport[64] = {'-'};
    char flag[64] = {'\0'};
    char dest_mac[64] = {'-'};
    sai_neighbor_entry_t neighbor_entry;

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ip_ver = *((uint8 *)(p_cb_data->value3));

    if (bucket_data->key.route.ip_ver != ip_ver)
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_memset(&neighbor_entry, 0, sizeof(sai_neighbor_entry_t));
    if (sal_memcmp(&neighbor_entry, &(p_dmp_grep->key.key.neighbor_entry), sizeof(neighbor_entry)))
    {
        return SAI_STATUS_SUCCESS;
    }
    ctc_sai_db_entry_unmapping_key(p_cb_data->lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, bucket_data, &neighbor_entry);
    if (!sal_memcmp(&neighbor_entry, &p_dmp_grep->key.key.neighbor_entry, sizeof(sai_neighbor_entry_t)))
    {
        return SAI_STATUS_SUCCESS;
    }

    ctc_sai_get_ip_str(&(neighbor_entry.ip_address), ip);
    ctc_sai_get_mac_str(p_neighbor_info->dest_mac, dest_mac);
    sal_sprintf(rif_id, "0x%016"PRIx64, neighbor_entry.rif_id);
    sal_sprintf(gport, "0x%04x", p_neighbor_info->gport);
    if (p_neighbor_info->neighbor_exists || p_neighbor_info->no_host_route)
    {
        if (p_neighbor_info->neighbor_exists )
        {
            sal_strcat(flag, "N");
        }
        if (p_neighbor_info->no_host_route)
        {
            sal_strcat(flag, "H");
        }
    }
    else
    {
        sal_strcat(flag, "-");
    }

    CTC_SAI_LOG_DUMP(p_file, "%-6d%-20s%-41s%-7d%-8s%-8d%-9d%-6s%-14s\n", num_cnt, rif_id, ip, p_neighbor_info->nh_id, gport, p_neighbor_info->arp_id, p_neighbor_info->ref_cnt, flag, dest_mac);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_db_deinit_cb(ctc_sai_entry_property_t* bucket_data, void* user_data)
{
    ctc_sai_neighbor_t* p_neighbor_info = (ctc_sai_neighbor_t*)(bucket_data->data);
    ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
    ctc_slistnode_t        *ctc_slistnode, *ctc_slistnode_next;
    if (NULL == bucket_data)
    {
        return SAI_STATUS_SUCCESS;
    }
    if (p_neighbor_info && p_neighbor_info->nh_list)
    {
        if (p_neighbor_info->nh_list)
        {
            CTC_SLIST_LOOP_DEL(p_neighbor_info->nh_list, ctc_slistnode, ctc_slistnode_next)
            {
                p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
                mem_free(p_neighbor_nh_node);
            }
            mem_free(p_neighbor_info->nh_list);
        }
    }
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t neighbor_attr_fn_entries[] = {
    { SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS,
      _ctc_sai_neighbor_get_attr,
      _ctc_sai_neighbor_set_attr},
    { SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION,
      _ctc_sai_neighbor_get_attr,
      _ctc_sai_neighbor_set_attr},
    { SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID,
      NULL,
      NULL},
    { SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE,
      _ctc_sai_neighbor_get_attr,
      _ctc_sai_neighbor_set_attr},
    { SAI_NEIGHBOR_ENTRY_ATTR_META_DATA,
      NULL,
      NULL},
    { SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID,
      NULL,
      NULL},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

#define ________INTERNAL_API________

sai_status_t
ctc_sai_neighbor_alloc_ipuc_nexthop(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, uint32 nh_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    uint8 rif_type;
    ctc_ip_nh_param_t  nh_param;
    ctc_misc_nh_param_t misc_nh;
    ctc_nh_info_t nh_info;

    sal_memset(&nh_param, 0 , sizeof(ctc_ip_nh_param_t));
    sal_memset(&misc_nh, 0 , sizeof(ctc_misc_nh_param_t));
    sal_memset(&nh_info, 0, sizeof(ctc_nh_info_t));

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, NULL, NULL));
    CTC_SAI_ERROR_RETURN(_ctc_sai_neighbor_build_db(lchip, rif_id, ip_address, &p_neighbor_info, 1));
    if (0 == p_neighbor_info->ref_cnt)/*not create neighbor before, obey action of rif*/
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_router_interface_get_miss_action(rif_id, &p_neighbor_info->action), status, error1);
        CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_nexthop(lchip, rif_id, p_neighbor_info, (uint8)ip_address->addr_family), status, error1);
    }
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
    {
        nh_param.arp_id = p_neighbor_info->arp_id;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_ipuc(lchip, nh_id, &nh_param), status, error2);
    }
    else
    {
        nh_info.p_nh_param = &misc_nh;
        //nh_info.nh_type == CTC_NH_TYPE_MISC;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_get_nh_info(lchip, p_neighbor_info->nh_id, &nh_info), status, error2);
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_misc(lchip, nh_id, &misc_nh), status, error2);
    }
    p_neighbor_info->ref_cnt++;
    goto out;
error2:
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
    {
        _ctc_sai_neighbor_remove_nexthop(lchip, rif_id, p_neighbor_info);
    }
error1:
    _ctc_sai_neighbor_remove_db(lchip, rif_id, ip_address, 1);
out:
    return status;
}
sai_status_t
ctc_sai_neighbor_free_ipuc_nexthop(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, uint32 nh_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    uint8 rif_type;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    ctc_sai_router_interface_get_rif_info(rif_id, &rif_type, NULL, NULL, NULL);
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
    {
        ctcs_nh_remove_ipuc(lchip, nh_id);
    }
    else
    {
        ctcs_nh_remove_misc(lchip, nh_id);
    }
    if (1 == p_neighbor_info->ref_cnt)
    {
        _ctc_sai_neighbor_remove_nexthop(lchip, rif_id, p_neighbor_info);
        _ctc_sai_neighbor_remove_db(lchip, rif_id, ip_address, 1);
    }
    else
    {
        p_neighbor_info->ref_cnt--;
    }

    return status;
}

sai_status_t
ctc_sai_neighbor_get_arp_id(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, uint16* arp_id)
{
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (arp_id)
    {
        *arp_id = p_neighbor_info->arp_id;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_neighbor_get_outgoing_param(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, uint32* gport, sai_mac_t mac)
{
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (gport)
    {
        *gport = p_neighbor_info->gport;
    }
    if (mac)
    {
        sal_memcpy(mac, p_neighbor_info->dest_mac, sizeof(sai_mac_t));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_neighbor_binding_next_hop(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, sai_object_id_t next_hop_id)
{
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
    ctc_slistnode_t* ctc_slistnode = NULL;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);

    chip_type = ctcs_get_chip_type(lchip);
    if (chip_type == CTC_CHIP_DUET2)
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (NULL == p_neighbor_info->nh_list)
    {
        p_neighbor_info->nh_list = ctc_slist_new();
        if (NULL == p_neighbor_info->nh_list)
        {
            return CTC_E_NO_MEMORY;
        }
    }

    CTC_SLIST_LOOP(p_neighbor_info->nh_list, ctc_slistnode)
    {
        p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
        if ((p_neighbor_nh_node) && (p_neighbor_nh_node->next_hop_id == next_hop_id))
        {
            return SAI_STATUS_SUCCESS;
        }
    }

    p_neighbor_nh_node = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_neighbor_nh_node_t));
    if (NULL == p_neighbor_nh_node)
    {
        //ctc_slist_free(p_neighbor_info->nh_list);
        //p_neighbor_info->nh_list = NULL;
        return CTC_E_NO_MEMORY;
    }
    p_neighbor_nh_node->next_hop_id = next_hop_id;
    ctc_slist_add_tail(p_neighbor_info->nh_list, &(p_neighbor_nh_node->head));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_neighbor_unbinding_next_hop(uint8 lchip, sai_object_id_t rif_id, sai_ip_address_t* ip_address, sai_object_id_t next_hop_id)
{
    sai_neighbor_entry_t neighbor_entry;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_slistnode_t* ctc_slistnode = NULL;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);

    chip_type = ctcs_get_chip_type(lchip);
    if (chip_type == CTC_CHIP_DUET2)
    {
        return SAI_STATUS_SUCCESS;
    }

    sal_memset(&neighbor_entry, 0, sizeof(neighbor_entry));
    neighbor_entry.rif_id = rif_id;
    sal_memcpy(&neighbor_entry.ip_address, ip_address, sizeof(sai_ip_address_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SLIST_LOOP(p_neighbor_info->nh_list, ctc_slistnode)
    {
        ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
        p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
        if ((p_neighbor_nh_node) && (p_neighbor_nh_node->next_hop_id == next_hop_id))
        {
            ctc_slist_delete_node(p_neighbor_info->nh_list, &(p_neighbor_nh_node->head));
            mem_free(p_neighbor_nh_node);
            break;
        }
    }

    if (0 == CTC_SLISTCOUNT(p_neighbor_info->nh_list))
    {
        ctc_slist_free(p_neighbor_info->nh_list);
        p_neighbor_info->nh_list = NULL;
    }

    return SAI_STATUS_SUCCESS;
}

/* for fdb create/remove/learning/aging/flush when neighbor output rif is vlanif*/
sai_status_t
ctc_sai_neighbor_update_arp(uint8 lchip, const sai_fdb_entry_t* fdb_entry, uint8 is_remove, uint8 is_flush)
{
    ctc_sai_neighbor_traverse_param_t traverse_param;
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);

    CTC_SAI_PTR_VALID_CHECK(fdb_entry);
    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.traverse_type = is_flush? CTC_SAI_NEIGHBOR_FLUSH_FDB
                                                 : (is_remove? CTC_SAI_NEIGHBOR_REMOVE_FDB
                                                                : CTC_SAI_NEIGHBOR_CREATE_FDB);
    traverse_param.switch_id = fdb_entry->switch_id;
    traverse_param.fdb_entry = fdb_entry;
    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, (hash_traversal_fn)_ctc_sai_neighbor_hash_traverse_fun, (void*)(&traverse_param));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_neighbor_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_wb_data_t wb_data;
    ctc_sai_neighbor_key_t* p_neighbor_key =  &(((ctc_sai_entry_property_t*)key)->key.neighbor);
    uint32  max_entry_cnt = 0;
    ctc_sai_neighbor_t* p_neighbor_info = (ctc_sai_neighbor_t*)data;
    ctc_sai_neighbor_wb_t neighbor_wb;
    ctc_slistnode_t* ctc_slistnode = NULL;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_neighbor_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NEIGHBOR);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    CTC_SLIST_LOOP(p_neighbor_info->nh_list, ctc_slistnode)
    {
        ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
        p_neighbor_nh_node = _ctc_container_of(ctc_slistnode, ctc_sai_neighbor_nh_node_t, head);
        if (p_neighbor_nh_node)
        {
            offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
            sal_memcpy((uint8*)(&neighbor_wb.key), p_neighbor_key, sizeof(ctc_sai_neighbor_key_t));
            neighbor_wb.index = index;
            neighbor_wb.next_hop_id = p_neighbor_nh_node->next_hop_id;
            sal_memcpy((uint8*)wb_data.buffer + offset, &neighbor_wb, (wb_data.key_len + wb_data.data_len));
            if (++wb_data.valid_cnt == max_entry_cnt)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
                wb_data.valid_cnt = 0;
            }
            index++;
        }
    }
    if (wb_data.valid_cnt)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctc_wb_add_entry(&wb_data), status, out);
    }

out:
done:
    CTC_WB_FREE_BUFFER(wb_data.buffer);

    return status;
}

static sai_status_t
_ctc_sai_neighbor_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_neighbor_t* p_neighbor_info = (ctc_sai_neighbor_t*)data;
    if (p_neighbor_info->arp_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_ARP, p_neighbor_info->arp_id));
    }
    if (p_neighbor_info->nh_id)
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, p_neighbor_info->nh_id));
    }
    return status;
}

static sai_status_t
_ctc_sai_neighbor_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    ctc_sai_neighbor_nh_node_t* p_neighbor_nh_node = NULL;
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    ctc_sai_neighbor_wb_t neighbor_wb;
    sai_neighbor_entry_t neighbor_entry;
    ctc_wb_query_t wb_query;
	uint8 gchip = 0;
	
	ctcs_get_gchip_id(lchip, &gchip);
    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_neighbor_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_NEIGHBOR);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
    offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
    entry_cnt++;
    sal_memcpy(&neighbor_wb, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_neighbor_wb_t));
    sal_memset(&neighbor_entry, 0 , sizeof(neighbor_entry));
    neighbor_entry.rif_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, neighbor_wb.key.sai_rif_type, 0, neighbor_wb.key.l3if_id);
    neighbor_entry.switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32)gchip);
    neighbor_entry.ip_address.addr_family = neighbor_wb.key.ip_ver;
    sal_memcpy(&neighbor_entry.ip_address.addr, &(neighbor_wb.key.addr) , sizeof(sai_ip6_t));
    p_neighbor_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, &neighbor_entry);
    if (NULL == p_neighbor_info)
    {
        continue;
    }
    if (NULL == p_neighbor_info->nh_list)
    {
        p_neighbor_info->nh_list = ctc_slist_new();
        if (NULL == p_neighbor_info->nh_list)
        {
            return CTC_E_NO_MEMORY;
        }
    }
    p_neighbor_nh_node = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_neighbor_nh_node_t));
    if (NULL == p_neighbor_info->nh_list)
    {
        ctc_slist_free(p_neighbor_info->nh_list);
        p_neighbor_info->nh_list = NULL;
        return CTC_E_NO_MEMORY;
    }
    p_neighbor_nh_node->next_hop_id = neighbor_wb.next_hop_id;
    ctc_slist_add_tail(p_neighbor_info->nh_list, &(p_neighbor_nh_node->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));
done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
    return ret;
}

void ctc_sai_neighbor_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    uint8 ip_ver = SAI_IP_ADDR_FAMILY_IPV4;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.lchip = lchip;
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Neighbor MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ROUTE_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Neighbor");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_neighbor_t(flag H:no_host_route, flag N:neighbor_exists)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-6s%-20s%-41s%-7s%-8s%-8s%-9s%-6s%-14s\n", "No.", "rif_id", "ip4", "nh_id", "gport", "arp_id", "ref_cnt", "flag", "dest_mac");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        sai_cb_data.value3 = &ip_ver;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR,
                                            (hash_traversal_fn)_ctc_sai_neighbor_dump_print_cb, (void*)(&sai_cb_data));
        num_cnt = 1;
        ip_ver = SAI_IP_ADDR_FAMILY_IPV6;
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_neighbor_t(flag H:no_host_route, flag N:neighbor_exists)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-6s%-20s%-41s%-7s%-8s%-8s%-9s%-6s%-14s\n", "No.", "rif_id", "ip6", "nh_id", "gport", "arp_id", "ref_cnt", "flag", "dest_mac");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        sai_cb_data.value3 = &ip_ver;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR,
                                            (hash_traversal_fn)_ctc_sai_neighbor_dump_print_cb, (void*)(&sai_cb_data));
    }
}


#define ________SAI_API________
static sai_status_t
ctc_sai_neighbor_create_neighbor(const sai_neighbor_entry_t *neighbor_entry,
                                                          uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_neighbor_t* p_neighbor_info = NULL;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint8 rif_type;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    CTC_SAI_PTR_VALID_CHECK(neighbor_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_build_db(lchip, neighbor_entry->rif_id, (sai_ip_address_t*)(&(neighbor_entry->ip_address)), &p_neighbor_info, 0), status, out);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS, &attr_value, &index);
    if (CTC_SAI_ERROR(status))
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto error1;
    }
    sal_memcpy(p_neighbor_info->dest_mac, attr_value->mac, sizeof(sai_mac_t));

    p_neighbor_info->action = SAI_PACKET_ACTION_FORWARD;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_neighbor_info->action = attr_value->s32;
    }

    ctc_sai_router_interface_get_rif_info(neighbor_entry->rif_id, &rif_type, NULL, NULL, NULL);
    CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info, (uint8)neighbor_entry->ip_address.addr_family), status, error1);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE, &attr_value, &index);
    if (SAI_STATUS_SUCCESS == status)/* create ipuc nexthop and host route */
    {
        p_neighbor_info->no_host_route = attr_value->booldata;
    }
    if (0 == p_neighbor_info->no_host_route)
    {
        if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_ipuc_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info), status, error2);
        }
        CTC_SAI_ERROR_GOTO(_ctc_sai_neighbor_add_host_route(lchip, neighbor_entry, p_neighbor_info), status, error3);
    }
    p_neighbor_info->ref_cnt++;

    p_switch_master = ctc_sai_get_switch_property(lchip);
    p_switch_master->neighbor_cnt[neighbor_entry->ip_address.addr_family]++;

    goto out;

error3:
    CTC_SAI_LOG_ERROR(SAI_API_NEIGHBOR, "rollback to error3\n");
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE != rif_type)
    {
        _ctc_sai_neighbor_remove_ipuc_nexthop(lchip, p_neighbor_info);
    }
error2:
    CTC_SAI_LOG_ERROR(SAI_API_NEIGHBOR, "rollback to error2\n");
    _ctc_sai_neighbor_remove_nexthop(lchip, neighbor_entry->rif_id, p_neighbor_info);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_NEIGHBOR, "rollback to error1\n");
    _ctc_sai_neighbor_remove_db(lchip, neighbor_entry->rif_id, (sai_ip_address_t*)(&(neighbor_entry->ip_address)), 0);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_neighbor_remove_neighbor(const sai_neighbor_entry_t *neighbor_entry)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    CTC_SAI_PTR_VALID_CHECK(neighbor_entry);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    status = _ctc_sai_neighbor_remove_neighbor(neighbor_entry);
    if (SAI_STATUS_SUCCESS == status)
    {
        p_switch_master = ctc_sai_get_switch_property(lchip);
        p_switch_master->neighbor_cnt[neighbor_entry->ip_address.addr_family]--;
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_neighbor_set_neighbor_attr(const sai_neighbor_entry_t *neighbor_entry,
                                                            const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    CTC_SAI_PTR_VALID_CHECK(neighbor_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memcpy(&key.key.neighbor_entry, neighbor_entry, sizeof(sai_neighbor_entry_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_NEIGHBOR_ENTRY,  neighbor_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_neighbor_get_neighbor_attr(const sai_neighbor_entry_t *neighbor_entry,
                                                             uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    CTC_SAI_PTR_VALID_CHECK(neighbor_entry);
    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(neighbor_entry->switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);
    sal_memcpy(&key.key.neighbor_entry, neighbor_entry, sizeof(sai_neighbor_entry_t));
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_NEIGHBOR_ENTRY, loop, neighbor_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_neighbor_remove_all_neighbor(sai_object_id_t switch_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_neighbor_traverse_param_t traverse_param;
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_NEIGHBOR);

    sal_memset(&traverse_param, 0, sizeof(traverse_param));
    traverse_param.traverse_type = CTC_SAI_NEIGHBOR_REMOVE_ALL;
    traverse_param.switch_id = switch_id;

    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, (hash_traversal_fn)_ctc_sai_neighbor_hash_traverse_fun, (void*)(&traverse_param));

    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_neighbor_api_t ctc_sai_neighbor_api = {
     ctc_sai_neighbor_create_neighbor,
     ctc_sai_neighbor_remove_neighbor,
     ctc_sai_neighbor_set_neighbor_attr,
     ctc_sai_neighbor_get_neighbor_attr,
     ctc_sai_neighbor_remove_all_neighbor
};

sai_status_t
ctc_sai_neighbor_api_init()
{
    ctc_sai_register_module_api(SAI_API_NEIGHBOR, (void*)&ctc_sai_neighbor_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_neighbor_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_NEIGHBOR;
    wb_info.data_len = sizeof(ctc_sai_neighbor_t);
    wb_info.wb_sync_cb = _ctc_sai_neighbor_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_neighbor_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_neighbor_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_neighbor_db_deinit(uint8 lchip)
{
    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_NEIGHBOR, (hash_traversal_fn)_ctc_sai_neighbor_db_deinit_cb, NULL);
    return SAI_STATUS_SUCCESS;
}

