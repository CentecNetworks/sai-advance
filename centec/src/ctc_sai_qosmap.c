#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_port.h"
#include "ctc_sai_router_interface.h"
#include "ctc_sai_qosmap.h"
#include "ctc_sai_mpls.h"
#include "ctc_sai_next_hop.h"

//domain = 0, used for switch
#define QOS_MAP_DOMAIN_ID_START       1
#define QOS_MAP_SAI_TC_TO_CTC_PRI     2
#define QOS_MAP_CTC_PRI_TO_SAI_DSCP   4

#define QOS_MAP_COLOR_SAI_TO_CTC(sai, ctc)\
{\
    if (sai == SAI_PACKET_COLOR_RED)\
        {ctc = CTC_QOS_COLOR_RED;}\
    else if (sai == SAI_PACKET_COLOR_YELLOW)\
        {ctc = CTC_QOS_COLOR_YELLOW;}\
    else\
        {ctc = CTC_QOS_COLOR_GREEN;}\
}

typedef struct  ctc_sai_qos_map_wb_s
{
    /*key*/
    sai_object_id_t oid;
    uint32 index;
    uint32 calc_key_len[0];
    /*data*/
    sai_qos_map_t qos_map;
}ctc_sai_qos_map_wb_t;

static sai_status_t
_ctc_sai_qos_map_port_get_ctc_domain_id(uint8 lchip, uint32 gport, sai_qos_map_type_t map_type, uint8* domain_id)
{
    uint32 ctc_domain = 0;
    uint32 property = 0;
    ctc_direction_t dir;
    uint8 chip_type = 0;

    chip_type = ctcs_get_chip_type(lchip);
    if (chip_type < CTC_CHIP_DUET2)
    {
        property = CTC_PORT_DIR_PROP_QOS_DOMAIN;
        switch (map_type)
        {
            case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                dir = CTC_INGRESS;
                break;
            case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
                dir = CTC_EGRESS;
                break;
            default:
                return SAI_STATUS_NOT_SUPPORTED;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_direction_property(lchip, gport, property, dir, &ctc_domain));
        *domain_id = ctc_domain;
        CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "lchip:%d gport:0x%x map_type:%d domain:%d\n", lchip, gport, map_type, *domain_id);
        return SAI_STATUS_SUCCESS;
    }

    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            property = CTC_PORT_DIR_PROP_QOS_COS_DOMAIN;
            dir = CTC_INGRESS;
            break;
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            property = CTC_L3IF_PROP_IGS_QOS_DSCP_DOMAIN;
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            property = CTC_L3IF_PROP_EGS_QOS_DSCP_DOMAIN;
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            property = CTC_PORT_DIR_PROP_QOS_COS_DOMAIN;
            dir = CTC_EGRESS;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P))
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_port_get_direction_property(lchip, gport, property, dir, &ctc_domain));
    }
    else
    {
        ctc_sai_rif_traverse_param_t rif_param;
        sal_memset(&rif_param, 0, sizeof(ctc_sai_rif_traverse_param_t));
        rif_param.set_type = CTC_SAI_RIF_SET_TYPE_PORT;
        rif_param.cmp_value = &gport;
        rif_param.lchip = lchip;
        rif_param.l3if_prop = property;
        rif_param.p_value = &ctc_domain;
        CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_get_param(&rif_param));
    }
    *domain_id = ctc_domain;
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "lchip:%d gport:0x%x map_type:%d domain:%d\n", lchip, gport, map_type, *domain_id);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_mpls_ilm_alloc_domain(uint8 lchip,
                                    uint32 inseg_label_or_nhid, sai_qos_map_type_t map_type,
                                    ctc_sai_qos_domain_map_id_t* domain_node,
                                    bool enable, uint8* new_domain,
                                    uint8* old_domain, uint8* new_alloc, uint8 is_nh)
{
    uint8 domain_idx = 0;
    uint8 find = 0;
    uint8 domain_num = QOS_MAP_DOMAIN_NUM_DOT1P;
    ctc_sai_switch_master_t* p_switch_db = NULL;
    ctc_sai_qos_domain_map_id_t* domain_switch = NULL;
    uint8 old_domain_id = 0;
    uint8 find_idx = 0;
    uint32 value1 = 0;
    uint32 value2 = 0;
    ctc_mpls_property_t mpls_pro;
    ctc_mpls_ilm_qos_map_t ilm_qos_map;
    ctc_mpls_nexthop_param_t nh_mpls_param;
    ctc_nh_info_t ctc_nh_info;
    ctc_mpls_nexthop_push_param_t* p_push = NULL;
    ctc_mpls_nexthop_tunnel_param_t mpls_tunnel_param;
    ctc_mpls_nexthop_tunnel_info_t* p_tunnel_info = NULL;

    *new_alloc = 0;

    sal_memset(&ilm_qos_map, 0, sizeof(ctc_mpls_ilm_qos_map_t));
    sal_memset(&mpls_pro, 0, sizeof(mpls_pro));
    sal_memset(&nh_mpls_param, 0, sizeof(nh_mpls_param));
    sal_memset(&ctc_nh_info, 0, sizeof(ctc_nh_info));
    sal_memset(&mpls_tunnel_param, 0, sizeof(mpls_tunnel_param));

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);

    if(!is_nh)
    {
        mpls_pro.label = inseg_label_or_nhid;
        mpls_pro.value = &ilm_qos_map;
        mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
        ctcs_mpls_get_ilm_property(lchip, &mpls_pro);

        old_domain_id = ilm_qos_map.exp_domain;
    }
    else
    {
        ctc_nh_info.p_nh_param = &nh_mpls_param;
        if(ctcs_nh_get_nh_info(lchip, inseg_label_or_nhid, &ctc_nh_info) == 0)
        {
            if(ctc_nh_info.nh_type == CTC_NH_TYPE_MPLS)
            {
                if(nh_mpls_param.nh_prop == CTC_MPLS_NH_PUSH_TYPE)
                {
                    p_push = (ctc_mpls_nexthop_push_param_t*)&nh_mpls_param.nh_para.nh_param_push;
                    if(p_push->tunnel_id && !p_push->label_num) //mpls tunnel nh
                    {
                        ctcs_nh_get_mpls_tunnel_label(lchip, p_push->tunnel_id, &mpls_tunnel_param);
                        p_tunnel_info = &mpls_tunnel_param.nh_param;
                        old_domain_id = p_tunnel_info->tunnel_label[0].exp_domain;
                    }
                    else
                    {
                        old_domain_id = p_push->push_label[0].exp_domain;
                    }
                }            
            }
        }
        else
        {
            //nh not exist, consider old_domain_id as 0.
        }

        
    }
        
    *old_domain = old_domain_id;
    //free domain on label, so return the default domain id = 0; and it is new alloc
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            if ((0 == domain_node->tc.exp_to_tc_map_id)
                && (0 == domain_node->color.exp_to_color_map_id))
            {
                *new_domain = 0;
                if (old_domain_id)
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            if (0 == domain_node->tc_color.tc_color_to_dot1p_map_id)
            {
                *new_domain = 0;
                if (old_domain_id)
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
            break;
        default:
            break;
    }

    p_switch_db = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if ((map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP))
    {
        domain_num = QOS_MAP_DOMAIN_NUM_EXP;
        domain_switch = p_switch_db->qos_domain_exp;
    }
    
    //find twice, the first time to find old used domain; and the second time to find the new unused domain.
    for (find_idx = 0; find_idx < 2; find_idx++)
    {
        for (domain_idx = QOS_MAP_DOMAIN_ID_START; domain_idx < domain_num; domain_idx++)
        {
            switch (map_type)
            {
                case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
                    value1 = (find_idx == 0) ? domain_node->tc.exp_to_tc_map_id : 0;
                    value2 = (find_idx == 0) ? domain_node->color.exp_to_color_map_id : 0;
                    if (((value1 == domain_switch[domain_idx].tc.exp_to_tc_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_tc)
                            && !domain_switch[domain_idx].color.exp_to_color_map_id
                            && !value2)
                    || ((value2 == domain_switch[domain_idx].color.exp_to_color_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_color)
                            && (0 == domain_switch[domain_idx].tc.exp_to_tc_map_id))
                    || ((value1 == domain_switch[domain_idx].tc.exp_to_tc_map_id)
                            && (value2 == domain_switch[domain_idx].color.exp_to_color_map_id)))
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
                    value1 = (find_idx == 0) ? domain_node->tc.exp_to_tc_map_id : 0;
                    value2 = (find_idx == 0) ? domain_node->color.exp_to_color_map_id : 0;
                    if (((value1 == domain_switch[domain_idx].tc.exp_to_tc_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_tc)
                            && (0 == domain_switch[domain_idx].color.exp_to_color_map_id))
                    || ((value2 == domain_switch[domain_idx].color.exp_to_color_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_color)
                            && !domain_switch[domain_idx].tc.exp_to_tc_map_id
                            && !value1)
                    || ((value1 == domain_switch[domain_idx].tc.exp_to_tc_map_id)
                            && (value2 == domain_switch[domain_idx].color.exp_to_color_map_id)))
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
                    value1 = (find_idx == 0) ? domain_node->tc_color.tc_color_to_exp_map_id : 0;
                    if (value1 == domain_switch[domain_idx].tc_color.tc_color_to_exp_map_id)
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                default:
                    break;
            }
            if (find)
            {
                if (old_domain_id && (*new_domain != old_domain_id))
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
        }
    }

    if (!find && !enable)
    {
        /*maybe domain X only used for one ilm/nh. so if disable, the ilm/nh also only use the domain*/
        if (((domain_switch[old_domain_id].ref_cnt_tc == 1)
            && (domain_switch[old_domain_id].tc.exp_to_tc_map_id == domain_node->tc.exp_to_tc_map_id))
            || ((domain_switch[old_domain_id].ref_cnt_color == 1)
            && (domain_switch[old_domain_id].color.exp_to_color_map_id == domain_node->color.exp_to_color_map_id)))
        {
            *new_domain = old_domain_id;
            return SAI_STATUS_SUCCESS;
        }
    }

    if (!find)
    {
        /*no enough domain*/
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_port_alloc_domain(uint8 lchip,
                                    uint32 gport, sai_qos_map_type_t map_type,
                                    ctc_sai_qos_domain_map_id_t* domain_node,
                                    bool enable, uint8* new_domain,
                                    uint8* old_domain, uint8* new_alloc)
{
    uint8 domain_idx = 0;
    uint8 find = 0;
    uint8 domain_num = QOS_MAP_DOMAIN_NUM_DOT1P;
    ctc_sai_switch_master_t* p_switch_db = NULL;
    ctc_sai_qos_domain_map_id_t* domain_switch = NULL;
    uint8 old_domain_id = 0;
    uint8 find_idx = 0;
    uint32 value1 = 0;
    uint32 value2 = 0;

    *new_alloc = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_port_get_ctc_domain_id(lchip, gport, map_type, &old_domain_id));
    *old_domain = old_domain_id;
    //free domain on port, so return the default domain id = 0; and it is new alloc
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            if ((0 == domain_node->tc.dot1p_to_tc_map_id)
                && (0 == domain_node->color.dot1p_to_color_map_id))
            {
                *new_domain = 0;
                if (old_domain_id)
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            if (0 == domain_node->tc_color.tc_color_to_dot1p_map_id)
            {
                *new_domain = 0;
                if (old_domain_id)
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
            break;
        default:
            break;
    }

    p_switch_db = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if ((map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP))
    {
        domain_num = (CTC_CHIP_DUET2 <= ctcs_get_chip_type(lchip)) ? QOS_MAP_DOMAIN_NUM_DSCP : 8;
        domain_switch = p_switch_db->qos_domain_dscp;
    }
    else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P))
    {
        domain_switch = p_switch_db->qos_domain_dot1p;
    }

    //find twice, the first time to find old used domain; and the second time to find the new unused domain.
    for (find_idx = 0; find_idx < 2; find_idx++)
    {
        for (domain_idx = QOS_MAP_DOMAIN_ID_START; domain_idx < domain_num; domain_idx++)
        {
            switch (map_type)
            {
                case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
                case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
                    value1 = (find_idx == 0) ? domain_node->tc.dot1p_to_tc_map_id : 0;
                    value2 = (find_idx == 0) ? domain_node->color.dot1p_to_color_map_id : 0;
                    if (((value1 == domain_switch[domain_idx].tc.dot1p_to_tc_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_tc)
                            && !domain_switch[domain_idx].color.dot1p_to_color_map_id
                            && !value2)
                    || ((value2 == domain_switch[domain_idx].color.dot1p_to_color_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_color)
                            && (0 == domain_switch[domain_idx].tc.dot1p_to_tc_map_id))
                    || ((value1 == domain_switch[domain_idx].tc.dot1p_to_tc_map_id)
                            && (value2 == domain_switch[domain_idx].color.dot1p_to_color_map_id)))
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                    value1 = (find_idx == 0) ? domain_node->tc.dot1p_to_tc_map_id : 0;
                    value2 = (find_idx == 0) ? domain_node->color.dot1p_to_color_map_id : 0;
                    if (((value1 == domain_switch[domain_idx].tc.dot1p_to_tc_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_tc)
                            && (0 == domain_switch[domain_idx].color.dot1p_to_color_map_id))
                    || ((value2 == domain_switch[domain_idx].color.dot1p_to_color_map_id)
                            && (1 == domain_switch[domain_idx].ref_cnt_color)
                            && !domain_switch[domain_idx].tc.dot1p_to_tc_map_id
                            && !value1)
                    || ((value1 == domain_switch[domain_idx].tc.dot1p_to_tc_map_id)
                            && (value2 == domain_switch[domain_idx].color.dot1p_to_color_map_id)))
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
                case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
                    value1 = (find_idx == 0) ? domain_node->tc_color.tc_color_to_dot1p_map_id : 0;
                    if (value1 == domain_switch[domain_idx].tc_color.tc_color_to_dot1p_map_id)
                    {
                        *new_domain = domain_idx;
                        find = 1;
                    }
                    break;
                default:
                    break;
            }
            if (find)
            {
                if (old_domain_id && (*new_domain != old_domain_id))
                {
                    *new_alloc = 1;
                }
                return SAI_STATUS_SUCCESS;
            }
        }
    }

    if (!find && !enable)
    {
        /*maybe domain X only used for one gport. so if disable, the gport also only use the domain*/
        if (((domain_switch[old_domain_id].ref_cnt_tc == 1)
            && (domain_switch[old_domain_id].tc.dot1p_to_tc_map_id == domain_node->tc.dot1p_to_tc_map_id))
            || ((domain_switch[old_domain_id].ref_cnt_color == 1)
            && (domain_switch[old_domain_id].color.dot1p_to_color_map_id == domain_node->color.dot1p_to_color_map_id)))
        {
            *new_domain = old_domain_id;
            return SAI_STATUS_SUCCESS;
        }
    }

    if (!find)
    {
        /*no enough domain*/
        return SAI_STATUS_FAILURE;
    }
    return SAI_STATUS_SUCCESS;
}

//domain 0 for switch use
static sai_status_t
_ctc_sai_qos_map_set_ctc_domain_map(uint8 lchip, uint32 map_id, uint8 domain_id, uint8 is_set)
{
    uint8 idx = 0;
    uint8 idx2 = 0;
    ctc_qos_domain_map_t domain_map;
    sai_object_id_t qos_map_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    sai_qos_map_t* map_list = NULL;
    sai_qos_map_type_t map_type;
    ctc_sai_switch_master_t* p_switch_db = NULL;
    ctc_sai_qos_domain_map_id_t* domain_switch = NULL;

    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "lchip:%d ctc_map_id:0x%x domain:%d op:%s\n", lchip, map_id, domain_id, is_set?"SET":"UNSET");
    if (map_id == 0)
    {
        return SAI_STATUS_SUCCESS;
    }
    qos_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, map_id);
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    map_list = p_map_db->map_list.list;
    map_type = p_map_db->map_type;
    p_switch_db = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if ((map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP))
    {
        domain_switch = p_switch_db->qos_domain_dscp;
    }
   else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P))
    {
        domain_switch = p_switch_db->qos_domain_dot1p;
    }
    else if ((map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP))
    {
        domain_switch = p_switch_db->qos_domain_exp;
    }
    //domain unset, need not unset again, should return error
    if (!is_set
        && ((map_id != domain_switch[domain_id].tc.dot1p_to_tc_map_id)
             && (map_id != domain_switch[domain_id].color.dot1p_to_color_map_id)
             && (map_id != domain_switch[domain_id].tc_color.tc_color_to_dot1p_map_id)))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "unset qosmap id[0x%"PRIx64"] error!, Not found domian[%d]", qos_map_id, domain_id);
        return SAI_STATUS_ADDR_NOT_FOUND;
    }

    sal_memset(&domain_map, 0, sizeof(domain_map));
    domain_map.domain_id = domain_id;
    for (idx = 0; idx < p_map_db->map_list.count; idx++)
    {
        switch (map_type)
        {
            case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                domain_map.type = CTC_QOS_DOMAIN_MAP_IGS_COS_TO_PRI_COLOR;
                domain_map.hdr_pri.dot1p.cos = map_list[idx].key.dot1p;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_domain_map(lchip, &domain_map));
                if (map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
                {
                    domain_map.priority = (is_set ? map_list[idx].value.tc : domain_map.hdr_pri.dot1p.cos)* QOS_MAP_SAI_TC_TO_CTC_PRI;
                }
                else
                {
                    if (is_set)
                    {
                        QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].value.color, domain_map.color);
                    }
                    else
                    {
                        domain_map.color = CTC_QOS_COLOR_GREEN;
                    }
                }
                for (idx2 = 0; idx2 <= 1; idx2++)
                {
                    domain_map.hdr_pri.dot1p.dei = idx2;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                }
                break;
            case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                domain_map.type = CTC_QOS_DOMAIN_MAP_IGS_DSCP_TO_PRI_COLOR;
                domain_map.hdr_pri.tos.dscp = map_list[idx].key.dscp;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_domain_map(lchip, &domain_map));
                if (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
                {
                    domain_map.priority = is_set ?  (map_list[idx].value.tc * QOS_MAP_SAI_TC_TO_CTC_PRI) : (domain_map.hdr_pri.tos.dscp/QOS_MAP_CTC_PRI_TO_SAI_DSCP);
                }
                else
                {
                    if (is_set)
                    {
                        QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].value.color, domain_map.color);
                    }
                    else
                    {
                        domain_map.color = CTC_QOS_COLOR_GREEN;
                    }
                }
                for (idx2 = 0; idx2 <= 3; idx2++)
                {
                    domain_map.hdr_pri.tos.ecn = idx2;
                    CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                }
                break;
            case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
                domain_map.type = CTC_QOS_DOMAIN_MAP_IGS_EXP_TO_PRI_COLOR;
                domain_map.hdr_pri.exp = map_list[idx].key.mpls_exp;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_domain_map(lchip, &domain_map));
                if (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC)
                {
                    domain_map.priority = (is_set ? map_list[idx].value.tc : domain_map.hdr_pri.exp)* QOS_MAP_SAI_TC_TO_CTC_PRI;
                }
                else
                {
                    if (is_set)
                    {
                        QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].value.color, domain_map.color);
                    }
                    else
                    {
                        domain_map.color = CTC_QOS_COLOR_GREEN;
                    }
                }

                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                
                break;
            case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
                domain_map.type = CTC_QOS_DOMAIN_MAP_EGS_PRI_COLOR_TO_DSCP;
                domain_map.priority = map_list[idx].key.tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
                QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].key.color, domain_map.color);
                domain_map.hdr_pri.tos.dscp = is_set ? map_list[idx].value.dscp
                                              : domain_map.priority * QOS_MAP_CTC_PRI_TO_SAI_DSCP;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                break;
            case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
                domain_map.type = CTC_QOS_DOMAIN_MAP_EGS_PRI_COLOR_TO_COS;
                domain_map.priority = map_list[idx].key.tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
                QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].key.color, domain_map.color);
                domain_map.hdr_pri.dot1p.cos = is_set ? map_list[idx].value.dot1p : map_list[idx].key.tc;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                break;
            case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
                domain_map.type = CTC_QOS_DOMAIN_MAP_EGS_PRI_COLOR_TO_EXP;
                domain_map.priority = map_list[idx].key.tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
                QOS_MAP_COLOR_SAI_TO_CTC(map_list[idx].key.color, domain_map.color);
                domain_map.hdr_pri.exp = is_set ? map_list[idx].value.mpls_exp : map_list[idx].key.tc;
                CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
                break;
            default:
                break;
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_domain_set_map_id(uint8 lchip, uint8 domain_id, uint32 map_id, uint8 is_set)
{
    ctc_sai_switch_master_t* p_switch_db = NULL;
    ctc_sai_qos_domain_map_id_t* domain_switch = NULL;
    sai_qos_map_type_t map_type;
    uint16* ref_cnt = NULL;
    uint32* map_id_temp  = NULL;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    sai_object_id_t qos_map_id;

    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "lchip:%d ctc_map_id:0x%x domain:%d op:%s\n", lchip, map_id, domain_id, is_set?"SET":"UNSET");
    if (map_id == 0)
    {
        return SAI_STATUS_SUCCESS;
    }
    qos_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP,lchip, 0, 0, map_id);
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    map_type = p_map_db->map_type;

    p_switch_db = ctc_sai_get_switch_property(lchip);
    if (NULL == p_switch_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if ((map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP))
    {
        domain_switch = p_switch_db->qos_domain_dscp;
    }
    else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P))
    {
        domain_switch = p_switch_db->qos_domain_dot1p;
    }
    else if ((map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC)
        || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR)
        || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP))
    {
        domain_switch = p_switch_db->qos_domain_exp;
    }
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            ref_cnt = &domain_switch[domain_id].ref_cnt_tc;
            map_id_temp = &domain_switch[domain_id].tc.dot1p_to_tc_map_id;
            break;
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            ref_cnt = &domain_switch[domain_id].ref_cnt_color;
            map_id_temp = &domain_switch[domain_id].color.dot1p_to_color_map_id;
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            ref_cnt = &domain_switch[domain_id].ref_cnt_tc_color;
            map_id_temp = &domain_switch[domain_id].tc_color.tc_color_to_dot1p_map_id;
            break;
        default:
            return SAI_STATUS_NOT_IMPLEMENTED;
    }

    if (is_set)
    {
        //add map
        if (*ref_cnt == 0)
        {
            *map_id_temp = map_id;
            CTC_BIT_SET(p_map_db->domain_bmp, domain_id);
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_ctc_domain_map(lchip, map_id, domain_id, is_set));
        }
        (*ref_cnt)++;
    }
    else if (*ref_cnt)
    {
        if (*map_id_temp != map_id)
        {
            CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "Failed set map_id:%d, domain[%d]_mapId:\n", map_id, domain_id, *map_id_temp);
            return SAI_STATUS_FAILURE;
        }
        //free map
        (*ref_cnt)--;
        if (*ref_cnt == 0)
        {
            //need to revert domain
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_ctc_domain_map(lchip, map_id, domain_id, is_set));
            *map_id_temp = 0;
            CTC_BIT_UNSET(p_map_db->domain_bmp, domain_id);
        }
    }
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_qos_map_set_attr(sai_object_key_t *key, const sai_attribute_t* attr)
{
    sai_object_id_t qos_map_id = key->key.object_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    ctc_object_id_t ctc_object_id;
    uint8 lchip = 0;
    uint8 domain_id = 0;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_QOS_MAP, qos_map_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
            if (attr->value.maplist.count == 0)
            {
                CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map attribute count = 0\n");
                return SAI_STATUS_INVALID_PARAMETER;
            }
            if (attr->value.maplist.count != p_map_db->map_list.count)
            {
                sai_qos_map_t* list_temp = NULL;
                list_temp = (sai_qos_map_t*)mem_malloc(MEM_QUEUE_MODULE, attr->value.maplist.count * sizeof(sai_qos_map_t));
                if (NULL == list_temp)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map attribute no memory\n");
                    return SAI_STATUS_NO_MEMORY;
                }
                sal_memset(list_temp, 0, attr->value.maplist.count * sizeof(sai_qos_map_t));
                mem_free(p_map_db->map_list.list);
                p_map_db->map_list.count = attr->value.maplist.count;
                p_map_db->map_list.list = list_temp;
            }
            sal_memcpy(p_map_db->map_list.list, attr->value.maplist.list, p_map_db->map_list.count * sizeof(sai_qos_map_t));
            if (p_map_db->map_type == SAI_QOS_MAP_TYPE_TC_TO_QUEUE)
            {
                ctc_sai_switch_master_t* p_switch = NULL;
                p_switch = ctc_sai_get_switch_property(lchip);
                if (NULL == p_switch)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map attribute switch db not found\n");
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                if (p_switch->tc_to_queue_map_id == ctc_object_id.value)
                {
                    CTC_SAI_ERROR_RETURN(ctc_sai_qos_map_switch_set_map(lchip, ctc_object_id.value, SAI_QOS_MAP_TYPE_TC_TO_QUEUE, TRUE));
                }
            }
            else if (p_map_db->domain_bmp)
            {
                for (domain_id = 0; domain_id < 16; domain_id++)
                {
                    //include switch map & port map
                    if (!CTC_IS_BIT_SET(p_map_db->domain_bmp, domain_id))
                    {
                        continue;
                    }
                    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_ctc_domain_map(lchip, ctc_object_id.value, domain_id, 1));
                }
            }
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_get_attr(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t qos_map_id = key->key.object_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    uint8 lchip = 0;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, qos_map_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QOS_MAP)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_QOS_MAP_ATTR_TYPE:
            attr->value.u32 = p_map_db->map_type;
            break;
        case SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
            CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_qos_map_t), (void*)p_map_db->map_list.list, p_map_db->map_list.count, (void*)(&(attr->value.maplist))));
            break;
        default:
            CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map attribute not implement\n");
            return  SAI_STATUS_NOT_IMPLEMENTED;
    }

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  qos_map_attr_fn_entries[] =
{
        {SAI_QOS_MAP_ATTR_TYPE,
            _ctc_sai_qos_map_get_attr,
            NULL},
        {SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST,
            _ctc_sai_qos_map_get_attr,
            _ctc_sai_qos_map_set_attr},
        { CTC_SAI_FUNC_ATTR_END_ID,
          NULL,
          NULL }
};

