/*sai include file*/
#include "sai.h"
#include "saitypes.h"
#include "saistatus.h"

/*ctc_sai include file*/
#include "ctc_sai.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_virtual_router.h"
#include "ctc_sai_vlan.h"
#include "ctc_sai_hostif.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_port.h"
#include "ctc_sai_acl.h"

/*sdk include file*/
#include "ctcs_api.h"



typedef struct  ctc_sai_rif_lkp_param_s
{
   uint8 lchip;
   uint8 type;
   uint16 vlan;
   uint32 gport;
   sai_object_id_t router_interface_id;
}ctc_sai_rif_lkp_param_t;

static sai_status_t
_ctc_sai_router_interface_build_db(uint8 lchip, sai_object_id_t router_interface_id, ctc_sai_router_interface_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    p_rif_info = mem_malloc(MEM_L3IF_MODULE, sizeof(ctc_sai_router_interface_t));
    if (NULL == p_rif_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_rif_info, 0, sizeof(ctc_sai_router_interface_t));
    status = ctc_sai_db_add_object_property(lchip, router_interface_id, (void*)p_rif_info);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_rif_info);
        return status;
    }
    p_rif_info->neighbor_miss_action = SAI_PACKET_ACTION_TRAP;
    p_rif_info->v4_state = 1;
    p_rif_info->v6_state = 1;
    p_rif_info->mtu = 1514;
    p_rif_info->stats_state = 1;
    *oid_property = p_rif_info;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_remove_db(uint8 lchip, sai_object_id_t router_interface_id)
{
    ctc_sai_router_interface_t* p_rif_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, router_interface_id);
    mem_free(p_rif_info);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_create_attr_check(uint8 lchip, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    int32 sub_type = 0;
    ctc_sai_oid_property_t* p_oid_property = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
    if (NULL == p_oid_property)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_TYPE, &attr_value, &index));
    if (CTC_SAI_ERROR(status))
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }
    sub_type = attr_value->s32;
    if (SAI_ROUTER_INTERFACE_TYPE_VLAN == sub_type)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_VLAN_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
    }
    if ((SAI_ROUTER_INTERFACE_TYPE_PORT == sub_type) || (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == sub_type))
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_PORT_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        p_oid_property = ctc_sai_db_get_object_property(lchip, attr_value->oid);
        if (NULL == p_oid_property)
        {
            /*return SAI_STATUS_ITEM_NOT_FOUND;*/
        }
    }
    if (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == sub_type)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }
    else if(SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT == sub_type)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }
    else if(SAI_ROUTER_INTERFACE_TYPE_BRIDGE == sub_type)
    {
        status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID, &attr_value, &index));
        if (CTC_SAI_ERROR(status))
        {
            return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_check_hw_exist(sai_object_id_t router_interface_id, uint8* exist)
{
    uint8 lchip = 0;
    uint16 l3if_id = 0;
    uint32 value = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_oid_get_lchip(router_interface_id, &lchip);
    ctc_sai_oid_get_l3if_id(router_interface_id, &l3if_id);
    status = ctcs_l3if_get_property(lchip, l3if_id, CTC_L3IF_PROP_VRF_EN, &value);
    *exist = status? 0 : 1;
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_set_attr_hw(sai_object_id_t router_interface_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_l3if_property_t l3if_prop[MAX_CTC_L3IF_PROP_NUM] = {MAX_CTC_L3IF_PROP_NUM};
    uint32 l3if_prop_value[MAX_CTC_L3IF_PROP_NUM] = {0};
    uint8 l3if_prop_cnt = 0;
    uint8 i = 0;
    uint16 l3if_id = 0;
    ctc_stats_statsid_t stats_statsid_in;
    ctc_stats_statsid_t stats_statsid_eg;
    ctc_l3if_router_mac_t router_mac;
    ctc_object_id_t ctc_object_id;
    uint8 exist = 0, need_update_egr_mac = 0;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_oid_get_lchip(router_interface_id, &lchip);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, router_interface_id, &ctc_object_id);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type)
    {
         _ctc_sai_router_interface_check_hw_exist(router_interface_id, &exist);
        if (0 == exist)
        {
            return SAI_STATUS_SUCCESS;
        }
    }
    else if((SAI_ROUTER_INTERFACE_TYPE_LOOPBACK == ctc_object_id.sub_type)
        ||(SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER == ctc_object_id.sub_type))
    {
        return SAI_STATUS_SUCCESS;
    }
    if (!p_rif_info->is_virtual)
    {
        ctc_sai_oid_get_l3if_id(router_interface_id, &l3if_id);
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_VRF_ID;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->vrf_id;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_VRF_EN;
        l3if_prop_value[l3if_prop_cnt++] = 1;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_IPV4_UCAST;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->v4_state;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_IPV6_UCAST;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->v6_state;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_IPV4_MCAST;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->v4_mc_state;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_IPV6_MCAST;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->v6_mc_state;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_MTU_SIZE;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->mtu;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_MTU_EN;
        l3if_prop_value[l3if_prop_cnt++] = 1;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_MTU_EXCEPTION_EN;
        l3if_prop_value[l3if_prop_cnt++] = 1;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_MPLS_EN;
        l3if_prop_value[l3if_prop_cnt++] = 1;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_NAT_IFTYPE;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->nat_iftype;
        l3if_prop[l3if_prop_cnt] = CTC_L3IF_PROP_IPV4_SA_TYPE;
        l3if_prop_value[l3if_prop_cnt++] = p_rif_info->snat_en ? CTC_L3IF_IPSA_LKUP_TYPE_NAT : CTC_L3IF_IPSA_LKUP_TYPE_NONE;

        for (i = 0; i < l3if_prop_cnt; i++)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_property(lchip, l3if_id, l3if_prop[i], l3if_prop_value[i]));
        }

        if(p_rif_info->stats_state && !(p_rif_info->ing_statsid) && !(p_rif_info->egs_statsid))
        {
            stats_statsid_in.dir = CTC_INGRESS;
            stats_statsid_in.type = CTC_STATS_STATSID_TYPE_L3IF;
            status = ctcs_stats_create_statsid(lchip, &stats_statsid_in);
            if (CTC_E_NONE != status)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "stats ingress no resource\n");
                goto error1;
            }
            else
            {
                status = ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_STATS, stats_statsid_in.stats_id);
                if (CTC_E_NONE != status)
                {

                    goto error2;
                }
                else
                {
                    p_rif_info->ing_statsid = stats_statsid_in.stats_id;
                }

           }

            stats_statsid_eg.dir = CTC_EGRESS;
            stats_statsid_eg.type = CTC_STATS_STATSID_TYPE_L3IF;
            status = ctcs_stats_create_statsid(lchip, &stats_statsid_eg);
            if (CTC_E_NONE != status)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "stats ingress no resource\n");
                goto error3;
            }
            else
            {
                status = ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_EGS_STATS, stats_statsid_eg.stats_id);
                if (CTC_E_NONE != status)
                {
                    goto error4;
                }
                else
                {
                    p_rif_info->egs_statsid = stats_statsid_eg.stats_id;
                }
            }

        }
        else if(!(p_rif_info->stats_state) && p_rif_info->ing_statsid && p_rif_info->egs_statsid)
        {
            ctcs_stats_destroy_statsid(lchip, p_rif_info->ing_statsid);
            ctcs_stats_destroy_statsid(lchip, p_rif_info->egs_statsid);
            ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_STATS, 0);
            ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_EGS_STATS, 0);
            p_rif_info->ing_statsid = 0;
            p_rif_info->ing_statsid = 0;
        }
    }
    else
    {
        l3if_id = p_rif_info->actual_l3if_id;
    }

    sal_memset(&router_mac, 0, sizeof(router_mac));
    router_mac.num = 1;
    if(p_rif_info->is_virtual && !(CTC_CHIP_GOLDENGATE== ctcs_get_chip_type(lchip)))
    {
        router_mac.dir = CTC_INGRESS;
        router_mac.mode = CTC_L3IF_APPEND_ROUTE_MAC;
        sal_memcpy(router_mac.mac[0], p_rif_info->src_mac, sizeof(sai_mac_t));
    }
    else if(p_rif_info->is_virtual)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_interface_router_mac(lchip, l3if_id, &router_mac));
        sal_memcpy(router_mac.mac[router_mac.num], p_rif_info->src_mac, sizeof(sai_mac_t));
        router_mac.num += 1;
    }
    else
    {
        sai_object_id_t vr_obj_id;
        ctc_sai_virtual_router_t* p_vr_info = NULL;
        vr_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, p_rif_info->vrf_id);
        p_vr_info = ctc_sai_db_get_object_property(lchip, vr_obj_id);
        if (NULL == p_rif_info)
        {
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        //mac_addr_t mac;
        //sal_memset(mac, 0, sizeof(mac_addr_t));
        //CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_router_mac(lchip, mac));

        if(sal_memcmp(p_vr_info->src_mac, p_rif_info->src_mac, sizeof(sai_mac_t))) 
        {
            //CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_interface_router_mac(lchip, l3if_id, &router_mac));

            router_mac.dir = CTC_INGRESS;
            router_mac.mode = CTC_L3IF_UPDATE_ROUTE_MAC;
            sal_memcpy(router_mac.mac[0], p_vr_info->src_mac, sizeof(sai_mac_t));
            sal_memcpy(router_mac.mac[1], p_rif_info->src_mac, sizeof(sai_mac_t));
            router_mac.num = 2;
            need_update_egr_mac = 1;
        }
        else
        {
            router_mac.dir = CTC_INGRESS;
            router_mac.mode = CTC_L3IF_UPDATE_ROUTE_MAC;
            sal_memcpy(router_mac.mac[0], p_rif_info->src_mac, sizeof(sai_mac_t));
            router_mac.num = 1;
            need_update_egr_mac = 1;
        }

    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_interface_router_mac(lchip, l3if_id, router_mac));

    /* update egress mac use interface mac */
    if(need_update_egr_mac)
    {
        sal_memset(&router_mac, 0, sizeof(router_mac));
        router_mac.num = 1;
        router_mac.dir = CTC_EGRESS;
        router_mac.mode = CTC_L3IF_UPDATE_ROUTE_MAC;
        sal_memcpy(router_mac.mac[0], p_rif_info->src_mac, sizeof(sai_mac_t));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_interface_router_mac(lchip, l3if_id, router_mac));
    }

    return SAI_STATUS_SUCCESS;
    error4:
        ctcs_stats_destroy_statsid(lchip, p_rif_info->egs_statsid);
    error3:
        p_rif_info->ing_statsid = 0;
        ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_STATS, 0);
    error2:
        ctcs_stats_destroy_statsid(lchip, p_rif_info->ing_statsid);
    error1:
        return SAI_STATUS_INSUFFICIENT_RESOURCES;
}

