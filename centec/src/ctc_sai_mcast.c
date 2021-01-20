/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
/*sdk include file*/
#include "ctcs_api.h"
#include "ctc_sai_db.h"
#include "ctc_sai_mcast.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_vlan.h"
#include "ctc_init.h"

#define ________COMMON_FUNCTION________
uint16 _ctc_sai_mcast_get_group_id(sai_object_id_t oid)
{
    ctc_object_id_t ctc_oid;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, oid, &ctc_oid);

    return ctc_oid.value2;
}

sai_object_id_t _ctc_sai_mcast_create_group_object_id(sai_object_type_t type, uint8 lchip, uint16 group_id)
{
    return ctc_sai_create_object_id(type, lchip, 0, group_id, 0);
}

sai_status_t ctc_sai_packet_action_merge(sai_packet_action_t action, sai_packet_action_t* update_action)
{
    switch(action)
    {
    case SAI_PACKET_ACTION_FORWARD:
        switch(*update_action)
        {
            case SAI_PACKET_ACTION_TRAP:
                *update_action = SAI_PACKET_ACTION_LOG;
                break;
            case SAI_PACKET_ACTION_LOG:
                *update_action = SAI_PACKET_ACTION_LOG;
                break;
            case SAI_PACKET_ACTION_DENY:
                *update_action = SAI_PACKET_ACTION_TRANSIT;
                break;
            case SAI_PACKET_ACTION_TRANSIT:
                *update_action = SAI_PACKET_ACTION_TRANSIT;
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action merge SAI_PACKET_ACTION_FORWARD! \n");
                break;
        }
        break;
    case SAI_PACKET_ACTION_DROP:
        switch(*update_action)
        {
            case SAI_PACKET_ACTION_TRAP:
                *update_action = SAI_PACKET_ACTION_TRAP;
                break;
            case SAI_PACKET_ACTION_LOG:
                *update_action = SAI_PACKET_ACTION_TRAP;
                break;
            case SAI_PACKET_ACTION_DENY:
                *update_action = SAI_PACKET_ACTION_DENY;
                break;
            case SAI_PACKET_ACTION_TRANSIT:
                *update_action = SAI_PACKET_ACTION_DENY;
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action merge SAI_PACKET_ACTION_DROP! \n");
                break;
        }
        break;
    case SAI_PACKET_ACTION_COPY:
        switch(*update_action)
        {
            case SAI_PACKET_ACTION_TRAP:
                *update_action = SAI_PACKET_ACTION_TRAP;
                break;
            case SAI_PACKET_ACTION_LOG:
                *update_action = SAI_PACKET_ACTION_LOG;
                break;
            case SAI_PACKET_ACTION_DENY:
                *update_action = SAI_PACKET_ACTION_TRAP;
                break;
            case SAI_PACKET_ACTION_TRANSIT:
                *update_action = SAI_PACKET_ACTION_LOG;
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action merge SAI_PACKET_ACTION_COPY! \n");
                break;
        }
        break;
    case SAI_PACKET_ACTION_COPY_CANCEL:
        switch(*update_action)
        {
            case SAI_PACKET_ACTION_TRAP:
                *update_action = SAI_PACKET_ACTION_DENY;
                break;
            case SAI_PACKET_ACTION_LOG:
                *update_action = SAI_PACKET_ACTION_TRANSIT;
                break;
            case SAI_PACKET_ACTION_DENY:
                *update_action = SAI_PACKET_ACTION_DENY;
                break;
            case SAI_PACKET_ACTION_TRANSIT:
                *update_action = SAI_PACKET_ACTION_TRANSIT;
                break;
            default:
                CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action merge SAI_PACKET_ACTION_COPY_CANCEL! \n");
                break;
        }
        break;
    case SAI_PACKET_ACTION_TRAP:
    case SAI_PACKET_ACTION_LOG:
    case SAI_PACKET_ACTION_DENY:
    case SAI_PACKET_ACTION_TRANSIT:
        *update_action = action;
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action merge! \n");
        break;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_mapping_ctc_action(uint32*flag, sai_packet_action_t action)
{
    switch(action)
    {
    case SAI_PACKET_ACTION_FORWARD:
        CTC_UNSET_FLAG(*flag, CTC_IPMC_FLAG_DROP);
        break;
    case SAI_PACKET_ACTION_DROP:
        CTC_SET_FLAG( *flag, CTC_IPMC_FLAG_DROP);
        break;
    case SAI_PACKET_ACTION_COPY:
        CTC_SET_FLAG(*flag, CTC_IPMC_FLAG_COPY_TOCPU);
        break;
    case SAI_PACKET_ACTION_COPY_CANCEL:
        CTC_UNSET_FLAG(*flag, CTC_IPMC_FLAG_COPY_TOCPU);
        break;
    case SAI_PACKET_ACTION_TRAP :
        CTC_SET_FLAG( *flag, CTC_IPMC_FLAG_DROP);
        CTC_SET_FLAG( *flag, CTC_IPMC_FLAG_COPY_TOCPU);
        break;
    case SAI_PACKET_ACTION_LOG:
        CTC_UNSET_FLAG( *flag, CTC_IPMC_FLAG_DROP);
        CTC_SET_FLAG( *flag, CTC_IPMC_FLAG_COPY_TOCPU);
        break;
    case SAI_PACKET_ACTION_DENY:
        CTC_UNSET_FLAG(*flag , CTC_IPMC_FLAG_COPY_TOCPU);
        CTC_SET_FLAG(*flag, CTC_IPMC_FLAG_DROP);
        break;
    case SAI_PACKET_ACTION_TRANSIT:
        CTC_UNSET_FLAG(*flag,  CTC_IPMC_FLAG_DROP);
        CTC_UNSET_FLAG(*flag, CTC_IPMC_FLAG_COPY_TOCPU);
        break;        
    default:
        CTC_SAI_LOG_ERROR(SAI_API_IPMC, "invalid action! \n");
        return SAI_STATUS_INVALID_ATTR_VALUE_0 + action;

    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_l2mc_to_param(const sai_l2mc_entry_t *p_l2mc_entry, ctc_ipmc_group_info_t* p_grp_param)
{
    uint16 fid = 0;
    p_grp_param->ip_version = (p_l2mc_entry->destination.addr_family == SAI_IP_ADDR_FAMILY_IPV4) ? CTC_IP_VER_4 : CTC_IP_VER_6;
    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(p_l2mc_entry->bv_id, &fid));
    if (p_grp_param->ip_version == CTC_IP_VER_4)
    {
        p_grp_param->group_ip_mask_len = 32;
        p_grp_param->src_ip_mask_len = (p_l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG) ? 32 : 0;
        p_grp_param->address.ipv4.group_addr = sal_ntohl(p_l2mc_entry->destination.addr.ip4);
        p_grp_param->address.ipv4.src_addr = sal_ntohl(p_l2mc_entry->source.addr.ip4);
        p_grp_param->address.ipv4.vrfid = fid;
    }
    else
    {
        p_grp_param->group_ip_mask_len = 128;
        p_grp_param->src_ip_mask_len = (p_l2mc_entry->type == SAI_L2MC_ENTRY_TYPE_SG) ? 128 : 0;
        p_grp_param->address.ipv6.vrfid = fid;
        sal_memcpy(p_grp_param->address.ipv6.group_addr, p_l2mc_entry->destination.addr.ip6, sizeof(sai_ip6_t));
        sal_memcpy(p_grp_param->address.ipv6.src_addr, p_l2mc_entry->source.addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.group_addr);
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.src_addr);
    }

    CTC_SET_FLAG(p_grp_param->flag, CTC_IPMC_FLAG_L2MC);
    CTC_SET_FLAG(p_grp_param->flag, CTC_IPMC_FLAG_SHARE_GROUP);

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_ipmc_to_param(const sai_ipmc_entry_t *p_ipmc_entry, ctc_ipmc_group_info_t* p_grp_param)
{
    ctc_object_id_t ctc_oid;
    p_grp_param->ip_version = (p_ipmc_entry->destination.addr_family == SAI_IP_ADDR_FAMILY_IPV4) ? CTC_IP_VER_4 : CTC_IP_VER_6;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, p_ipmc_entry->vr_id, &ctc_oid);
    if (p_grp_param->ip_version == CTC_IP_VER_4)
    {
        p_grp_param->group_ip_mask_len = 32;
        p_grp_param->src_ip_mask_len = (p_ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG) ? 32 : 0;
        p_grp_param->address.ipv4.group_addr = sal_ntohl(p_ipmc_entry->destination.addr.ip4);
        p_grp_param->address.ipv4.src_addr = sal_ntohl(p_ipmc_entry->source.addr.ip4);
        p_grp_param->address.ipv4.vrfid = ctc_oid.value;
    }
    else
    {
        p_grp_param->group_ip_mask_len = 128;
        p_grp_param->src_ip_mask_len = (p_ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG) ? 128 : 0;
        p_grp_param->address.ipv6.vrfid = ctc_oid.value;
        sal_memcpy(p_grp_param->address.ipv6.group_addr, p_ipmc_entry->destination.addr.ip6, sizeof(sai_ip6_t));
        sal_memcpy(p_grp_param->address.ipv6.src_addr, p_ipmc_entry->source.addr.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.group_addr);
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.src_addr);
    }

    CTC_SET_FLAG(p_grp_param->flag, CTC_IPMC_FLAG_SHARE_GROUP);

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_ipmc_key_to_param(ctc_sai_mcast_ip_key_t *p_ipmc_key, ctc_ipmc_group_info_t* p_grp_param)
{
    p_grp_param->ip_version = (p_ipmc_key->ip_ver == SAI_IP_ADDR_FAMILY_IPV4) ? CTC_IP_VER_4 : CTC_IP_VER_6;
    if (p_grp_param->ip_version == CTC_IP_VER_4)
    {
        p_grp_param->group_ip_mask_len = 32;
        p_grp_param->src_ip_mask_len = p_ipmc_key->src_mask_len;
        p_grp_param->address.ipv4.group_addr = sal_ntohl(p_ipmc_key->dst.ip4);
        p_grp_param->address.ipv4.src_addr = sal_ntohl(p_ipmc_key->src.ip4);
        p_grp_param->address.ipv4.vrfid = p_ipmc_key->vrf_id;
    }
    else
    {
        p_grp_param->group_ip_mask_len = 128;
        p_grp_param->src_ip_mask_len = p_ipmc_key->src_mask_len;
        p_grp_param->address.ipv6.vrfid = p_ipmc_key->vrf_id;
        sal_memcpy(p_grp_param->address.ipv6.group_addr, p_ipmc_key->dst.ip6, sizeof(sai_ip6_t));
        sal_memcpy(p_grp_param->address.ipv6.src_addr, p_ipmc_key->src.ip6, sizeof(sai_ip6_t));
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.group_addr);
        CTC_SAI_NTOH_V6(p_grp_param->address.ipv6.src_addr);
    }

    CTC_SET_FLAG(p_grp_param->flag, CTC_IPMC_FLAG_SHARE_GROUP);

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_sai_to_ctc_l3if_type(sai_router_interface_type_t sai_l3if_type, ctc_l3if_type_t *ctc_l3if_type)
{
    switch (sai_l3if_type)
    {
        case SAI_ROUTER_INTERFACE_TYPE_PORT:
            *ctc_l3if_type = CTC_L3IF_TYPE_PHY_IF;
            break;
        case SAI_ROUTER_INTERFACE_TYPE_VLAN:
            *ctc_l3if_type = CTC_L3IF_TYPE_VLAN_IF;
            break;
        case SAI_ROUTER_INTERFACE_TYPE_SUB_PORT:
            *ctc_l3if_type = CTC_L3IF_TYPE_SUB_IF;
            break;
        default:
            return SAI_STATUS_INVALID_PARAMETER;
            break;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t _ctc_sai_mcast_ipmc_key_to_entry(ctc_sai_mcast_ip_key_t *ipmc_entry_key, sai_ipmc_entry_t *p_ipmc_entry)
{
    p_ipmc_entry->type = SAI_IPMC_ENTRY_TYPE_XG;
    p_ipmc_entry->destination.addr_family = ipmc_entry_key->ip_ver;
    sal_memcpy(&(p_ipmc_entry->destination.addr), &(ipmc_entry_key->dst.ip6), sizeof(sai_ip6_t));

    if (ipmc_entry_key->src_mask_len)
    {
        p_ipmc_entry->type = SAI_IPMC_ENTRY_TYPE_SG;
        p_ipmc_entry->source.addr_family = ipmc_entry_key->ip_ver;
        sal_memcpy(&(p_ipmc_entry->source.addr), &(ipmc_entry_key->src.ip6), sizeof(sai_ip6_t));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_mcast_get_member_group_id(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_object_type_t   type = 0;
    uint16 grp_id = 0;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_oid_get_type(key->key.object_id, &type);

    grp_id = _ctc_sai_mcast_get_group_id(key->key.object_id);

    type = (type == SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER) ? SAI_OBJECT_TYPE_L2MC_GROUP : SAI_OBJECT_TYPE_IPMC_GROUP;
    attr->value.oid = _ctc_sai_mcast_create_group_object_id(type, lchip, grp_id);

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_mcast_get_member_output_id(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    ctc_object_id_t       ctc_oid;
    sai_object_type_t   type = 0;
    uint16 vid = 0;
    uint16 vlan_ptr = 0;
    uint16 destid = 0;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_oid_get_type(key->key.object_id, &type);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, key->key.object_id, &ctc_oid);

    if (type == SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER)
    {
        destid = ctc_oid.value;
        CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_bridge_port_oid(lchip, destid, 0, &attr->value.oid));
    }
    else
    {
        /*if sub_type is port or sub_port*/
        vid = ctc_oid.value >> 20; 
        destid = ctc_oid.value & 0xFFFFF;
        /*if sub_type is vlan*/
        if (ctc_oid.sub_type == SAI_ROUTER_INTERFACE_TYPE_VLAN)
        {
            vlan_ptr = ctc_oid.value;
            ctc_sai_vlan_get_vlan_id_from_vlan_ptr(lchip, vlan_ptr, &vid);
            destid = 0;
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_lookup_rif_oid(lchip, ctc_oid.sub_type, destid, vid, &attr->value.oid));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_mcast_get_group_member_count(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_slistnode_t       *node = NULL;
    uint32                     output_cnt = 0;
    uint8                       lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);

    p_group_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (!p_group_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        output_cnt++;
    }

    attr->value.u32 = output_cnt;

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_mcast_get_l2_group_member_bridge_port_list(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    sai_object_id_t *mcast_member_oid;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t       *node = NULL;
    uint32                     output_cnt = 0;
    uint8                       lchip = 0;
    uint16                        grp_id = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    grp_id = _ctc_sai_mcast_get_group_id(key->key.object_id);

    p_group_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (!p_group_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    mcast_member_oid = mem_malloc(MEM_SYSTEM_MODULE, attr->value.objlist.count * sizeof(sai_object_id_t));
    if (!mcast_member_oid)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        if (output_cnt < attr->value.objlist.count)
        {
            mcast_member_oid[output_cnt++] = po->output_id;          
        }
        else
        {
            status = SAI_STATUS_BUFFER_OVERFLOW;
            break;
        }
    }

    ctc_sai_fill_object_list(sizeof(sai_object_id_t), mcast_member_oid, output_cnt, (void*)&attr->value.objlist);
    mem_free(mcast_member_oid);

    return status;
}


sai_status_t ctc_sai_mcast_get_group_member_list(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    sai_object_id_t *mcast_member_oid;
    sai_object_id_t ipmc_member_oid;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t       *node = NULL;
    sai_router_interface_type_t sai_l3if_type = 0;
    uint32                     output_cnt = 0;
    uint32                        value = 0;
    uint16                        vlan_ptr = 0;
    uint16                        vlan_id = 0;
    uint16                        grp_id = 0;
    uint8                       lchip = 0;
    uint8                       oid_type = 0;
    ctc_sai_bridge_port_t*      p_bridge_port = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    grp_id = _ctc_sai_mcast_get_group_id(key->key.object_id);

    p_group_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (!p_group_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    mcast_member_oid = mem_malloc(MEM_SYSTEM_MODULE, attr->value.objlist.count * sizeof(sai_object_id_t));
    if (!mcast_member_oid)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    oid_type = sai_object_type_query(key->key.object_id);
    if (oid_type == SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER)
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            if (output_cnt < attr->value.objlist.count)
            {
                ctc_sai_router_interface_get_rif_info(po->output_id, (uint8*)&sai_l3if_type, NULL, &value, &vlan_id);
                if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN))
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_vlan_ptr(po->output_id, &vlan_ptr));
                    value = vlan_ptr;
                }
                else if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT))
                {
                    value = (vlan_id << 20) | (value & 0xFFFFF);
                }
                ipmc_member_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, lchip, sai_l3if_type, grp_id, value);
                mcast_member_oid[output_cnt++] = ipmc_member_oid;
            }
            else
            {
                status = SAI_STATUS_BUFFER_OVERFLOW;
                break;
            }
        }
    }
    else 
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            if (output_cnt < attr->value.objlist.count)
            {
                p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
                mcast_member_oid[output_cnt++] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, lchip, 0, grp_id, p_bridge_port->gport);          
            }
            else
            {
                status = SAI_STATUS_BUFFER_OVERFLOW;
                break;
            }
        }

    }

    ctc_sai_fill_object_list(sizeof(sai_object_id_t), mcast_member_oid, output_cnt, (void*)&attr->value.objlist);
    mem_free(mcast_member_oid);

    return status;
}