static sai_status_t
_ctc_sai_qos_map_set_domain(uint8 lchip, bool enable, uint32 map_id,
                                            sai_qos_map_type_t map_type, ctc_sai_qos_domain_map_id_t* domain_node,
                                            uint8 domain_id, uint8 old_domain, uint8 is_new_alloc, uint32 old_map_id)
{
    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "map_type:%d enable:%d map_id:%d new_domain:%d old_domain:%d new_alloc:%d\n",
                                        map_type, enable?1:0, map_id, domain_id, old_domain, is_new_alloc);
    if (enable || domain_id)
    {
        //if new_domain is first used on gport, need to bind all the map_id to domain
        if ((map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP)
            || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P)
            || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP))
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, domain_id, domain_node->tc_color.tc_color_to_dot1p_map_id, 1));
        }
        else if (is_new_alloc)
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, domain_id, domain_node->tc.dot1p_to_tc_map_id, 1));
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, domain_id, domain_node->color.dot1p_to_color_map_id, 1));
        }
        else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
                || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
                || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC))
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, domain_id, domain_node->tc.dot1p_to_tc_map_id, 1));
        }
        else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
                || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
                || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR))
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, domain_id, domain_node->color.dot1p_to_color_map_id, 1));
        }
    }

    if (!enable && old_domain)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, old_domain, map_id, 0));
    }
    //such as domain 2-->1, merge domain, need to reset original domain
    if (is_new_alloc && old_domain)
    {
        if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC)
            || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
            || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC))
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, old_domain, domain_node->color.dot1p_to_color_map_id, 0));
            if(old_map_id)
            {
                CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, old_domain, old_map_id, 0));
            }
        }
        else if ((map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR)
                || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
                || (map_type == SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR))
        {
            CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, old_domain, domain_node->tc.dot1p_to_tc_map_id, 0));
            if(old_map_id)
            {
                CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, old_domain, old_map_id, 0));
            }
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_db_deinit_cb(ctc_sai_oid_property_t* bucket_data, void* user_data)
{
    ctc_sai_qos_map_db_t* p_map_db = (ctc_sai_qos_map_db_t*)(bucket_data->data);
    if (NULL == bucket_data)
    {
        return SAI_STATUS_SUCCESS;
    }

    if (p_map_db && p_map_db->map_list.count)
    {
        mem_free(p_map_db->map_list.list);
    }
    return SAI_STATUS_SUCCESS;
}