static sai_status_t
_ctc_sai_router_interface_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    bool enable = FALSE;
    ctc_object_id_t ctc_oid;
    ctc_object_id_t ctc_oid1;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, key->key.object_id, &ctc_oid1);

    switch (attr->id)
    {
    case SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
        {
            uint16 ctc_vrf_id = 0;
            ctc_sai_oid_get_vrf_id(attr->value.oid, &ctc_vrf_id);
            p_rif_info->vrf_id = ctc_vrf_id;
        }
        break;
    case SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
        sal_memcpy(p_rif_info->src_mac, attr->value.mac, sizeof(sai_mac_t));
        break;
    case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->v4_state = (attr->value.booldata)? 1:0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->v6_state = (attr->value.booldata)? 1:0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_MTU:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->mtu = attr->value.u32;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->neighbor_miss_action = attr->value.s32;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->v4_mc_state = (attr->value.booldata)? 1:0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->v6_mc_state = (attr->value.booldata)? 1:0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        p_rif_info->stats_state = (attr->value.booldata)? 1:0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID:
        if(attr->value.u8 >= CTC_SAI_RIF_NAT_ZONE_MAX)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        else if(attr->value.u8 == CTC_SAI_RIF_NAT_ZONE_EXTERNAL)
        {
            p_rif_info->snat_en = 0;
            p_rif_info->nat_iftype = 0;
        }
        else /* CTC_SAI_RIF_NAT_ZONE_INTERNAL */
        {
            p_rif_info->snat_en = 1;
            p_rif_info->nat_iftype = 1;
        }
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:

        if (SAI_NULL_OBJECT_ID != attr->value.oid)
        {
            enable = TRUE;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, attr->value.oid, &ctc_oid);

        if (enable)
        {
            if (ctc_oid.value == p_rif_info->dscp_to_tc_map_id)
            {
                return SAI_STATUS_SUCCESS;
            }
            else if (p_rif_info->dscp_to_tc_map_id)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE,"[DSCP_TO_TC_MAP] Already exsit! map_id:%d", p_rif_info->dscp_to_tc_map_id);
                return SAI_STATUS_FAILURE;
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                            enable ? ctc_oid.value : p_rif_info->dscp_to_tc_map_id,
                                            SAI_QOS_MAP_TYPE_DSCP_TO_TC, enable));
        p_rif_info->dscp_to_tc_map_id = enable ? ctc_oid.value : 0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:

        if (SAI_NULL_OBJECT_ID != attr->value.oid)
        {
            enable = TRUE;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, attr->value.oid, &ctc_oid);

        if (enable)
        {
            if (ctc_oid.value == p_rif_info->dscp_to_color_map_id)
            {
                return SAI_STATUS_SUCCESS;
            }
            else if (p_rif_info->dscp_to_color_map_id)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE,"[DSCP_TO_COLOR_MAP] Already exsit! map_id:%d", p_rif_info->dscp_to_color_map_id);
                return SAI_STATUS_FAILURE;
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                            enable ? ctc_oid.value : p_rif_info->dscp_to_color_map_id,
                                            SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, enable));
        p_rif_info->dscp_to_color_map_id = enable ? ctc_oid.value : 0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:

        if (SAI_NULL_OBJECT_ID != attr->value.oid)
        {
            enable = TRUE;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, attr->value.oid, &ctc_oid);

        if (enable)
        {
            if (ctc_oid.value == p_rif_info->tc_color_to_dscp_map_id)
            {
                return SAI_STATUS_SUCCESS;
            }
            else if (p_rif_info->tc_color_to_dscp_map_id)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE,"[TC_AND_COLOR_TO_DSCP_MAP] Already exsit! map_id:%d", p_rif_info->tc_color_to_dscp_map_id);
                return SAI_STATUS_FAILURE;
            }
        }
        CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_port_set_map(key->key.object_id,
                                            enable ? ctc_oid.value : p_rif_info->tc_color_to_dscp_map_id,
                                            SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, enable));
        p_rif_info->tc_color_to_dscp_map_id = enable ? ctc_oid.value : 0;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
        ctcs_l3if_set_property(lchip, ctc_oid1.value, CTC_L3IF_PROP_DSCP_SELECT_MODE, attr->value.booldata ? CTC_DSCP_SELECT_MAP : CTC_DSCP_SELECT_NONE);
        break;
    default:
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint32 value = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t* p_bounded_oid = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, key->key.object_id, &ctc_object_id);

    switch (attr->id)
    {
    case SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, lchip, 0, 0, p_rif_info->vrf_id);
        break;
    case SAI_ROUTER_INTERFACE_ATTR_TYPE:
        attr->value.s32 = ctc_object_id.sub_type;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_PORT_ID:
        if (CTC_IS_LINKAGG_PORT(p_rif_info->gport))
        {
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport);
        }
        else
        {
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, p_rif_info->gport);
        }
        break;
    case SAI_ROUTER_INTERFACE_ATTR_VLAN_ID:
        attr->value.oid = p_rif_info->vlan_oid;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID:
        attr->value.u16 = p_rif_info->outer_vlan_id;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
        sal_memcpy(attr->value.mac, p_rif_info->src_mac, sizeof(sai_mac_t));
        break;
    case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.booldata = p_rif_info->v4_state;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.booldata = p_rif_info->v6_state;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_MTU:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.u32 = p_rif_info->mtu;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;
    case SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;
    case SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.s32 = p_rif_info->neighbor_miss_action;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.booldata = p_rif_info->v4_mc_state;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.booldata = p_rif_info->v6_mc_state;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
        if(p_rif_info->is_virtual)
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        attr->value.booldata = p_rif_info->stats_state;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID:
        attr->value.oid = p_rif_info->dot1d_bridge_id;
    case SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL:
        attr->value.booldata = p_rif_info->is_virtual;
    case SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID:
        if(p_rif_info->snat_en)
        {
            attr->value.u8 = p_rif_info->nat_iftype;
        }
        else
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
        value = p_rif_info->dscp_to_tc_map_id;
        attr->value.oid = value ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, value) : SAI_NULL_OBJECT_ID;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
        value = p_rif_info->dscp_to_color_map_id;
        attr->value.oid = value ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, value) : SAI_NULL_OBJECT_ID;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
        value = p_rif_info->tc_color_to_dscp_map_id;
        attr->value.oid = value ? ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, value) : SAI_NULL_OBJECT_ID;
        break;
    case SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
        ctcs_l3if_get_property(lchip, ctc_object_id.value, CTC_L3IF_PROP_DSCP_SELECT_MODE, &value);
        attr->value.booldata = (bool)value;
        break;
    default:
        return SAI_STATUS_NOT_SUPPORTED;
        break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_traverse_set_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_rif_traverse_param_t* user_data)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_router_interface_t* p_rif_info = bucket_data->data;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, bucket_data->oid, &ctc_object_id);


    if ((CTC_SAI_RIF_SET_TYPE_PORT == user_data->set_type)
        &&((SAI_ROUTER_INTERFACE_TYPE_PORT == ctc_object_id.sub_type)||(SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type)
        ||(SAI_ROUTER_INTERFACE_TYPE_VLAN == ctc_object_id.sub_type)))
    {
        if (p_rif_info->gport != *(user_data->cmp_value))
        {
            return SAI_STATUS_SUCCESS;
        }
    }
    else if (CTC_SAI_RIF_SET_TYPE_VRF == user_data->set_type)
    {
        if (p_rif_info->vrf_id != *(user_data->cmp_value))
        {
            return SAI_STATUS_SUCCESS;
        }
    }
    else
    {
        return SAI_STATUS_SUCCESS;
    }


    if (CTC_L3IF_PROP_ROUTE_MAC_LOW_8BITS == user_data->l3if_prop)
    {
        ctc_l3if_router_mac_t router_mac;
        sal_memset(&router_mac, 0, sizeof(ctc_l3if_router_mac_t));

        if(p_rif_info->is_virtual) /* virtual l3if do not update */
        {
            return SAI_STATUS_SUCCESS;
        }
        
        /*switch src mac(default vrf mac) share with dedicate vrf mac, use router_mac.mac[0] to set */
        
        //router_mac.dir = CTC_INGRESS;
        //CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_get_interface_router_mac(user_data->lchip, ctc_object_id.value, &router_mac));

        router_mac.dir = CTC_INGRESS;
        router_mac.mode = CTC_L3IF_UPDATE_ROUTE_MAC;
        router_mac.num = 2;
        sal_memcpy(router_mac.mac[0], user_data->p_value, sizeof(sai_mac_t));
        sal_memcpy(router_mac.mac[1], p_rif_info->src_mac, sizeof(sai_mac_t));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_interface_router_mac(user_data->lchip, ctc_object_id.value, router_mac));

        /*update egress mac with rif mac */
        sal_memset(&router_mac, 0, sizeof(router_mac));
        router_mac.num = 1;
        router_mac.dir = CTC_EGRESS;
        router_mac.mode = CTC_L3IF_UPDATE_ROUTE_MAC;
        sal_memcpy(router_mac.mac[0], p_rif_info->src_mac, sizeof(sai_mac_t));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_interface_router_mac(user_data->lchip, ctc_object_id.value, router_mac));
            
        

    }
    else if (CTC_L3IF_PROP_IPV4_UCAST == user_data->l3if_prop)
    {
        p_rif_info->v4_state = *(uint32*)(user_data->p_value);
        ctcs_l3if_set_property(user_data->lchip, ctc_object_id.value, user_data->l3if_prop, *(uint32*)(user_data->p_value));
    }
    else if (CTC_L3IF_PROP_IPV6_UCAST == user_data->l3if_prop)
    {
        p_rif_info->v6_state = *(uint32*)(user_data->p_value);
        ctcs_l3if_set_property(user_data->lchip, ctc_object_id.value, user_data->l3if_prop, *(uint32*)(user_data->p_value));
    }
    else
    {
        ctcs_l3if_set_property(user_data->lchip, ctc_object_id.value, user_data->l3if_prop, *(uint32*)(user_data->p_value));
    }
    return SAI_STATUS_SUCCESS;
}