static sai_status_t _ctc_sai_mcast_check_l2mc_member_list(sai_object_id_t bv_id, ctc_slist_t *output_id_head)
{
    sai_object_key_t key;
    sai_attribute_t attr, attr1;
    sai_object_id_t vlan_objlist[256] = {0};
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    uint16 loop = 0;
    uint8 find = 0;
    uint8 lchip = 0;
    ctc_object_id_t   ctc_obj_id;

    ctc_sai_oid_get_lchip(bv_id, &lchip);

    key.key.object_id = bv_id;
    attr.id = SAI_VLAN_ATTR_MEMBER_LIST;
    attr.value.objlist.list = vlan_objlist;
    attr.value.objlist.count = 256;
    CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_info(&key, &attr, 0));

    attr1.id = SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID;
    for (loop = 0; loop < attr.value.objlist.count; loop++)
    {
        key.key.object_id = attr.value.objlist.list[loop];
        CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_member(&key, &attr1, loop));
        vlan_objlist[loop] = attr1.value.oid;
    }

    CTC_SLIST_LOOP(output_id_head, node)
    {
        find = 0;
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, po->output_id, &ctc_obj_id);            
        for (loop = 0; loop < attr.value.objlist.count; loop++)
        {

            if (po->output_id == vlan_objlist[loop])
            {
                find = 1;
                break;
            }
        }

        if (!find)
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC,"bv id 0x%llx don't contain output id 0x%llx\n", bv_id, po->output_id);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t _ctc_sai_mcast_get_vlan_interface_member_list(
        uint8 lchip,
        uint16 vlan_ptr,
        sai_ipmc_entry_t *ipmc_entry,
        sai_object_list_t *objlist,
        ctc_sai_mcast_ipmc_bind_type_t *bind_type)
{
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    sai_mcast_fdb_entry_t mcast_fdb_entry = {0};
    sai_l2mc_entry_t l2mc_entry = {0};
    sai_object_id_t vlan_oid = 0;
    sai_object_key_t key;
    sai_attribute_t attr;

    if (bind_type)
    {
        *bind_type = CTC_SAI_MCAST_IPMC_BIND_NONE;
    }

    vlan_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, vlan_ptr);

    attr.value.objlist.count = objlist->count;
    attr.value.objlist.list = objlist->list;
    objlist->count = 0;

    l2mc_entry.switch_id = ipmc_entry->switch_id;
    l2mc_entry.bv_id = vlan_oid;
    sal_memcpy(&l2mc_entry.destination, &ipmc_entry->destination, sizeof(sai_ip_address_t));

    if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
    {
        l2mc_entry.type = SAI_L2MC_ENTRY_TYPE_SG;
        sal_memcpy(&l2mc_entry.source, &ipmc_entry->source, sizeof(sai_ip_address_t));
    }
    else
    {
        l2mc_entry.type = SAI_L2MC_ENTRY_TYPE_XG;
    }

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)&l2mc_entry);
    if (p_entry_data)
    {
        key.key.object_id = p_entry_data->group_oid;

        CTC_SAI_ERROR_RETURN(ctc_sai_mcast_get_l2_group_member_bridge_port_list(&key, &attr, 0));

        if (bind_type)
        {
            *bind_type = CTC_SAI_MCAST_IPMC_BIND_L2MC;
        }
        objlist->count = attr.value.objlist.count;
        return SAI_STATUS_SUCCESS;
    }

/* first sg lookup , if not find than xg lookup */
    
    if (ipmc_entry->type == SAI_IPMC_ENTRY_TYPE_SG)
    {
        l2mc_entry.type = SAI_L2MC_ENTRY_TYPE_XG;

        p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)&l2mc_entry);
        if (p_entry_data)
        {
            key.key.object_id = p_entry_data->group_oid;

            CTC_SAI_ERROR_RETURN(ctc_sai_mcast_get_l2_group_member_bridge_port_list(&key, &attr, 0));

            if (bind_type)
            {
                *bind_type = CTC_SAI_MCAST_IPMC_BIND_L2MC;
            }
            objlist->count = attr.value.objlist.count;
            return SAI_STATUS_SUCCESS;
        }
    }
    
    mcast_fdb_entry.switch_id = ipmc_entry->switch_id;
    mcast_fdb_entry.bv_id = vlan_oid;
    if (ipmc_entry->destination.addr_family == SAI_IP_ADDR_FAMILY_IPV4)
    {
        *(uint32*)&mcast_fdb_entry.mac_address[2] = sal_htonl(sal_htonl(ipmc_entry->destination.addr.ip4) & 0x7FFFFF);
        *(uint32*)&mcast_fdb_entry.mac_address[0] |= sal_htonl(0x01005E00);
    }
    else
    {
        *(uint32*)&mcast_fdb_entry.mac_address[2] = *(uint32*)&ipmc_entry->destination.addr.ip6[12];
        *(uint16*)&mcast_fdb_entry.mac_address[0] = sal_htons(0x3333);
    }

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)&mcast_fdb_entry);
    if (p_entry_data)
    {
        key.key.object_id = p_entry_data->group_oid;

        CTC_SAI_ERROR_RETURN(ctc_sai_mcast_get_l2_group_member_bridge_port_list(&key, &attr, 0));

        if (bind_type)
        {
            *bind_type = CTC_SAI_MCAST_IPMC_BIND_FDB;
        }
        objlist->count = attr.value.objlist.count;
        return SAI_STATUS_SUCCESS;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_mcast_update_ipmc_group_member(
            ctc_sai_entry_property_t *p_entry_property,
            sai_object_id_t member_or_output_id,
            uint8 is_add)
{
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_bridge_port_t *p_bridge_port = NULL;
    sai_ipmc_entry_t       ipmc_entry = {0};
    ctc_sai_mcast_entry_bind_node_t *bind_node = NULL;
    ctc_sai_mcast_ipmc_bind_type_t bind_type = 0;
    sai_router_interface_type_t sai_l3if_type = 0;
    sai_object_id_t          mem_list[256] = {0};
    sai_object_list_t         objlist;
    ctc_slistnode_t           *node = NULL;
    sai_object_type_t      type = 0;
    ctc_object_id_t         ctc_oid;
    uint32                        nh_id;
    uint16                        vlan_ptr = 0;
    uint16                        loop = 0;
    uint8                          lchip = 0;

    objlist.list = mem_list;
    objlist.count = 256;

    p_entry_data = (ctc_sai_mcast_entry_property_t *)p_entry_property->data;
    if (!p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP,"entry property data is NULL\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_oid_get_lchip(member_or_output_id, &lchip);

    nh_mcast_group.opcode = is_add ? CTC_NH_PARAM_MCAST_ADD_MEMBER : CTC_NH_PARAM_MCAST_DEL_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_IPMC_LOCAL;
    nh_mcast_group.mc_grp_id = p_entry_data->group_id;
    CTC_SAI_ERROR_RETURN(ctcs_nh_get_mcast_nh(lchip, nh_mcast_group.mc_grp_id, &nh_id));

    ctc_sai_oid_get_type(member_or_output_id, &type);

    if (type == SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, member_or_output_id, &ctc_oid);
        sai_l3if_type = ctc_oid.sub_type;

        if (sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN)
        {
            vlan_ptr = ctc_oid.value;
            CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_id_from_vlan_ptr(lchip, vlan_ptr, &nh_mcast_group.mem_info.vid));
        }
        else if (sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT)
        {
            nh_mcast_group.mem_info.destid = ctc_oid.value & 0xFFFFF;

            vlan_ptr = ctc_oid.value >> 20;
            CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_id_from_vlan_ptr(lchip, vlan_ptr, &nh_mcast_group.mem_info.vid));
        }
        else
        {
            nh_mcast_group.mem_info.destid = ctc_oid.value;
        }
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(member_or_output_id, (uint8*)&sai_l3if_type,
                NULL, &nh_mcast_group.mem_info.destid, &nh_mcast_group.mem_info.vid));
    }
    
    _ctc_sai_mcast_sai_to_ctc_l3if_type(sai_l3if_type, (ctc_l3if_type_t*)&nh_mcast_group.mem_info.l3if_type);

    if (sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN)
    {
        if (type != SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER)
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_vlan_ptr(member_or_output_id, &vlan_ptr));
        }

        CTC_SLIST_LOOP(p_entry_data->bind_type_head, node)
        {
            bind_node = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);
            if (bind_node->vlan_ptr == vlan_ptr)
            {
                break;
            }
            else
            {
                bind_node = NULL;
            }
        }

        if (is_add && bind_node)
        {
            CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "add ipmc group member, ipmc entry vlan ptr %d bind %s already\n", bind_node->vlan_ptr,
                    (bind_node->bind_type ? ((bind_node->bind_type == CTC_SAI_MCAST_IPMC_BIND_L2MC) ? "l2mc" : "fdb") : "none"));
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }
        else if (!is_add && !bind_node)
        {
            CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "delete ipmc group member, ipmc entry vlan ptr %d don't bind\n", vlan_ptr);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }

        if (!bind_node)
        {
            bind_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_bind_node_t));
            if (!bind_node)
            {
                return SAI_STATUS_NO_MEMORY;
            }
            bind_node->vlan_ptr = vlan_ptr;
        }

        _ctc_sai_mcast_ipmc_key_to_entry(&p_entry_property->key.mcast_ip, &ipmc_entry);
        CTC_SAI_ERROR_RETURN(_ctc_sai_mcast_get_vlan_interface_member_list(lchip, vlan_ptr, &ipmc_entry, &objlist, &bind_type));

        for (loop = 0; loop < objlist.count; loop++)
        {
            p_bridge_port = ctc_sai_db_get_object_property(lchip, objlist.list[loop]);
            if ( !p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
            {
                CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", objlist.list[loop]);
                return SAI_STATUS_INVALID_OBJECT_ID;
            }

            nh_mcast_group.mem_info.destid = p_bridge_port->gport;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group));

            CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "%s ipmc group member, nh_id: %d, group id: %d, %s oid: 0x%llx, l3if type: %d, vlan id: %d, port: %d\n",
                (is_add ? "Add" : "Remove"), nh_id, nh_mcast_group.mc_grp_id, ((type == SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER) ? "member" : "output"),
                member_or_output_id, nh_mcast_group.mem_info.l3if_type, nh_mcast_group.mem_info.vid, nh_mcast_group.mem_info.destid);
        }

        if (is_add)
        {
            bind_node->bind_type = bind_type;
            ctc_slist_add_tail(p_entry_data->bind_type_head, &(bind_node->node));
        }
        else
        {
            ctc_slist_delete_node(p_entry_data->bind_type_head, &(bind_node->node));
        }
    }
    else
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group));

        CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "%s ipmc group member, nh_id: %d, group id: %d, %s oid: 0x%llx, l3if type: %d, vlan id: %d, port: %d\n",
                (is_add ? "Add" : "Remove"), nh_id, nh_mcast_group.mc_grp_id, ((type == SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER) ? "member" : "output"),
                member_or_output_id, nh_mcast_group.mem_info.l3if_type, nh_mcast_group.mem_info.vid, nh_mcast_group.mem_info.destid);
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t _ctc_sai_mcast_sync_output_id(
        ctc_sai_entry_property_t *p_entry_property,
        ctc_sai_mcast_vlan_member_priv_t *p_travs_data)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = (ctc_sai_mcast_entry_property_t *)p_entry_property->data;
    ctc_sai_mcast_ip_key_t *key0 = &p_entry_property->key.mcast_ip;
    ctc_sai_mcast_ip_key_t *key1 = NULL;
    ctc_sai_mcast_fdb_key_t *key2 = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_bind_node_t *bind_node = NULL;
    ctc_sai_mcast_ipmc_bind_type_t bind_type = 0;
    ctc_slistnode_t *node = NULL;
    ctc_slistnode_t *node1 = NULL;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    sai_router_interface_type_t sai_l3if_type = 0;
    mac_addr_t      mac = {0};
    ctc_object_id_t ctc_oid;
    uint32               nh_id;
    uint16               vlan_ptr = 0;
    uint16               fid = 0;
    uint8                 match = 0;

    if (!p_entry_data->group_oid)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC)
    {
        key1 = &p_travs_data->p_entry_property->key.mcast_ip;
        if (key0->ip_ver != key1->ip_ver)
        {
            return SAI_STATUS_SUCCESS;
        }

        if (sal_memcmp(&key0->dst, &key1->dst, sizeof(sai_ip6_t)))
        {
            return SAI_STATUS_SUCCESS;
        }

        if (key1->src_mask_len)
        {
            if (sal_memcmp(&key0->src, &key1->src, sizeof(sai_ip6_t)))
            {
                return SAI_STATUS_SUCCESS;
            }
        }

        fid = key1->vrf_id;
    }
    else if (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB)
    {
        key2 = &p_travs_data->p_entry_property->key.mcast_fdb;

        if (key0->ip_ver == SAI_IP_ADDR_FAMILY_IPV4)
        {
            *(uint32*)&mac[2] = sal_htonl(sal_ntohl(key0->dst.ip4) & 0x7FFFFF);
            *(uint32*)&mac[0] |= sal_htonl(0x01005E00);
        }
        else
        {
            *(uint32*)&mac[2] = *(uint32*)&key0->dst.ip6[12];
            *(uint16*)&mac[0] = sal_htons(0x3333);
        }

        if (sal_memcmp(mac, key2->mac, sizeof(mac_addr_t)))
        {
            return SAI_STATUS_SUCCESS;
        }

        fid = key2->fid;
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "invalid entry type: %d\n", p_travs_data->p_entry_property->entry_type);
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SLIST_LOOP(p_entry_data->bind_type_head, node)
    {
        bind_node = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);
        if (bind_node->vlan_ptr == fid)
        {
            break;
        }
    }

    if ((p_travs_data->opt_type == CTC_SAI_DELETE) && !bind_node)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "delete l2mc/fdb group member, ipmc entry vlan ptr %d don't bind\n", fid);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    bind_type = bind_node ? bind_node->bind_type : CTC_SAI_MCAST_IPMC_BIND_NONE;

    /* valid if don't bind, or bind fdb -> l2mc when it is entry*/
    if (!p_travs_data->is_member && (p_travs_data->opt_type == CTC_SAI_ADD))
    {  
        if ((bind_type != CTC_SAI_MCAST_IPMC_BIND_NONE)
            && !((bind_type == CTC_SAI_MCAST_IPMC_BIND_FDB) && (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC)))
        {
            return SAI_STATUS_SUCCESS;
        }
    }
    else
    {
        if ((bind_type == CTC_SAI_MCAST_IPMC_BIND_NONE)
            || ((bind_type == CTC_SAI_MCAST_IPMC_BIND_L2MC) && (p_travs_data->p_entry_property->entry_type != CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC))
            || ((bind_type == CTC_SAI_MCAST_IPMC_BIND_FDB) && (p_travs_data->p_entry_property->entry_type != CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB)))
        {
                return SAI_STATUS_SUCCESS;
        }
    }

    p_group_data = ctc_sai_db_get_object_property(p_travs_data->lchip, p_entry_data->group_oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP,"ipmc group db is not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        ctc_sai_router_interface_get_vlan_ptr(po->output_id, &vlan_ptr);
        if (!vlan_ptr || (vlan_ptr != fid))
        {
            continue;
        }
        match = 1;
        break;
    }

    if (!match)
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_ERROR_RETURN(ctcs_nh_get_mcast_nh(p_travs_data->lchip, p_entry_data->group_id, &nh_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_vlan_id_from_vlan_ptr(p_travs_data->lchip, fid, &nh_mcast_group.mem_info.vid));

    nh_mcast_group.mc_grp_id = p_entry_data->group_id;
    nh_mcast_group.opcode = (p_travs_data->opt_type == CTC_SAI_ADD) ? CTC_NH_PARAM_MCAST_ADD_MEMBER : CTC_NH_PARAM_MCAST_DEL_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_IPMC_LOCAL;
    nh_mcast_group.mem_info.l3if_type = CTC_L3IF_TYPE_VLAN_IF;

    if (p_travs_data->is_member)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, p_travs_data->member.member_id, &ctc_oid);

        nh_mcast_group.mem_info.destid = ctc_oid.value;
        CTC_SAI_ERROR_RETURN(ctcs_nh_update_mcast(p_travs_data->lchip, nh_id, &nh_mcast_group));

        CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "%s ipmc group member, nh_id: %d, group id: %d, member oid: 0x%llx, l3if type: %d, vlan id: %d, port: %d\n",
                ((nh_mcast_group.opcode == CTC_NH_PARAM_MCAST_ADD_MEMBER) ? "Add" : "Remove"), nh_id, nh_mcast_group.mc_grp_id, p_travs_data->member.member_id,
                nh_mcast_group.mem_info.l3if_type, nh_mcast_group.mem_info.vid, nh_mcast_group.mem_info.destid);
    }
    else
    {
         /*clean nexthop if entry binded fdb*/
    
        if ((p_travs_data->opt_type == CTC_SAI_ADD)
            && (bind_type == CTC_SAI_MCAST_IPMC_BIND_FDB)
            && (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC))
        {  
            ctc_ipmc_group_info_t grp_param = {0};

            grp_param.group_id = p_entry_data->group_id;
            _ctc_sai_mcast_ipmc_key_to_param(key0, &grp_param);
            CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_KEEP_EMPTY_ENTRY);

            CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_remove_group(p_travs_data->lchip, &grp_param));
        }

        CTC_SLIST_LOOP(p_travs_data->member.output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            p_bridge_port = ctc_sai_db_get_object_property(p_travs_data->lchip, po->output_id);
            if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
            {
                CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
                continue;
            }

            nh_mcast_group.mem_info.destid = p_bridge_port->gport;
            CTC_SAI_ERROR_RETURN(ctcs_nh_update_mcast(p_travs_data->lchip, nh_id, &nh_mcast_group));

            CTC_SAI_LOG_INFO(SAI_API_L2MC_GROUP, "%s ipmc group member, nh_id: %d, group id: %d, output oid: 0x%llx, l3if type: %d, vlan id: %d, port: %d\n",
                ((nh_mcast_group.opcode == CTC_NH_PARAM_MCAST_ADD_MEMBER) ? "Add" : "Remove"), nh_id, nh_mcast_group.mc_grp_id, po->output_id,
                nh_mcast_group.mem_info.l3if_type, nh_mcast_group.mem_info.vid, nh_mcast_group.mem_info.destid);
        }

        if (p_travs_data->opt_type == CTC_SAI_UPDATE)
        {
            nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
            CTC_SLIST_LOOP(p_travs_data->new_output_id_head, node)
            {
                po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
                p_bridge_port = ctc_sai_db_get_object_property(p_travs_data->lchip, po->output_id);
                if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
                    continue;
                }

                nh_mcast_group.mem_info.destid = p_bridge_port->gport;
                CTC_SAI_ERROR_RETURN(ctcs_nh_update_mcast(p_travs_data->lchip, nh_id, &nh_mcast_group));

                CTC_SAI_LOG_INFO(SAI_API_L2MC_GROUP, "%s ipmc group member, nh_id: %d, group id: %d, output oid: 0x%llx, l3if type: %d, vlan id: %d, port: %d\n",
                    ((nh_mcast_group.opcode == CTC_NH_PARAM_MCAST_ADD_MEMBER) ? "Add" : "Remove"), nh_id, nh_mcast_group.mc_grp_id, po->output_id,
                    nh_mcast_group.mem_info.l3if_type, nh_mcast_group.mem_info.vid, nh_mcast_group.mem_info.destid);
            }
        }

        if (p_travs_data->opt_type == CTC_SAI_ADD)
        {
            if (!bind_node)
            {
                bind_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_bind_node_t));
                if (!bind_node)
                {
                    return SAI_STATUS_NO_MEMORY;
                }
                bind_node->vlan_ptr = vlan_ptr;
                bind_node->bind_type = (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC) ?
                                                                    CTC_SAI_MCAST_IPMC_BIND_L2MC : CTC_SAI_MCAST_IPMC_BIND_FDB;
                ctc_slist_add_tail(p_entry_data->bind_type_head, &(bind_node->node));
            }
            else
            {
                bind_node->bind_type = (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC) ?
                                                                    CTC_SAI_MCAST_IPMC_BIND_L2MC : CTC_SAI_MCAST_IPMC_BIND_FDB;
            }
        }
        else if (p_travs_data->opt_type == CTC_SAI_DELETE)
        {
            if (p_travs_data->p_entry_property->entry_type == CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC)
            {
                key1->is_pending = 1;
            }
            else
            {
                key2->is_pending = 1;
            }
            ctc_slist_delete_node(p_entry_data->bind_type_head, &(bind_node->node));
        }

        if ((p_travs_data->opt_type == CTC_SAI_DELETE)
            ||((p_travs_data->opt_type == CTC_SAI_ADD)
                && (bind_type == CTC_SAI_MCAST_IPMC_BIND_FDB)
                && (bind_node->bind_type == CTC_SAI_MCAST_IPMC_BIND_L2MC))) 
        {
            CTC_SLIST_LOOP(p_group_data->output_id_head, node)
            {
                po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
                CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_rif_info(po->output_id, (uint8*)&sai_l3if_type, NULL, NULL, NULL));
                
                if ((p_travs_data->opt_type == CTC_SAI_DELETE)
                    && (sai_l3if_type != SAI_ROUTER_INTERFACE_TYPE_VLAN))
                {
                    continue;
                }

                if (sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN) 
                {
                    ctc_sai_router_interface_get_vlan_ptr(po->output_id, &vlan_ptr);

                    /*try bind deleted vlan interface again*/
                    
                    if (p_travs_data->opt_type == CTC_SAI_DELETE) 
                    {
                        if (!vlan_ptr || (vlan_ptr != fid))
                        {
                            continue;
                        }
                    }
                    else  /*try bind all vlan interface except binded vlan*/
                    {
                        if (vlan_ptr == fid)
                        {
                            continue;
                        }

                        CTC_SLIST_LOOP(p_entry_data->bind_type_head, node1)
                        {
                            bind_node = _ctc_container_of(node1, ctc_sai_mcast_entry_bind_node_t, node);
                            if (bind_node->vlan_ptr == vlan_ptr)
                            {
                                ctc_slist_delete_node(p_entry_data->bind_type_head, &(bind_node->node));
                                continue;
                            }
                        }                        
                    }
                }

                CTC_SAI_ERROR_RETURN(_ctc_sai_mcast_update_ipmc_group_member(p_entry_property, po->output_id, 1));

                if (key1)
                {
                    key1->is_pending = 0;
                }
                
                if (key2)
                {
                    key2->is_pending = 0;
                }

                    
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_db_mcast_group_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t *node = NULL, *next_node = NULL;

    p_group_data = (ctc_sai_mcast_group_property_t*)bucket_data->data;
    CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        mem_free(pe);
    }
    mem_free(p_group_data->entry_head);

    CTC_SLIST_LOOP_DEL(p_group_data->output_id_head, node, next_node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        mem_free(po);
    }
    mem_free(p_group_data->output_id_head);

    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_mcast_db_mcast_entry_deinit_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_mcast_entry_property_t* p_mcast_entry = NULL;
    ctc_sai_mcast_entry_bind_node_t *pb = NULL;
    ctc_slistnode_t               *node = NULL, *next_node = NULL;

    p_mcast_entry = (ctc_sai_mcast_entry_property_t*)bucket_data->data;

    CTC_SLIST_LOOP_DEL(p_mcast_entry->bind_type_head, node, next_node)
    {
        pb = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);
        mem_free(pb);
    }
    mem_free(p_mcast_entry->bind_type_head);

    return SAI_STATUS_SUCCESS;
}

