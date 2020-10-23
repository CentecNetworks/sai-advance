#include "ctc_sai_vlan.h"
#include "ctc_sai_oid.h"
#include "ctc_sai_db.h"
#include "ctc_sai_fdb.h"
#include "ctc_sai_stp.h"
#include "ctc_sai_bridge.h"
#include "ctc_sai_acl.h"
#include "ctc_sai_ptp.h"
#include "ctc_sai_lag.h"
#include "ctc_sai_policer.h"

static sai_status_t
_ctc_sai_vlan_mapping_user_vlan( uint8 lchip,
                                uint32_t      attr_count,
                                const sai_attribute_t *attr_list,
                                ctc_vlan_uservlan_t *uservlan)
{
    sai_status_t status = 0;
    const sai_attribute_value_t*vid = NULL ;
    uint32_t  vid_index = 0;
    uint32 fid = 0; /*alloc fid  (0~4k) for 1Q bridge */

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_VLAN_ID, &vid, &vid_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_VLAN, &fid);
    if (status)
    {
        return  status;
    }

    uservlan->vlan_id = vid->u16;  /*mapping*/
    uservlan->user_vlanptr = fid;  /*alloc fid  (0~4k) for 1Q bridge */
    uservlan->fid = fid;           /*alloc fid  (0~4k) for 1Q bridge */
    uservlan->flag = 0;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_vlan_set_unknown_pkt_action(uint8 lchip, uint16 fid, uint32 swith_action_type, uint32 vlan_action_type, uint8 fdb_unknown_type)
{
    uint8 drop = 0;
    uint8 copy = 0;
    uint32 ctc_drop_action[3] =
    {
        CTC_L2_FID_PROP_DROP_UNKNOWN_UCAST, CTC_L2_FID_PROP_DROP_UNKNOWN_MCAST, CTC_L2_FID_PROP_DROP_BCAST
    };
    uint32 ctc_copy_action[3] =
    {
        CTC_L2_FID_PROP_UNKNOWN_UCAST_COPY_TO_CPU, CTC_L2_FID_PROP_UNKNOWN_MCAST_COPY_TO_CPU, CTC_L2_FID_PROP_BCAST_COPY_TO_CPU
    };

    switch(swith_action_type)
    {
    case SAI_PACKET_ACTION_DROP:
        drop = 1;
        break;
    case SAI_PACKET_ACTION_COPY:
        copy = 1;
        break;
    case SAI_PACKET_ACTION_TRAP: /** This is a combination of SAI packet action COPY and DROP. */
        drop = 1;
        copy = 1;
        break;
    case SAI_PACKET_ACTION_LOG:  /** This is a combination of SAI packet action COPY and FORWARD. */
        copy = 1;
        break;
    case SAI_PACKET_ACTION_DENY: /** This is a combination of SAI packet action COPY_CANCEL and DROP */
        drop = 1;
        break;
    default:
        break;
    }

    if ((0 == drop)&&(SAI_VLAN_FLOOD_CONTROL_TYPE_NONE == vlan_action_type)) /* only reference to fwd */
    {
        drop = 1;
    }

    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_set_fid_property(lchip, fid, ctc_drop_action[fdb_unknown_type], drop));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_set_fid_property(lchip, fid, ctc_copy_action[fdb_unknown_type], copy));
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_vlan_set_info(sai_object_key_t *key, const sai_attribute_t* attr)
{
    ctc_object_id_t ctc_object_id1;
    ctc_security_learn_limit_t learn_limit;
    ctc_sai_vlan_user_t *p_db_vlan;
    ctc_sai_ptp_db_t* p_ptp_db = NULL;
    uint16 vlan_id = 0;
    uint16 vlan_ptr = 0;
    uint8 i = 0;
    uint8 lchip = 0;
    uint8 step = 0;
    uint8 chip_type = 0;
    uint8 ingress_acl_num = 8;
    uint8 egress_acl_num = 3;
    bool is_enable = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    ctc_stats_statsid_t stats_statsid_in;
    ctc_stats_statsid_t stats_statsid_eg;
    sai_status_t status = 0;
    ctc_acl_property_t acl_prop;
    bool enable = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_db_vlan = ctc_sai_db_get_object_property(lchip,  key->key.object_id);
    if (NULL == p_db_vlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    vlan_id = p_db_vlan->vlan_id;
    vlan_ptr =  p_db_vlan->user_vlanptr;
    chip_type = ctcs_get_chip_type(lchip);
    switch(attr->id)
    {
    case  SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
        sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
        /*use default action*/
        learn_limit.limit_action = CTC_MACLIMIT_ACTION_FWD;
        learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_VLAN;
        learn_limit.vlan = vlan_ptr;
        if (attr->value.u32 == 0)
        {
            learn_limit.limit_num = 0xFFFFFFFF;
        }
        else
        {
            learn_limit.limit_num = attr->value.u32;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_set_learn_limit(lchip, &learn_limit));
        break;
    case  SAI_VLAN_ATTR_STP_INSTANCE:
        CTC_SAI_ERROR_RETURN(ctc_sai_stp_set_instance(lchip, vlan_id, vlan_ptr,  attr->value.oid, 1));
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_STP, attr->value.oid, &ctc_object_id1);
        p_db_vlan->stp_id = (uint8)ctc_object_id1.value;
        break;
    case  SAI_VLAN_ATTR_LEARN_DISABLE:
        is_enable = attr->value.booldata ? 0 : 1;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_learning_en(lchip, vlan_ptr, is_enable));
        break;
    case SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
    case SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
    case SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
        {
            if ((SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE == attr->id) && (chip_type == CTC_CHIP_GOLDENGATE))
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
            if ((SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP == attr->value.s32) || (SAI_VLAN_FLOOD_CONTROL_TYPE_COMBINED == attr->value.s32))
            {
                return SAI_STATUS_NOT_SUPPORTED;
            }
            if ((SAI_VLAN_FLOOD_CONTROL_TYPE_ALL > attr->value.s32) || (SAI_VLAN_FLOOD_CONTROL_TYPE_COMBINED < attr->value.s32))
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }

            step = SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE - SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE;
            p_db_vlan->ukwn_flood_ctr[(attr->id - SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE) / step] = attr->value.s32;
            p_switch_master = ctc_sai_get_switch_property(lchip);
            _ctc_sai_vlan_set_unknown_pkt_action(lchip, p_db_vlan->user_vlanptr, 
                                                p_switch_master->fdb_miss_action[(attr->id - SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE) / step], 
                                                p_db_vlan->ukwn_flood_ctr[(attr->id - SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE) / step],
                                                 (attr->id - SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE) / step);
            break;
        }
    case SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_set_fid_property(lchip, vlan_ptr, CTC_L2_FID_PROP_IGMP_SNOOPING, attr->value.booldata));
        break;
    case SAI_VLAN_ATTR_META_DATA:
        if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
        {
            ingress_acl_num = 8;
            egress_acl_num = 3;
        }

        for (i = 0; i < ingress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_INGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, vlan_ptr, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_acl_property(lchip, vlan_ptr, &acl_prop));
        }

        for (i = 0; i < egress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, vlan_ptr, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr->value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_acl_property(lchip, vlan_ptr, &acl_prop));
        }
        break;
    case SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
        if (attr->value.booldata)
        {
            if (p_db_vlan->stats_id_in)
            {
                CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan stats already is enable\n");
                return SAI_STATUS_INVALID_PARAMETER;
            }

            if (p_db_vlan->stats_id_eg)
            {
                CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan stats already is enable\n");
                return SAI_STATUS_INVALID_PARAMETER;
            }

            if ((chip_type == CTC_CHIP_DUET2) || (chip_type == CTC_CHIP_TSINGMA))
            {
                sal_memset(&stats_statsid_in, 0, sizeof(ctc_stats_statsid_t));
                stats_statsid_in.dir = CTC_INGRESS;
                stats_statsid_in.type = CTC_STATS_STATSID_TYPE_VLAN;
                stats_statsid_in.stats_id = p_db_vlan->user_vlanptr;

                status = ctcs_stats_create_statsid(lchip, &stats_statsid_in);

                if (CTC_E_NO_RESOURCE == status)
                {
                    return SAI_STATUS_INSUFFICIENT_RESOURCES;
                }
                else
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_direction_property(lchip, p_db_vlan->user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_INGRESS, stats_statsid_in.stats_id), status, error1);
                }

                sal_memset(&stats_statsid_eg, 0, sizeof(ctc_stats_statsid_t));
                stats_statsid_eg.dir = CTC_EGRESS;
                stats_statsid_eg.type = CTC_STATS_STATSID_TYPE_VLAN;
                stats_statsid_eg.stats_id = p_db_vlan->user_vlanptr + VLAN_NUM;

                status = ctcs_stats_create_statsid(lchip, &stats_statsid_eg);

                if (CTC_E_NO_RESOURCE == status)
                {
                    goto error1;
                }
                else
                {
                    CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_direction_property(lchip, p_db_vlan->user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_EGRESS, stats_statsid_eg.stats_id), status, error2);
                }

                p_db_vlan->stats_id_in = stats_statsid_in.stats_id;
                p_db_vlan->stats_id_eg = stats_statsid_eg.stats_id;
            }
        }
        else
        {
            if (!p_db_vlan->stats_id_in)
            {
                CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan stats already is disable\n");
                return SAI_STATUS_INVALID_PARAMETER;
            }

            if (!p_db_vlan->stats_id_eg)
            {
                CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan stats already is disable\n");
                return SAI_STATUS_INVALID_PARAMETER;
            }
            ctcs_vlan_set_direction_property(lchip, p_db_vlan->user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_INGRESS, 0);
            ctcs_vlan_set_direction_property(lchip, p_db_vlan->user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_EGRESS, 0);
            ctcs_stats_destroy_statsid(lchip, p_db_vlan->stats_id_in);
            ctcs_stats_destroy_statsid(lchip, p_db_vlan->stats_id_eg);
            p_db_vlan->stats_id_in = 0;
            p_db_vlan->stats_id_eg = 0;
        }
        break;
    case SAI_VLAN_ATTR_PTP_DOMAIN_ID:           // the value cannnot be 0
        if(SAI_NULL_OBJECT_ID == attr->value.oid)
        {
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_PTP_EN, FALSE));
            p_db_vlan->ptp_domain_id= 0;
        }
        else
        {
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, attr->value.oid, &ctc_object_id1);
            p_ptp_db = ctc_sai_db_get_object_property(lchip,  attr->value.oid);
            if ((NULL == p_ptp_db)||(SAI_OBJECT_TYPE_PTP_DOMAIN != ctc_object_id1.type))
            {
                CTC_SAI_LOG_ERROR(SAI_API_PORT, "ptp domain not found \n");
                return SAI_STATUS_INVALID_PARAMETER;
            }

            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, vlan_ptr, CTC_VLAN_PROP_PTP_EN, TRUE));
            p_db_vlan->ptp_domain_id= ctc_object_id1.value;
        }
        break;

    case SAI_VLAN_ATTR_POLICER_ID: 
        if(SAI_NULL_OBJECT_ID != attr->value.oid)
        {
            enable = 1;
        }
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr->value.oid, &ctc_object_id1);
        
        CTC_SAI_ERROR_RETURN(ctc_sai_policer_vlan_set_policer(lchip, p_db_vlan->vlan_id, enable ? ctc_object_id1.value : p_db_vlan->policer_id, enable));

        //revert old policer oid
        if (p_db_vlan->policer_id && ctc_object_id1.value && (p_db_vlan->policer_id != ctc_object_id1.value) )
        {
            CTC_SAI_ERROR_RETURN(ctc_sai_policer_revert_policer(lchip, p_db_vlan->policer_id));
        }

        p_db_vlan->policer_id = enable ? ctc_object_id1.value : 0;
        break;
        
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED;

    }

    return  SAI_STATUS_SUCCESS;