static int32
_ctc_sai_router_interface_traverse_get_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_rif_traverse_param_t* user_data)
{
    int32 ret = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_router_interface_t* p_rif_info = bucket_data->data;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, bucket_data->oid, &ctc_object_id);

    if ((CTC_SAI_RIF_SET_TYPE_PORT == user_data->set_type)
        &&((SAI_ROUTER_INTERFACE_TYPE_PORT == ctc_object_id.sub_type)||(SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type)))
    {
        *(uint32*)(user_data->p_value) = 0;
        if (p_rif_info->gport != *(user_data->cmp_value))
        {
            return 0;
        }
        ret = ctcs_l3if_get_property(user_data->lchip, ctc_object_id.value, user_data->l3if_prop, (uint32*)(user_data->p_value));
        if (ret == 0)
        {
            return -1;
        }
    }

    return 0;
}

static sai_status_t
_ctc_sai_router_interface_traverse_lkp_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_rif_lkp_param_t* user_data)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_router_interface_t* p_rif_info = bucket_data->data;
    uint16 vlan_id = 0;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, bucket_data->oid, &ctc_object_id);


    if (p_rif_info->vlan_oid)
    {
        ctc_sai_vlan_get_vlan_id(p_rif_info->vlan_oid, &vlan_id);
    }
    else if(p_rif_info->outer_vlan_id)
    {
        vlan_id = p_rif_info->outer_vlan_id;
    }

    if ((ctc_object_id.sub_type == user_data->type)
        && (p_rif_info->gport == user_data->gport)
        && (vlan_id == user_data->vlan))
    {
        user_data->router_interface_id = bucket_data->oid;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_set_domain(uint8 lchip, uint32 gport, uint32 l3if_id)
{
    uint32 value = 0;
    uint32 ctc_domain = 0;
    /*ingress*/
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_QOS_POLICY, &value));
    if (value == CTC_QOS_TRUST_DSCP)
    {
        value = 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_TRUST_DSCP, value));
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_direction_property(lchip, gport, CTC_PORT_DIR_PROP_QOS_DSCP_DOMAIN, CTC_INGRESS, &ctc_domain));
    if (ctc_domain)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_IGS_QOS_DSCP_DOMAIN, ctc_domain));
    }

    /*egress*/
    value = 0;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_property(lchip, gport, CTC_PORT_PROP_REPLACE_DSCP_EN, &value));
    if (value)
    {
        value = CTC_DSCP_SELECT_MAP;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_DSCP_SELECT_MODE, value));
    }
    ctc_domain= 0;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_direction_property(lchip, gport, CTC_PORT_DIR_PROP_QOS_DSCP_DOMAIN, CTC_EGRESS, &ctc_domain));
    if (ctc_domain)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_EGS_QOS_DSCP_DOMAIN, ctc_domain));
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    ctc_sai_router_interface_t*    p_rif_info = (ctc_sai_router_interface_t*)(bucket_data->data);
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    ctc_object_id_t ctc_object_id;
    uint32 num_cnt = 0;
    char state[8]       = {0};
    char rif_oid[64] = {'-'};
    char vlan_oid[64] = {'-'};
    char outer_vlan_id[16] = {'-'};
    char gport[64] = {'-'};
    char bridge_id[64] = {'-'};
    char src_mac[64] = {0};

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (bucket_data->oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }
    sal_sprintf(rif_oid, "0x%016"PRIx64, bucket_data->oid);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, bucket_data->oid, &ctc_object_id);
    if ((SAI_ROUTER_INTERFACE_TYPE_PORT == ctc_object_id.sub_type)
        || (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type)
        || (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type))
    {
        sal_sprintf(gport, "0x%04x", p_rif_info->gport);
    }
    if ((SAI_ROUTER_INTERFACE_TYPE_VLAN == ctc_object_id.sub_type)
        || (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type))
    {
        sal_sprintf(vlan_oid, "0x%016"PRIx64, p_rif_info->vlan_oid);
    }
    if (SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type)
    {
        sal_sprintf(outer_vlan_id, "%d", p_rif_info->outer_vlan_id);
    }
    if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type)
    {
        sal_sprintf(bridge_id, "%d", p_rif_info->bridge_id);
    }
    sal_strcat(state, p_rif_info->v4_state? "1" : "0");
    sal_strcat(state, p_rif_info->v6_state? "1" : "0");
    sal_strcat(state, p_rif_info->v4_mc_state? "1" : "0");
    sal_strcat(state, p_rif_info->v6_mc_state? "1" : "0");
    ctc_sai_get_mac_str(p_rif_info->src_mac, src_mac);
    CTC_SAI_LOG_DUMP(p_file, "%-8d%-20s%-20s%-12s%-10d%-12s%-10s%-10d%-20s\n0x%-13x0x%-13x\n",
           num_cnt, rif_oid, vlan_oid, gport, p_rif_info->vrf_id, bridge_id, state, p_rif_info->mtu, src_mac, p_rif_info->ing_statsid, p_rif_info->egs_statsid);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t rif_attr_fn_entries[] = {
    { SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_TYPE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_PORT_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_VLAN_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_INNER_VLAN_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_MTU,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL,
      _ctc_sai_router_interface_get_attr,
      ctc_sai_acl_bind_point_set},
    { SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL,
      _ctc_sai_router_interface_get_attr,
      ctc_sai_acl_bind_point_set},
    { SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID,
      _ctc_sai_router_interface_get_attr,
      NULL},
    { SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL,
      _ctc_sai_router_interface_get_attr,
      NULL},
    { SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    { SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP,
      _ctc_sai_router_interface_get_attr,
      _ctc_sai_router_interface_set_attr},
    {CTC_SAI_FUNC_ATTR_END_ID,NULL,NULL}
};

#define ________INTERNAL_API________
sai_status_t
ctc_sai_router_interface_get_rif_info(sai_object_id_t router_interface_id, uint8* type,
                                                 uint16* vrf_id,  uint32* gport, uint16* vlan)
{
    uint8 lchip = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_oid_get_lchip(router_interface_id, &lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, router_interface_id, &ctc_object_id);
    if (type)
    {
        *type = ctc_object_id.sub_type;
    }
    if (vrf_id)
    {
        *vrf_id = p_rif_info->vrf_id;
    }
    if (gport)
    {
        *gport = p_rif_info->gport;
    }
    if (vlan)
    {
        *vlan = 0;
        if ((p_rif_info->vlan_oid)&&(SAI_ROUTER_INTERFACE_TYPE_VLAN == ctc_object_id.sub_type))
        {
            ctc_sai_vlan_get_vlan_id(p_rif_info->vlan_oid, vlan);
        }
        else if ((p_rif_info->outer_vlan_id)&&(SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type))
        {
            *vlan = p_rif_info->outer_vlan_id;
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_router_interface_get_vlan_ptr(sai_object_id_t router_interface_id, uint16* vlan_ptr)
{
    uint16 tmp_vlan_ptr = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_router_interface_t* p_rif_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, router_interface_id, &ctc_object_id);
    p_rif_info = ctc_sai_db_get_object_property(ctc_object_id.lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if ((0 == p_rif_info->vlan_oid) && (0 == p_rif_info->bridge_id))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    if (SAI_ROUTER_INTERFACE_TYPE_VLAN == ctc_object_id.sub_type)
    {
        ctc_sai_oid_get_vlanptr(p_rif_info->vlan_oid, &tmp_vlan_ptr);
    }
    else if (SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type)
    {
        tmp_vlan_ptr = p_rif_info->bridge_id;
    }

    if (vlan_ptr)
    {
        *vlan_ptr = tmp_vlan_ptr;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_router_interface_get_src_mac(sai_object_id_t router_interface_id, sai_mac_t src_mac)
{
    uint8 lchip = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_sai_oid_get_lchip(router_interface_id, &lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memcpy(src_mac, p_rif_info->src_mac, sizeof(sai_mac_t));
    return SAI_STATUS_SUCCESS;
}


sai_status_t
ctc_sai_router_interface_lookup_rif_oid(uint8 lchip, uint8 type, uint32 gport, uint16 vlan, sai_object_id_t* router_interface_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_rif_lkp_param_t lkp_param;
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_PTR_VALID_CHECK(router_interface_id);


    sal_memset(&lkp_param, 0, sizeof(lkp_param));
    lkp_param.lchip = lchip;
    lkp_param.type = type;
    lkp_param.gport = gport;
    lkp_param.vlan = vlan;
    status = ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ROUTER_INTERFACE,
                          (hash_traversal_fn)_ctc_sai_router_interface_traverse_lkp_cb, &lkp_param);
    if ((status == SAI_STATUS_SUCCESS) && lkp_param.router_interface_id)
    {
        *router_interface_id = lkp_param.router_interface_id;
        return SAI_STATUS_SUCCESS;
    }
    else
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

}

sai_status_t
ctc_sai_router_interface_get_miss_action(sai_object_id_t router_interface_id, sai_packet_action_t* action)
{
    uint8 lchip = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    ctc_sai_oid_get_lchip(router_interface_id, &lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (action)
    {
        *action = p_rif_info->neighbor_miss_action;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_router_interface_traverse_set(ctc_sai_rif_traverse_param_t* traverse_param)
{
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_PTR_VALID_CHECK(traverse_param);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->cmp_value);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->p_value);
    ctc_sai_db_traverse_object_property(traverse_param->lchip, SAI_OBJECT_TYPE_ROUTER_INTERFACE, (hash_traversal_fn)_ctc_sai_router_interface_traverse_set_cb, traverse_param);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_router_interface_get_param(ctc_sai_rif_traverse_param_t* traverse_param)
{
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_PTR_VALID_CHECK(traverse_param);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->cmp_value);
    CTC_SAI_PTR_VALID_CHECK(traverse_param->p_value);
    ctc_sai_db_traverse_object_property(traverse_param->lchip, SAI_OBJECT_TYPE_ROUTER_INTERFACE, (hash_traversal_fn)_ctc_sai_router_interface_traverse_get_cb, traverse_param);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_router_interface_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_id_t router_interface_id = *(sai_object_id_t*)key;
    ctc_object_id_t ctc_object_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP_GROUP, router_interface_id, &ctc_object_id);

    if(( SAI_ROUTER_INTERFACE_TYPE_PORT == ctc_object_id.sub_type) || ( SAI_ROUTER_INTERFACE_TYPE_VLAN == ctc_object_id.sub_type)
        || ( SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == ctc_object_id.sub_type) || ( SAI_ROUTER_INTERFACE_TYPE_BRIDGE == ctc_object_id.sub_type))
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, ctc_object_id.value));
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_VIF, ctc_object_id.value));
    }

    return status;
}

sai_status_t
ctc_sai_router_interface_update_bridge_rif(uint8 lchip, uint16 l3if_id, uint16 vlan_id, bool is_add)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_l3if_t l3if;
    sai_object_id_t router_interface_id;

    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    router_interface_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, l3if_id);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
    l3if.vlan_id = vlan_id;
    if (is_add)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l3if_create(lchip, l3if_id, &l3if));
        CTC_SAI_ERROR_GOTO(_ctc_sai_router_interface_set_attr_hw(router_interface_id), status, error1);
        p_rif_info->bridge_id = vlan_id;
    }
    else
    {
        CTC_SAI_ERROR_RETURN(ctcs_l3if_destory(lchip, l3if_id, &l3if));
        p_rif_info->bridge_id = 0;
    }

    return SAI_STATUS_SUCCESS;