#define ________INTERNAL_API________

sai_status_t
ctc_sai_qos_map_port_set_map(sai_object_id_t port_oid, uint32 map_id, sai_qos_map_type_t map_type, bool enable)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    ctc_sai_port_db_t* p_port_db = NULL;
    ctc_sai_qos_domain_map_id_t domain_node;
    uint8 new_domain = 0;
    uint8 old_domain = 0;
    uint8 is_new_alloc = 0;
    ctc_direction_t dir;
    uint32 property = 0;
    uint32 property_l3if = 0;
    uint32 qos_trust = 0;
    uint32 gport = 0;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint32 old_map_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "port_id:0x%"PRIx64" ctc_map_id:0x%x map_type:%d enable:%d\n",port_oid, map_id, map_type, enable?1:0);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(port_oid, &lchip));

    chip_type = ctcs_get_chip_type(lchip);
    sal_memset(&domain_node, 0, sizeof(domain_node));
    p_map_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, map_id));
    if (NULL == p_map_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_map_db->map_type != map_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "port qos map type not match\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_port_db = ctc_sai_db_get_object_property(lchip, port_oid);
    if (NULL == p_port_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PORT, port_oid, &ctc_object_id);
    gport = ctc_object_id.value;
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_COS_DOMAIN;
            dir = CTC_INGRESS;
            domain_node.tc.dot1p_to_tc_map_id = enable ? map_id : 0;
            domain_node.color.dot1p_to_color_map_id = p_port_db->dot1p_to_color_map_id;
            qos_trust = CTC_QOS_TRUST_COS;
            old_map_id = p_port_db->dot1p_to_tc_map_id;
            break;
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_DSCP_DOMAIN;
            dir = CTC_INGRESS;
            property_l3if = CTC_L3IF_PROP_IGS_QOS_DSCP_DOMAIN;
            domain_node.tc.dscp_to_tc_map_id = enable ? map_id : 0;
            domain_node.color.dscp_to_color_map_id = p_port_db->dscp_to_color_map_id;
            qos_trust = enable ? CTC_QOS_TRUST_DSCP : CTC_QOS_TRUST_COS;
            old_map_id = p_port_db->dscp_to_tc_map_id;
            break;
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_COS_DOMAIN;
            dir = CTC_INGRESS;
            domain_node.color.dot1p_to_color_map_id = enable ? map_id : 0;
            domain_node.tc.dot1p_to_tc_map_id = p_port_db->dot1p_to_tc_map_id;
            qos_trust = CTC_QOS_TRUST_COS;
            old_map_id = p_port_db->dot1p_to_color_map_id;
            break;
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_DSCP_DOMAIN;
            dir = CTC_INGRESS;
            property_l3if = CTC_L3IF_PROP_IGS_QOS_DSCP_DOMAIN;
            domain_node.color.dscp_to_color_map_id = enable ? map_id : 0;
            domain_node.tc.dscp_to_tc_map_id = p_port_db->dscp_to_tc_map_id;
            qos_trust = enable ? CTC_QOS_TRUST_DSCP : CTC_QOS_TRUST_COS;
            old_map_id = p_port_db->dscp_to_color_map_id;
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_DSCP_DOMAIN;
            dir = CTC_EGRESS;
            property_l3if = CTC_L3IF_PROP_EGS_QOS_DSCP_DOMAIN;
            domain_node.tc_color.tc_color_to_dscp_map_id = enable ? map_id : 0;
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            property = (chip_type < CTC_CHIP_DUET2) ? CTC_PORT_DIR_PROP_QOS_DOMAIN : CTC_PORT_DIR_PROP_QOS_COS_DOMAIN;
            domain_node.tc_color.tc_color_to_dot1p_map_id = enable ? map_id : 0;
            dir = CTC_EGRESS;
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_port_alloc_domain(lchip, gport, map_type,
                                                            &domain_node,
                                                            enable, &new_domain,
                                                            &old_domain, &is_new_alloc));

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_domain(lchip, enable, map_id, map_type, &domain_node, new_domain, old_domain, is_new_alloc, old_map_id));
    //set ctc api
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_direction_property(lchip, gport, property, dir, new_domain));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_port_set_property(lchip, gport, CTC_PORT_PROP_QOS_POLICY, qos_trust));

    {
        //for D2, need to set l3if
        if (((chip_type == CTC_CHIP_DUET2)||(chip_type == CTC_CHIP_TSINGMA))
            && ((map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC)
            || (map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR)
            || (map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP)))
        {
            uint32 rif_value = 0;
            ctc_sai_rif_traverse_param_t rif_param;
            sal_memset(&rif_param, 0, sizeof(ctc_sai_rif_traverse_param_t));
            rif_param.set_type = CTC_SAI_RIF_SET_TYPE_PORT;
            rif_param.cmp_value = &gport;
            rif_param.lchip = lchip;

            rif_param.l3if_prop = property_l3if;
            rif_value = new_domain;
            rif_param.p_value = &rif_value;
            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_traverse_set(&rif_param));

            rif_param.l3if_prop = CTC_L3IF_PROP_TRUST_DSCP;
            rif_value = enable ? 1 : 0;
            rif_param.p_value = &rif_value;
            CTC_SAI_ERROR_RETURN(ctc_sai_router_interface_traverse_set(&rif_param));
        }
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_qos_map_switch_set_map(uint8 lchip, uint32 map_id, sai_qos_map_type_t map_type, bool enable)
{
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    sai_object_id_t qos_map_id;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] = {0};
    uint32 index = 0;
    uint8 chip_type = 0;
    uint8 gchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "ctc_map_id:0x%x map_type:%d enable:%d\n", map_id, map_type, enable?1:0);
    qos_map_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, map_id);
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_map_db->map_type != map_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "switch qos map type not match\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    chip_type = ctcs_get_chip_type(lchip);

    if (map_type != SAI_QOS_MAP_TYPE_TC_TO_QUEUE)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_domain_set_map_id(lchip, 0, map_id, enable ? 1 : 0));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; index++)
            {
                ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, index), CTC_PORT_PROP_QOS_POLICY, CTC_QOS_TRUST_COS);
            }
            break;
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; index++)
            {
                ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, index), CTC_PORT_PROP_QOS_POLICY, CTC_QOS_TRUST_DSCP);
            }
            //D2 need set l3if
            if (chip_type == CTC_CHIP_DUET2 || chip_type == CTC_CHIP_TSINGMA)
            {
                for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_L3IF_NUM]; index++)
                {
                    ctcs_l3if_set_property(lchip, index, CTC_L3IF_PROP_TRUST_DSCP, enable ? 1 : 0);
                }
            }
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; index++)
            {
                ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, index), CTC_PORT_PROP_REPLACE_DSCP_EN, enable ? 1 : 0);
            }
            //D2 need set l3if
            if (chip_type == CTC_CHIP_DUET2 || chip_type == CTC_CHIP_TSINGMA)
            {
                for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_L3IF_NUM]; index++)
                {
                    ctcs_l3if_set_property(lchip, index, CTC_L3IF_PROP_DSCP_SELECT_MODE, enable ? CTC_DSCP_SELECT_MAP : CTC_DSCP_SELECT_NONE);
                }
            }
            break;
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            for (index = 0; index <= capability[CTC_GLOBAL_CAPABILITY_MAX_PHY_PORT_NUM]; index++)
            {
                ctcs_port_set_property(lchip, CTC_MAP_LPORT_TO_GPORT(gchip, index), CTC_PORT_PROP_REPLACE_STAG_COS, enable ? 1 : 0);
            }
            break;
        case SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
            {
                ctc_qos_queue_cfg_t queue_cfg;
                ctc_qos_color_t color;
                sal_memset(&queue_cfg, 0, sizeof(queue_cfg));
                queue_cfg.type = CTC_QOS_QUEUE_CFG_PRI_MAP;
                for (index = 0; index < p_map_db->map_list.count; index++)
                {
                    queue_cfg.value.pri_map.priority = p_map_db->map_list.list[index].key.tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
                    if (enable)
                    {
                        queue_cfg.value.pri_map.queue_select = p_map_db->map_list.list[index].value.queue_index;
                    }
                    else
                    {
                        queue_cfg.value.pri_map.queue_select = p_map_db->map_list.list[index].key.tc;
                    }
                    for (color = CTC_QOS_COLOR_RED; color <= CTC_QOS_COLOR_GREEN; color++)
                    {
                        queue_cfg.value.pri_map.color = color;
                        queue_cfg.value.pri_map.drop_precedence = color - 1;
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_queue(lchip, &queue_cfg));
                    }
                }
                p_map_db->domain_bmp = enable ? 0xFFFF : 0;
            }
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_qos_map_switch_set_default_tc(uint8 lchip, uint8 tc)
{
    uint8 idx = 0;
    uint8 dei = 0;
    ctc_qos_domain_map_t domain_map;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "lchip:%d default_tc:%d\n", lchip, tc);
    sal_memset(&domain_map, 0, sizeof(domain_map));
    domain_map.domain_id = 0;
    domain_map.type = CTC_QOS_DOMAIN_MAP_IGS_COS_TO_PRI_COLOR;
    for (idx = 0; idx < 8; idx++)
    {
        domain_map.hdr_pri.dot1p.cos = idx;
        for (dei = 0; dei <= 1; dei++)
        {
            domain_map.hdr_pri.dot1p.dei = dei;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_get_domain_map(lchip, &domain_map));
            domain_map.priority = tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_qos_set_domain_map(lchip, &domain_map));
        }
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_qos_map_mpls_inseg_set_map(const sai_inseg_entry_t* inseg_entry, uint32 pcs_type, uint8 qos_tc,
    uint32 map_id, sai_qos_map_type_t map_type, bool enable)
{
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    ctc_sai_mpls_t* p_mpls_info = NULL;
    ctc_sai_qos_domain_map_id_t domain_node;
    ctc_mpls_property_t mpls_pro;
    ctc_mpls_ilm_qos_map_t ilm_qos_map;
    uint8 new_domain = 0;
    uint8 old_domain = 0;
    uint8 is_new_alloc = 0;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint32 old_map_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "label:%d pcs_type:%d qos_tc:%d ctc_map_id:0x%x map_type:%d enable:%d\n",
        inseg_entry->label, pcs_type, qos_tc, map_id, map_type, enable?1:0);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(inseg_entry->switch_id, &lchip));

    chip_type = ctcs_get_chip_type(lchip);
    sal_memset(&domain_node, 0, sizeof(domain_node));
    sal_memset(&mpls_pro, 0, sizeof(mpls_pro));
    sal_memset(&ilm_qos_map, 0, sizeof(ilm_qos_map));
    
    p_map_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, map_id));
    if (NULL == p_map_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_map_db->map_type != map_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "port qos map type not match\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    p_mpls_info = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_MPLS, (void*)inseg_entry);
    if (NULL == p_mpls_info)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    
    if(SAI_INSEG_ENTRY_PSC_TYPE_LLSP == pcs_type)
    {
        ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_LLSP;
    }
    else
    {
        ilm_qos_map.mode = CTC_MPLS_ILM_QOS_MAP_ELSP;
    }
    
    ilm_qos_map.priority = qos_tc * QOS_MAP_SAI_TC_TO_CTC_PRI;
    
    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            domain_node.tc.exp_to_tc_map_id = enable ? map_id : 0;            
            domain_node.color.exp_to_color_map_id = p_mpls_info->exp_to_color_map_id;

            old_map_id = enable ? p_mpls_info->exp_to_tc_map_id : 0;
            break;
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            domain_node.color.exp_to_color_map_id = enable ? map_id : 0;
            domain_node.tc.exp_to_tc_map_id = p_mpls_info->exp_to_tc_map_id;

            old_map_id = enable ? p_mpls_info->exp_to_color_map_id : 0;
            break;
        
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_mpls_ilm_alloc_domain(lchip, (uint32)inseg_entry->label, map_type,
                                                            &domain_node,
                                                            enable, &new_domain,
                                                            &old_domain, &is_new_alloc, 0));

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_domain(lchip, enable, map_id, map_type, &domain_node, new_domain, old_domain, is_new_alloc, old_map_id));

    ilm_qos_map.exp_domain = new_domain;
    mpls_pro.label = inseg_entry->label;
    mpls_pro.property_type = CTC_MPLS_ILM_QOS_MAP;
    mpls_pro.value = &ilm_qos_map;

    CTC_SAI_CTC_ERROR_RETURN(ctcs_mpls_set_ilm_property(lchip, &mpls_pro));

    return SAI_STATUS_SUCCESS;

}