error2:
    ctcs_stats_destroy_statsid(lchip, stats_statsid_eg.stats_id);
error1:
    ctcs_vlan_set_direction_property(lchip, p_db_vlan->user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_INGRESS, 0);
    ctcs_stats_destroy_statsid(lchip, stats_statsid_in.stats_id);

    return SAI_STATUS_FAILURE;
}

sai_status_t
ctc_sai_vlan_get_info(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    ctc_object_id_t ctc_object_id;
    uint32 bit_cnt = 0;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] ;
    uint32 port_num = 0;
    sai_object_id_t*vlan_members;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_security_learn_limit_t learn_limit;
    uint8 stp_id = 0;
    bool is_enable = 0;
    ctc_sai_vlan_user_t *p_db_vlan;
    uint16 vlan_ptr = 0;
    uint32 u_value_32 = 0;
    uint8 lchip = 0;
    uint8 gchip = 0;
    uint32 gport = 0;
    uint32 ctc_ptp_domain_id = 0;
    sai_object_id_t *p_bounded_oid = NULL;
    ctc_acl_property_t acl_prop;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, key->key.object_id, &ctc_object_id);
    lchip = ctc_object_id.lchip;
    uint32 lag_gport = 0;

    p_db_vlan = ctc_sai_db_get_object_property(ctc_object_id.lchip, key->key.object_id);
    if (NULL == p_db_vlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    vlan_ptr =  p_db_vlan->user_vlanptr;
    switch(attr->id)
    {

    case SAI_VLAN_ATTR_INGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_INGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;
    case SAI_VLAN_ATTR_EGRESS_ACL:
        p_bounded_oid = ctc_sai_db_entry_property_get(lchip, CTC_SAI_DB_ENTRY_TYPE_ACL_BIND_EGRESS, (void*)(&key->key.object_id));
        attr->value.oid = (p_bounded_oid ? *p_bounded_oid : SAI_NULL_OBJECT_ID);
        break;
    case SAI_VLAN_ATTR_VLAN_ID:
        attr->value.u16 = p_db_vlan->vlan_id;
        break;
    case  SAI_VLAN_ATTR_MEMBER_LIST:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(ctc_object_id.lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
        vlan_members =  mem_malloc(MEM_VLAN_MODULE, sizeof(sai_object_id_t)*capability[CTC_GLOBAL_CAPABILITY_MAX_PORT_NUM]);
        if (NULL == vlan_members)
        {
            return SAI_STATUS_NO_MEMORY;
        }

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_vlan->vlan_member_port_bind_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_vlan->vlan_member_port_bind_bits, bit_cnt))
            {
                gport = CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt);
                vlan_members[port_num++] =  ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN_MEMBER, ctc_object_id.lchip, 0, ctc_object_id.value, gport);
            }
        }

        for (bit_cnt = 0; bit_cnt < sizeof(p_db_vlan->vlan_member_lag_bind_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_vlan->vlan_member_lag_bind_bits, bit_cnt))
            {
                lag_gport = CTC_MAP_LPORT_TO_GPORT(0x1f, bit_cnt);
                vlan_members[port_num++] =  ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN_MEMBER, ctc_object_id.lchip, 0, ctc_object_id.value, lag_gport);
            }
        }

        status = ctc_sai_fill_object_list(sizeof(sai_object_id_t), vlan_members, port_num, &attr->value.objlist);
        mem_free(vlan_members);
        break;
    case  SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
        sal_memset(&learn_limit, 0, sizeof(ctc_security_learn_limit_t));
        learn_limit.limit_type = CTC_SECURITY_LEARN_LIMIT_TYPE_VLAN;
        learn_limit.vlan = vlan_ptr;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_mac_security_get_learn_limit(ctc_object_id.lchip, &learn_limit));
        if (0xFFFFFFFF == learn_limit.limit_num)
        {
            /*Zero means learning limit is disabled.*/
            attr->value.u32 = 0;
        }
        else
        {
            attr->value.u32 = learn_limit.limit_num;
        }
        break;
    case  SAI_VLAN_ATTR_STP_INSTANCE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_stp_get_vlan_stpid(ctc_object_id.lchip, vlan_ptr, &stp_id));
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, ctc_object_id.lchip, 0, 0, (uint32) stp_id);
        break;
    case  SAI_VLAN_ATTR_LEARN_DISABLE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_learning_en(ctc_object_id.lchip, vlan_ptr, &is_enable));
        attr->value.booldata = is_enable ? 0 : 1;
        break;
    case SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fid_property(ctc_object_id.lchip, vlan_ptr, CTC_L2_FID_PROP_DROP_UNKNOWN_UCAST, &u_value_32));
        attr->value.s32 = u_value_32;
        break;
    case SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fid_property(ctc_object_id.lchip, vlan_ptr, CTC_L2_FID_PROP_DROP_UNKNOWN_MCAST, &u_value_32));
        attr->value.s32 = u_value_32;
        break;
    case SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fid_property(ctc_object_id.lchip, vlan_ptr, CTC_L2_FID_PROP_DROP_BCAST, &u_value_32));
        attr->value.s32 = u_value_32;
        break;

    case SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
        CTC_SAI_CTC_ERROR_RETURN(ctcs_l2_get_fid_property(ctc_object_id.lchip, vlan_ptr, CTC_L2_FID_PROP_IGMP_SNOOPING, &u_value_32));
        attr->value.booldata = u_value_32;
        break;
    case SAI_VLAN_ATTR_META_DATA:
        sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
        acl_prop.direction = CTC_INGRESS;
        acl_prop.acl_priority = 0;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, vlan_ptr, &acl_prop));
        attr->value.u32 = CTC_SAI_META_DATA_CTC_TO_SAI(acl_prop.class_id);
        break;
    case SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
        if ((p_db_vlan->stats_id_in)&&(p_db_vlan->stats_id_eg))
        {
            attr->value.booldata = 1;
        }
        else
        {
            attr->value.booldata = 0;
        }
        break;
    case SAI_VLAN_ATTR_PTP_DOMAIN_ID:           // the value cannnot be 0
        ctc_ptp_domain_id = p_db_vlan->ptp_domain_id;
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_PTP_DOMAIN, lchip, 0, 0, ctc_ptp_domain_id);
        break;
    case SAI_VLAN_ATTR_POLICER_ID: 
        attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_POLICER, lchip, 0, 0, p_db_vlan->policer_id);
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "vlan attribute not implement\n");
        return  SAI_STATUS_NOT_IMPLEMENTED + attr_idx;

    }

    return  status;
}