error1:
    ctcs_l3if_destory(lchip, l3if_id, &l3if);
    return status;
}

void ctc_sai_router_interface_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Router Interface MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_ROUTER_INTERFACE))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Router Interface");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_router_interface_t(state bitmap from left to right: v4, v6, v4_mc, v6_mc)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-8s%-20s%-20s%-12s%-10s%-12s%-10s%-10s%-20s\n%-15s%-20s\n", "No.", "router_interface_id", "vlan_oid","gport", "vrf_id", "bridge_id", "state", "mtu", "src_mac", "ing_statsid", "egs_statsid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_ROUTER_INTERFACE,
                                            (hash_traversal_fn)_ctc_sai_router_interface_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
static sai_status_t
ctc_sai_router_interface_get_stats(sai_object_id_t router_interface_id, uint32_t number_of_counters,
const sai_stat_id_t *counter_ids, uint64_t *counters)
{
    uint8 lchip = 0;
    uint8 index = 0;
    uint8 not_support = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "Failed to get route interface, invalid router_interface_id %d!\n", router_interface_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    sal_memset(&stats_igs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->ing_statsid, &stats_igs), status, out);
    sal_memset(&stats_egs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->egs_statsid, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if (0 != p_rif_info->ing_statsid && (SAI_ROUTER_INTERFACE_STAT_IN_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_IN_PACKETS == counter_ids[index]))
        {
            if (SAI_ROUTER_INTERFACE_STAT_IN_PACKETS == counter_ids[index])
            {
                counters[index] = stats_igs.packet_count - p_rif_info->igs_packet_count;
            }
            else
            {
                counters[index] = stats_igs.byte_count - p_rif_info->igs_byte_count;
            }
            continue;
        }

        if (0 != p_rif_info->egs_statsid && (SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS == counter_ids[index]))
        {
            if (SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS == counter_ids[index])
            {
                counters[index] = stats_egs.packet_count - p_rif_info->egs_packet_count;
            }
            else
            {
                counters[index] = stats_egs.byte_count - p_rif_info->egs_byte_count;
            }
            continue;
        }

        not_support = TRUE;
    }

    if ( TRUE == not_support)
    {
        status = SAI_STATUS_NOT_SUPPORTED ;
    }
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_get_stats_ext(sai_object_id_t router_interface_id, uint32_t number_of_counters,
const sai_stat_id_t *counter_ids, sai_stats_mode_t mode, uint64_t *counters)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;
    uint32 index = 0;
    uint32 not_support = 0;
    uint8 clear_ing = 0;
    uint8 clear_egs = 0;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "Failed to get route interface, invalid router_interface_id %d!\n", router_interface_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    sal_memset(&stats_igs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->ing_statsid, &stats_igs), status, out);
    sal_memset(&stats_egs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->egs_statsid, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if (0 != p_rif_info->ing_statsid && (SAI_ROUTER_INTERFACE_STAT_IN_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_IN_PACKETS == counter_ids[index]))
        {
            clear_ing = 1;
            if (SAI_ROUTER_INTERFACE_STAT_IN_PACKETS == counter_ids[index])
            {
                counters[index] = stats_igs.packet_count - p_rif_info->igs_packet_count;
            }
            else
            {
                counters[index] = stats_igs.byte_count - p_rif_info->igs_byte_count;
            }
            continue;
        }

        if (0 != p_rif_info->egs_statsid && (SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS == counter_ids[index]))
        {
            clear_egs = 1;
            if (SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS == counter_ids[index])
            {
                counters[index] = stats_egs.packet_count - p_rif_info->egs_packet_count;
            }
            else
            {
                counters[index] = stats_egs.byte_count - p_rif_info->egs_byte_count;
            }
            continue;
        }

        not_support = TRUE;
    }
    if (SAI_STATS_MODE_READ_AND_CLEAR == mode && clear_ing)
    {
        p_rif_info->igs_packet_count = stats_igs.packet_count;
        p_rif_info->igs_byte_count = stats_igs.byte_count;
    }
    if (SAI_STATS_MODE_READ_AND_CLEAR == mode && clear_egs)
    {
        p_rif_info->egs_packet_count = stats_egs.packet_count;
        p_rif_info->egs_byte_count = stats_egs.byte_count;
    }

    if ( TRUE == not_support)
    {
        status = SAI_STATUS_NOT_SUPPORTED ;
    }


    CTC_SAI_DB_UNLOCK(lchip);
    return status;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_clear_stats(sai_object_id_t router_interface_id, uint32_t number_of_counters,
const sai_stat_id_t *counter_ids)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    uint32 index = 0;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "Failed to get route interface, invalid router_interface_id %d!\n", router_interface_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    sal_memset(&stats_igs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->ing_statsid, &stats_igs), status, out);
    sal_memset(&stats_egs, 0, sizeof(ctc_stats_basic_t));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_rif_info->egs_statsid, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index++)
    {
        if (SAI_ROUTER_INTERFACE_STAT_IN_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_IN_PACKETS == counter_ids[index] )
        {
            if (0 != p_rif_info->ing_statsid)
            {
                p_rif_info->igs_packet_count = stats_igs.packet_count;
                p_rif_info->igs_byte_count = stats_igs.byte_count;
            }
        }

        if (SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS == counter_ids[index] || SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS == counter_ids[index] )
        {
            if (0 != p_rif_info->egs_statsid)
            {
                p_rif_info->egs_packet_count = stats_egs.packet_count;
                p_rif_info->egs_byte_count = stats_egs.byte_count;
            }
        }
    }

    CTC_SAI_DB_UNLOCK(lchip);
    return status;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_create_rif(sai_object_id_t *router_interface_id, sai_object_id_t switch_id,
                                                          uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 l3if_id = 0;
    uint16 actual_l3if_id = 0;
    sai_object_id_t rif_obj_id = 0;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    const sai_attribute_value_t *attr_value;
    uint32_t index = 0;
    uint8          loop = 0;
    sai_object_key_t key;
    ctc_l3if_t l3if;
    sai_mac_t src_mac = {0};
    uint8 v4_state = 0;
    uint8 v6_state = 0;
    uint8 port_valid = 0;
    uint32 gports[128] = {0};
    uint16 agg_member_cnt = 0;
    uint8 is_1d_bridge = 0;/*for 1d bridge, create hw l3if by bridge port*/
    uint16 vlan_ptr = 0;
    int32 sub_type = 0;
    uint32 stats_status = 1;
    ctc_stats_statsid_t stats_statsid_in;
    ctc_stats_statsid_t stats_statsid_eg;
    sai_object_id_t dot1d_bridge_id = 0;
    ctc_l3if_router_mac_t router_mac;
    uint32_t vifbypass = 0;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t port_oid;
    ctc_sai_port_db_t* p_port_db = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_PTR_VALID_CHECK(router_interface_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_ERROR_RETURN(_ctc_sai_router_interface_create_attr_check(lchip, attr_count, attr_list));

    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    sal_memset(&stats_statsid_in, 0, sizeof(stats_statsid_in));
    sal_memset(&stats_statsid_eg, 0, sizeof(stats_statsid_eg));
    sal_memset(&router_mac, 0, sizeof(ctc_l3if_router_mac_t));
#if 0/*SYSTEM MODIFIED by xgu, bug 51934,  2019/12/12*/
    l3if.l3if_type = MAX_L3IF_TYPE_NUM;
    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, out);
    CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_TYPE, &attr_value, &index), status, out);
    if (SAI_ROUTER_INTERFACE_TYPE_VLAN == attr_value->s32)
    {
        l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
    }
    else if (SAI_ROUTER_INTERFACE_TYPE_PORT == attr_value->s32)
    {
        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
    }
    else if ((SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == attr_value->s32))
    {
        l3if.l3if_type = CTC_L3IF_TYPE_SUB_IF;
    }
    else if((SAI_ROUTER_INTERFACE_TYPE_BRIDGE == attr_value->s32))
    {
        l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
        is_1d_bridge = 1;
    }