#define ________WARMBOOT_FUNCTION________
static sai_status_t
_ctc_sai_mcast_group_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    sai_object_id_t group_oid = *(sai_object_id_t*)key;
    ctc_sai_mcast_group_property_t *p_group_data = (ctc_sai_mcast_group_property_t *)data;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_wb_mcast_group_property_t wb_group_data = {0};
    ctc_wb_data_t wb_data;
    uint16  max_entry_cnt = 0;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_mcast_group_property_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_GROUP_OUTPUT_LIST);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);

        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_group_data.group_oid = group_oid;
        wb_group_data.output_id = po->output_id;
        wb_group_data.index = index++;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_group_data, (wb_data.key_len + wb_data.data_len));
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

    return SAI_STATUS_SUCCESS;

done:
out:
    if (wb_data.buffer)
    {
        CTC_WB_FREE_BUFFER(wb_data.buffer);
    }

    return status;
}

static sai_status_t
_ctc_sai_mcast_group_wb_sync_cb_ip(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    sai_object_id_t group_oid = *(sai_object_id_t*)key;
    ctc_sai_mcast_group_property_t *p_group_data = (ctc_sai_mcast_group_property_t *)data;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_wb_mcast_group_property_t wb_group_data = {0};
    ctc_wb_data_t wb_data;
    uint16  max_entry_cnt = 0;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_mcast_group_property_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_IP_MCAST_GROUP_OUTPUT_LIST);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);

        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_group_data.group_oid = group_oid;
        wb_group_data.output_id = po->output_id;
        wb_group_data.index = index++;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_group_data, (wb_data.key_len + wb_data.data_len));
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

    return SAI_STATUS_SUCCESS;

done:
out:
    if (wb_data.buffer)
    {
        CTC_WB_FREE_BUFFER(wb_data.buffer);
    }

    return status;
}


static sai_status_t
_ctc_sai_mcast_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t group_oid = *(sai_object_id_t*)key;
    ctc_sai_mcast_group_property_t *p_group_data = (ctc_sai_mcast_group_property_t *)data;
    uint16 group_id = 0;

    group_id = _ctc_sai_mcast_get_group_id(group_oid);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, group_id));

    p_group_data->entry_head = ctc_slist_new();
    p_group_data->output_id_head = ctc_slist_new();
    if (!p_group_data->entry_head || !p_group_data->output_id_head)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return status;
}

static sai_status_t
_ctc_sai_mcast_group_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_wb_mcast_group_property_t wb_group_data = {0};
    ctc_sai_mcast_member_output_id_t *output_id_node = NULL;
    ctc_wb_query_t wb_query;
    uint16 entry_cnt = 0;
    uint32 offset = 0;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_mcast_group_property_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_GROUP_OUTPUT_LIST);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_group_data, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_mcast_group_property_t));
        p_group_data = ctc_sai_db_get_object_property(lchip, wb_group_data.group_oid);
        if (!p_group_data)
        {
            continue;
        }

        output_id_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_member_output_id_t));
        if (!output_id_node)
        {
            continue;
        }
        output_id_node->output_id = wb_group_data.output_id;
        ctc_slist_add_tail(p_group_data->output_id_head, &(output_id_node->node));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_mcast_group_wb_reload_cb1_ip(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_wb_mcast_group_property_t wb_group_data = {0};
    ctc_sai_mcast_member_output_id_t *output_id_node = NULL;
    ctc_wb_query_t wb_query;
    uint16 entry_cnt = 0;
    uint32 offset = 0;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_mcast_group_property_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_IP_MCAST_GROUP_OUTPUT_LIST);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_group_data, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_mcast_group_property_t));
        p_group_data = ctc_sai_db_get_object_property(lchip, wb_group_data.group_oid);
        if (!p_group_data)
        {
            continue;
        }

        output_id_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_member_output_id_t));
        if (!output_id_node)
        {
            continue;
        }
        output_id_node->output_id = wb_group_data.output_id;
        ctc_slist_add_tail(p_group_data->output_id_head, &(output_id_node->node));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}


static sai_status_t
_ctc_sai_mcast_entry_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_sai_mcast_entry_property_t *p_entry_data = (ctc_sai_mcast_entry_property_t *)data;
    ctc_sai_mcast_entry_bind_node_t *pb = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_wb_mcast_entry_bind_node_t wb_bind_node = {0};
    ctc_wb_data_t wb_data;
    uint16  max_entry_cnt = 0;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_wb_mcast_entry_bind_node_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_ENTRY_BIND_LIST);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_entry_data->bind_type_head, node)
    {
        pb = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);

        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        wb_bind_node.group_id = p_entry_data->group_id;
        wb_bind_node.index = index++;
        wb_bind_node.vlan_ptr = pb->vlan_ptr;
        wb_bind_node.bind_type = pb->bind_type;
        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_bind_node, (wb_data.key_len + wb_data.data_len));
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
    if (wb_data.buffer)
    {
        CTC_WB_FREE_BUFFER(wb_data.buffer);
    }

    return status;
}

static sai_status_t _ctc_sai_mcast_lookup_entry_property_fn(
        ctc_sai_entry_property_t *p_entry_property,
        ctc_sai_mcast_entry_travs_data_t *p_travs_data)
{
    ctc_sai_mcast_entry_property_t *p_entry_data = (ctc_sai_mcast_entry_property_t *)p_entry_property->data;

    if (p_travs_data->group_id == p_entry_data->group_id)
    {
        p_travs_data->p_entry_data = p_entry_data;
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_entry_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;    
    uint32                        nh_id = 0;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    
    p_entry_data = (ctc_sai_mcast_entry_property_t*)data;
    ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id);

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id));
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_entry_data->group_id));

    p_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "mcast group property not found, group oid: 0x%llx\n", p_entry_data->group_oid);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
    if (!ptr_node)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    ptr_node->entry_property = (ctc_sai_entry_property_t *)key;

    if (CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC == ptr_node->entry_property->entry_type )
    {
        p_entry_data->bind_type_head = ctc_slist_new();
    }
    ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

    return status;

}


static sai_status_t
_ctc_sai_mcast_entry_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_wb_mcast_entry_bind_node_t wb_bind_node = {0};
    ctc_sai_mcast_entry_bind_node_t *bind_node = NULL;
    ctc_sai_mcast_entry_travs_data_t travs_data = {0};
    ctc_wb_query_t wb_query;
    uint16 entry_cnt = 0;
    uint32 offset = 0;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_wb_mcast_entry_bind_node_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_MCAST_ENTRY_BIND_LIST);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
    
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_bind_node, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_wb_mcast_entry_bind_node_t));

        travs_data.group_id = wb_bind_node.group_id;
        
        ret = ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_lookup_entry_property_fn, &travs_data);
        if ((ret != SAI_STATUS_ITEM_ALREADY_EXISTS) || !travs_data.p_entry_data)
        {
            continue;
        }
        
        p_entry_data = (ctc_sai_mcast_entry_property_t *)travs_data.p_entry_data;
        
        bind_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_bind_node_t));
        if (!bind_node)
        {
            continue;
        }
        bind_node->vlan_ptr = wb_bind_node.vlan_ptr;
        bind_node->bind_type = wb_bind_node.bind_type;    
        ctc_slist_add_tail(p_entry_data->bind_type_head, &(bind_node->node));
        
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_mcast_rpf_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_object_id_t group_oid = *(sai_object_id_t*)key;
    uint16 rpf_group_id = 0;

    rpf_group_id = _ctc_sai_mcast_get_group_id(group_oid);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_RPF_GROUP, rpf_group_id));

    return SAI_STATUS_SUCCESS;
}

#define ________SAI_API________
#define ________L2MC_GROUP________
/**
 * @brief Create L2MC group
 *
 * @param[out] l2mc_group_id L2MC group id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_l2mc_group(
        _Out_ sai_object_id_t *l2mc_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    sai_status_t            status = SAI_STATUS_SUCCESS;
    sai_object_id_t       grp_oid = 0;
    uint32                     grp_id = 0;
    uint8                       lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    
    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, &grp_id), status, out);
    grp_oid = _ctc_sai_mcast_create_group_object_id(SAI_OBJECT_TYPE_L2MC_GROUP, lchip, grp_id);

    p_group_data = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_group_property_t));
    if (!p_group_data)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }

    p_group_data->entry_head = ctc_slist_new();
    p_group_data->output_id_head = ctc_slist_new();
    if (!p_group_data->entry_head || !p_group_data->output_id_head)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error2;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, grp_oid, p_group_data), status, error2);
    *l2mc_group_id = grp_oid;

    status = SAI_STATUS_SUCCESS;
    goto out;


error2:
    if (p_group_data)
    {
        if (p_group_data->output_id_head)
        {
            mem_free(p_group_data->output_id_head);
        }

        if (p_group_data->entry_head)
        {
            mem_free(p_group_data->entry_head);
        }
        mem_free(p_group_data);
    }

error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, grp_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to create l2mc group :%d\n", status);
    }
    return status;
}

/**
 * @brief Remove L2MC group
 *
 * @param[in] l2mc_group_id L2MC group id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_l2mc_group(
        _In_ sai_object_id_t l2mc_group_id)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t        *node, *next_node;
    uint16                     grp_id = 0;
    uint8                       lchip = 0;
    sai_status_t            status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    p_group_data = ctc_sai_db_get_object_property(lchip, l2mc_group_id);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "l2mc group property not found, group oid: 0x%llx\n", l2mc_group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    grp_id = _ctc_sai_mcast_get_group_id(l2mc_group_id);
    
    CTC_SAI_LOG_INFO(SAI_API_L2MC_GROUP, "remove sai l2mc group id: %d, oid: 0x%llx\n", grp_id, l2mc_group_id);

    ctc_sai_db_remove_object_property(lchip, l2mc_group_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, grp_id);

    CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        mem_free(pe);
    }
    mem_free(p_group_data->entry_head);

    CTC_SLIST_LOOP_DEL(p_group_data->output_id_head, node, next_node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        mem_free(po);
    }
    mem_free(p_group_data->output_id_head);

    mem_free(p_group_data);

    status = SAI_STATUS_SUCCESS;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to remove l2mc group :%d\n", status);
    }
    return status;
}
        

static  ctc_sai_attr_fn_entry_t l2mc_group_attr_fn_entries[] = {
    { SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT,
      ctc_sai_mcast_get_group_member_count,
      NULL},
    { SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST,
      ctc_sai_mcast_get_group_member_list,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set L2MC Group attribute
 *
 * @param[in] l2mc_group_id L2MC group id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_l2mc_group_attribute(
        _In_ sai_object_id_t l2mc_group_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_id, &lchip));
    key.key.object_id = l2mc_group_id;

    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, NULL,SAI_OBJECT_TYPE_L2MC_GROUP,  l2mc_group_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to set l2mc group attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Get L2MC Group attribute
 *
 * @param[in] l2mc_group_id L2MC group id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_l2mc_group_attribute(
        _In_ sai_object_id_t l2mc_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = l2mc_group_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_L2MC_GROUP, loop, l2mc_group_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to get l2mc group attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Create L2MC group member
 *
 * @param[out] l2mc_group_member_id L2MC group member id
 * @param[in] switch_id Switch ID
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_l2mc_group_member(
        _Out_ sai_object_id_t *l2mc_group_member_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_id1 = NULL, *attr_id2 = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *output_id_node = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_sai_bridge_port_t* p_bridge_port_tmp = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    sai_object_id_t          member_oid = 0;
    sai_status_t               status = SAI_STATUS_SUCCESS;
    uint32                        attr_idx1;
    uint32                        attr_idx2;
    uint32                        attr_idx3;
    uint32                        nh_id;
    uint16                        grp_id = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID, &attr_grp, &attr_idx1);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Missing mandatory SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }
        
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID, &attr_id1, &attr_idx2);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Missing mandatory SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP, &attr_id2, &attr_idx3);
    if (status == SAI_STATUS_SUCCESS)
    {
        status = SAI_STATUS_NOT_IMPLEMENTED;
        goto out;
    }

    p_bridge_port = ctc_sai_db_get_object_property(lchip, attr_id1->oid);
    if (NULL == p_bridge_port || SAI_BRIDGE_PORT_TYPE_PORT  != p_bridge_port->port_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", attr_id1->oid);
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    p_group_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc group property db not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    /* assert l2mc group member exist */
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port_tmp = ctc_sai_db_get_object_property(lchip, po->output_id);
        if ( p_bridge_port_tmp->gport == p_bridge_port->gport )
        {
            status = SAI_STATUS_ITEM_ALREADY_EXISTS;
            goto out;
        }

    }

    output_id_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_member_output_id_t));
    if (!output_id_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto out;
    }

    output_id_node->output_id = attr_id1->oid;
    ctc_slist_add_tail(p_group_data->output_id_head, &(output_id_node->node));

    grp_id = _ctc_sai_mcast_get_group_id(attr_grp->oid);
    member_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, lchip, 0, grp_id, p_bridge_port->gport);

    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
    nh_mcast_group.mem_info.destid = p_bridge_port->gport;

    travs_data.lchip = lchip;
    travs_data.is_member = 1;
    travs_data.opt_type = CTC_SAI_ADD;
    travs_data.member.member_id = member_oid;
    
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        p_entry_data = (ctc_sai_mcast_entry_property_t *)(pe->entry_property->data);
        if (!p_entry_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property data is NULL\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error0;
        }

        nh_mcast_group.mc_grp_id = p_entry_data->group_id;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_get_mcast_nh(lchip, nh_mcast_group.mc_grp_id, &nh_id), status, error0);
        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error0);

        travs_data.p_entry_property = pe->entry_property;
        
        CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error0);
    }

    *l2mc_group_member_id = member_oid;
    
    CTC_SAI_LOG_INFO(SAI_API_L2MC_GROUP, "create l2mc group member, group id: %d, group oid: 0x%llx, output oid: 0x%llx, port: %d, oid: 0x%llx\n",
            grp_id, attr_grp->oid, attr_id1->oid, p_bridge_port->gport, *l2mc_group_member_id);

    status = SAI_STATUS_SUCCESS;
    goto out;