sai_status_t
ctc_sai_vlan_get_vlan_property(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint16 vlan_ptr = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_oid_get_vlanptr(key->key.object_id, &vlan_ptr);

    p_dbvlan = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_dbvlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    switch(attr->id)
    {
    case SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
        attr->value.s32 = p_dbvlan->ipv4_mcast_lookup_type;
        break;
    case  SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
        attr->value.s32 = p_dbvlan->ipv6_mcast_lookup_type;
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Unsupported attribute id %d\n", attr->id);
        return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}
sai_status_t
ctc_sai_vlan_set_vlan_property(sai_object_key_t *key,  const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    uint16 vlan_ptr = 0;
    uint32 value = 0;
    uint32 value1 = 0;
    ctc_vlan_property_t vlan_prop = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL;


    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctc_sai_oid_get_vlanptr(key->key.object_id, &vlan_ptr);

    p_dbvlan = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_dbvlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    if ((attr->value.s32 < SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA) || (attr->value.s32 > SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG ))
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    switch(attr->id)
    {
    case SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
        vlan_prop = CTC_VLAN_PROP_IPV4_BASED_L2MC;
        value = attr->value.s32;
        p_dbvlan->ipv4_mcast_lookup_type = attr->value.s32;
        break;
    case  SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
        vlan_prop = CTC_VLAN_PROP_IPV6_BASED_L2MC;
        value = attr->value.s32;
        p_dbvlan->ipv6_mcast_lookup_type = attr->value.s32;
        break;
    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Unsupported attribute id %d\n", attr->id);
        return SAI_STATUS_NOT_SUPPORTED;
    }
    value1 = value ? 1 : 0;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_property(lchip, vlan_ptr, vlan_prop, value1));

    return SAI_STATUS_SUCCESS;
}

static ctc_sai_attr_fn_entry_t  vlan_attr_fn_entries[] =
{
    { SAI_VLAN_ATTR_VLAN_ID,
      ctc_sai_vlan_get_info,
      NULL},
    { SAI_VLAN_ATTR_MEMBER_LIST,
      ctc_sai_vlan_get_info,
      NULL},
    { SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
    { SAI_VLAN_ATTR_STP_INSTANCE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
    { SAI_VLAN_ATTR_LEARN_DISABLE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info},
    { SAI_VLAN_ATTR_INGRESS_ACL,
      ctc_sai_vlan_get_info,
      ctc_sai_acl_bind_point_set},
    { SAI_VLAN_ATTR_EGRESS_ACL,
      ctc_sai_vlan_get_info,
      ctc_sai_acl_bind_point_set},
    { SAI_VLAN_ATTR_META_DATA,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE,
      ctc_sai_vlan_get_vlan_property,
      ctc_sai_vlan_set_vlan_property },
      { SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE,
      ctc_sai_vlan_get_vlan_property,
      ctc_sai_vlan_set_vlan_property },
      { SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_PTP_DOMAIN_ID,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { SAI_VLAN_ATTR_POLICER_ID,
      ctc_sai_vlan_get_info,
      ctc_sai_vlan_set_info },
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};


sai_status_t ctc_sai_vlan_get_vlan_member(sai_object_key_t *key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint16  vlanptr;
    uint32 gport;
    sai_status_t         status;
    uint8 lchip = 0;
    ctc_object_id_t   ctc_bridge_port_id;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    sal_memset(&ctc_bridge_port_id, 0, sizeof(ctc_object_id_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vlan_member_id(key->key.object_id, &vlanptr, &gport));
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    switch (attr->id)
    {
        case SAI_VLAN_MEMBER_ATTR_VLAN_ID:
            attr->value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, (uint32) vlanptr);
            break;

        case SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID:
            ctc_bridge_port_id.lchip = lchip;
            ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
            ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
            ctc_bridge_port_id.value2 = 0;
            ctc_bridge_port_id.value = gport;
            CTC_SAI_ERROR_RETURN(ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, &attr->value.oid));
            break;

        default:
            CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Unsupported attribute id %d\n", attr->id);
            status = SAI_STATUS_INVALID_ATTR_VALUE_0 + attr->id;
            return status;

    }

    return SAI_STATUS_SUCCESS;
}


static sai_status_t ctc_sai_vlan_get_vlan_member_tag(sai_object_key_t *key,  sai_attribute_t* attr, uint32 attr_idx)
{
    uint16  vlan_ptr;
    uint32 gport;
    ctc_port_bitmap_t port_bitmap_tagged;
    ctc_port_bitmap_t port_bitmap ;
    uint32 capability[CTC_GLOBAL_CAPABILITY_MAX] ;
    uint8 lchip = 0;
    uint8 gchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vlan_member_id(key->key.object_id, &vlan_ptr, &gport));
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);

    sal_memset(port_bitmap_tagged, 0, sizeof(port_bitmap_tagged));
    sal_memset(port_bitmap, 0, sizeof(port_bitmap));
    sal_memset(capability, 0, sizeof(capability));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_CHIP_CAPABILITY, capability));
    if (CTC_MAP_GPORT_TO_LPORT(gport) > capability[CTC_GLOBAL_CAPABILITY_MAX_PORT_NUM])
    {
        return SAI_STATUS_INVALID_PORT_NUMBER;

    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_ports(lchip, vlan_ptr, gchip, port_bitmap));
    if (!CTC_BMP_ISSET(port_bitmap, CTC_MAP_GPORT_TO_LPORT(gport)))
    {
        return SAI_STATUS_INVALID_PORT_MEMBER;
    }

    /*TODO:SAI_VLAN_TAGGING_MODE_PRIORITY_TAGGED*/

    CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_tagged_ports(lchip, vlan_ptr, gchip, port_bitmap_tagged));
    if (CTC_BMP_ISSET(port_bitmap_tagged, CTC_MAP_GPORT_TO_LPORT(gport)))
    {
        attr->value.s32 = SAI_VLAN_TAGGING_MODE_TAGGED;
    }
    else
    {
        attr->value.s32 = SAI_VLAN_TAGGING_MODE_UNTAGGED;
    }


    return SAI_STATUS_SUCCESS;
}