#else
    l3if.l3if_type = MAX_L3IF_TYPE_NUM;
    CTC_SAI_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_TYPE, &attr_value, &index), status, out);
    switch(attr_value->s32)
    {
        case SAI_ROUTER_INTERFACE_TYPE_VLAN:
            l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, out);
            break;
        case SAI_ROUTER_INTERFACE_TYPE_PORT:
            l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, out);
            break;
        case SAI_ROUTER_INTERFACE_TYPE_SUB_PORT:
            l3if.l3if_type = CTC_L3IF_TYPE_SUB_IF;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, out);
            break;
        case SAI_ROUTER_INTERFACE_TYPE_BRIDGE:
            l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
            is_1d_bridge = 1;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, &l3if_id), status, out);
            break;
        case SAI_ROUTER_INTERFACE_TYPE_LOOPBACK:
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VIF, &l3if_id), status, out);
            vifbypass = 1;
            break;
        case SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER:
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VIF, &l3if_id), status, out);
            vifbypass = 1;
            break;
        case SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT:
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VIF, &l3if_id), status, out);
            vifbypass = 1;
            break;
        default:
            CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "Ignore l3if create for type of  = 0x%"PRIx64"\n", attr_value->s32);
            goto out;
            break;
    }
#endif

    sub_type = attr_value->s32;
    rif_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, lchip, sub_type, 0, l3if_id);
    CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "create router_interface_id = 0x%"PRIx64"\n", rif_obj_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_router_interface_build_db(lchip, rif_obj_id, &p_rif_info), status, error1);
    CTC_SAI_LOG_NOTICE(SAI_API_ROUTER_INTERFACE, "create router_interface_id func. type=0x%"PRIx64", %u, rif_obj_id=0x%"PRIx64", vifbypass:%u, status:%u\n",
                                                attr_value->s32, l3if_id, rif_obj_id, vifbypass, status);

    /* SONiC not all route interface will have this attr */
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        dot1d_bridge_id = attr_value->oid;
    }
    else
    {
        dot1d_bridge_id = 0;
    }

    if(vifbypass)
    {
        *router_interface_id = rif_obj_id;
        p_rif_info->dot1d_bridge_id = dot1d_bridge_id;
        CTC_SAI_CTC_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID, &attr_value, &index), status, error6);
        if(!CTC_SAI_ERROR(status))
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VIRTUAL_ROUTER, attr_value->oid, &ctc_object_id);
            p_rif_info->vrf_id = ctc_object_id.value;
        }
        goto out;
    }

    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        if (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
        {
            status = SAI_STATUS_NOT_SUPPORTED;
            goto error2;
        }
        p_rif_info->is_virtual = attr_value->booldata;
    }
    else
    {
        p_rif_info->is_virtual = 0;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_VLAN_ID, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        if (SAI_ROUTER_INTERFACE_TYPE_VLAN == sub_type)
        {
            ctc_sai_vlan_get_vlan_id(attr_value->oid, &l3if.vlan_id);
            p_rif_info->vlan_oid = attr_value->oid;
        }
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        if ((SAI_ROUTER_INTERFACE_TYPE_SUB_PORT == sub_type)||(SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT == sub_type))
        {
            l3if.vlan_id = attr_value->u16;
            p_rif_info->outer_vlan_id = attr_value->u16;
        }
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_PORT_ID, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        ctc_sai_oid_get_gport(attr_value->oid, &l3if.gport);
        p_rif_info->gport = l3if.gport;
        port_valid = 1;
    }
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE, &attr_value, &index));
    if (!CTC_SAI_ERROR(status))
    {
        stats_status = attr_value->booldata;
    }
    if(p_rif_info->is_virtual)
    {
        CTC_SAI_ERROR_GOTO(ctcs_l3if_get_l3if_id(lchip, &l3if, &actual_l3if_id), status, error2);
        CTC_SAI_ERROR_GOTO(ctcs_l3if_get_interface_router_mac(lchip, actual_l3if_id, &router_mac), status, error2);
        if (((CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip)) || (CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip))) && router_mac.num >= 4)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_NO_MEMORY;
        }
        else if (((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) || (CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))) && router_mac.num >= 8)
        {
            CTC_SAI_DB_UNLOCK(lchip);
            return SAI_STATUS_NO_MEMORY;
        }
        p_rif_info->actual_l3if_id = actual_l3if_id;
    }

    p_rif_info->dot1d_bridge_id = dot1d_bridge_id;

    if (!is_1d_bridge && (MAX_L3IF_TYPE_NUM != l3if.l3if_type) && !p_rif_info->is_virtual)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_l3if_create(lchip, l3if_id, &l3if), status, error2);
    }
    if (!is_1d_bridge && !p_rif_info->is_virtual)
    {
        stats_statsid_in.dir = CTC_INGRESS;
        stats_statsid_in.type = CTC_STATS_STATSID_TYPE_L3IF;
        if(!stats_status)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "router interface stats  is disable\n");
            stats_statsid_in.stats_id = 0;/*0 means invalid*/
            p_rif_info->ing_statsid = 0;

        }
        else
        {
            status = ctcs_stats_create_statsid(lchip, &stats_statsid_in);
            if (CTC_E_NONE != status)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "stats ingress no resource\n");
                status = SAI_STATUS_INSUFFICIENT_RESOURCES;
                goto error3;
            }
            else
            {
                status = ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_STATS, stats_statsid_in.stats_id);
                if (CTC_E_NONE != status)
                {
                    p_rif_info->ing_statsid = 0;
                }
                else
                {
                    p_rif_info->ing_statsid = stats_statsid_in.stats_id;
                }

            }
        }

        stats_statsid_eg.dir = CTC_EGRESS;
        stats_statsid_eg.type = CTC_STATS_STATSID_TYPE_L3IF;
        if(!stats_status)
        {
            CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "router interface stats is disable\n");
            stats_statsid_eg.stats_id = 0;/*0 means invalid*/
            p_rif_info->egs_statsid = 0;

        }
        else
        {
            status = ctcs_stats_create_statsid(lchip, &stats_statsid_eg);
            if (CTC_E_NONE != status)
            {
                CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "stats egress no resource\n");
                status = SAI_STATUS_INSUFFICIENT_RESOURCES;
                goto error4;
            }
            else
            {
                status = ctcs_l3if_set_property(lchip, l3if_id, CTC_L3IF_PROP_EGS_STATS, stats_statsid_eg.stats_id);
                if (CTC_E_NONE != status)
                {
                    p_rif_info->egs_statsid = 0;
                }
                else
                {
                    p_rif_info->egs_statsid = stats_statsid_eg.stats_id;
                }
            }
        }
    }

    if (CTC_L3IF_TYPE_PHY_IF == l3if.l3if_type && !p_rif_info->is_virtual)
    {
        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_linkagg_get_member_ports(lchip, CTC_MAP_GPORT_TO_LPORT(l3if.gport), gports, &agg_member_cnt), status, error5);
            ctc_sai_lag_binding_rif(ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport), 1, l3if.l3if_type);
        }
        else
        {
            agg_member_cnt = 1;
            gports[0] = l3if.gport;
        }
        for (index = 0; index < agg_member_cnt; index++)
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_phy_if_en(lchip, gports[index], 1), status, error5);
            /* L3 pdu mcast route force bridge */
            ctcs_port_set_property(lchip, gports[index], CTC_PORT_PROP_BRIDGE_EN, TRUE);
        }

    }
    else if (CTC_L3IF_TYPE_SUB_IF == l3if.l3if_type && !p_rif_info->is_virtual)
    {
        ctc_port_scl_property_t port_scl_property;
        sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_PORT_SVLAN;

        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            CTC_SAI_CTC_ERROR_GOTO(ctcs_linkagg_get_member_ports(lchip, CTC_MAP_GPORT_TO_LPORT(l3if.gport), gports, &agg_member_cnt), status, error5);
            ctc_sai_lag_binding_rif(ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport), 1, l3if.l3if_type);
            for (index = 0; index < agg_member_cnt; index++)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_scl_property(lchip, gports[index], &port_scl_property), status, error5);
            }
        }
        else
        {
            port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, l3if.gport);
            CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(port_oid, &p_port_db));
            p_port_db->sub_if_ref_cnt++;
            if (1 == p_port_db->sub_if_ref_cnt)
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_port_set_scl_property(lchip, l3if.gport, &port_scl_property), status, error5);
            }
        }

    }

    sal_memset(&key, 0, sizeof(key));
    key.key.object_id = rif_obj_id;
    while (loop < attr_count)
    {
        if (SAI_ROUTER_INTERFACE_ATTR_BRIDGE_ID == (&attr_list[loop])->id ||
            SAI_ROUTER_INTERFACE_ATTR_IS_VIRTUAL == (&attr_list[loop])->id)
        {
            loop++ ;
            continue;
        }
        status = ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_ROUTER_INTERFACE,  rif_attr_fn_entries, &attr_list[loop]);
        if(CTC_SAI_ERROR(status))
        {
            CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "set attribute fail, loop = %d, id = %u\n", loop, (&attr_list[loop])->id);
            goto error6;
        }
        loop++ ;
    }

    /* default value*/
    CTC_SAI_CTC_ERROR_GOTO(ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID, &attr_value, &index), status, error6);
    CTC_SAI_CTC_ERROR_GOTO(ctc_sai_virtual_router_get_vr_info(attr_value->oid, &v4_state, &v6_state,  src_mac), status, error6);
    status = (ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, &attr_value, &index));
    if (SAI_STATUS_ITEM_NOT_FOUND == status)
    {
        CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "use SRC_MAC_ADDRESS on vr\n");
        sal_memcpy(p_rif_info->src_mac, src_mac, sizeof(sai_mac_t));
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_router_interface_set_attr_hw(rif_obj_id), status, error6);

    if (port_valid && (CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip)||CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip) || CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip)))
    {
        /*D2 need set l3if*/
        for (index = 0; index < agg_member_cnt; index++)
        {
            CTC_SAI_ERROR_GOTO(_ctc_sai_router_interface_set_domain(lchip, gports[index], l3if_id), status, error6);
        }
    }

    if (MAX_L3IF_TYPE_NUM != l3if.l3if_type || !p_rif_info->is_virtual)
    {
        if (CTC_L3IF_TYPE_VLAN_IF != l3if.l3if_type)
        {
            ctc_sai_hostif_l3if_en(lchip, p_rif_info->gport, true);
        }
        else if(SAI_ROUTER_INTERFACE_TYPE_BRIDGE != sub_type)
        {
            ctc_sai_oid_get_vlanptr(p_rif_info->vlan_oid, &vlan_ptr);
            ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_ARP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU);
            ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_DHCP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU);
        }
    }

    *router_interface_id = rif_obj_id;
    /*stats count init*/
    p_rif_info->igs_packet_count = 0;
    p_rif_info->igs_byte_count = 0;
    p_rif_info->egs_packet_count = 0;
    p_rif_info->egs_byte_count = 0;

    /*flush fdb*/
    if (CTC_L3IF_TYPE_PHY_IF == l3if.l3if_type)
    {
        ctc_object_id_t              ctc_bridge_port_id = {0};
        sai_object_id_t bridge_port_id;
        sai_attribute_t attr_list;
        ctc_bridge_port_id.lchip = lchip;
        ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
        ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
        ctc_bridge_port_id.value = p_rif_info->gport;
        ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, &bridge_port_id);
        attr_list.id = SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID;
        attr_list.value.oid = bridge_port_id;
        if (!p_rif_info->is_virtual)
        {
            ctc_sai_fdb_flush_fdb(switch_id, 1, &attr_list);
        }
    }

    goto out;