sai_status_t
ctc_sai_qos_map_mpls_nh_set_map(sai_object_id_t nh_oid, uint32 map_id, sai_qos_map_type_t map_type, bool enable, uint8* ret_domain)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    //ctc_sai_next_hop_t* p_next_hop_info = NULL;
    ctc_sai_qos_domain_map_id_t domain_node;

    uint8 new_domain = 0;
    uint8 old_domain = 0;
    uint8 is_new_alloc = 0;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint32 old_map_id = 0;
    uint32 nh_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_LOG_INFO(SAI_API_QOS_MAP, "nh_id:0x%"PRIx64" ctc_map_id:0x%x map_type:%d enable:%d\n",
        nh_oid, map_id, map_type, enable?1:0);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(nh_oid, &lchip));

    chip_type = ctcs_get_chip_type(lchip);
    sal_memset(&domain_node, 0, sizeof(domain_node));
    
    p_map_db = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, map_id));
    if (NULL == p_map_db)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "qos map db not found\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    if (p_map_db->map_type != map_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "port qos map type not match\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }

    //p_next_hop_info = ctc_sai_db_get_object_property(lchip, nh_oid);
    //if (NULL == p_next_hop_info)
    //{
    //    return SAI_STATUS_ITEM_NOT_FOUND;
    //}


    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NEXT_HOP, nh_oid, &ctc_object_id);
    nh_id = ctc_object_id.value;

    switch (map_type)
    {
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            domain_node.tc_color.tc_color_to_exp_map_id = enable ? map_id : 0;

            //old_map_id = enable ? p_mpls_info->exp_to_tc_map_id : 0;
            break;        
        
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_mpls_ilm_alloc_domain(lchip, nh_id, map_type,
                                                            &domain_node,
                                                            enable, &new_domain,
                                                            &old_domain, &is_new_alloc, 1));

    CTC_SAI_ERROR_RETURN(_ctc_sai_qos_map_set_domain(lchip, enable, map_id, map_type, &domain_node, new_domain, old_domain, is_new_alloc, old_map_id));

    *ret_domain = new_domain;
    
    return SAI_STATUS_SUCCESS;

}    