sai_status_t ctc_sai_vlan_get_ctc_tag( sai_vlan_tagging_mode_t      mode,
                                         uint8* tagenable )
{
    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_PTR_VALID_CHECK(tagenable);
    switch (mode) {
    case SAI_VLAN_TAGGING_MODE_UNTAGGED:
        *tagenable = false;
        break;

    case SAI_VLAN_TAGGING_MODE_TAGGED:
        *tagenable = true;
        break;

    case SAI_VLAN_TAGGING_MODE_PRIORITY_TAGGED:
        return SAI_STATUS_NOT_IMPLEMENTED;

    default:
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Invalid tagging mode %d\n", mode);
        return SAI_STATUS_INVALID_PARAMETER;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t ctc_sai_vlan_set_vlan_member_tag(sai_object_key_t *key,  const sai_attribute_t* attr)
{
    uint32 gport;
    uint8 tagenable;
    uint16 vlanptr;
    uint8 lchip = 0;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vlan_member_id(key->key.object_id, &vlanptr, &gport));
    CTC_SAI_ERROR_RETURN(ctc_sai_vlan_get_ctc_tag(attr->value.s32, &tagenable));
    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    ctcs_get_gchip_id(lchip, &gchip);

    if(CTC_IS_LINKAGG_PORT(gport))
    {
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
        if (NULL == p_db_lag)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), tagenable));
            }
        }
    }
    else
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, gport, tagenable));
    }

    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t vlan_member_attr_fn_entries[] = {
    { SAI_VLAN_MEMBER_ATTR_VLAN_ID,
      ctc_sai_vlan_get_vlan_member,
      NULL },
    { SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID,
      ctc_sai_vlan_get_vlan_member,
      NULL },
    { SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE,
      ctc_sai_vlan_get_vlan_member_tag,
      ctc_sai_vlan_set_vlan_member_tag},
      { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static sai_status_t _ctc_sai_vlan_create_vlan_member( sai_object_id_t     * vlan_member_id,
                                                     sai_object_id_t        switch_id,
                                                     uint32_t               attr_count,
                                                     const sai_attribute_t *attr_list)
{
    const sai_attribute_value_t *vid = NULL, *bridgeportvalue = NULL, *tagging = NULL;
    uint32_t    vid_index, bridge_port_index, tagging_index;
    uint16_t                     vlanptr = 0;
    sai_status_t                 status = SAI_STATUS_SUCCESS;
    uint32_t gport = 0;
    ctc_sai_bridge_port_t* p_bridge_port = NULL;
    uint8 lchip= 0;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;
    ctc_sai_vlan_user_t* p_db_vlan = NULL;

    if (NULL == vlan_member_id || 0 == attr_count || NULL == attr_list )
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, " vlan member parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    ctc_sai_oid_get_lchip(switch_id, &lchip);
    ctcs_get_gchip_id(lchip, &gchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_MEMBER_ATTR_VLAN_ID, &vid, &vid_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    p_db_vlan = ctc_sai_db_get_object_property(lchip, vid->oid);
    if (NULL == p_db_vlan)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_ERROR_RETURN (ctc_sai_oid_get_vlanptr(vid->oid, &vlanptr));
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, &bridgeportvalue, &bridge_port_index);
    if(SAI_STATUS_SUCCESS != status)
    {
        return SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
    }

    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridgeportvalue->oid);
    if (NULL == p_bridge_port || SAI_BRIDGE_PORT_TYPE_PORT  != p_bridge_port->port_type )
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Bridge port info wrong\n");
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    gport = p_bridge_port->gport;

    if (CTC_IS_LINKAGG_PORT(gport))
    {
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_add_port(lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt)), status, out);
            }
        }
    }
    else
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_add_port(lchip, vlanptr, gport), status, out);
    }

    *vlan_member_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN_MEMBER, lchip, 0, vlanptr, gport);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, &tagging, &tagging_index);

    sai_object_key_t  key;
    key.key.object_id = *vlan_member_id;

    if ( SAI_STATUS_SUCCESS == status )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_vlan_member_tag(&key, &attr_list[tagging_index] ), status, error1);
    }
    else
    {
           if(CTC_IS_LINKAGG_PORT(gport))
            {
                sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
                p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
                if (NULL == p_db_lag)
                {
                    return SAI_STATUS_INVALID_OBJECT_ID;
                }
                for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
                {
                    if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
                    {
                        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), false));
                    }
                }
            }
            else
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, gport, false));
            }

    }


    if(CTC_IS_LINKAGG_PORT(gport))
    {
        p_db_vlan->vlan_member_lag_bind_count++;
        CTC_BMP_SET(p_db_vlan->vlan_member_lag_bind_bits, (uint8)gport);
    }
    else
    {
        p_db_vlan->vlan_member_port_bind_count++;
        CTC_BMP_SET(p_db_vlan->vlan_member_port_bind_bits, CTC_MAP_GPORT_TO_LPORT(gport));
    }


    CTC_BMP_SET(p_bridge_port->vlan_member_bind_bits, vlanptr);
    p_bridge_port->vlan_member_bind_count++;


    CTC_BMP_SET(p_bridge_port->vlan_member_bind_bits, vlanptr);
    p_bridge_port->vlan_member_bind_count++;
    if( NULL == tagging)
    {
        p_bridge_port->vlan_member_tag_mode[vlanptr] = false;
    }
    else
    {
        p_bridge_port->vlan_member_tag_mode[vlanptr] = tagging->s32;
    }


    goto out;

    error1:
    if (CTC_IS_LINKAGG_PORT(gport))
    {
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
        if (NULL == p_db_lag)
        {
            status = SAI_STATUS_INVALID_OBJECT_ID;
            goto out;
        }
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                ctcs_vlan_remove_port( lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt));
            }
        }
    }
    else
    {
        ctcs_vlan_remove_port( lchip, vlanptr, gport);
    }

    out:
    return status;
}

static sai_status_t _ctc_sai_vlan_remove_vlan_member( sai_object_id_t vlan_member_id)
{
    uint16 vlan_id;
    uint32  gport;
    uint8 lchip;
    sai_object_id_t vlan_oid;
    uint16 vlanptr;
    //ctc_object_id_t ctc_bridge_port_id = {0};
    //sai_object_id_t bridge_port_id;
    //sai_attribute_t attr_list[2];
    //sai_object_id_t        switch_id;
    uint32 bit_cnt = 0;
    ctc_sai_lag_info_t *p_db_lag;
    uint8 gchip = 0;
    sai_object_id_t sai_lag_id;
    ctc_sai_bridge_port_t* p_bridge_port;
    sai_object_id_t  bridge_port_oid;
    ctc_sai_vlan_user_t* p_db_vlan = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_member_id, &lchip));
    ctcs_get_gchip_id(lchip, &gchip);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vlan_member_id(vlan_member_id, &vlan_id, &gport));

    vlan_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, (uint32) vlan_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_vlanptr(vlan_oid, &vlanptr));

    p_db_vlan = ctc_sai_db_get_object_property(lchip, vlan_oid);
    if (NULL == p_db_vlan)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (CTC_IS_LINKAGG_PORT(gport))
    {
        sai_lag_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_LAG, lchip, 0, 0, gport);
        p_db_lag = ctc_sai_db_get_object_property(lchip, sai_lag_id);
        if (NULL == p_db_lag)
        {
            return SAI_STATUS_INVALID_OBJECT_ID;
        }
        for (bit_cnt = 0; bit_cnt < sizeof(p_db_lag->member_ports_bits)*8; bit_cnt++)
        {
            if (CTC_BMP_ISSET(p_db_lag->member_ports_bits, bit_cnt))
            {
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_remove_port(lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt)));
                CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, CTC_MAP_LPORT_TO_GPORT(gchip, bit_cnt), true));

            }
        }
    }
    else
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_remove_port(lchip, vlanptr, gport));
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_tagged_port( lchip, vlanptr, gport, true));
    }

/*
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32) gchip);
    ctc_bridge_port_id.lchip = lchip;
    ctc_bridge_port_id.type = SAI_OBJECT_TYPE_BRIDGE_PORT;
    ctc_bridge_port_id.sub_type = SAI_BRIDGE_PORT_TYPE_PORT;
    ctc_bridge_port_id.value = gport;
    ctc_bridge_port_id.value2 = 0;
    ctc_sai_get_sai_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, &ctc_bridge_port_id, &bridge_port_id);
    attr_list[0].id = SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID;
    attr_list[0].value.oid = bridge_port_id;
    attr_list[1].id = SAI_FDB_FLUSH_ATTR_BV_ID;
    attr_list[1].value.oid = vlan_oid;
    ctc_sai_fdb_flush_fdb(switch_id, 2, attr_list);
*/

    if(CTC_IS_LINKAGG_PORT(gport))
    {
        p_db_vlan->vlan_member_lag_bind_count--;
        CTC_BMP_UNSET(p_db_vlan->vlan_member_lag_bind_bits, (uint8)gport);
    }
    else
    {
        p_db_vlan->vlan_member_port_bind_count--;
        CTC_BMP_UNSET(p_db_vlan->vlan_member_port_bind_bits, CTC_MAP_GPORT_TO_LPORT(gport));
    }


    bridge_port_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_BRIDGE_PORT, lchip, 0, SAI_BRIDGE_PORT_TYPE_PORT, gport);
    p_bridge_port = ctc_sai_db_get_object_property(lchip, bridge_port_oid);
    CTC_BMP_UNSET(p_bridge_port->vlan_member_bind_bits, vlanptr);
    p_bridge_port->vlan_member_bind_count--;
    p_bridge_port->vlan_member_tag_mode[vlanptr] = SAI_VLAN_TAGGING_MODE_UNTAGGED;

    return SAI_STATUS_SUCCESS;
}