error0:
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        p_entry_data = (ctc_sai_mcast_entry_property_t *)(pe->entry_property->data);
        if (!p_entry_data)
        {
            continue;
        }

        nh_mcast_group.mc_grp_id = p_entry_data->group_id;

        ctcs_nh_get_mcast_nh(lchip, nh_mcast_group.mc_grp_id, &nh_id);
        ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
    }
    
    ctc_slist_delete_node(p_group_data->output_id_head, &(output_id_node->node));
    mem_free(output_id_node);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to create l2mc group member :%d\n", status);
    }
    return status;
}    


/**
 * @brief Remove L2MC group member
 *
 * @param[in] l2mc_group_member_id L2MC group member id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_l2mc_group_member(
        _In_ sai_object_id_t l2mc_group_member_id)
{
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    sai_status_t               status = SAI_STATUS_SUCCESS;
    ctc_object_id_t          ctc_oid;
    sai_object_id_t          grp_oid = 0;
    uint32                        nh_id = 0;
    uint8                          lchip = 0;
    uint8                     found = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, l2mc_group_member_id, &ctc_oid);
    grp_oid = _ctc_sai_mcast_create_group_object_id(SAI_OBJECT_TYPE_L2MC_GROUP, lchip, ctc_oid.value2);

    p_group_data = ctc_sai_db_get_object_property(lchip, grp_oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc group property db not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if (NULL == p_bridge_port || SAI_BRIDGE_PORT_TYPE_PORT  != p_bridge_port->port_type)
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }

        if (p_bridge_port->gport == ctc_oid.value)
        {
            ctc_slist_delete_node(p_group_data->output_id_head, node);
            mem_free(po);
            found = 1;
            break;
        }
    }

    if (!found)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    

    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
    nh_mcast_group.mem_info.destid = ctc_oid.value;

    travs_data.lchip = lchip;
    travs_data.is_member = 1;
    travs_data.opt_type = CTC_SAI_DELETE;
    travs_data.member.member_id = l2mc_group_member_id;
    
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        p_entry_data = (ctc_sai_mcast_entry_property_t *)(pe->entry_property->data);
        if (!p_entry_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property data is NULL\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error0;
        }

        nh_mcast_group.mc_grp_id = p_entry_data->group_id;

        CTC_SAI_ERROR_GOTO(ctcs_nh_get_mcast_nh(lchip, nh_mcast_group.mc_grp_id, &nh_id), status, error0);
        CTC_SAI_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error0);

        travs_data.p_entry_property = pe->entry_property;
        CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error0);
    }

    CTC_SAI_LOG_INFO(SAI_API_L2MC_GROUP, "remove l2mc group member, group id: %d, port: %d, oid: 0x%llx\n",
            ctc_oid.value2, nh_mcast_group.mem_info.destid, l2mc_group_member_id);

    status = SAI_STATUS_SUCCESS;
    goto out;

error0:
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        p_entry_data = (ctc_sai_mcast_entry_property_t *)(pe->entry_property->data);
        if (!p_entry_data)
        {
            continue;
        }

        nh_mcast_group.mc_grp_id = p_entry_data->group_id;

        ctcs_nh_get_mcast_nh(lchip, nh_mcast_group.mc_grp_id, &nh_id);
        ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to remove l2mc group member :%d\n", status);
    }
    return status;
}


static  ctc_sai_attr_fn_entry_t l2mc_member_attr_fn_entries[] = {
    { SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID,
      ctc_sai_mcast_get_member_group_id,
      NULL},
    { SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID,
      ctc_sai_mcast_get_member_output_id,
      NULL},
    { SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_ENDPOINT_IP,
      NULL,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL}
};

/**
 * @brief Set L2MC Group attribute
 *
 * @param[in] l2mc_group_member_id L2MC group member id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_l2mc_group_member_attribute(
        _In_ sai_object_id_t l2mc_group_member_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_member_id, &lchip)); 
    CTC_SAI_DB_LOCK(lchip);
    key.key.object_id = l2mc_group_member_id;
    status = ctc_sai_set_attribute(&key, NULL,SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER,  l2mc_member_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);

    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to set l2mc group member attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Get L2MC Group attribute
 *
 * @param[in] l2mc_group_member_id L2MC group member id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_l2mc_group_member_attribute(
        _In_ sai_object_id_t l2mc_group_member_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_group_member_id, &lchip)); 
    CTC_SAI_DB_LOCK(lchip);

    key.key.object_id = l2mc_group_member_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, loop, l2mc_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Failed to get l2mc group member attr:%d\n", status);
    }

    return status;
}

const sai_l2mc_group_api_t ctc_sai_l2mc_group_api = {
    ctc_sai_mcast_create_l2mc_group,
    ctc_sai_mcast_remove_l2mc_group,
    ctc_sai_mcast_set_l2mc_group_attribute,
    ctc_sai_mcast_get_l2mc_group_attribute,
    ctc_sai_mcast_create_l2mc_group_member,
    ctc_sai_mcast_remove_l2mc_group_member,
    ctc_sai_mcast_set_l2mc_group_member_attribute,
    ctc_sai_mcast_get_l2mc_group_member_attribute
};

#define ________L2MC_ENTRY________
/**
 * @brief Create L2MC entry
 *
 * @param[in] l2mc_entry L2MC entry
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_l2mc_entry(
        _In_ const sai_l2mc_entry_t *l2mc_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_act = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_bridge_port_t *p_bridge_port = NULL;
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    sai_status_t    status = SAI_STATUS_SUCCESS;
    sai_packet_action_t   action, update_action = SAI_PACKET_ACTION_TRANSIT;
    uint32                        attr_idx;
    uint32                        nh_id = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC);

    sal_memset(&action, 0, sizeof(sai_packet_action_t));

    if (!l2mc_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"NULL l2mc entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    
    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    if (p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property db is exist\n");
        status = SAI_STATUS_ITEM_ALREADY_EXISTS;
        goto out;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, &attr_act, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC, "Missing mandatory SAI_L2MC_ENTRY_ATTR_PACKET_ACTION attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }

    action = attr_list[attr_idx].value.s32;
    CTC_SAI_ERROR_GOTO(ctc_sai_packet_action_merge(action, &update_action), status, out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_mapping_ctc_action(&grp_param.flag, update_action), status, out);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, &attr_grp, &attr_idx);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_group_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
        if (!p_group_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"l2mc group db is not found\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto out;
        }

        CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_check_l2mc_member_list(l2mc_entry->bv_id, p_group_data->output_id_head), status, out);
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id), status, out);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, (uint32 *)&grp_param.group_id), status, error0);

    nh_mcast_group.mc_grp_id = grp_param.group_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mcast(lchip, nh_id, &nh_mcast_group), status, error1);

    _ctc_sai_mcast_l2mc_to_param(l2mc_entry, &grp_param);

    if (CTC_IP_VER_4 == grp_param.ip_version)
    {
        CTC_SAI_LOG_INFO(SAI_API_L2MC, "source ip is 0x%x, dest group is 0x%x\n",
                         grp_param.address.ipv4.src_addr,
                         grp_param.address.ipv4.group_addr);
    }
    else
    {
        CTC_SAI_LOG_INFO(SAI_API_L2MC, "source ip is %x:%x:%x:%x, dest group is %x:%x:%x:%x\n",
                         grp_param.address.ipv6.src_addr[0],
                         grp_param.address.ipv6.src_addr[1],
                         grp_param.address.ipv6.src_addr[2],
                         grp_param.address.ipv6.src_addr[3],
                         grp_param.address.ipv6.group_addr[0],
                         grp_param.address.ipv6.group_addr[1],
                         grp_param.address.ipv6.group_addr[2],
                         grp_param.address.ipv6.group_addr[3]);
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_ipmc_add_group(lchip, &grp_param), status, error2);

    CTC_SAI_LOG_INFO(SAI_API_L2MC, "create l2mc entry, ctc group id: %d, oid: 0x%llx, nh_id: %d, action: %d\n",
                grp_param.group_id, (attr_grp ? attr_grp->oid : 0), nh_id, update_action);

    p_entry_data = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_property_t));
    if (!p_entry_data)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    
    sal_memset(p_entry_data, 0, sizeof(ctc_sai_mcast_entry_property_t));

    p_entry_data->group_oid = attr_grp ? attr_grp->oid : 0;
    p_entry_data->group_id = grp_param.group_id;
    p_entry_data->action = update_action;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry, (void*)p_entry_data), status, error4);
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);

    if (p_group_data)
    {
        nh_mcast_group.mc_grp_id = p_entry_data->group_id;
        nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
        nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
            if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
            {
                CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
                status = SAI_STATUS_INVALID_OBJECT_ID;
                goto error5;
            }

            nh_mcast_group.mem_info.destid = p_bridge_port->gport;

            CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error5);
        }

        ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
        if (!ptr_node)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto error5;
        }

        ptr_node->entry_property = p_entry_property;
        ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

        travs_data.lchip = lchip;
        travs_data.is_member = 0;
        travs_data.opt_type = CTC_SAI_ADD;
        travs_data.member.output_id_head = p_group_data->output_id_head;
        travs_data.p_entry_property = p_entry_property;
        CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error6);
    }

    status = SAI_STATUS_SUCCESS;
    goto out;

error6:
    ctc_slist_delete_node(p_group_data->entry_head, &(ptr_node->node));
    mem_free(ptr_node);

error5:
    if (p_group_data)
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
            if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
            {
                continue;
            }

            nh_mcast_group.mem_info.destid = p_bridge_port->gport;

            ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
        }
    }

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);

error4:
    mem_free(p_entry_data);

error3:
    ctcs_ipmc_remove_group(lchip, &grp_param);

error2:
    ctcs_nh_remove_mcast(lchip, nh_id);

error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, grp_param.group_id);

error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC, "Failed to create l2mc entry :%d\n", status);
    }
    return status;
}


/**
 * @brief Remove L2MC entry
 *
 * @param[in] l2mc_entry L2MC entry
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_l2mc_entry(
        _In_ const sai_l2mc_entry_t *l2mc_entry)
{
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node, *next_node;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    uint32                        nh_id = 0;
    uint8                          lchip = 0;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC);

    if (!l2mc_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"NULL l2mc entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    if (!p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property db not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_entry_data = (ctc_sai_mcast_entry_property_t*)(p_entry_property->data);
    if (p_entry_data->group_oid)
    {
        p_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (!p_group_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc group property db not found\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto out;
        }
    }

    _ctc_sai_mcast_l2mc_to_param(l2mc_entry, &grp_param);
    ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id);
    ctcs_ipmc_remove_group(lchip, &grp_param);
    ctcs_nh_remove_mcast(lchip, nh_id);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_entry_data->group_id);

    if (p_group_data)
    {
        CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
        {
            pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
            if (pe->entry_property == p_entry_property)
            {
                ctc_slist_delete_node(p_group_data->entry_head, node);
                mem_free(pe);
                break;
            }
        }

        travs_data.lchip = lchip;
        travs_data.is_member = 0;
        travs_data.opt_type = CTC_SAI_DELETE;
        travs_data.member.output_id_head = p_group_data->output_id_head;
        travs_data.p_entry_property = p_entry_property;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data);
    }

    CTC_SAI_LOG_INFO(SAI_API_L2MC, "remove l2mc entry, ctc group id: %d, oid: 0x%llx, nh_id: %d, action: %d\n",
                p_entry_data->group_id, p_entry_data->group_oid, nh_id, p_entry_data->action);

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    mem_free(p_entry_data);

    status = SAI_STATUS_SUCCESS;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC, "Failed to remove l2mc entry :%d\n", status);
    }
    return status;
}

static sai_status_t ctc_sai_mcast_get_l2mc_entry_info(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_l2mc_entry_t *l2mc_entry = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    uint8                          lchip = 0;

    l2mc_entry = &key->key.l2mc_entry;
    ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
            attr->value.s32 = p_entry_data->action;
            break;
        case SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
            attr->value.oid = p_entry_data->group_oid;
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_l2mc_packet_action(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_l2mc_entry_t *l2mc_entry = NULL;
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    uint8 lchip = 0;
    sai_packet_action_t update_action;

    l2mc_entry = &key->key.l2mc_entry;
    ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    grp_param.group_id = p_entry_data->group_id;

    update_action = p_entry_data->action;
    CTC_SAI_ERROR_RETURN(ctc_sai_packet_action_merge(attr->value.s32, &update_action));

    _ctc_sai_mcast_mapping_ctc_action(&grp_param.flag, update_action);

    _ctc_sai_mcast_l2mc_to_param(l2mc_entry, &grp_param);

    grp_param.group_id = p_entry_data->group_id;
    
    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_add_group(lchip, &grp_param));
    p_entry_data->action = update_action;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_l2mc_group_id(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_l2mc_entry_t *l2mc_entry = NULL;
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL, *p_old_group_data = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t        *node, *next_node;
    ctc_sai_bridge_port_t *p_bridge_port = NULL;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint32                        nh_id;
    uint8                          lchip = 0;

    l2mc_entry = &key->key.l2mc_entry;
    ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip);

    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)l2mc_entry);
    if (NULL == p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_entry_data = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id));

    p_group_data = ctc_sai_db_get_object_property(lchip, attr->value.oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC,"l2mc group db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    grp_param.group_id = p_entry_data->group_id;
    _ctc_sai_mcast_l2mc_to_param(l2mc_entry, &grp_param);
    CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_KEEP_EMPTY_ENTRY);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_remove_group(lchip, &grp_param));

     if (p_entry_data->group_oid)
    {
        p_old_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (p_old_group_data)
        {
            CTC_SLIST_LOOP_DEL(p_old_group_data->entry_head, node, next_node)
            {
                pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
                if (pe->entry_property == p_entry_property)
                {
                    ctc_slist_delete_node(p_old_group_data->entry_head, node);
                    mem_free(pe);
                }
            }
        }
    }

    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
        {
            CTC_SAI_LOG_ERROR(SAI_API_L2MC_GROUP, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto error0;
        }

        nh_mcast_group.mem_info.destid = p_bridge_port->gport;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error0);
    }

    ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
    if (!ptr_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    ptr_node->entry_property = p_entry_property;
    ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

    p_entry_data->group_oid = attr->value.oid;

    travs_data.lchip = lchip;
    travs_data.is_member = 0;
    travs_data.opt_type = CTC_SAI_UPDATE;
    travs_data.new_output_id_head = p_group_data->output_id_head;
    travs_data.member.output_id_head = p_old_group_data ? p_old_group_data->output_id_head : NULL;
    travs_data.p_entry_property = p_entry_property;
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error1);

    return SAI_STATUS_SUCCESS;

error1:
    ctc_slist_delete_node(p_group_data->entry_head, &(ptr_node->node));
    mem_free(ptr_node);

error0:
    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
        {
            continue;
        }

        nh_mcast_group.mem_info.destid = p_bridge_port->gport;

        ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
    }

    return status;
}

static  ctc_sai_attr_fn_entry_t l2mc_attr_fn_entries[] = {
    { SAI_L2MC_ENTRY_ATTR_PACKET_ACTION,
      ctc_sai_mcast_get_l2mc_entry_info,
      ctc_sai_mcast_set_l2mc_packet_action},
      { SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID,
      ctc_sai_mcast_get_l2mc_entry_info,
      ctc_sai_mcast_set_l2mc_group_id},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set L2MC entry attribute value
 *
 * @param[in] l2mc_entry L2MC entry
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_l2mc_entry_attribute(
        _In_ const sai_l2mc_entry_t *l2mc_entry,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memcpy(&key.key.l2mc_entry, l2mc_entry, sizeof(sai_l2mc_entry_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_L2MC_ENTRY,  l2mc_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC, "Failed to set l2mc entry attr:%d\n", status);
    }

    return status;
}
/**
 * @brief Get L2MC entry attribute value
 *
 * @param[in] l2mc_entry L2MC entry
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_l2mc_entry_attribute(
        _In_ const sai_l2mc_entry_t *l2mc_entry,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;
    uint8           lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_L2MC);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(l2mc_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memcpy(&key.key.l2mc_entry, l2mc_entry, sizeof(sai_l2mc_entry_t));
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_L2MC_ENTRY, loop, l2mc_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_L2MC, "Failed to get l2mc entry attr:%d\n", status);
    }

    return status;
}

const sai_l2mc_api_t ctc_sai_l2mc_api = {
    ctc_sai_mcast_create_l2mc_entry,
    ctc_sai_mcast_remove_l2mc_entry,
    ctc_sai_mcast_set_l2mc_entry_attribute,
    ctc_sai_mcast_get_l2mc_entry_attribute
};

#define ________MCAST_FDB_ENTRY________
sai_status_t _ctc_sai_mcast_fdb_mapping_ctc_action(uint32*flag, sai_packet_action_t action)
{
    switch(action)
    {
    case SAI_PACKET_ACTION_FORWARD:
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_DROP:
        CTC_SET_FLAG( *flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_COPY:
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_COPY_CANCEL:
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_TRAP :
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_LOG:
        CTC_UNSET_FLAG( *flag, CTC_L2_FLAG_DISCARD);
        CTC_SET_FLAG( *flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;
    case SAI_PACKET_ACTION_DENY:
        CTC_UNSET_FLAG(*flag , CTC_L2_FLAG_COPY_TO_CPU);
        CTC_SET_FLAG(*flag, CTC_L2_FLAG_DISCARD);
        break;
    case SAI_PACKET_ACTION_TRANSIT:
        CTC_UNSET_FLAG(*flag,  CTC_L2_FLAG_DISCARD);
        CTC_UNSET_FLAG(*flag, CTC_L2_FLAG_COPY_TO_CPU);
        break;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "invalid action\n");
        return SAI_STATUS_INVALID_ATTR_VALUE_0 + action;
    }

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Create Multicast FDB entry
 *
 * @param[in] mcast_fdb_entry FDB entry
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_mcast_fdb_entry(
        _In_ const sai_mcast_fdb_entry_t *mcast_fdb_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_act = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_l2_mcast_addr_t grp_param;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_bridge_port_t *p_bridge_port = NULL;
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    sai_status_t    status = SAI_STATUS_SUCCESS;
    sai_packet_action_t   action, update_action = SAI_PACKET_ACTION_TRANSIT;
    uint32                        attr_idx;
    uint32                        nh_id = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MCAST_FDB);

    if (!mcast_fdb_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"NULL mcast fdb entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    
    sal_memset(&grp_param, 0, sizeof(ctc_l2_mcast_addr_t));
    sal_memset(&action, 0, sizeof(sai_packet_action_t));

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    if (p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb property db is already exist\n");
        status = SAI_STATUS_ITEM_ALREADY_EXISTS;
        goto out;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, &attr_act, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }
        
    action = attr_list[attr_idx].value.s32;
    CTC_SAI_ERROR_GOTO(ctc_sai_packet_action_merge(action, &update_action), status, out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_fdb_mapping_ctc_action(&grp_param.flag, update_action),status,out);
    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, &attr_grp, &attr_idx);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_BRIDGE, "Missing mandatory SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID attr\n");
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto out;
    }
    
    p_group_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb group db is not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_check_l2mc_member_list(mcast_fdb_entry->bv_id, p_group_data->output_id_head),status,out);

    CTC_SAI_ERROR_GOTO(ctc_sai_bridge_get_fid(mcast_fdb_entry->bv_id, &grp_param.fid),status,out);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id),status,out);
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, (uint32 *)&grp_param.l2mc_grp_id), status, error0);

    nh_mcast_group.mc_grp_id = grp_param.l2mc_grp_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mcast(lchip, nh_id, &nh_mcast_group), status, error1);

    grp_param.share_grp_en = 1;
    sal_memcpy(grp_param.mac, mcast_fdb_entry->mac_address, sizeof(sai_mac_t));
    
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_MCAST_FDB_ENTRY_ATTR_META_DATA, &attr_act, &attr_idx);
    if (status == SAI_STATUS_SUCCESS)
    {
        grp_param.cid= CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[attr_idx].value.u32);
    }
    
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2mcast_add_addr(lchip, &grp_param), status, error2);

    CTC_SAI_LOG_INFO(SAI_API_MCAST_FDB, "create mcast fdb entry, ctc group id: %d, oid: 0x%llx, action: %d, mac: %.2x%.2x.%.2x%.2x.%.2x%.2x, fid: %d\n",
                grp_param.l2mc_grp_id, attr_grp->oid, action, grp_param.mac[0], grp_param.mac[1], grp_param.mac[2], grp_param.mac[3], grp_param.mac[4],
                grp_param.mac[5], grp_param.fid);

    p_entry_data = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_property_t));
    if (!p_entry_data)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    
    sal_memset(p_entry_data, 0, sizeof(ctc_sai_mcast_entry_property_t));
    p_entry_data->group_oid = attr_grp->oid;
    p_entry_data->group_id = grp_param.l2mc_grp_id;
    p_entry_data->action = update_action;
    p_entry_data->cid = grp_param.cid;
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry, (void*)p_entry_data), status, error4);

    nh_mcast_group.mc_grp_id = p_entry_data->group_id;
    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
    
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if ( !p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
        {
            CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto error5;
        }

        nh_mcast_group.mem_info.destid = p_bridge_port->gport;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error5);
    }

    ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
    if (!ptr_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error5;
    }
    
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    ptr_node->entry_property = p_entry_property;
    ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

    travs_data.lchip = lchip;
    travs_data.is_member = 0;
    travs_data.opt_type = CTC_SAI_ADD;
    travs_data.member.output_id_head = p_group_data->output_id_head;
    travs_data.p_entry_property = p_entry_property;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error6);

    status = SAI_STATUS_SUCCESS;
    goto out;

error6:
    ctc_slist_delete_node(p_group_data->entry_head, &(ptr_node->node));
    mem_free(ptr_node);

error5:
    if (p_group_data)
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
            if ( !p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
            {
                continue;
            }

            nh_mcast_group.mem_info.destid = p_bridge_port->gport;

            ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
        }
    }

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);

error4:
    mem_free(p_entry_data);

error3:
    ctcs_l2mcast_remove_addr(lchip, &grp_param);

error2:
    ctcs_nh_remove_mcast(lchip, nh_id);

error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, grp_param.l2mc_grp_id);

error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Failed to create mcast fdb entry :%d\n", status);
    }
    return status;
}


/**
 * @brief Remove Multicast FDB entry
 *
 * @param[in] mcast_fdb_entry FDB entry
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_mcast_fdb_entry(
        _In_ const sai_mcast_fdb_entry_t *mcast_fdb_entry)
{
    ctc_l2_mcast_addr_t grp_param;
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node, *next_node;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};
    uint32                        nh_id = 0;
    uint8                          lchip = 0;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_MCAST_FDB);
    sal_memset(&grp_param, 0, sizeof(ctc_l2_mcast_addr_t));

    if (!mcast_fdb_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"NULL l2mc entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    if (NULL == p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb property db not found\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    p_entry_data = (ctc_sai_mcast_entry_property_t*)(p_entry_property->data);
    if (p_entry_data->group_oid)
    {
        p_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (!p_group_data)
        {
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto out;
        }
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_bridge_get_fid(mcast_fdb_entry->bv_id, &grp_param.fid), status, out);

    grp_param.share_grp_en = 1;
    grp_param.l2mc_grp_id = p_entry_data->group_id;
    sal_memcpy(grp_param.mac, mcast_fdb_entry->mac_address, sizeof(sai_mac_t));

    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_l2mcast_remove_addr(lchip, &grp_param), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_remove_mcast(lchip, nh_id), status, out);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_entry_data->group_id);

    if (p_group_data)
    {
        CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
        {
            pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
            if (pe->entry_property == p_entry_property)
            {
                ctc_slist_delete_node(p_group_data->entry_head, node);
                mem_free(pe);
                break;
            }
        }

        travs_data.lchip = lchip;
        travs_data.is_member = 0;
        travs_data.opt_type = CTC_SAI_DELETE;
        travs_data.member.output_id_head = p_group_data->output_id_head;
        travs_data.p_entry_property = p_entry_property;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data);
    }

    CTC_SAI_LOG_INFO(SAI_API_MCAST_FDB, "remove mcast fdb entry, ctc group id: %d, oid: 0x%llx, nh_id: %d, action: %d\n",
                p_entry_data->group_id, p_entry_data->group_oid, nh_id, p_entry_data->action);

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    mem_free(p_entry_data);

    status = SAI_STATUS_SUCCESS;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Failed to remove mcast fdb entry :%d\n", status);
    }
    return status;
}

static sai_status_t ctc_sai_mcast_get_mcast_fdb_entry_info(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_mcast_fdb_entry_t *mcast_fdb_entry = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    uint8                          lchip = 0;

    mcast_fdb_entry = &key->key.mcast_fdb_entry;
    ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
            attr->value.s32 = p_entry_data->action;
            break;
        case SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
            attr->value.oid = p_entry_data->group_oid;
            break;
        case SAI_MCAST_FDB_ENTRY_ATTR_META_DATA:
            attr->value.u32 = CTC_SAI_META_DATA_CTC_TO_SAI(p_entry_data->cid);
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_mcast_fdb_action_and_metadata(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_mcast_fdb_entry_t *mcast_fdb_entry = NULL;
    ctc_l2_mcast_addr_t grp_param;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    uint8 lchip = 0;
    sai_packet_action_t update_action;

    sal_memset(&grp_param, 0, sizeof(ctc_l2_mcast_addr_t));

    mcast_fdb_entry = &key->key.mcast_fdb_entry;
    ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(mcast_fdb_entry->bv_id, &grp_param.fid));

    grp_param.share_grp_en = 1;
    grp_param.l2mc_grp_id = p_entry_data->group_id;
    sal_memcpy(grp_param.mac, mcast_fdb_entry->mac_address, sizeof(sai_mac_t));
    switch (attr->id)
    {
        case SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
            update_action = p_entry_data->action;
            CTC_SAI_ERROR_RETURN(ctc_sai_packet_action_merge(attr->value.s32, &update_action));

            _ctc_sai_mcast_fdb_mapping_ctc_action(&grp_param.flag, update_action);
            break;
        case SAI_MCAST_FDB_ENTRY_ATTR_META_DATA:
            grp_param.cid = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            break;
        default:
            break;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2mcast_add_addr(lchip, &grp_param));
    
    if (SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION == attr->id)
    {
        p_entry_data->action = update_action;
    }
    else if(SAI_MCAST_FDB_ENTRY_ATTR_META_DATA == attr->id)
    {
        p_entry_data->cid = grp_param.cid;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_mcast_fdb_group_id(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_mcast_fdb_entry_t *mcast_fdb_entry = NULL;
    ctc_l2_mcast_addr_t grp_param;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL, *p_old_group_data = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t        *node, *next_node;
    ctc_sai_bridge_port_t *p_bridge_port = NULL;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint32                        nh_id;
    uint8                          lchip = 0;
    ctc_sai_mcast_vlan_member_priv_t travs_data = {0};

    sal_memset(&grp_param, 0, sizeof(ctc_l2_mcast_addr_t));

    mcast_fdb_entry = &key->key.mcast_fdb_entry;
    ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip);

    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)mcast_fdb_entry);
    if (NULL == p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_entry_data = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id));

    p_group_data = ctc_sai_db_get_object_property(lchip, attr->value.oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"mcast fdb group db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_bridge_get_fid(mcast_fdb_entry->bv_id, &grp_param.fid));

    grp_param.l2mc_grp_id = p_entry_data->group_id;
    CTC_SET_FLAG(grp_param.flag, CTC_L2_FLAG_KEEP_EMPTY_ENTRY);
    sal_memcpy(grp_param.mac, mcast_fdb_entry->mac_address, sizeof(sai_mac_t));

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2mcast_remove_addr(lchip, &grp_param));

    if (p_entry_data->group_oid)
    {
        p_old_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (p_old_group_data)
        {
            CTC_SLIST_LOOP_DEL(p_old_group_data->entry_head, node, next_node)
            {
                pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
                if (pe->entry_property == p_entry_property)
                {
                    ctc_slist_delete_node(p_old_group_data->entry_head, node);
                    mem_free(pe);
                }
            }
        }
    }

    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_ADD_MEMBER;
    nh_mcast_group.mem_info.member_type = CTC_NH_PARAM_MEM_BRGMC_LOCAL;
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
        {
            CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Bridge port info wrong, output oid: 0x%llx\n", po->output_id);
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto error0;
        }

        nh_mcast_group.mem_info.destid = p_bridge_port->gport;

        CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group), status, error0);
    }

    ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
    if (!ptr_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    ptr_node->entry_property = p_entry_property;
    ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

    p_entry_data->group_oid = attr->value.oid;

    travs_data.lchip = lchip;
    travs_data.is_member = 0;
    travs_data.opt_type = CTC_SAI_UPDATE;
    travs_data.new_output_id_head = p_group_data->output_id_head;
    travs_data.member.output_id_head = p_old_group_data->output_id_head ;
    travs_data.p_entry_property = p_entry_property;
    
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_sync_output_id, &travs_data), status, error0);
    

    return SAI_STATUS_SUCCESS;

error0:
    nh_mcast_group.opcode = CTC_NH_PARAM_MCAST_DEL_MEMBER;
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if (!p_bridge_port || (SAI_BRIDGE_PORT_TYPE_PORT != p_bridge_port->port_type))
        {
            continue;
        }

        nh_mcast_group.mem_info.destid = p_bridge_port->gport;

        ctcs_nh_update_mcast(lchip, nh_id, &nh_mcast_group);
    }

    return status;
}

static  ctc_sai_attr_fn_entry_t mcast_fdb_attr_fn_entries[] = {
      { SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID,
      ctc_sai_mcast_get_mcast_fdb_entry_info,
      ctc_sai_mcast_set_mcast_fdb_group_id},
      { SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION,
      ctc_sai_mcast_get_mcast_fdb_entry_info,
      ctc_sai_mcast_set_mcast_fdb_action_and_metadata},
      { SAI_MCAST_FDB_ENTRY_ATTR_META_DATA,
      ctc_sai_mcast_get_mcast_fdb_entry_info,
      ctc_sai_mcast_set_mcast_fdb_action_and_metadata},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }

};

/**
 * @brief Set multicast FDB entry attribute value
 *
 * @param[in] mcast_fdb_entry FDB entry
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_mcast_fdb_entry_attribute(
        _In_ const sai_mcast_fdb_entry_t *mcast_fdb_entry,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8           lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MCAST_FDB);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memcpy(&key.key.mcast_fdb_entry, mcast_fdb_entry, sizeof(sai_mcast_fdb_entry_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_MCAST_FDB_ENTRY,  mcast_fdb_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Failed to set mcast fdb entry attr:%d\n", status);
    }

    return status;
}
/**
 * @brief Get FDB entry attribute value
 *
 * @param[in] mcast_fdb_entry FDB entry
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_mcast_fdb_entry_attribute(
        _In_ const sai_mcast_fdb_entry_t *mcast_fdb_entry,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;
    uint8              lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_MCAST_FDB);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(mcast_fdb_entry->switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memcpy(&key.key.mcast_fdb_entry, mcast_fdb_entry, sizeof(sai_mcast_fdb_entry_t));
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_MCAST_FDB_ENTRY, loop, mcast_fdb_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB, "Failed to get mcast fdb entry attr:%d\n", status);
    }

    return status;
}

const sai_mcast_fdb_api_t ctc_sai_mcast_fdb_api = {
    ctc_sai_mcast_create_mcast_fdb_entry,
    ctc_sai_mcast_remove_mcast_fdb_entry,
    ctc_sai_mcast_set_mcast_fdb_entry_attribute,
    ctc_sai_mcast_get_mcast_fdb_entry_attribute
};

#define ________IPMC_GROUP________
/**
 * @brief Create IPMC group
 *
 * @param[out] ipmc_group_id IPMC group id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_ipmc_group(
        _Out_ sai_object_id_t *ipmc_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    sai_object_id_t       grp_oid = 0;
    uint32                     grp_id = 0;
    uint8                       lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, &grp_id), status, error0);
    grp_oid = _ctc_sai_mcast_create_group_object_id(SAI_OBJECT_TYPE_IPMC_GROUP, lchip, grp_id);

    if (ctc_sai_db_get_object_property(lchip, grp_oid))
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "ipmc group property exist, group oid: 0x%llx\n", grp_oid);
        status = SAI_STATUS_ITEM_ALREADY_EXISTS;
        goto error0;
    }

    p_group_data = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_group_property_t));
    if (!p_group_data)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    p_group_data->entry_head = ctc_slist_new();
    p_group_data->output_id_head = ctc_slist_new();
    if (!p_group_data->entry_head || !p_group_data->output_id_head)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error1;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, grp_oid, p_group_data), status, error1);
    *ipmc_group_id = grp_oid;

    CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "create ipmc sai group id: %d, oid: 0x%llx\n", grp_id, *ipmc_group_id);

    return SAI_STATUS_SUCCESS;

error1:
    if (p_group_data)
    {
        if (p_group_data->output_id_head)
        {
            mem_free(p_group_data->output_id_head);
        }

        if (p_group_data->entry_head)
        {
            mem_free(p_group_data->entry_head);
        }
        mem_free(p_group_data);
    }
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, grp_id);

error0:
    
    return status;
}

/**
 * @brief Remove IPMC group
 *
 * @param[in] ipmc_group_id IPMC group id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_ipmc_group(
        _In_ sai_object_id_t ipmc_group_id)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t        *node, *next_node;
    uint16                     grp_id = 0;
    uint8                       lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ipmc_group_id, &lchip));

    p_group_data = ctc_sai_db_get_object_property(lchip, ipmc_group_id);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "ipmc group property not found, group oid: 0x%llx\n", ipmc_group_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    grp_id = _ctc_sai_mcast_get_group_id(ipmc_group_id);
    CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "remove ipmc sai group id: %d, oid: 0x%llx\n", grp_id, ipmc_group_id);

    ctc_sai_db_remove_object_property(lchip, ipmc_group_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SAI_MCAST_GROUP, grp_id);

    CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        mem_free(pe);
    }
    mem_free(p_group_data->entry_head);

    CTC_SLIST_LOOP_DEL(p_group_data->output_id_head, node, next_node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        mem_free(po);
    }
    mem_free(p_group_data->output_id_head);

    mem_free(p_group_data);

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t ipmc_group_attr_fn_entries[] = {
    { SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT,
      ctc_sai_mcast_get_group_member_count,
      NULL},
    { SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST,
      ctc_sai_mcast_get_group_member_list,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set IPMC Group attribute
 *
 * @param[in] ipmc_group_id IPMC group id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_ipmc_group_attribute(
        _In_ sai_object_id_t ipmc_group_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    key.key.object_id = ipmc_group_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_IPMC_GROUP,  ipmc_group_attr_fn_entries, attr), status, out);

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "Failed to set ipmc group attr:%d\n", status);
    }

    return status;
}
/**
 * @brief Get IPMC Group attribute
 *
 * @param[in] ipmc_group_id IPMC group id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_ipmc_group_attribute(
        _In_ sai_object_id_t ipmc_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    key.key.object_id = ipmc_group_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_IPMC_GROUP, loop, ipmc_group_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "Failed to get ipmc group attr:%d\n", status);
    }

    return status;
}
/**
 * @brief Create IPMC group member
 *
 * @param[out] ipmc_group_member_id IPMC group member id
 * @param[in] switch_id Switch ID
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_ipmc_group_member(
        _Out_ sai_object_id_t *ipmc_group_member_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_id = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *output_id_node = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node = NULL;
    sai_router_interface_type_t sai_l3if_type = 0;
    sai_status_t               status = SAI_STATUS_SUCCESS;
    uint32                        value = 0;
    uint32                        attr_idx;
    uint16                        vlan_ptr = 0;
    uint16                        vlan_id = 0;
    uint16                        grp_id = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID, &attr_grp, &attr_idx));
    CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID, &attr_id, &attr_idx));

    ctc_sai_router_interface_get_rif_info(attr_id->oid, (uint8*)&sai_l3if_type, NULL, &value, &vlan_id);
    if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_vlan_ptr(attr_id->oid, &vlan_ptr));
        value = vlan_ptr;
    }
    else if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT))
    {
        value = (vlan_id << 20) | (value & 0xFFFFF);
    }

    p_group_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc group property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        if (attr_id->oid == po->output_id)
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }
        
    }

    output_id_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_member_output_id_t));
    if (!output_id_node)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    output_id_node->output_id = attr_id->oid;
    ctc_slist_add_tail(p_group_data->output_id_head, &(output_id_node->node));

    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_update_ipmc_group_member(pe->entry_property, attr_id->oid, 1), status, error0);
    }

    grp_id = _ctc_sai_mcast_get_group_id(attr_grp->oid);
    *ipmc_group_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, lchip, sai_l3if_type, grp_id, value);

    CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "create ipmc group member oid: 0x%llx, group oid: 0x%llx, output oid: 0x%llx\n", *ipmc_group_member_id, attr_grp->oid, attr_id->oid);

    return SAI_STATUS_SUCCESS;

error0:
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        _ctc_sai_mcast_update_ipmc_group_member(pe->entry_property, attr_id->oid, 0);
    }

    ctc_slist_delete_node(p_group_data->output_id_head, &(output_id_node->node));
    mem_free(output_id_node);

    return status;
}

/**
 * @brief Remove IPMC group member
 *
 * @param[in] ipmc_group_member_id IPMC group member id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_ipmc_group_member(
        _In_ sai_object_id_t ipmc_group_member_id)
{
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_object_id_t          ctc_oid;
    sai_object_id_t          grp_oid = 0;
    sai_router_interface_type_t sai_l3if_type = 0;
    uint32                        value = 0;
    uint16                        vlan_ptr = 0;
    uint16                        vlan_id = 0;
    uint8                          lchip = 0;
    uint8                         found = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ipmc_group_member_id, &lchip));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, ipmc_group_member_id, &ctc_oid);
    grp_oid = _ctc_sai_mcast_create_group_object_id(SAI_OBJECT_TYPE_IPMC_GROUP, lchip, ctc_oid.value2);

    p_group_data = ctc_sai_db_get_object_property(lchip, grp_oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        ctc_sai_router_interface_get_rif_info(po->output_id, (uint8*)&sai_l3if_type, NULL, &value, &vlan_id);
        if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN))
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_vlan_ptr(po->output_id, &vlan_ptr));
            value = vlan_ptr;
        }
        else if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT))
        {
            value = (vlan_id << 20) | (value & 0xFFFFF);
        }

        if ((sai_l3if_type == ctc_oid.sub_type) && (value == ctc_oid.value))
        {
            ctc_slist_delete_node(p_group_data->output_id_head, node);
            mem_free(po);
            found = 1;
            break;
        }
    }
    if (1 != found)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    CTC_SLIST_LOOP(p_group_data->entry_head, node)
    {
        pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
        _ctc_sai_mcast_update_ipmc_group_member(pe->entry_property, ipmc_group_member_id, 0);
    }

    CTC_SAI_LOG_INFO(SAI_API_IPMC_GROUP, "remove ipmc group member oid: 0x%llx\n", ipmc_group_member_id);

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t ipmc_member_attr_fn_entries[] = {
    { SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID,
      ctc_sai_mcast_get_member_group_id,
      NULL},
    { SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID,
      ctc_sai_mcast_get_member_output_id,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set IPMC Group attribute
 *
 * @param[in] ipmc_group_member_id IPMC group member id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_ipmc_group_member_attribute(
        _In_ sai_object_id_t ipmc_group_member_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    key.key.object_id = ipmc_group_member_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER,  ipmc_member_attr_fn_entries, attr), status, out);

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "Failed to set ipmc group member attr:%d\n", status);
    }

    return status;
}
/**
 * @brief Get IPMC Group attribute
 *
 * @param[in] ipmc_group_member_id IPMC group member ID
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_ipmc_group_member_attribute(
        _In_ sai_object_id_t ipmc_group_member_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC_GROUP);

    key.key.object_id = ipmc_group_member_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, loop, ipmc_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC_GROUP, "Failed to get ipmc group member attr:%d\n", status);
    }

    return status;
}

const sai_ipmc_group_api_t ctc_sai_ipmc_group_api = {
    ctc_sai_mcast_create_ipmc_group,
    ctc_sai_mcast_remove_ipmc_group,
    ctc_sai_mcast_set_ipmc_group_attribute,
    ctc_sai_mcast_get_ipmc_group_attribute,
    ctc_sai_mcast_create_ipmc_group_member,
    ctc_sai_mcast_remove_ipmc_group_member,
    ctc_sai_mcast_set_ipmc_group_member_attribute,
    ctc_sai_mcast_get_ipmc_group_member_attribute
};

#define ________RPF_GROUP________
/**
 * @brief Create RPF interface group
 *
 * @param[out] rpf_group_id RPF interface group id
 * @param[in] switch_id Switch id
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_rpf_group(
        _Out_ sai_object_id_t *rpf_group_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    ctc_sai_rpf_group_property_t *rpf_grp = NULL;
    uint32 rpf_group_idx = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_RPF_GROUP, &rpf_group_idx));

    *rpf_group_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP, lchip, 0, rpf_group_idx, 0);

    CTC_SAI_LOG_INFO(SAI_API_RPF_GROUP, "create rpf group id: %d, oid: 0x%llx\n", rpf_group_idx, *rpf_group_id);

    rpf_grp = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_rpf_group_property_t));
    if (NULL == rpf_grp)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }
    sal_memset(rpf_grp, 0, sizeof(ctc_sai_rpf_group_property_t));

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *rpf_group_id, (void*)rpf_grp), status, error1);

    return SAI_STATUS_SUCCESS;

error1:
    mem_free(rpf_grp);

error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_RPF_GROUP, rpf_group_idx);

    return status;
}

/**
 * @brief Remove RPF interface group
 *
 * @param[in] rpf_group_id RPF interface group id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_rpf_group(
        _In_ sai_object_id_t rpf_group_id)
{
    sai_status_t    status = SAI_STATUS_SUCCESS;
    ctc_sai_rpf_group_property_t *rpf_grp = NULL;
    uint16 rpf_group_idx = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(rpf_group_id, &lchip));

    rpf_grp = ctc_sai_db_get_object_property(lchip, rpf_group_id);
    if (NULL == rpf_grp)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        return status;
    }

    rpf_group_idx = _ctc_sai_mcast_get_group_id(rpf_group_id);

    CTC_SAI_LOG_INFO(SAI_API_RPF_GROUP, "remove rpf group id: %d, oid: 0x%llx\n", rpf_group_idx, rpf_group_id);

    CTC_SAI_ERROR_RETURN(ctc_sai_db_remove_object_property(lchip, rpf_group_id));

    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_RPF_GROUP, rpf_group_idx), status, error0);

    mem_free(rpf_grp);

    return SAI_STATUS_SUCCESS;

error0:
    ctc_sai_db_add_object_property(lchip, rpf_group_id, (void*)rpf_grp);

    return status;
}

sai_status_t ctc_sai_mcast_get_rpf_group_info(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_object_id_t rpf_member_oid[CTC_IP_MAX_RPF_IF];
    ctc_sai_rpf_group_property_t *rpf_grp = NULL;
    uint16                     rpf_group_idx = 0;
    uint8                       loop = 0;
    uint8                       intf_cnt = 0;
    uint8                       lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);

    rpf_grp = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == rpf_grp)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    rpf_group_idx = _ctc_sai_mcast_get_group_id(key->key.object_id);

    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (CTC_IS_BIT_SET(rpf_grp->bmp, loop))
        {
            rpf_member_oid[intf_cnt++] = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP_MEMBER, lchip, 0, rpf_group_idx, rpf_grp->intf[loop]);
        }
    }

    switch (attr->id)
    {
        case SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT:
            attr->value.u32 = intf_cnt;
            break;
        case SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST:
            intf_cnt = (intf_cnt < attr->value.objlist.count) ? intf_cnt: attr->value.objlist.count;
            ctc_sai_fill_object_list(sizeof(sai_object_id_t), rpf_member_oid, intf_cnt, &attr->value.objlist);
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t rpf_group_attr_fn_entries[] = {
    { SAI_RPF_GROUP_ATTR_RPF_INTERFACE_COUNT,
      ctc_sai_mcast_get_rpf_group_info,
      NULL},
    { SAI_RPF_GROUP_ATTR_RPF_MEMBER_LIST,
      ctc_sai_mcast_get_rpf_group_info,
      NULL },
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set RPF interface Group attribute
 *
 * @param[in] rpf_group_id RPF interface group id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_rpf_group_attribute(
        _In_ sai_object_id_t rpf_group_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    key.key.object_id = rpf_group_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_RPF_GROUP,  rpf_group_attr_fn_entries, attr), status, out);

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_RPF_GROUP, "Failed to set rpf group attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Get RPF interface Group attribute
 *
 * @param[in] rpf_group_id RPF interface group id
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_rpf_group_attribute(
        _In_ sai_object_id_t rpf_group_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    key.key.object_id = rpf_group_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_RPF_GROUP, loop, rpf_group_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_RPF_GROUP, "Failed to get rpf group attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Create RPF interface group member
 *
 * @param[out] rpf_group_member_id RPF interface group member id
 * @param[in] switch_id Switch ID
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_rpf_group_member(
        _Out_ sai_object_id_t *rpf_group_member_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_id = NULL;
    ctc_sai_rpf_group_property_t *rpf_grp_data = NULL;
    uint32                        attr_idx;
    uint16                        intf_id = 0;
    uint16                        rpf_group_idx = 0;
    uint8                          loop = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID, &attr_grp, &attr_idx));
    CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID, &attr_id, &attr_idx));

    rpf_grp_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
    if (NULL == rpf_grp_data)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    rpf_group_idx = _ctc_sai_mcast_get_group_id(attr_grp->oid);

    ctc_sai_oid_get_l3if_id(attr_id->oid, &intf_id);
    
    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (intf_id == rpf_grp_data->intf[loop])
        {
            return SAI_STATUS_ITEM_ALREADY_EXISTS;
        }
    }

    *rpf_group_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP_MEMBER, lchip, 0, rpf_group_idx, intf_id);

    CTC_SAI_LOG_INFO(SAI_API_RPF_GROUP, "create rpf group member, group id: %d, group oid: 0x%llx, intf id: %d, intf oid: 0x%llx, member oid: 0x%llx\n",
                rpf_group_idx, attr_grp->oid, intf_id, attr_id->oid, *rpf_group_member_id);

    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (!CTC_IS_BIT_SET(rpf_grp_data->bmp, loop))
        {
            rpf_grp_data->intf[loop] = intf_id;
            CTC_BIT_SET(rpf_grp_data->bmp, loop);
            break;
        }
    }

    return SAI_STATUS_SUCCESS;
}

/**
 * @brief Remove RPF interface group member
 *
 * @param[in] rpf_group_member_id RPF interface group member id
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_rpf_group_member(
        _In_ sai_object_id_t rpf_group_member_id)
{
    ctc_object_id_t ctc_oid;
    sai_object_id_t rpf_group_id;
    ctc_sai_rpf_group_property_t *rpf_grp_data = NULL;
    uint32                        intf_id = 0;
    uint16                        rpf_group_idx = 0;
    uint8                          loop = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(rpf_group_member_id, &lchip));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_RPF_GROUP, rpf_group_member_id, &ctc_oid);
    rpf_group_idx = ctc_oid.value2;
    intf_id = ctc_oid.value;

    rpf_group_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP, lchip, 0, rpf_group_idx, 0);

    rpf_grp_data = ctc_sai_db_get_object_property(lchip, rpf_group_id);
    if (NULL == rpf_grp_data)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    CTC_SAI_LOG_INFO(SAI_API_RPF_GROUP, "remove rpf group member, group id: %d, group oid: 0x%llx, intf id: %d, member oid: 0x%llx\n",
                rpf_group_idx, rpf_group_id, intf_id, rpf_group_member_id);

    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (CTC_IS_BIT_SET(rpf_grp_data->bmp, loop) && (rpf_grp_data->intf[loop] == intf_id))
        {
            rpf_grp_data->intf[loop] = 0;
            CTC_BIT_UNSET(rpf_grp_data->bmp, loop);
            goto out;
        }
    }
    return SAI_STATUS_ITEM_NOT_FOUND;
out:
    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_mcast_get_rpf_member_info(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    ctc_object_id_t       ctc_oid;
    sai_object_id_t  if_oid = 0;
    ctc_sai_router_interface_t* p_sai_router_if = NULL;
    uint8 if_type = 0;
    uint8 lchip = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_RPF_GROUP, key->key.object_id, &ctc_oid);

    switch (attr->id)
    {
        case SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP, lchip, 0, ctc_oid.value2, 0);
            break;
        case SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID:
            for (if_type=SAI_ROUTER_INTERFACE_TYPE_PORT; if_type<=SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT; if_type++)
            {
                if_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, if_type, 0, ctc_oid.value);
                p_sai_router_if = ctc_sai_db_get_object_property(lchip, if_oid);
                if (NULL != p_sai_router_if)
                {
                    attr->value.oid = if_oid;
                    break;
                }
            }
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t rpf_member_attr_fn_entries[] = {
    { SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID,
      ctc_sai_mcast_get_rpf_member_info,
      NULL},
    { SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID,
      ctc_sai_mcast_get_rpf_member_info,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set RPF interface Group attribute
 *
 * @param[in] rpf_group_member_id RPF interface group member id
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_rpf_group_member_attribute(
        _In_ sai_object_id_t rpf_group_member_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    key.key.object_id = rpf_group_member_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_RPF_GROUP_MEMBER,  rpf_member_attr_fn_entries, attr), status, out);

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_RPF_GROUP, "Failed to set rpf group member attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Get RPF interface Group attribute
 *
 * @param[in] rpf_group_member_id RPF group member ID
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_rpf_group_member_attribute(
        _In_ sai_object_id_t rpf_group_member_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;

    CTC_SAI_LOG_ENTER(SAI_API_RPF_GROUP);

    key.key.object_id = rpf_group_member_id;
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_RPF_GROUP_MEMBER, loop, rpf_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_RPF_GROUP, "Failed to get rpf group member attr:%d\n", status);
    }

    return status;
}

const sai_rpf_group_api_t ctc_sai_rpf_group_api = {
    ctc_sai_mcast_create_rpf_group,
    ctc_sai_mcast_remove_rpf_group,
    ctc_sai_mcast_set_rpf_group_attribute,
    ctc_sai_mcast_get_rpf_group_attribute,
    ctc_sai_mcast_create_rpf_group_member,
    ctc_sai_mcast_remove_rpf_group_member,
    ctc_sai_mcast_set_rpf_group_member_attribute,
    ctc_sai_mcast_get_rpf_group_member_attribute
};

#define ________IPMC_ENTRY________
/**
 * @brief Create IPMC entry
 *
 * @param[in] ipmc_entry IPMC entry
 * @param[in] attr_count Number of attributes
 * @param[in] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_create_ipmc_entry(
        _In_ const sai_ipmc_entry_t *ipmc_entry,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *attr_grp  = NULL, *attr_rpf  = NULL, *attr_act = NULL;
    ctc_mcast_nh_param_group_t nh_mcast_group = {0};
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_rpf_group_property_t *rpf_grp_data = NULL;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    sai_packet_action_t   action = 0, update_action = SAI_PACKET_ACTION_TRANSIT;
    uint32                        attr_idx;
    uint32                        nh_id = 0;
    uint8                          loop = 0, loop1 = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC);

    if (!ipmc_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"NULL ipmc entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip));
    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db is exist\n");
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, &attr_act, &attr_idx);
    if (status == SAI_STATUS_SUCCESS)
    {
        action = attr_list[attr_idx].value.s32;
        CTC_SAI_ERROR_RETURN(ctc_sai_packet_action_merge(action, &update_action));
        CTC_SAI_ERROR_RETURN(_ctc_sai_mcast_mapping_ctc_action(&grp_param.flag, update_action));
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"mandatory attribute SAI_IPMC_ENTRY_ATTR_PACKET_ACTION missing! \n");
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, &attr_grp, &attr_idx);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_group_data = ctc_sai_db_get_object_property(lchip, attr_grp->oid);
        if (!p_group_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_MCAST_FDB,"ipmc group db is not found\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, &attr_rpf, &attr_idx);
    if (attr_rpf)
    {
        rpf_grp_data = ctc_sai_db_get_object_property(lchip, attr_rpf->oid);
        if (NULL == rpf_grp_data)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }

        for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
        {
            if (CTC_IS_BIT_SET(rpf_grp_data->bmp, loop))
            {
                grp_param.rpf_intf[loop1] = rpf_grp_data->intf[loop];
                grp_param.rpf_intf_valid[loop1] = 1;
                CTC_SAI_LOG_INFO(SAI_API_IPMC, "rpf[%d]: %d  ", loop1, grp_param.rpf_intf[loop1]);
                loop1++;
            }
        }
        CTC_SAI_LOG_INFO(SAI_API_IPMC, "\n");
        CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_RPF_CHECK);
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, &nh_id));
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, (uint32 *)&grp_param.group_id), status, error0);

    nh_mcast_group.mc_grp_id = grp_param.group_id;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_nh_add_mcast(lchip, nh_id, &nh_mcast_group), status, error1);

    _ctc_sai_mcast_ipmc_to_param(ipmc_entry, &grp_param);

    if (CTC_IP_VER_4 == grp_param.ip_version)
    {
        CTC_SAI_LOG_INFO(SAI_API_IPMC, "source ip is 0x%x, dest group is 0x%x\n",
                         grp_param.address.ipv4.src_addr,
                         grp_param.address.ipv4.group_addr);
    }
    else
    {
        CTC_SAI_LOG_INFO(SAI_API_IPMC, "source ip is %x:%x:%x:%x, dest group is %x:%x:%x:%x\n",
                         grp_param.address.ipv6.src_addr[0],
                         grp_param.address.ipv6.src_addr[1],
                         grp_param.address.ipv6.src_addr[2],
                         grp_param.address.ipv6.src_addr[3],
                         grp_param.address.ipv6.group_addr[0],
                         grp_param.address.ipv6.group_addr[1],
                         grp_param.address.ipv6.group_addr[2],
                         grp_param.address.ipv6.group_addr[3]);
    }

    CTC_SAI_CTC_ERROR_GOTO(ctcs_ipmc_add_group(lchip, &grp_param), status, error2);

    CTC_SAI_LOG_INFO(SAI_API_IPMC, "create ipmc entry, ctc group id: %d, oid: 0x%llx, nh_id: %d, action: %d, rpf group oid: 0x%llx\n",
                grp_param.group_id, (attr_grp ? attr_grp->oid : 0), nh_id, action, (attr_rpf ? attr_rpf->oid : 0));

    p_entry_data = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_property_t));
    if (!p_entry_data)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    sal_memset(p_entry_data, 0, sizeof(ctc_sai_mcast_entry_property_t));

    p_entry_data->group_oid = attr_grp ? attr_grp->oid : 0;
    p_entry_data->rpf_group_oid = attr_rpf ? attr_rpf->oid : 0;
    p_entry_data->group_id = grp_param.group_id;
    p_entry_data->action = update_action;
    p_entry_data->bind_type_head = ctc_slist_new();
    if (!p_entry_data->bind_type_head)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error4;
    }
    CTC_SAI_ERROR_GOTO(ctc_sai_db_entry_property_add(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry, (void*)p_entry_data), status, error4);
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);

    if (p_group_data)
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_update_ipmc_group_member(p_entry_property, po->output_id, 1), status, error5);
        }

        ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
        if (!ptr_node)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto error5;
        }

        ptr_node->entry_property = p_entry_property;
        ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));
    }

    return SAI_STATUS_SUCCESS;

error5:
    if (p_group_data)
    {
        CTC_SLIST_LOOP(p_group_data->output_id_head, node)
        {
            po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
            _ctc_sai_mcast_update_ipmc_group_member(p_entry_property, po->output_id, 0);
        }
    }

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);

error4:
    mem_free(p_entry_data);

error3:
    ctcs_ipmc_remove_group(lchip, &grp_param);

error2:
    ctcs_nh_remove_mcast(lchip, nh_id);

error1:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, grp_param.group_id);

error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);

    return status;
}
/**
 * @brief Remove IPMC entry
 *
 * @param[in] ipmc_entry IPMC entry
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_remove_ipmc_entry(
        _In_ const sai_ipmc_entry_t *ipmc_entry)
{
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL;
    ctc_sai_mcast_entry_bind_node_t *pb = NULL;
    ctc_sai_mcast_entry_node_t *pe = NULL;
    ctc_slistnode_t               *node, *next_node;
    uint32                        nh_id = 0;
    uint8                          lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC);

    if (!ipmc_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"NULL ipmc entry param\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip));
    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (!p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_entry_data = (ctc_sai_mcast_entry_property_t*)(p_entry_property->data);
    if (p_entry_data->group_oid)
    {
        p_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (!p_group_data)
        {
            CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc group property db not found\n");
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }

    _ctc_sai_mcast_ipmc_to_param(ipmc_entry, &grp_param);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_remove_group(lchip, &grp_param));
    ctcs_nh_remove_mcast(lchip, nh_id);

    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_NEXTHOP, nh_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_CTC_MCAST_GROUP, p_entry_data->group_id);

    CTC_SAI_LOG_INFO(SAI_API_IPMC, "remove ipmc entry, ctc group id: %d, oid: 0x%llx, nh_id: %d, action: %d, rpf group oid: 0x%llx\n",
                p_entry_data->group_id, p_entry_data->group_oid, nh_id, p_entry_data->action, p_entry_data->rpf_group_oid);

    ctc_sai_db_entry_property_remove(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);

    CTC_SLIST_LOOP_DEL(p_entry_data->bind_type_head, node, next_node)
    {
        pb = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);
        mem_free(pb);
    }
    mem_free(p_entry_data->bind_type_head);
    mem_free(p_entry_data);

    if (p_group_data)
    {
        CTC_SLIST_LOOP_DEL(p_group_data->entry_head, node, next_node)
        {
            pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
            if (pe->entry_property == p_entry_property)
            {
                ctc_slist_delete_node(p_group_data->entry_head, node);
                mem_free(pe);
                break;
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_get_ipmc_entry_info(sai_object_key_t *key, sai_attribute_t *attr, uint32 attr_idx)
{
    sai_ipmc_entry_t *ipmc_entry = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    uint8                          lchip = 0;

    ipmc_entry = &key->key.ipmc_entry;
    ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_IPMC_ENTRY_ATTR_PACKET_ACTION:
            attr->value.s32 = p_entry_data->action;
            break;
        case SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID:
            attr->value.oid = p_entry_data->group_oid;
            break;
        case SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID:
            attr->value.oid = p_entry_data->rpf_group_oid;
            break;
        default:
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_ipmc_packet_action(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_ipmc_entry_t *ipmc_entry = NULL;
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_rpf_group_property_t *rpf_grp_data = NULL;
    uint8 lchip = 0;
    uint8 loop = 0, loop1 = 0;
    sai_packet_action_t update_action;

    sal_memset(&grp_param, 0, sizeof(ctc_ipmc_group_info_t));

    ipmc_entry = &key->key.ipmc_entry;
    ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    update_action = p_entry_data->action;
    CTC_SAI_ERROR_RETURN(ctc_sai_packet_action_merge(attr->value.s32, &update_action));

    _ctc_sai_mcast_mapping_ctc_action(&grp_param.flag, update_action);
    
    _ctc_sai_mcast_ipmc_to_param(ipmc_entry, &grp_param);
    CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_SHARE_GROUP);
    grp_param.group_id = p_entry_data->group_id;
    rpf_grp_data = ctc_sai_db_get_object_property(lchip, p_entry_data->rpf_group_oid);

    /*can't set drop and rpf-check flag at the same time*/
    if((NULL != rpf_grp_data)&&(SAI_PACKET_ACTION_DROP != attr->value.s32))
    {
        CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_RPF_CHECK);
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_add_group(lchip, &grp_param));
    p_entry_data->action = update_action;
    
    /*set action need to recover rpf information*/
    if((NULL != rpf_grp_data)&&(SAI_PACKET_ACTION_DROP != attr->value.s32))
    {
  
        for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
        {
            if (CTC_IS_BIT_SET(rpf_grp_data->bmp, loop))
            {
                grp_param.rpf_intf[loop1] = rpf_grp_data->intf[loop];
                grp_param.rpf_intf_valid[loop1] = 1;
                loop1++;
            }
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_update_rpf(lchip, &grp_param));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_mcast_set_ipmc_group_id(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_ipmc_entry_t *ipmc_entry = NULL;
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_entry_property_t *p_entry_property = NULL;
    ctc_sai_mcast_group_property_t *p_group_data = NULL, *p_old_group_data = NULL;
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_sai_mcast_entry_node_t* pe = NULL;
    ctc_sai_mcast_entry_bind_node_t *pb = NULL;
    ctc_slistnode_t        *node, *next_node;
    ctc_sai_mcast_entry_node_t *ptr_node = NULL;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint32                        nh_id;
    uint8                          lchip = 0;

    ipmc_entry = &key->key.ipmc_entry;
    ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip);

    p_entry_property = ctc_sai_db_entry_property_get_property(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (NULL == p_entry_property)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    p_entry_data = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_nh_get_mcast_nh(lchip, p_entry_data->group_id, &nh_id));

    p_group_data = ctc_sai_db_get_object_property(lchip, attr->value.oid);
    if (!p_group_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc group db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    grp_param.group_id = p_entry_data->group_id;
    _ctc_sai_mcast_ipmc_to_param(ipmc_entry, &grp_param);
    CTC_SET_FLAG(grp_param.flag, CTC_IPMC_FLAG_KEEP_EMPTY_ENTRY);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_remove_group(lchip, &grp_param));

     if (p_entry_data->group_oid)
    {
        p_old_group_data = ctc_sai_db_get_object_property(lchip, p_entry_data->group_oid);
        if (p_old_group_data)
        {
            CTC_SLIST_LOOP_DEL(p_old_group_data->entry_head, node, next_node)
            {
                pe = _ctc_container_of(node, ctc_sai_mcast_entry_node_t, node);
                if (pe->entry_property == p_entry_property)
                {
                    ctc_slist_delete_node(p_old_group_data->entry_head, node);
                    mem_free(pe);
                }
            }
        }
    }

    CTC_SLIST_LOOP_DEL(p_entry_data->bind_type_head, node, next_node)
    {
        pb = _ctc_container_of(node, ctc_sai_mcast_entry_bind_node_t, node);
        ctc_slist_delete_node(p_entry_data->bind_type_head, node);
        mem_free(pb);
    }

    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        CTC_SAI_ERROR_GOTO(_ctc_sai_mcast_update_ipmc_group_member(p_entry_property, po->output_id, 1), status, error0);
    }

    ptr_node = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_mcast_entry_node_t));
    if (!ptr_node)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error0;
    }

    ptr_node->entry_property = p_entry_property;
    ctc_slist_add_tail(p_group_data->entry_head, &(ptr_node->node));

    p_entry_data->group_oid = attr->value.oid;

    return SAI_STATUS_SUCCESS;