static sai_status_t
_ctc_sai_qos_map_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t qos_map_id = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_qos_map_db_t* p_map_db = (ctc_sai_qos_map_db_t*)data;
    ctc_sai_qos_map_wb_t qos_map_wb;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_qos_map_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_QOSMAP);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    for (index = 0; index < p_map_db->map_list.count; index++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        qos_map_wb.oid = qos_map_id;
        qos_map_wb.index = index;
        sal_memcpy(&qos_map_wb.qos_map, &(p_map_db->map_list.list[index]), sizeof(sai_qos_map_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &qos_map_wb, (wb_data.key_len + wb_data.data_len));
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

out:
done:
    CTC_WB_FREE_BUFFER(wb_data.buffer);
    return status;
}

static sai_status_t
_ctc_sai_qos_map_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t qos_map_id = *(sai_object_id_t*)key;
    ctc_sai_qos_map_db_t* p_map_db = (ctc_sai_qos_map_db_t*)data;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, qos_map_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    p_map_db->map_list.list = (sai_qos_map_t*)mem_malloc(MEM_QUEUE_MODULE, p_map_db->map_list.count * sizeof(sai_qos_map_t));
    if (NULL == p_map_db->map_list.list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_qos_map_wb_reload_cb1(uint8 lchip)
{
    sai_status_t           ret = SAI_STATUS_SUCCESS;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    ctc_sai_qos_map_wb_t qos_map_wb;
    ctc_wb_query_t wb_query;

    sal_memset(&wb_query, 0, sizeof(wb_query));
    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_qos_map_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_QOSMAP);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
    offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
    entry_cnt++;
    sal_memcpy(&qos_map_wb, (uint8*)(wb_query.buffer) + offset,  (wb_query.key_len + wb_query.data_len));
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_wb.oid);
    if ((NULL == p_map_db) || (NULL == p_map_db->map_list.list))
    {
        continue;
    }

    sal_memcpy(&(p_map_db->map_list.list[qos_map_wb.index]), &qos_map_wb.qos_map,  sizeof(sai_qos_map_t));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }
    return ret;
}