sai_status_t ctc_sai_vlan_get_vlan_id(sai_object_id_t oid, uint16 *vlan_id)
{
    ctc_object_id_t* ctc_oid ;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;

    ctc_oid = (ctc_object_id_t*)&oid;
    p_dbvlan = ctc_sai_db_get_object_property(ctc_oid->lchip, oid);
    if (NULL == p_dbvlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if (vlan_id)
    {
        *vlan_id = p_dbvlan->vlan_id;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_vlan_get_vlan_id_from_vlan_ptr(uint8 lchip, uint16 vlan_ptr, uint16 *vlan_id)
{
    sai_object_id_t oid;
    ctc_object_id_t* ctc_oid ;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;

    oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, (uint32) vlan_ptr);

    ctc_oid = (ctc_object_id_t*)&oid;
    p_dbvlan = ctc_sai_db_get_object_property(ctc_oid->lchip, oid);
    if (NULL == p_dbvlan)
    {
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    if (vlan_id)
    {
        *vlan_id = p_dbvlan->vlan_id;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_vlan_get_vlan_ptr_from_db(ctc_sai_oid_property_t* bucket_data, ctc_sai_vlan_traverse_param_t* user_data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_vlan_user_t* p_dbvlan = (ctc_sai_vlan_user_t*)(bucket_data->data);

    if (p_dbvlan->vlan_id == user_data->vlan_id)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, bucket_data->oid, &ctc_object_id);
        user_data->vlan_ptr = ctc_object_id.value;
        user_data->is_found = TRUE;
    }
    return status;
}

sai_status_t
ctc_sai_vlan_get_vlan_ptr_from_vlan_id(uint8 lchip, uint16 vlan_id, uint16 *vlan_ptr)
{
    ctc_sai_vlan_traverse_param_t vlan_traser_para;

    sal_memset(&vlan_traser_para, 0, sizeof(ctc_sai_vlan_traverse_param_t));
    vlan_traser_para.vlan_id = vlan_id;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_VLAN,
                                             (hash_traversal_fn)_ctc_sai_vlan_get_vlan_ptr_from_db, (void*)(&vlan_traser_para));
    if (vlan_traser_para.is_found)
    {
        *vlan_ptr = vlan_traser_para.vlan_ptr;
    }
    else
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_vlan_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_sai_vlan_user_t *p_dbvlan = (ctc_sai_vlan_user_t*)data;
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_VLAN, p_dbvlan->user_vlanptr));
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_vlan_set_unkown_pkt_action_cb(ctc_sai_oid_property_t* p_vlan, void* user_data)
{
    uint8 lchip = 0;
    uint8 fdb_unknown_type = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    ctc_sai_vlan_user_t* p_vlan_usr = (ctc_sai_vlan_user_t*)p_vlan->data;
    ctc_sai_db_traverse_param_t *p_vlan_cb = (ctc_sai_db_traverse_param_t*)user_data;
    lchip = p_vlan_cb->lchip;
    p_switch_master = (ctc_sai_switch_master_t*)p_vlan_cb->value0;
    fdb_unknown_type = *((uint8*)p_vlan_cb->value1);
    _ctc_sai_vlan_set_unknown_pkt_action(lchip, p_vlan_usr->user_vlanptr, p_switch_master->fdb_miss_action[fdb_unknown_type], p_vlan_usr->ukwn_flood_ctr[fdb_unknown_type], fdb_unknown_type);

    return SAI_STATUS_SUCCESS;
}

#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_vlan_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  vlan_oid_cur = 0;
    ctc_sai_vlan_user_t    ctc_sai_vlan_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;

    sal_memset(&ctc_sai_vlan_cur, 0, sizeof(ctc_sai_vlan_user_t));

    vlan_oid_cur = bucket_data->oid;
    sal_memcpy((ctc_sai_vlan_user_t*)(&ctc_sai_vlan_cur), bucket_data->data, sizeof(ctc_sai_vlan_user_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (vlan_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

    CTC_SAI_LOG_DUMP(p_file, "%-4d  0x%016"PRIx64 "  %-11d  %-7d  0x%-9x  0x%-9x  %-6d  0x%-4x 0x%-4x 0x%-4x\n",\
        num_cnt, vlan_oid_cur, ctc_sai_vlan_cur.user_vlanptr, ctc_sai_vlan_cur.vlan_id, ctc_sai_vlan_cur.stats_id_in, ctc_sai_vlan_cur.stats_id_eg,\
        ctc_sai_vlan_cur.stp_id, ctc_sai_vlan_cur.ukwn_flood_ctr[0], ctc_sai_vlan_cur.ukwn_flood_ctr[1], ctc_sai_vlan_cur.ukwn_flood_ctr[2]);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________

sai_status_t
ctc_sai_vlan_traverse_set_unkown_pkt_action(uint8 lchip, void* p_sw_master, uint8 fdb_unknown_type)
{
    ctc_sai_db_traverse_param_t vlan_cb;
    ctc_sai_switch_master_t* p_switch_master = (ctc_sai_switch_master_t*)p_sw_master;

    sal_memset(&vlan_cb, 0, sizeof(ctc_sai_db_traverse_param_t));

    vlan_cb.value0 = (void*)p_switch_master;
    vlan_cb.value1 = (void*)(&fdb_unknown_type);

    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_VLAN, (hash_traversal_fn)_ctc_sai_vlan_set_unkown_pkt_action_cb, (void*)&vlan_cb);
    return SAI_STATUS_SUCCESS;
}

void ctc_sai_vlan_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Vlan MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_VLAN))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Vlan");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_vlan_user_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s  %-18s  %-11s  %-7s  %-11s  %-11s  %-6s  %-*s\n", \
            "No.", "Vlan_oid", "Usr_vlanptr", "Vlan_id", "Stats_id_in", "Stats_id_eg", "Stp_id",\
            CTC_SAI_STR_LENTH("Ukwn_flood_ctr[3]"), "Ukwn_flood_ctr[3]");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_VLAN,
                                            (hash_traversal_fn)_ctc_sai_vlan_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________