error0:
    CTC_SLIST_LOOP(p_group_data->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        _ctc_sai_mcast_update_ipmc_group_member(p_entry_property, po->output_id, 0);
    }

    return status;
}

static sai_status_t ctc_sai_mcast_set_ipmc_rpf_group_id(sai_object_key_t *key, const  sai_attribute_t *attr)
{
    sai_ipmc_entry_t *ipmc_entry = NULL;
    ctc_ipmc_group_info_t grp_param = {0};
    ctc_sai_mcast_entry_property_t *p_entry_data = NULL;
    ctc_sai_rpf_group_property_t *rpf_grp_data = NULL;
    uint8                          loop = 0, loop1 = 0;
    uint8                          lchip = 0;

    sal_memset(&grp_param, 0, sizeof(ctc_ipmc_group_info_t));

    ipmc_entry = &key->key.ipmc_entry;
    ctc_sai_oid_get_lchip(ipmc_entry->switch_id, &lchip);

    p_entry_data = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)ipmc_entry);
    if (NULL == p_entry_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipmc property db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    rpf_grp_data = ctc_sai_db_get_object_property(lchip, attr->value.oid);
    if (NULL == rpf_grp_data)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (CTC_IS_BIT_SET(rpf_grp_data->bmp, loop))
        {
            grp_param.rpf_intf[loop1] = rpf_grp_data->intf[loop];
            grp_param.rpf_intf_valid[loop1] = 1;
            loop1++;
        }
    }

    _ctc_sai_mcast_ipmc_to_param(ipmc_entry, &grp_param);

    CTC_SAI_CTC_ERROR_RETURN(ctcs_ipmc_update_rpf(lchip, &grp_param));
    p_entry_data->rpf_group_oid = attr->value.oid;

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t ipmc_attr_fn_entries[] = {
    { SAI_IPMC_ENTRY_ATTR_PACKET_ACTION,
      ctc_sai_mcast_get_ipmc_entry_info,
      ctc_sai_mcast_set_ipmc_packet_action},
      { SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID,
      ctc_sai_mcast_get_ipmc_entry_info,
      ctc_sai_mcast_set_ipmc_group_id},
      { SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID,
      ctc_sai_mcast_get_ipmc_entry_info,
      ctc_sai_mcast_set_ipmc_rpf_group_id},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

/**
 * @brief Set IPMC entry attribute value
 *
 * @param[in] ipmc_entry IPMC entry
 * @param[in] attr Attribute
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_set_ipmc_entry_attribute(
        _In_ const sai_ipmc_entry_t *ipmc_entry,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC);

    sal_memcpy(&key.key.ipmc_entry, ipmc_entry, sizeof(sai_ipmc_entry_t));
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL,
                                             SAI_OBJECT_TYPE_IPMC_ENTRY,  ipmc_attr_fn_entries, attr), status, out);

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC, "Failed to set ipmc entry attr:%d\n", status);
    }

    return status;
}

/**
 * @brief Get IPMC entry attribute value
 *
 * @param[in] ipmc_entry IPMC entry
 * @param[in] attr_count Number of attributes
 * @param[inout] attr_list Array of attributes
 *
 * @return #SAI_STATUS_SUCCESS on success, failure status code on error
 */
static sai_status_t ctc_sai_mcast_get_ipmc_entry_attribute(
        _In_ const sai_ipmc_entry_t *ipmc_entry,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key;
    sai_status_t    status = SAI_STATUS_SUCCESS;
    uint8               loop = 0;

    CTC_SAI_LOG_ENTER(SAI_API_IPMC);

    sal_memcpy(&key.key.ipmc_entry, ipmc_entry, sizeof(sai_ipmc_entry_t));
    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_IPMC_ENTRY, loop, ipmc_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_IPMC, "Failed to get ipmc entry attr:%d\n", status);
    }

    return status;
}