#define ________SAI_DUMP________

static char*
_ctc_sai_qos_map_convert_map_type(sai_qos_map_type_t type)
{
    switch (type)
    {
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            return "DOT1P_TO_TC";
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            return "DOT1P_TO_COLOR";
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            return "DSCP_TO_TC";
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            return "DSCP_TO_COLOR";
        case SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
            return "TC_TO_QUEUE";
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            return "TC_AND_COLOR_TO_DSCP";
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            return "TC_AND_COLOR_TO_DOT1P";
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:
            return "MPLS_EXP_TO_TC";
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:
            return "MPLS_EXP_TO_COLOR";
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:
            return "TC_AND_COLOR_TO_MPLS_EXP";
        default:
            return "None";
    }
}

#define CTC_SAI_QOS_MAP_CONVERT_MAP_LIST(str, type, list)\
    switch (type)\
    {\
        case SAI_QOS_MAP_TYPE_DOT1P_TO_TC:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.dot1p, "-", (list)->value.tc);\
            break;\
        case SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.dot1p, "-", (list)->value.color);\
            break;\
        case SAI_QOS_MAP_TYPE_DSCP_TO_TC:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.dscp, "-", (list)->value.tc);\
            break;\
        case SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.dscp, "-", (list)->value.color);\
            break; \
        case SAI_QOS_MAP_TYPE_TC_TO_QUEUE: \
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.tc, "-", (list)->value.queue_index);\
            break;\
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:\
            sal_sprintf((str), "tc:%-7d color:%-4d %-10d", (list)->key.tc, (list)->key.color, (list)->value.dscp);\
            break;\
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:\
            sal_sprintf((str), "tc:%-7d color:%-4d %-10d", (list)->key.tc, (list)->key.color, (list)->value.dot1p);\
            break;\
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_TC:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.mpls_exp, "-", (list)->value.tc);\
            break;\
        case SAI_QOS_MAP_TYPE_MPLS_EXP_TO_COLOR:\
            sal_sprintf((str), "%-10d %-10s %-10d", (list)->key.mpls_exp, "-", (list)->value.color);\
            break;\
        case SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_MPLS_EXP:\
            sal_sprintf((str), "tc:%-7d color:%-4d %-10d", (list)->key.tc, (list)->key.color, (list)->value.mpls_exp);\
            break;\
        default:\
            sal_sprintf((str), "%s","None");\
            break;\
    }