sai_status_t ctc_sai_vlan_create_vlan( sai_object_id_t      *sai_vlan_id,
                                      sai_object_id_t        switch_id,
                                      uint32_t               attr_count,
                                      const sai_attribute_t *attr_list)
{
    ctc_vlan_uservlan_t  vlan ;
    sai_status_t status = 0;
    ctc_object_id_t vlan_oid ;
    ctc_sai_vlan_user_t *p_dbvlan = NULL;
    uint8 lchip = 0;
    const sai_attribute_value_t *attr_value = NULL;
    uint32                   attr_index = 0;
    ctc_stats_statsid_t stats_statsid_in;
    ctc_stats_statsid_t stats_statsid_eg;
    sai_object_key_t key ;
    sai_attribute_t attr_tmp;
    uint8 i = 0;
    uint8 ingress_acl_num = 0;
    uint8 egress_acl_num = 0;
    uint8 chip_type = 0;
    uint8 vlan_stats_flag = 1;
    ctc_acl_property_t acl_prop;
    uint8 enable = 0;
    ctc_object_id_t ctc_object_id;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    if (NULL == sai_vlan_id || 0 == attr_count || NULL == attr_list )
    {
        return SAI_STATUS_INVALID_PARAMETER;
    }

    sal_memset(&vlan, 0, sizeof(vlan));
    sal_memset(&vlan_oid, 0, sizeof(vlan_oid));
    sal_memset(&key, 0, sizeof(sai_object_key_t));
    sal_memset(&attr_tmp, 0, sizeof(sai_attribute_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_vlan_mapping_user_vlan(lchip, attr_count, attr_list, &vlan);
    if (status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "create vlan : vlan mapping error:%d\n", status);
        CTC_SAI_DB_UNLOCK(lchip);
        return  status;
    }

    status = ctcs_vlan_create_uservlan(lchip, &vlan);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "create vlan error:%d\n", status);
        status = ctc_sai_mapping_error_ctc(status);
        goto error0;
    }

    *sai_vlan_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_VLAN, lchip, 0, 0, (uint32)vlan.user_vlanptr);
    key.key.object_id = *sai_vlan_id ;
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error1);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_LEARN_DISABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error1);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if ( !attr_value->booldata )
        {
            vlan_stats_flag = 0;
        }
    }

    sal_memset(&stats_statsid_in, 0, sizeof(ctc_stats_statsid_t));
    sal_memset(&stats_statsid_eg, 0, sizeof(ctc_stats_statsid_t));

    if (vlan_stats_flag)
    {
        chip_type = ctcs_get_chip_type(lchip);
        if ((chip_type == CTC_CHIP_DUET2) || (chip_type == CTC_CHIP_TSINGMA))
        {
            stats_statsid_in.dir = CTC_INGRESS;
            stats_statsid_in.type = CTC_STATS_STATSID_TYPE_VLAN;
            stats_statsid_in.stats_id = vlan.user_vlanptr;

            status = ctcs_stats_create_statsid(lchip, &stats_statsid_in);
            if (CTC_E_NO_RESOURCE == status)
            {
                status = SAI_STATUS_INSUFFICIENT_RESOURCES;
                goto error1;
            }
            else
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_direction_property(lchip, vlan.user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_INGRESS, stats_statsid_in.stats_id), status, error2);
            }

            stats_statsid_eg.dir = CTC_EGRESS;
            stats_statsid_eg.type = CTC_STATS_STATSID_TYPE_VLAN;
            stats_statsid_eg.stats_id = vlan.user_vlanptr + VLAN_NUM;

            status = ctcs_stats_create_statsid(lchip, &stats_statsid_eg);
            if (CTC_E_NO_RESOURCE == status)
            {
                status = SAI_STATUS_INSUFFICIENT_RESOURCES;
                goto error2;

            }
            else
            {
                CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_set_direction_property(lchip, vlan.user_vlanptr, CTC_VLAN_DIR_PROP_VLAN_STATS_ID, CTC_EGRESS, stats_statsid_eg.stats_id), status, error3);
            }
        }
   }

    p_dbvlan = mem_malloc(MEM_VLAN_MODULE, sizeof(ctc_sai_vlan_user_t));
    if (NULL == p_dbvlan)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to allocate vlan db entry:%d\n", status);
        goto error3;
    }
    sal_memset(p_dbvlan, 0, sizeof(ctc_sai_vlan_user_t));
    p_dbvlan->user_vlanptr = vlan.user_vlanptr;
    p_dbvlan->vlan_id = vlan.vlan_id;

    if ((chip_type == CTC_CHIP_DUET2) || (chip_type == CTC_CHIP_TSINGMA))
    {
        p_dbvlan->stats_id_in = stats_statsid_in.stats_id;
        p_dbvlan->stats_id_eg = stats_statsid_eg.stats_id;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, *sai_vlan_id, p_dbvlan ), status, error4);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_STP_INSTANCE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error4);
    }
    else
    {
        /*set default stp:SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID*/
        attr_tmp.id = SAI_VLAN_ATTR_STP_INSTANCE;
        attr_tmp.value.oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, lchip, 0, 0, 0);
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_tmp), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_vlan_property(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_vlan_property(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_INGRESS_ACL, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_acl_bind_point_set(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_EGRESS_ACL, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_acl_bind_point_set(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_vlan_set_info(&key, &attr_list[attr_index]), status, error4);
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_POLICER_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if(SAI_NULL_OBJECT_ID != attr_value->oid)
        {
            enable = 1;
        
            ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, attr_value->oid, &ctc_object_id);
            
            CTC_SAI_ERROR_GOTO(ctc_sai_policer_vlan_set_policer(lchip, p_dbvlan->vlan_id, ctc_object_id.value, enable), status, error4);

            p_dbvlan->policer_id = ctc_object_id.value;
        }
    }    

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_VLAN_ATTR_META_DATA, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip))
        {
            ingress_acl_num = 8;
            egress_acl_num = 3;
        }

        for (i = 0; i < ingress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_INGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, vlan.user_vlanptr, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[attr_index].value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_acl_property(lchip, vlan.user_vlanptr, &acl_prop));
        }

        for (i = 0; i < egress_acl_num; i++)
        {
            sal_memset(&acl_prop, 0, sizeof(ctc_acl_property_t));
            acl_prop.direction = CTC_EGRESS;
            acl_prop.acl_priority = i;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_get_acl_property(lchip, vlan.user_vlanptr, &acl_prop));
            if (0 == acl_prop.acl_en)
            {
                acl_prop.tcam_lkup_type = CTC_ACL_TCAM_LKUP_TYPE_MAX;
            }
            acl_prop.acl_en = 1;
            acl_prop.acl_priority = i;
            acl_prop.class_id = CTC_SAI_META_DATA_SAI_TO_CTC(attr_list[attr_index].value.u32);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_set_acl_property(lchip, vlan.user_vlanptr, &acl_prop));
        }
    }

    status = SAI_STATUS_SUCCESS;
    goto out;

error4:
    mem_free(p_dbvlan);
error3:
    ctcs_stats_destroy_statsid(lchip, stats_statsid_eg.stats_id);
error2:
    ctcs_stats_destroy_statsid(lchip, stats_statsid_in.stats_id);
error1:
    ctcs_vlan_destroy_vlan( lchip, vlan.vlan_id);
error0:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_VLAN, vlan.user_vlanptr);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to create vlan entry:%d\n", status);
    }
    return status;
}



/*
 * Routine Description:
 *    Remove a VLAN
 *
 * Arguments:
 *    [in] vlan_id - VLAN id
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_vlan_remove_vlan( sai_object_id_t sai_vlan_id)
{
    ctc_object_id_t ctc_object_id ;
    sai_status_t status = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;
    sai_object_id_t stp_oid = 0;
    sai_attribute_t attr_list;
    sai_object_id_t switch_id = 0;
    uint8 gchip;

    sal_memset(&ctc_object_id, 0 , sizeof(ctc_object_id_t));
    sal_memset(&attr_list, 0 , sizeof(sai_attribute_t));

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_VLAN, sai_vlan_id, &ctc_object_id);
    CTC_SAI_DB_LOCK(ctc_object_id.lchip);
    p_dbvlan = ctc_sai_db_get_object_property(ctc_object_id.lchip, sai_vlan_id);
    if (NULL == p_dbvlan)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }
    if (0 != p_dbvlan->stats_id_in)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_destroy_statsid(ctc_object_id.lchip, p_dbvlan->stats_id_in), status, out);
    }
    if (0 != p_dbvlan->stats_id_eg)
    {
        CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_destroy_statsid(ctc_object_id.lchip, p_dbvlan->stats_id_eg), status, out);
    }
    if (0 != p_dbvlan->policer_id)
    {
        ctc_sai_policer_vlan_set_policer(ctc_object_id.lchip, p_dbvlan->vlan_id, p_dbvlan->policer_id, 0);
    }
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(ctc_object_id.lchip, CTC_SAI_DB_ID_TYPE_VLAN, p_dbvlan->user_vlanptr), status, out);

    stp_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_STP, ctc_object_id.lchip, 0, 0, (uint32)p_dbvlan->stp_id);
    CTC_SAI_ERROR_GOTO(ctc_sai_stp_set_instance(ctc_object_id.lchip, p_dbvlan->vlan_id, p_dbvlan->user_vlanptr, stp_oid, 0), status, out);

    /*not vlanptr*/
    CTC_SAI_CTC_ERROR_GOTO(ctcs_vlan_destroy_vlan( ctc_object_id.lchip, p_dbvlan->vlan_id), status, out);

    /*flush fdb*/
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(ctc_object_id.lchip, &gchip));
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, ctc_object_id.lchip, 0, 0, (uint32) gchip);
    attr_list.id = SAI_FDB_FLUSH_ATTR_BV_ID;
    attr_list.value.oid = sai_vlan_id;
    ctc_sai_fdb_flush_fdb(switch_id, 1, &attr_list);

    mem_free(p_dbvlan);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_remove_object_property(ctc_object_id.lchip, sai_vlan_id ), status, out);

out:
    CTC_SAI_DB_UNLOCK(ctc_object_id.lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to remove vlan entry%d\n", status);
    }
    return status;
}




/*
 * Routine Description:
 *    Set VLAN attribute Value
 *
 * Arguments:
 *    [in] vlan_id - VLAN id
 *    [in] attr - attribute
 *
 * Return Values:
 *    SAI_STATUS_SUCCESS on success
 *    Failure status code on error
 */
static sai_status_t ctc_sai_vlan_set_vlan_attribute( sai_object_id_t vlan_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key = { .key.object_id = vlan_id };
    sai_status_t           status = 0;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key,key_str,   SAI_OBJECT_TYPE_VLAN,  vlan_attr_fn_entries,attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to set vlan attr:%d, status:%d\n", attr->id,status);
    }
    return status;
}


static sai_status_t ctc_sai_vlan_get_vlan_attribute( sai_object_id_t vlan_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = vlan_id
    }
    ;
    sai_status_t    status = 0;
    char           key_str[MAX_KEY_STR_LEN];
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, key_str,
                                                 SAI_OBJECT_TYPE_VLAN, loop, vlan_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to get vlan attr:%d, status:%d\n", attr_list[loop].id, status);
    }
    return status;
}





/*
 *  \brief Create VLAN Member
 *  \param[out] vlan_member_id VLAN member ID
 *  \param[in] attr_count number of attributes
 *  \param[in] attr_list array of attributes
 *  \return Success: SAI_STATUS_SUCCESS
 *  Failure: failure status code on error
 */