const sai_ipmc_api_t ctc_sai_ipmc_api = {
    ctc_sai_mcast_create_ipmc_entry,
    ctc_sai_mcast_remove_ipmc_entry,
    ctc_sai_mcast_set_ipmc_entry_attribute,
    ctc_sai_mcast_get_ipmc_entry_attribute
};

sai_status_t
ctc_sai_mcast_api_init()
{
    ctc_sai_register_module_api(SAI_API_L2MC_GROUP, (void*)&ctc_sai_l2mc_group_api);
    ctc_sai_register_module_api(SAI_API_L2MC, (void*)&ctc_sai_l2mc_api);
    ctc_sai_register_module_api(SAI_API_MCAST_FDB, (void*)&ctc_sai_mcast_fdb_api);
    ctc_sai_register_module_api(SAI_API_IPMC_GROUP, (void*)&ctc_sai_ipmc_group_api);
    ctc_sai_register_module_api(SAI_API_RPF_GROUP, (void*)&ctc_sai_rpf_group_api);
    ctc_sai_register_module_api(SAI_API_IPMC, (void*)&ctc_sai_ipmc_api);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_rpf_group_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  rpf_grp_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_rpf_group_property_t* p_rpf_grp = NULL;
    uint8 loop = 0;
    uint8 index = 0;
    uint8 lchip = 0;

    rpf_grp_oid = bucket_data->oid;
    p_rpf_grp = (ctc_sai_rpf_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ctc_sai_oid_get_lchip(rpf_grp_oid, &lchip);

    if ((0 != p_dmp_grep->key.key.object_id) && (rpf_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (CTC_IS_BIT_SET(p_rpf_grp->bmp, loop))
        {
            index++;
        }
    }
    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-14d\n", num_cnt, rpf_grp_oid, index);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_rpf_member_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  rpf_grp_oid = 0;
    sai_object_id_t rpf_member_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_rpf_group_property_t* p_rpf_grp = NULL;
    uint8 loop = 0;
    uint32 rpf_group_idx = 0;
    uint8 lchip = 0;

    rpf_grp_oid = bucket_data->oid;
    p_rpf_grp = (ctc_sai_rpf_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ctc_sai_oid_get_lchip(rpf_grp_oid, &lchip);

    rpf_group_idx = _ctc_sai_mcast_get_group_id(rpf_grp_oid);
    for (loop = 0; loop < CTC_IP_MAX_RPF_IF; loop++)
    {
        if (CTC_IS_BIT_SET(p_rpf_grp->bmp, loop))
        {
            rpf_member_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_RPF_GROUP_MEMBER, lchip, 0, rpf_group_idx, p_rpf_grp->intf[loop]);
            if ((0 != p_dmp_grep->key.key.object_id) && (rpf_member_oid != p_dmp_grep->key.key.object_id))
            {
                continue;
            }
            CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" 0x%016"PRIx64" %-7d\n", num_cnt, rpf_member_oid, rpf_grp_oid, p_rpf_grp->intf[loop]);
            num_cnt++;
        }
    }

    *((uint32 *)(p_cb_data->value1)) = num_cnt;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_l2mc_group_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  l2mc_grp_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_group_property_t* p_l2mc_grp = NULL;

    l2mc_grp_oid = bucket_data->oid;
    p_l2mc_grp = (ctc_sai_mcast_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (l2mc_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-15d\n", num_cnt, l2mc_grp_oid, p_l2mc_grp->output_id_head->count);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_l2mc_member_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  l2mc_grp_oid = 0;
    sai_object_id_t l2mc_member_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_group_property_t* p_l2mc_grp = NULL;
    uint8 lchip = 0;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    uint16 grp_id = 0;

    l2mc_grp_oid = bucket_data->oid;
    p_l2mc_grp = (ctc_sai_mcast_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ctc_sai_oid_get_lchip(l2mc_grp_oid, &lchip);

    if ((0 != p_dmp_grep->key.key.object_id) && (l2mc_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    grp_id = _ctc_sai_mcast_get_group_id(l2mc_grp_oid);
    CTC_SLIST_LOOP(p_l2mc_grp->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        p_bridge_port = ctc_sai_db_get_object_property(lchip, po->output_id);
        if ((NULL == p_bridge_port) || (SAI_BRIDGE_PORT_TYPE_PORT  != p_bridge_port->port_type))
        {
            continue;
        }
        l2mc_member_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER, lchip, 0, grp_id, p_bridge_port->gport);
        if ((0 != p_dmp_grep->key.key.object_id) && (l2mc_member_oid != p_dmp_grep->key.key.object_id))
        {
            continue;
        }
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" 0x%016"PRIx64" 0x%016"PRIx64"\n", num_cnt, l2mc_member_oid, l2mc_grp_oid, po->output_id);
        num_cnt++;
    }

    *((uint32 *)(p_cb_data->value1)) = num_cnt;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_ipmc_group_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  ipmc_grp_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_group_property_t* p_ipmc_grp = NULL;

    ipmc_grp_oid = bucket_data->oid;
    p_ipmc_grp = (ctc_sai_mcast_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (ipmc_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" %-15d\n", num_cnt, ipmc_grp_oid, p_ipmc_grp->output_id_head->count);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_ipmc_member_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  ipmc_grp_oid = 0;
    sai_object_id_t ipmc_member_oid = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_group_property_t* p_l2mc_grp = NULL;
    uint8 lchip = 0;
    ctc_sai_mcast_member_output_id_t *po = NULL;
    ctc_slistnode_t               *node = NULL;
    uint16 grp_id = 0;
    uint16 vlan_ptr = 0;
    uint16 vlan_id = 0;
    uint32 value = 0;
    uint8 sai_l3if_type = 0;

    ipmc_grp_oid = bucket_data->oid;
    p_l2mc_grp = (ctc_sai_mcast_group_property_t*)bucket_data->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    ctc_sai_oid_get_lchip(ipmc_grp_oid, &lchip);

    if ((0 != p_dmp_grep->key.key.object_id) && (ipmc_grp_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    grp_id = _ctc_sai_mcast_get_group_id(ipmc_grp_oid);
    CTC_SLIST_LOOP(p_l2mc_grp->output_id_head, node)
    {
        po = _ctc_container_of(node, ctc_sai_mcast_member_output_id_t, node);
        ctc_sai_router_interface_get_rif_info(po->output_id, (uint8*)&sai_l3if_type, NULL, &value, &vlan_id);
        if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_VLAN))
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_vlan_ptr(po->output_id, &vlan_ptr));
            value = vlan_ptr;
        }
        else if ((vlan_id)&&(sai_l3if_type == SAI_ROUTER_INTERFACE_TYPE_SUB_PORT))
        {
            value = (vlan_id << 20) | (value & 0xFFFFF);
        }

        ipmc_member_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER, lchip, sai_l3if_type, grp_id, value);
        if ((0 != p_dmp_grep->key.key.object_id) && (ipmc_member_oid != p_dmp_grep->key.key.object_id))
        {
            continue;
        }
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64" 0x%016"PRIx64" 0x%016"PRIx64"\n", num_cnt, ipmc_member_oid, ipmc_grp_oid, po->output_id);
        num_cnt++;
    }

    *((uint32 *)(p_cb_data->value1)) = num_cnt;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_l2mc_entry_print_cb(ctc_sai_entry_property_t* p_entry_property, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_entry_property_t* p_l2mc_mcast_entry = NULL;
    sai_ip_address_t ip_src;
    sai_ip_address_t ip_dst;
    char ip_src_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char ip_dst_buf[CTC_IPV6_ADDR_STR_LEN] = {0};

    p_l2mc_mcast_entry = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    ip_src.addr_family = p_entry_property->key.mcast_ip.ip_ver;
    ip_dst.addr_family = p_entry_property->key.mcast_ip.ip_ver;
    if (SAI_IP_ADDR_FAMILY_IPV4 == ip_src.addr_family)
    {
        sal_memcpy(&(ip_src.addr.ip4), &(p_entry_property->key.mcast_ip.src.ip4), sizeof(sai_ip4_t));
        sal_memcpy(&(ip_dst.addr.ip4), &(p_entry_property->key.mcast_ip.dst.ip4), sizeof(sai_ip4_t));
    }
    else
    {
        sal_memcpy(&(ip_src.addr.ip6), &(p_entry_property->key.mcast_ip.src.ip6), sizeof(sai_ip6_t));
        sal_memcpy(&(ip_dst.addr.ip6), &(p_entry_property->key.mcast_ip.dst.ip6), sizeof(sai_ip6_t));
    }

    ctc_sai_get_ip_str(&ip_src, ip_src_buf);
    ctc_sai_get_ip_str(&ip_dst, ip_dst_buf);
    CTC_SAI_LOG_DUMP(p_file, "%-4d %-5d %-19s %-19s %-5d %-6d %-7d 0x%016"PRIx64" 0x%016"PRIx64" %-3d %-3d\n", num_cnt, p_entry_property->key.mcast_ip.vrf_id, ip_src_buf, ip_dst_buf, \
           p_entry_property->key.mcast_ip.is_bridge, p_entry_property->key.mcast_ip.is_pending, p_l2mc_mcast_entry->group_id, p_l2mc_mcast_entry->rpf_group_oid,  p_l2mc_mcast_entry->group_oid, p_l2mc_mcast_entry->action, p_l2mc_mcast_entry->cid);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_ipmc_entry_print_cb(ctc_sai_entry_property_t* p_entry_property, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_entry_property_t* p_ipmc_mcast_entry = NULL;
    sai_ip_address_t ip_src;
    sai_ip_address_t ip_dst;
    char ip_src_buf[CTC_IPV6_ADDR_STR_LEN] = {0};
    char ip_dst_buf[CTC_IPV6_ADDR_STR_LEN] = {0};

    p_ipmc_mcast_entry = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));


    ip_src.addr_family = p_entry_property->key.mcast_ip.ip_ver;
    ip_dst.addr_family = p_entry_property->key.mcast_ip.ip_ver;
    if (SAI_IP_ADDR_FAMILY_IPV4 == ip_src.addr_family)
    {
        sal_memcpy(&(ip_src.addr.ip4), &(p_entry_property->key.mcast_ip.src.ip4), sizeof(sai_ip4_t));
        sal_memcpy(&(ip_dst.addr.ip4), &(p_entry_property->key.mcast_ip.dst.ip4), sizeof(sai_ip4_t));
    }
    else
    {
        sal_memcpy(&(ip_src.addr.ip6), &(p_entry_property->key.mcast_ip.src.ip6), sizeof(sai_ip6_t));
        sal_memcpy(&(ip_dst.addr.ip6), &(p_entry_property->key.mcast_ip.dst.ip6), sizeof(sai_ip6_t));
    }

    ctc_sai_get_ip_str(&ip_src, ip_src_buf);
    ctc_sai_get_ip_str(&ip_dst, ip_dst_buf);
    CTC_SAI_LOG_DUMP(p_file, "%-4d %-5d %-19s %-19s %-5d %-6d %-6d 0x%016"PRIx64" 0x%016"PRIx64" %-3d %-3d\n", num_cnt, p_entry_property->key.mcast_ip.vrf_id, ip_src_buf, ip_dst_buf, \
           p_entry_property->key.mcast_ip.is_bridge, p_entry_property->key.mcast_ip.is_pending, p_ipmc_mcast_entry->group_id, p_ipmc_mcast_entry->rpf_group_oid,  p_ipmc_mcast_entry->group_oid, p_ipmc_mcast_entry->action, p_ipmc_mcast_entry->cid);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_mcast_dump_mcast_fdb_entry_print_cb(ctc_sai_entry_property_t* p_entry_property, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_mcast_entry_property_t* p_mcast_fdb_entry = NULL;
    char src_mac[64] = {0};

    p_mcast_fdb_entry = (ctc_sai_mcast_entry_property_t*)p_entry_property->data;
    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    ctc_sai_get_mac_str(p_entry_property->key.mcast_fdb.mac, src_mac);
    CTC_SAI_LOG_DUMP(p_file, "%-4d %-20s %-4d %-5d %-6d %-6d 0x%016"PRIx64" 0x%016"PRIx64" %-3d %-3d\n", num_cnt, src_mac, p_entry_property->key.mcast_fdb.fid, p_entry_property->key.mcast_fdb.is_pending,\
           p_entry_property->key.mcast_fdb.is_bridge, p_mcast_fdb_entry->group_id, p_mcast_fdb_entry->rpf_group_oid,  p_mcast_fdb_entry->group_oid, p_mcast_fdb_entry->action, p_mcast_fdb_entry->cid);

    (*((uint32 *)(p_cb_data->value1)))++;

    return SAI_STATUS_SUCCESS;
}

void ctc_sai_rpf_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Rpf group MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_RPF_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Rpf group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_rpf_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-14s\n", "No.", "Rpf_grp_oid", "Rpf_member_cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_RPF_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_rpf_group_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_RPF_GROUP_MEMBER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Rpf group member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-7s\n", "No.", "Rpf_member_id", "Rpf_grp_id", "Intf_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_RPF_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_rpf_member_print_cb, (void*)(&sai_cb_data));
    }
}