static sai_status_t
_ctc_sai_qos_map_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t             qos_map_id = bucket_data->oid;
    ctc_sai_qos_map_db_t*       p_db       = (ctc_sai_qos_map_db_t*)bucket_data->data;
    ctc_sai_dump_grep_param_t*  p_dump     = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;
    sal_file_t                  p_file     = (sal_file_t)p_cb_data->value0;
    uint32*                     cnt        = (uint32 *)(p_cb_data->value1);
    uint32                      dump_detail= *((uint32 *)(p_cb_data->value3));
    uint32                      ii = 0;
    /*SYSTEM MODIFIED by xgu for bug 54639, for GCC-8.3 compile pass, modify from str[32]  to str[256], length will be more than 32, 2019/12/28 */
    char                        str[256] = {0};

    if (p_dump->key.key.object_id && (qos_map_id != p_dump->key.key.object_id))
    {/*Dump some DB by the given oid*/
        return SAI_STATUS_SUCCESS;
    }

    if (dump_detail)
    {
        if (0 == p_db->map_list.count)
        {
            return SAI_STATUS_SUCCESS;
        }
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-30s %-25s %-5s\n", "No.", "QoSMap_Table_Name", "Map_Type","Count");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "--------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4d QosMap_Table_%-16"PRIx64"  %-25s %-5d\n",
                        *cnt, qos_map_id, _ctc_sai_qos_map_convert_map_type(p_db->map_type),p_db->map_list.count);
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-6s %-10s %-10s %-10s\n", "Index", "KEY_1", "KEY_2", "VALUE");
        CTC_SAI_LOG_DUMP(p_file, "%s\n","---------------------------------------");
        for (ii = 0; ii < p_db->map_list.count; ii++)
        {
            CTC_SAI_QOS_MAP_CONVERT_MAP_LIST(str, p_db->map_type, &(p_db->map_list.list[ii]));
            CTC_SAI_LOG_DUMP(p_file, "%-6d %32s\n", ii, str);
        }
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    }
    else
    {
        CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%-16"PRIx64" 0x%-8x %-4d %-5d QosMap_Table_%-16"PRIx64"\n",
                        *cnt,qos_map_id, p_db->domain_bmp, p_db->map_type, p_db->map_list.count, qos_map_id);
    }
    (*cnt)++;
    return SAI_STATUS_SUCCESS;
}