static sai_status_t ctc_sai_vlan_create_vlan_member( sai_object_id_t     * vlan_member_id,
                                                    sai_object_id_t        switch_id,
                                                    uint32_t               attr_count,
                                                    const sai_attribute_t *attr_list)
{
    sai_status_t  status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    if (NULL == vlan_member_id || 0 == attr_count || NULL == attr_list )
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, " vlan member parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_vlan_create_vlan_member(vlan_member_id, switch_id, attr_count, attr_list);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to create vlan member:%d\n", status);
    }
    return status;
}



/*
 *  \brief Remove VLAN Member
 *  \param[in] vlan_member_id VLAN member ID
 *  \return Success: SAI_STATUS_SUCCESS
 *  Failure: failure status code on error
 */
static sai_status_t ctc_sai_vlan_remove_vlan_member( sai_object_id_t vlan_member_id)
{
    sai_status_t                 status;
    uint8 lchip;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = _ctc_sai_vlan_remove_vlan_member(vlan_member_id);
    CTC_SAI_DB_UNLOCK(lchip);
     if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to remove vlan member:%d\n", status);
    }
    return status;
}

/*
 *  \brief Set VLAN Member Attribute
 *  \param[in] vlan_member_id VLAN member ID
 *  \param[in] attr attribute structure containing ID and value
 *  \return Success: SAI_STATUS_SUCCESS
 *  Failure: failure status code on error
 */
static sai_status_t ctc_sai_vlan_set_vlan_member_attribute( sai_object_id_t vlan_member_id,  const sai_attribute_t *attr)
{
    sai_object_key_t key =
    {
        .key.object_id = vlan_member_id
    }
    ;
    char                   key_str[MAX_KEY_STR_LEN];
    uint8 lchip = 0;
    sai_status_t status = 0;


    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    if (NULL == attr)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "set member attr parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    status = ctc_sai_set_attribute(&key, key_str,   SAI_OBJECT_TYPE_VLAN_MEMBER,  vlan_member_attr_fn_entries, attr);
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to set vlan member attr:%d\n", status);
    }
    return status;
}


static sai_status_t ctc_sai_vlan_get_vlan_member_attribute( sai_object_id_t vlan_member_id,  sai_uint32_t   attr_count,  sai_attribute_t *attr_list)
{
    sai_object_key_t key =
    {
        .key.object_id = vlan_member_id
    }
    ;
    sai_status_t    status = 0;
    uint8          loop = 0;
    uint8 lchip = 0;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    if (NULL == attr_list ||0 == attr_count )
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "get member attr parameter invalid\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(vlan_member_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    while (loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL,
                                                 SAI_OBJECT_TYPE_VLAN_MEMBER, loop, vlan_member_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }
    out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to get vlan member attr:%d\n", status);
    }
    return status;
}

/**
 * @brief Bulk vlan members creation.
 *
 * @param[in] switch_id SAI Switch object id
 * @param[in] object_count Number of objects to create
 * @param[in] attr_count List of attr_count. Caller passes the number
 *    of attribute for each object to create.
 * @param[in] attr_list List of attributes for every object.
 * @param[in] mode Bulk operation error handling mode.
 *
 * @param[out] object_id List of object ids returned
 * @param[out] object_statuses List of status for every object. Caller needs to allocate the buffer.
 *
 * @return #SAI_STATUS_SUCCESS on success when all objects are created or #SAI_STATUS_FAILURE when
 * any of the objects fails to create. When there is failure, Caller is expected to go through the
 * list of returned statuses to find out which fails and which succeeds.
 */
sai_status_t ctc_sai_vlan_create_vlan_members( sai_object_id_t          switch_id,
                                              uint32_t                 object_count,
                                              const uint32_t          *attr_count,
                                              const sai_attribute_t  **attr_list,
                                              sai_bulk_op_error_mode_t mode,
                                              sai_object_id_t        *object_id,
                                              sai_status_t           *object_statuses)
{
    uint32 index = 0;
    sai_status_t status = 0;
    uint8 is_found_error;
    uint8 lchip = 0 ;

    if (NULL == object_id || NULL == attr_count || NULL == attr_list || NULL == object_statuses || 0 == object_count)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, " vlan member invalid parameter\n");
        return SAI_STATUS_INVALID_PARAMETER;
    }
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_vlan_create_vlan_member(&object_id[index], switch_id, attr_count[index], attr_list[index]);
        object_statuses[index] =  status;

        if (status != SAI_STATUS_SUCCESS  )
        {
            is_found_error = TRUE;
        }

        if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
        {
            break;
        }
    }

    if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
    {
        for (index++; index < object_count; index++)
        {
            object_statuses[index] = SAI_STATUS_NOT_EXECUTED;
        }
    }

    if (TRUE == is_found_error)
    {
        status = SAI_STATUS_FAILURE;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to create vlan members :%d\n", status);
    }
    return status;
}

/**
 * @brief Bulk vlan members removal.
 *
 * @param[in] object_count Number of objects to create
 * @param[in] object_id List of object ids
 * @param[in] mode Bulk operation error handling mode.
 * @param[out] object_statuses List of status for every object. Caller needs to allocate the buffer.
 *
 * @return #SAI_STATUS_SUCCESS on success when all objects are removed or #SAI_STATUS_FAILURE when
 * any of the objects fails to remove. When there is failure, Caller is expected to go through the
 * list of returned statuses to find out which fails and which succeeds.
 */
sai_status_t ctc_sai_vlan_remove_vlan_members( uint32_t                 object_count,
                                              const sai_object_id_t   *object_id,
                                              sai_bulk_op_error_mode_t mode,
                                              sai_status_t           *object_statuses)
{

    uint32 index = 0;
    sai_status_t status = 0;
    uint8 is_found_error;
    uint8 lchip = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(object_id[index], &lchip));
    CTC_SAI_DB_LOCK(lchip);
    for (index = 0; index < object_count; index++)
    {
        status = _ctc_sai_vlan_remove_vlan_member(object_id[index]);
        object_statuses[index] =  status;

        if (status != SAI_STATUS_SUCCESS  )
        {
            is_found_error = TRUE;
        }

        if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
        {
            break;
        }
    }

    if (status != SAI_STATUS_SUCCESS  && SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR == mode )
    {
        for (index++; index < object_count; index++)
        {
            object_statuses[index] = SAI_STATUS_NOT_EXECUTED;
        }
    }

    if (TRUE == is_found_error)
    {
        status = SAI_STATUS_FAILURE;
    }

    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to remove vlan members:%d\n", status);
    }
    return status;
}