void ctc_sai_l2mc_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI L2mc group MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_L2MC_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "L2mc group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-15s\n", "No.", "L2mc_grp_id", "L2mc_member_cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_L2MC_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_l2mc_group_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_L2MC_GROUP_MEMBER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "L2mc group member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-18s\n", "No.", "L2mc_member_id", "L2mc_grp_id", "Output_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_L2MC_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_l2mc_member_print_cb, (void*)(&sai_cb_data));
    }
}

void ctc_sai_ipmc_group_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Ipmc group MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_IPMC_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Ipmc group");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-15s\n", "No.", "Ipmc_grp_id", "Ipmc_member_cnt");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_IPMC_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_ipmc_group_print_cb, (void*)(&sai_cb_data));
    }

    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_IPMC_GROUP_MEMBER))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Ipmc group member");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_group_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-18s\n", "No.", "Ipmc_member_id", "Ipmc_grp_id", "Output_id");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_IPMC_GROUP,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_ipmc_member_print_cb, (void*)(&sai_cb_data));
    }
}

void ctc_sai_l2mc_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI L2mc MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_L2MC_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "L2mc entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_entry_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-5s %-19s %-19s %-5s %-6s %-7s %-18s %-18s %-3s %-3s\n", "No.", "vrfid", "Ip_src", "Ip_dst", "Pding", "Bridge", "Ctc_grp", "Rpf_grp_id", "Group_id", "Act", "Cid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_l2mc_entry_print_cb, (void*)(&sai_cb_data));
    }
}