void
ctc_sai_qos_map_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t* dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    uint32  dump_detail = 0;

    if (NULL == dump_grep_param)
    {
        return;
    }
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "%s\n", "# SAI QoS Map MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_QOS_MAP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "QoS Map");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_qos_map_db_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-10s %-4s %-5s %-30s\n", "No.","Qosmap_Oid", "Domain_BMP", "Type", "Count", "Map_List_Table");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        sai_cb_data.value3 = &dump_detail;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_QOS_MAP,
                                                (hash_traversal_fn)_ctc_sai_qos_map_dump_print_cb, (void*)(&sai_cb_data));

        num_cnt = 1;
        dump_detail = 1;
        CTC_SAI_LOG_DUMP(p_file, "\n");
        CTC_SAI_LOG_DUMP(p_file, ">>>>DUMP QoS Map List Table:\n");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_QOS_MAP,
                                                (hash_traversal_fn)_ctc_sai_qos_map_dump_print_cb, (void*)(&sai_cb_data));
    }
    CTC_SAI_LOG_DUMP(p_file, "\n");
}



#define ________SAI_API________

sai_status_t
ctc_sai_qos_map_create_map_id(
        _Out_ sai_object_id_t *qos_map_id,
        _In_ sai_object_id_t switch_id,
        _In_ uint32_t attr_count,
        _In_ const sai_attribute_t *attr_list)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    const sai_attribute_value_t *attr_value;
    uint32                   attr_index;
    sai_object_id_t qos_map_oid;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    uint32  ctc_qos_map_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_PTR_VALID_CHECK(qos_map_id);
    *qos_map_id = 0;

    sal_memset(&qos_map_oid, 0, sizeof(qos_map_oid));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    p_map_db = (ctc_sai_qos_map_db_t*)mem_malloc(MEM_QUEUE_MODULE, sizeof(ctc_sai_qos_map_db_t));
    if (NULL == p_map_db)
    {
        status = SAI_STATUS_NO_MEMORY;
        goto error_0;
    }
    sal_memset(p_map_db, 0, sizeof(ctc_sai_qos_map_db_t));

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QOS_MAP_ATTR_TYPE, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "Missing mandatory SAI_QOS_MAP_ATTR_TYPE attr\n");
        goto error_1;
    }
    else
    {
        p_map_db->map_type = attr_value->s32;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, &attr_value, &attr_index);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "Missing mandatory SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST attr\n");
        goto error_1;
    }
    else
    {
        if (attr_value->qosmap.count == 0)
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error_1;
        }
        p_map_db->map_list.count = attr_value->qosmap.count;
        p_map_db->map_list.list = (sai_qos_map_t*)mem_malloc(MEM_QUEUE_MODULE, p_map_db->map_list.count * sizeof(sai_qos_map_t));
        if (NULL == p_map_db->map_list.list)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto error_1;
        }
        sal_memcpy(p_map_db->map_list.list, attr_value->qosmap.list, p_map_db->map_list.count * sizeof(sai_qos_map_t));
    }
    //opf alloc qosmap id
    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_qos_map_id);
    if (CTC_SAI_ERROR(status))
    {
        goto error_2;
    }
    qos_map_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_QOS_MAP, lchip, 0, 0, ctc_qos_map_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, qos_map_oid, p_map_db), status, error_3);
    *qos_map_id = qos_map_oid;

    CTC_SAI_DB_UNLOCK(lchip);
    return SAI_STATUS_SUCCESS;

error_3:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_qos_map_id);
error_2:
    mem_free(p_map_db->map_list.list);
error_1:
    mem_free(p_map_db);
error_0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

sai_status_t
ctc_sai_qos_map_remove_map_id(
        _In_ sai_object_id_t qos_map_id)
{
    ctc_object_id_t ctc_object_id;
    ctc_sai_qos_map_db_t* p_map_db = NULL;
    sai_status_t status = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, qos_map_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QOS_MAP)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    p_map_db = ctc_sai_db_get_object_property(lchip, qos_map_id);
    if (NULL == p_map_db)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error_return;
    }
    if (p_map_db->domain_bmp)
    {
        status = SAI_STATUS_OBJECT_IN_USE;
        goto error_return;
    }
    mem_free(p_map_db->map_list.list);
    mem_free(p_map_db);
    ctc_sai_db_remove_object_property(lchip, qos_map_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value);

error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (status != SAI_STATUS_SUCCESS)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "remove qosmap id[0x%"PRIx64"] error! status=%d", qos_map_id, status);
    }
    return status;
}

sai_status_t
ctc_sai_qos_map_set_map_attribute(
        _In_ sai_object_id_t qos_map_id,
        _In_ const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = qos_map_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_PTR_VALID_CHECK(attr);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, qos_map_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QOS_MAP)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str, SAI_OBJECT_TYPE_QOS_MAP,  qos_map_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "Failed to set qos map attr:%d\n", status);
    }
    return status;
}

sai_status_t
ctc_sai_qos_map_get_map_attribute(
        _In_ sai_object_id_t qos_map_id,
        _In_ uint32_t attr_count,
        _Inout_ sai_attribute_t *attr_list)
{
    sai_object_key_t key ={ .key.object_id = qos_map_id };
    sai_status_t     status = 0;
    char             key_str[MAX_KEY_STR_LEN];
    uint8            loop = 0;
    uint8            lchip = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_QOS_MAP);
    CTC_SAI_PTR_VALID_CHECK(attr_list);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, qos_map_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    if (ctc_object_id.type != SAI_OBJECT_TYPE_QOS_MAP)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_QOS_MAP, loop, qos_map_attr_fn_entries, &attr_list[loop]), status, error_return);
        loop++ ;
    }
error_return:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_QOS_MAP, "Failed to get qosmap attr:%d\n", status);
    }
    return status;
}

sai_qos_map_api_t g_ctc_sai_qosmap_api = {
    ctc_sai_qos_map_create_map_id,
    ctc_sai_qos_map_remove_map_id,
    ctc_sai_qos_map_set_map_attribute,
    ctc_sai_qos_map_get_map_attribute
};

sai_status_t
ctc_sai_qos_map_api_init()
{
    ctc_sai_register_module_api(SAI_API_QOS_MAP, (void*)&g_ctc_sai_qosmap_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_qos_map_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_QOSMAP;
    wb_info.data_len = sizeof(ctc_sai_qos_map_db_t);
    wb_info.wb_sync_cb = _ctc_sai_qos_map_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_qos_map_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_qos_map_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_QOS_MAP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_qos_map_db_deinit(uint8 lchip)
{
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_QOS_MAP, (hash_traversal_fn)_ctc_sai_qos_map_db_deinit_cb, NULL);
    return SAI_STATUS_SUCCESS;
}