error6:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "rollback to error4\n");
    if (CTC_L3IF_TYPE_PHY_IF == l3if.l3if_type)
    {
        for (index = 0; index < agg_member_cnt; index++)
        {
            ctcs_port_set_phy_if_en(lchip, gports[index], 0);
        }
        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            ctc_sai_lag_binding_rif(ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport), 0, l3if.l3if_type);
        }
    }
    else if (CTC_L3IF_TYPE_SUB_IF == l3if.l3if_type)
    {
        ctc_port_scl_property_t port_scl_property;
        sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;
        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            for (index = 0; index < agg_member_cnt; index++)
            {
                ctcs_port_set_scl_property(lchip, gports[index], &port_scl_property);
            }
            ctc_sai_lag_binding_rif(ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport), 0, l3if.l3if_type);
        }
        else
        {
            p_port_db->sub_if_ref_cnt--;
            if (0 == p_port_db->sub_if_ref_cnt)
            {
                ctcs_port_set_scl_property(lchip, l3if.gport, &port_scl_property);
            }
        }
    }
error5:
    ctcs_stats_destroy_statsid(lchip, p_rif_info->egs_statsid);
error4:
    ctcs_stats_destroy_statsid(lchip, p_rif_info->ing_statsid);

error3:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "rollback to error3\n");
    if (!is_1d_bridge && (MAX_L3IF_TYPE_NUM != l3if.l3if_type) && !p_rif_info->is_virtual)
    {
        ctcs_l3if_destory(lchip, l3if_id, &l3if);
    }