void ctc_sai_ipmc_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Ipmc MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_IPMC_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Ipmc entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_entry_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-5s %-19s %-19s %-5s %-6s %-6s %-18s %-18s %-3s %-3s\n", "No.", "vrfid", "Ip_src", "Ip_dst", "Pding", "Bridge", "Ctc_grp", "Rpf_grp_id", "Group_id", "Act", "Cid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_ipmc_entry_print_cb, (void*)(&sai_cb_data));
    }
}

void ctc_sai_mcast_fdb_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Mcast fdb MODULE");
    num_cnt = 1;
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_MCAST_FDB_ENTRY))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Mcast fdb entry");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_mcast_entry_property_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-20s %-4s %-5s %-6s %-6s %-18s %-18s %-3s %-3s\n", "No.", "Mac_addr", "Fid", "Pding", "Bridge", "Ctc_grp", "Rpf_grp_id", "Group_id", "Act", "Cid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB,
                                            (hash_traversal_fn)_ctc_sai_mcast_dump_mcast_fdb_entry_print_cb, (void*)(&sai_cb_data));
    }
}

sai_status_t
ctc_sai_mcast_db_init(uint8 lchip)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_db_wb_t wb_info;
    ctc_ipmc_force_route_t mcv4_route;
    ctc_ipmc_force_route_t mcv6_route;

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_L2MCGROUP;
    wb_info.data_len = sizeof(ctc_sai_mcast_group_property_t);
    wb_info.wb_sync_cb = _ctc_sai_mcast_group_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_mcast_group_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_mcast_group_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_L2MC_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_IPMCGROUP;
    wb_info.data_len = sizeof(ctc_sai_mcast_group_property_t);
    wb_info.wb_sync_cb = _ctc_sai_mcast_group_wb_sync_cb_ip;
    wb_info.wb_reload_cb = _ctc_sai_mcast_group_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_mcast_group_wb_reload_cb1_ip;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_IPMC_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_RPFGROUP;
    wb_info.data_len = sizeof(ctc_sai_rpf_group_property_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_mcast_rpf_group_wb_reload_cb;
    wb_info.wb_reload_cb1 = NULL;    
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_RPF_GROUP, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_MCASTFDB;
    wb_info.data_len = sizeof(ctc_sai_mcast_entry_property_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_mcast_entry_wb_reload_cb;
    wb_info.wb_reload_cb1 = NULL;     
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (void*)(&wb_info));
    
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_L2MC;
    wb_info.data_len = sizeof(ctc_sai_mcast_entry_property_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_mcast_entry_wb_reload_cb;
    wb_info.wb_reload_cb1 = NULL;    
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_IPMC;
    wb_info.data_len = sizeof(ctc_sai_mcast_entry_property_t);
    wb_info.wb_sync_cb = _ctc_sai_mcast_entry_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_mcast_entry_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_mcast_entry_wb_reload_cb1; 
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_ENTRY, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    CTC_SAI_LOG_ERROR(SAI_API_IPMC,"force route entry set start\n");
    /* ipv4 L3 pdu mcast route force bridge */
    /*for ipv4 pdu packets*/
    sal_memset(&mcv4_route, 0, sizeof(ctc_ipmc_force_route_t));
    mcv4_route.ip_version = CTC_IP_VER_4;
    mcv4_route.force_bridge_en = 1;

    mcv4_route.ipaddr0_valid = 1;
    mcv4_route.ip_addr0.ipv4 = 0xE0000000;
    mcv4_route.addr0_mask = 24;
    //CTC_SAI_CTC_ERROR_GOTO(ctc_ipmc_set_mcast_force_route(&mcv4_route), status, out);

    mcv4_route.ipaddr1_valid = 1;
    mcv4_route.ip_addr1.ipv4 = 0x0;
    mcv4_route.addr1_mask = 32;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_ipmc_set_mcast_force_route(lchip, &mcv4_route), status, error1);

    /* ipv6 set mcast address in order to send ndp, ospf packet to cpu via force bridge when packet
    is multicast
    #define ALLNODE                            "ff02::1"
    #define ALLROUTER                        "ff02::2"
    #define SOLICITED_PREFIX            "ff02::1:ff00:0"*/
    sal_memset(&mcv6_route, 0, sizeof(ctc_ipmc_force_route_t));
    mcv6_route.ip_version = CTC_IP_VER_6;
    mcv6_route.force_bridge_en = 1;
    //mcv6_route.force_ucast_en = 1;

    mcv6_route.ipaddr0_valid = 1;
    mcv6_route.ip_addr0.ipv6[0] = 0xFF020000;
    mcv6_route.ip_addr0.ipv6[1] = 0x00000000;
    mcv6_route.ip_addr0.ipv6[2] = 0x00000000;
    mcv6_route.ip_addr0.ipv6[3] = 0x00000000;
    mcv6_route.addr0_mask = 120;
    //ret = ctc_ipmc_set_mcast_force_route(&mcv6_route);

    mcv6_route.ipaddr1_valid = 1;
    mcv6_route.ip_addr1.ipv6[0] = 0xFF020000;
    mcv6_route.ip_addr1.ipv6[1] = 0x00000000;
    mcv6_route.ip_addr1.ipv6[2] = 0x00000001;
    mcv6_route.ip_addr1.ipv6[3] = 0xFF000000;
    mcv6_route.addr1_mask = 104;
    CTC_SAI_CTC_ERROR_GOTO(ctcs_ipmc_set_mcast_force_route(lchip, &mcv6_route), status, error2);

    goto out;
    
error2:
    CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipv6 force route entry set fail\n");

error1:
    CTC_SAI_LOG_ERROR(SAI_API_IPMC,"ipv4 force route entry set fail\n");
out:
    return status;
}

sai_status_t
ctc_sai_mcast_db_deinit(uint8 lchip)
{

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_IPMC_GROUP, (hash_traversal_fn)_ctc_sai_mcast_db_mcast_group_deinit_cb, NULL);
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_L2MC_GROUP, (hash_traversal_fn)_ctc_sai_mcast_db_mcast_group_deinit_cb, NULL);
    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_IPMC, (hash_traversal_fn)_ctc_sai_mcast_db_mcast_entry_deinit_cb, NULL);
    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_L2MC, (hash_traversal_fn)_ctc_sai_mcast_db_mcast_entry_deinit_cb, NULL);
    ctc_sai_db_entry_property_traverse(lchip, CTC_SAI_DB_ENTRY_TYPE_MCAST_FDB, (hash_traversal_fn)_ctc_sai_mcast_db_mcast_entry_deinit_cb, NULL);

    return SAI_STATUS_SUCCESS;
}