/**
 * @brief Get vlan statistics counters.
 *
 * @param[in] vlan_id VLAN id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 * @param[out] counters Array of resulting counter values.
 *
 * @return #SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t ctc_sai_vlan_get_vlan_stats( sai_object_id_t        sai_vlan_id,
                                                uint32_t               number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                uint64_t             *counters)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;
    uint32 index = 0;
    uint32 not_support = 0;


    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_vlan_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

   p_dbvlan = ctc_sai_db_get_object_property(lchip,  sai_vlan_id);
    if (NULL == p_dbvlan)
    {
        status =  SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    sal_memset(&stats_igs, 0, sizeof(stats_igs));
    sal_memset(&stats_egs, 0, sizeof(stats_egs));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_in, &stats_igs), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_eg, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if (0 != p_dbvlan->stats_id_in && (SAI_VLAN_STAT_IN_PACKETS == counter_ids[index] || SAI_VLAN_STAT_IN_OCTETS == counter_ids[index]))
        {

            if (SAI_VLAN_STAT_IN_PACKETS == counter_ids[index])
            {
                counters[index] = stats_igs.packet_count - p_dbvlan->igs_packet_count;
            }
            else
            {
                counters[index] = stats_igs.byte_count - p_dbvlan->igs_byte_count;
            }
            continue;
        }

        if (0 != p_dbvlan->stats_id_eg && (SAI_VLAN_STAT_OUT_PACKETS == counter_ids[index] || SAI_VLAN_STAT_OUT_OCTETS == counter_ids[index]))
        {

            if (SAI_VLAN_STAT_OUT_PACKETS == counter_ids[index])
            {
                counters[index] = stats_egs.packet_count - p_dbvlan->egs_packet_count;
            }
            else
            {
                counters[index] = stats_egs.byte_count - p_dbvlan->egs_byte_count;
            }
            continue;
        }

        not_support = TRUE;
    }

    if ( TRUE == not_support)
    {
        status = SAI_STATUS_NOT_SUPPORTED ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to get vlan stats,status =%d\n", status);
    }
    return status;
}

static sai_status_t
ctc_sai_vlan_get_vlan_stats_ext( sai_object_id_t        sai_vlan_id,
                                                uint32_t               number_of_counters,
                                                const sai_stat_id_t *counter_ids,
                                                sai_stats_mode_t mode,
                                                uint64_t             *counters)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;
    uint32 index = 0;
    uint32 not_support = 0;
    uint8 clear_ing = 0;
    uint8 clear_egs = 0;


    CTC_SAI_LOG_ENTER(SAI_API_VLAN);

    CTC_SAI_PTR_VALID_CHECK(counter_ids);
    CTC_SAI_PTR_VALID_CHECK(counters);
    CTC_SAI_MAX_VALUE_CHECK(mode, SAI_STATS_MODE_READ_AND_CLEAR);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_vlan_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    p_dbvlan = ctc_sai_db_get_object_property(lchip,  sai_vlan_id);
    if (NULL == p_dbvlan)
    {
        status =  SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    sal_memset(&stats_igs, 0, sizeof(stats_igs));
    sal_memset(&stats_egs, 0, sizeof(stats_egs));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_in, &stats_igs), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_eg, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index ++ )
    {
        if (0 != p_dbvlan->stats_id_in && (SAI_VLAN_STAT_IN_PACKETS == counter_ids[index] || SAI_VLAN_STAT_IN_OCTETS == counter_ids[index]))
        {
            clear_ing = 1;
            if (SAI_VLAN_STAT_IN_PACKETS == counter_ids[index])
            {
                counters[index] = stats_igs.packet_count - p_dbvlan->igs_packet_count;
            }
            else
            {
                counters[index] = stats_igs.byte_count - p_dbvlan->igs_byte_count;
            }
            continue;
        }

        if (0 != p_dbvlan->stats_id_eg && (SAI_VLAN_STAT_OUT_PACKETS == counter_ids[index] || SAI_VLAN_STAT_OUT_OCTETS == counter_ids[index]))
        {
            clear_egs = 1;
            if (SAI_VLAN_STAT_OUT_PACKETS == counter_ids[index])
            {
                counters[index] = stats_egs.packet_count - p_dbvlan->egs_packet_count;
            }
            else
            {
                counters[index] = stats_egs.byte_count - p_dbvlan->egs_byte_count;
            }
            continue;
        }

        not_support = TRUE;
    }
    if (SAI_STATS_MODE_READ_AND_CLEAR == mode && clear_ing)
    {
        p_dbvlan->igs_packet_count = stats_igs.packet_count;
        p_dbvlan->igs_byte_count = stats_igs.byte_count;
    }
    if (SAI_STATS_MODE_READ_AND_CLEAR == mode && clear_egs)
    {
        p_dbvlan->egs_packet_count = stats_egs.packet_count;
        p_dbvlan->egs_byte_count = stats_egs.byte_count;
    }

    if ( TRUE == not_support)
    {
        status = SAI_STATUS_NOT_SUPPORTED ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to get vlan stats,status =%d\n", status);
    }
    return status;
}

/**
 * @brief Clear vlan statistics counters.
 *
 * @param[in] vlan_id Vlan id
 * @param[in] number_of_counters Number of counters in the array
 * @param[in] counter_ids Specifies the array of counter ids
 *
 * @return SAI_STATUS_SUCCESS on success Failure status code on error
 */
static sai_status_t ctc_sai_vlan_clear_vlan_stats( sai_object_id_t        sai_vlan_id,
                                                  uint32_t               number_of_counters,
                                                  const sai_stat_id_t *counter_ids)
{
    uint8 lchip = 0;
    sai_status_t status = 0;
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;
    uint32 index = 0;
    ctc_stats_basic_t stats_igs;
    ctc_stats_basic_t stats_egs;

    CTC_SAI_LOG_ENTER(SAI_API_VLAN);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_vlan_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_dbvlan = ctc_sai_db_get_object_property(lchip, sai_vlan_id);
    if (NULL == p_dbvlan)
    {
        status = SAI_STATUS_INVALID_OBJECT_ID;
        goto out;
    }

    sal_memset(&stats_igs, 0, sizeof(stats_igs));
    sal_memset(&stats_egs, 0, sizeof(stats_egs));
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_in, &stats_igs), status, out);
    CTC_SAI_CTC_ERROR_GOTO(ctcs_stats_get_stats(lchip, p_dbvlan->stats_id_eg, &stats_egs), status, out);

    for (index = 0; index < number_of_counters; index++)
    {
        if (SAI_VLAN_STAT_IN_PACKETS == counter_ids[index] || SAI_VLAN_STAT_IN_OCTETS == counter_ids[index] )
        {
            if (0 != p_dbvlan->stats_id_in)
            {
                p_dbvlan->igs_packet_count = stats_igs.packet_count;
                p_dbvlan->igs_byte_count = stats_igs.byte_count;
            }
        }

        if (SAI_VLAN_STAT_OUT_PACKETS == counter_ids[index] || SAI_VLAN_STAT_OUT_OCTETS == counter_ids[index] )
        {
            if (0 != p_dbvlan->stats_id_eg)
            {
                p_dbvlan->egs_packet_count = stats_egs.packet_count;
                p_dbvlan->egs_byte_count = stats_egs.byte_count;
            }
        }
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_VLAN, "Failed to clear vlan stats, status = %d\n", status);
    }
    return status;
}

const sai_vlan_api_t ctc_sai_vlan_api = {
    ctc_sai_vlan_create_vlan,
    ctc_sai_vlan_remove_vlan,
    ctc_sai_vlan_set_vlan_attribute,
    ctc_sai_vlan_get_vlan_attribute,
    ctc_sai_vlan_create_vlan_member,
    ctc_sai_vlan_remove_vlan_member,
    ctc_sai_vlan_set_vlan_member_attribute,
    ctc_sai_vlan_get_vlan_member_attribute,
    ctc_sai_vlan_create_vlan_members,
    ctc_sai_vlan_remove_vlan_members,
    ctc_sai_vlan_get_vlan_stats,
    ctc_sai_vlan_get_vlan_stats_ext,
    ctc_sai_vlan_clear_vlan_stats
};

sai_status_t
ctc_sai_vlan_db_init(uint8 lchip)
{
    sai_object_id_t    sai_vlan_id = 0;
    sai_object_id_t        switch_id;
    sai_attribute_t attr_list[5];
    ctc_global_panel_ports_t local_panel_ports;
    uint32 num = 0;
    uint8 gchip = 0;
    uint32 gport = 0;
    uint16_t                     vlanptr;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_VLAN;
    wb_info.data_len = sizeof(ctc_sai_vlan_user_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_vlan_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_VLAN, (void*)(&wb_info));
    ctc_sai_vlan_user_t *p_dbvlan = NULL ;

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);
    sal_memset(attr_list, 0, sizeof(attr_list));
    attr_list[0].id = SAI_VLAN_ATTR_VLAN_ID;
    attr_list[0].value.u16 = 1;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_get_gchip_id(lchip, &gchip));
    switch_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_SWITCH, lchip, 0, 0, (uint32) gchip);
    CTC_SAI_ERROR_RETURN(ctc_sai_vlan_create_vlan(&sai_vlan_id, switch_id, 1, attr_list));
    ctcs_vlan_set_property(lchip, 1, CTC_VLAN_PROP_ARP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU);
    ctcs_vlan_set_property(lchip, 1, CTC_VLAN_PROP_DHCP_EXCP_TYPE, CTC_EXCP_FWD_AND_TO_CPU);

    sal_memset(&local_panel_ports, 0, sizeof(local_panel_ports));

    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_get(lchip, CTC_GLOBAL_PANEL_PORTS, (void*)&local_panel_ports));
    CTC_SAI_ERROR_RETURN (ctc_sai_oid_get_vlanptr(sai_vlan_id, &vlanptr));
    p_dbvlan = ctc_sai_db_get_object_property(lchip, sai_vlan_id);
    for (num = 0; num < local_panel_ports.count; num ++)
    {
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, local_panel_ports.lport[num]);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_vlan_add_port(lchip, vlanptr, gport));
        CTC_BMP_SET(p_dbvlan->vlan_member_port_bind_bits, local_panel_ports.lport[num]);
    }

    p_dbvlan->vlan_member_port_bind_count = local_panel_ports.count;

    return SAI_STATUS_SUCCESS;
}
sai_status_t
ctc_sai_vlan_api_init()
{
    ctc_sai_register_module_api(SAI_API_VLAN, (void*)&ctc_sai_vlan_api);

    return SAI_STATUS_SUCCESS;
}