error2:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "rollback to error2\n");
    _ctc_sai_router_interface_remove_db(lchip, rif_obj_id);
error1:
    CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_remove_rif(sai_object_id_t router_interface_id)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_router_interface_t* p_rif_info = NULL;
    uint16 l3if_id = 0;
    ctc_l3if_t l3if;
    ctc_object_id_t ctc_object_id;
    sai_object_id_t sai_lag_id;
    uint32 gports[128] = {0};
    uint16 agg_member_cnt = 0;
    uint8 index = 0;
    uint16 vlan_ptr = 0;
    uint8 exist = 0;
    uint32 number = 1;
    ctc_l3if_router_mac_t router_mac;
    ctc_sai_lag_info_t *p_db_lag = NULL;
    sai_object_id_t port_oid;
    ctc_sai_port_db_t* p_port_db = NULL;
    uint8 is_bridge_rif = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "router_interface_id = %llu\n", router_interface_id);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_ROUTER_INTERFACE, router_interface_id, &ctc_object_id);
    p_rif_info = ctc_sai_db_get_object_property(lchip, router_interface_id);
    if (NULL == p_rif_info)
    {
        CTC_SAI_LOG_ERROR(SAI_API_ROUTER_INTERFACE, "Failed to remove route interface, invalid router_interface_id %d!\n", router_interface_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    sal_memset(&l3if, 0, sizeof(ctc_l3if_t));
    l3if.l3if_type = MAX_L3IF_TYPE_NUM;
    ctc_sai_oid_get_l3if_id(router_interface_id, &l3if_id);
    switch(ctc_object_id.sub_type)
    {
         case SAI_ROUTER_INTERFACE_TYPE_VLAN:
        l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
             break;

         case SAI_ROUTER_INTERFACE_TYPE_PORT:
        l3if.l3if_type = CTC_L3IF_TYPE_PHY_IF;
             break;

         case SAI_ROUTER_INTERFACE_TYPE_SUB_PORT:
        l3if.l3if_type = CTC_L3IF_TYPE_SUB_IF;
             break;

         case SAI_ROUTER_INTERFACE_TYPE_BRIDGE:
             l3if.l3if_type = CTC_L3IF_TYPE_VLAN_IF;
             is_bridge_rif = 1;
        _ctc_sai_router_interface_check_hw_exist(router_interface_id, &exist);/*must remove by bridge port*/
        if (exist)
        {
            status = SAI_STATUS_ITEM_ALREADY_EXISTS;
            goto out;
        }
             break;

         case SAI_ROUTER_INTERFACE_TYPE_LOOPBACK:
         case SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER:
         case SAI_ROUTER_INTERFACE_TYPE_QINQ_PORT:
             ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VIF, l3if_id);
             _ctc_sai_router_interface_remove_db(lchip, router_interface_id);
             goto out;
             break;
         default:
             CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "Ignore l3if create for type of  = 0x%"PRIx64"\n", ctc_object_id.sub_type);
             goto out;
             break;
    }

    if (!p_rif_info->is_virtual)
    {
        if ((CTC_L3IF_TYPE_VLAN_IF != l3if.l3if_type) && (MAX_L3IF_TYPE_NUM != l3if.l3if_type))
        {
            ctc_sai_hostif_l3if_en(lchip, p_rif_info->gport, false);
        }
    }
    l3if.gport = p_rif_info->gport;
    if ((p_rif_info->vlan_oid)&&(SAI_ROUTER_INTERFACE_TYPE_VLAN ==ctc_object_id.sub_type))
    {
        ctc_sai_vlan_get_vlan_id(p_rif_info->vlan_oid, &l3if.vlan_id);
    }
    else if ((p_rif_info->outer_vlan_id)&&(SAI_ROUTER_INTERFACE_TYPE_SUB_PORT ==ctc_object_id.sub_type))
    {
        l3if.vlan_id  = p_rif_info->outer_vlan_id;
    }
    if (CTC_L3IF_TYPE_PHY_IF == l3if.l3if_type && !p_rif_info->is_virtual)
    {
        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            ctcs_linkagg_get_member_ports(lchip, CTC_MAP_GPORT_TO_LPORT(l3if.gport), gports, &agg_member_cnt) ;
            ctc_sai_lag_binding_rif(ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport), 0, l3if.l3if_type);
        }
        else
        {
            agg_member_cnt = 1;
            gports[0] = l3if.gport;
        }
        for (index = 0; index < agg_member_cnt; index++)
        {
            ctcs_port_set_phy_if_en(lchip, gports[index], 0);
        }
        //ctcs_port_set_phy_if_en(lchip, l3if.gport, 0);
    }
    else if (CTC_L3IF_TYPE_SUB_IF == l3if.l3if_type && !p_rif_info->is_virtual)
    {
        ctc_port_scl_property_t port_scl_property;
        sal_memset(&port_scl_property, 0, sizeof(ctc_port_scl_property_t));
        port_scl_property.hash_type = CTC_PORT_IGS_SCL_HASH_TYPE_DISABLE;

        if (CTC_IS_LINKAGG_PORT(l3if.gport))
        {
            ctcs_linkagg_get_member_ports(lchip, CTC_MAP_GPORT_TO_LPORT(l3if.gport), gports, &agg_member_cnt) ;
            sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, p_rif_info->gport);
            ctc_sai_lag_binding_rif(sai_lag_id, 0, l3if.l3if_type);
            p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
            if (0 == p_db_lag->is_binding_sub_rif)
            {
                for (index = 0; index < agg_member_cnt; index++)
                {
                    ctcs_port_set_scl_property(lchip, gports[index], &port_scl_property);
                }
            }
        }
        else
        {
            port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PORT, lchip, 0, 0, l3if.gport);
            CTC_SAI_ERROR_RETURN(_ctc_sai_port_get_port_db(port_oid, &p_port_db));
            p_port_db->sub_if_ref_cnt--;
            if (0 == p_port_db->sub_if_ref_cnt)
            {
                ctcs_port_set_scl_property(lchip, l3if.gport, &port_scl_property);
            }
        }
    }
    else if (CTC_L3IF_TYPE_VLAN_IF == l3if.l3if_type && !p_rif_info->is_virtual && !is_bridge_rif)
    {
        ctc_sai_oid_get_vlanptr(p_rif_info->vlan_oid, &vlan_ptr);
        ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_ARP_EXCP_TYPE, CTC_EXCP_NORMAL_FWD);
        ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_DHCP_EXCP_TYPE, CTC_EXCP_NORMAL_FWD);
    }
    if (MAX_L3IF_TYPE_NUM != l3if.l3if_type  && !p_rif_info->is_virtual && !is_bridge_rif)
    {
         ctcs_l3if_destory(lchip, l3if_id, &l3if);
    }
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id);
    if(!p_rif_info->is_virtual)
    {
        if (p_rif_info->stats_state)
        {
            ctcs_stats_destroy_statsid(lchip, p_rif_info->ing_statsid);
            ctcs_stats_destroy_statsid(lchip, p_rif_info->egs_statsid);
        }
    }
    else
    {
        sal_memset(&router_mac, 0, sizeof(router_mac));
        if ((CTC_CHIP_GOLDENGATE != ctcs_get_chip_type(lchip)))
        {
            sal_memcpy(router_mac.mac[0], p_rif_info->src_mac, sizeof(sai_mac_t));
            router_mac.dir = CTC_INGRESS;
            router_mac.mode = CTC_L3IF_DELETE_ROUTE_MAC;
            router_mac.num = number;
            CTC_SAI_CTC_ERROR_GOTO(ctcs_l3if_set_interface_router_mac(lchip, p_rif_info->actual_l3if_id, router_mac), status, out);
        }
    }
    _ctc_sai_router_interface_remove_db(lchip, router_interface_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_set_rif_attr(sai_object_id_t router_interface_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "router_interface_id = %llu\n", router_interface_id);
    key.key.object_id = router_interface_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_ROUTER_INTERFACE,  rif_attr_fn_entries, attr), status, out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_router_interface_set_attr_hw(router_interface_id), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_router_interface_get_rif_attr(sai_object_id_t router_interface_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8          loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(router_interface_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_ROUTER_INTERFACE);
    CTC_SAI_LOG_INFO(SAI_API_ROUTER_INTERFACE, "router_interface_id = %llu\n", router_interface_id);
    key.key.object_id = router_interface_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_ROUTER_INTERFACE, loop, rif_attr_fn_entries, &attr_list[loop]), status, out);
        loop++;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_router_interface_api_t ctc_sai_router_interface_api = {
    ctc_sai_router_interface_create_rif,
    ctc_sai_router_interface_remove_rif,
    ctc_sai_router_interface_set_rif_attr,
    ctc_sai_router_interface_get_rif_attr,
    ctc_sai_router_interface_get_stats,
    ctc_sai_router_interface_get_stats_ext,
    ctc_sai_router_interface_clear_stats
};

sai_status_t
ctc_sai_router_interface_api_init()
{
    ctc_sai_register_module_api(SAI_API_ROUTER_INTERFACE, (void*)&ctc_sai_router_interface_api);

    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_router_interface_db_init(uint8 lchip)
{
    // skip Tsingma_mx rsv L3IF 4093,4094
    uint32 l3if_id = 0;
	for(l3if_id = L3IF_RSV_START; l3if_id <= L3IF_RSV_END; l3if_id++)
	{
        CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_L3IF, l3if_id));
	}
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_ROUTERINTERFACE;
    wb_info.data_len = sizeof(ctc_sai_router_interface_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_router_interface_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_ROUTER_INTERFACE, (void*)(&wb_info));

    return SAI_STATUS_SUCCESS;
}
