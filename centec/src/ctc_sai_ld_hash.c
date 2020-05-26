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
#include "ctc_sai_ld_hash.h"
#include "ctc_sai_udf.h"
#include "ctc_init.h"

#define LAG_HASH_OID 0x201C
#define ECMP_HASH_OID 0x1C

typedef struct  ctc_sai_ld_hash_wb_s
{
    /*key*/
    sai_object_id_t oid;
    uint32 index;
    uint32 calc_key_len[0];

    /*data*/
    sai_object_id_t udf_grp_id;
}ctc_sai_ld_hash_wb_t;

sai_status_t
_ctc_sai_ld_hash_set_info(const sai_attribute_t* attr, ctc_sai_ld_hash_t* p_sai_hash)
{
    uint8 loop_i = 0;

    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    switch(attr->id)
    {
    case  SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
        {
            for (loop_i = 0; loop_i < attr->value.s32list.count; loop_i++)
            {
                CTC_BIT_SET(p_sai_hash->field_bmp, attr->value.s32list.list[loop_i]);
            }
            break;
        }
    case  SAI_HASH_ATTR_UDF_GROUP_LIST :
        {
            if (0 == attr->value.objlist.count)
            {
                p_sai_hash->udf_group_list.count = 0;
                p_sai_hash->udf_group_list.list = NULL;
            }
            else
            {
                p_sai_hash->udf_group_list.list = mem_malloc(MEM_SYSTEM_MODULE, sizeof(sai_object_id_t)*attr->value.objlist.count);
                if (NULL == p_sai_hash->udf_group_list.list)
                {
                    return SAI_STATUS_NO_MEMORY;
                }
                sal_memset(p_sai_hash->udf_group_list.list, 0, sizeof(sai_object_id_t)*attr->value.objlist.count);
                for (loop_i = 0; loop_i < attr->value.objlist.count; loop_i++)
                {
                    p_sai_hash->udf_group_list.list[loop_i] = attr->value.objlist.list[loop_i];
                }
                p_sai_hash->udf_group_list.count = loop_i;
            }
            break;
        }
    default:
        CTC_SAI_LOG_ERROR(SAI_API_HASH, "set hash attribute not support: attribute_id %d\n", attr->id);
        return  SAI_STATUS_NOT_SUPPORTED;
    }
    return  SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_build_db(uint8 lchip, sai_object_id_t hash_obj_id, ctc_sai_ld_hash_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_ld_hash_t* p_hash_data = NULL;

    p_hash_data = mem_malloc(MEM_HASH_MODULE, sizeof(ctc_sai_ld_hash_t));
    if (NULL == p_hash_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HASH, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_hash_data, 0, sizeof(ctc_sai_ld_hash_t));
    status = ctc_sai_db_add_object_property(lchip, hash_obj_id, (void*)p_hash_data);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_hash_data);
    }
    *oid_property = p_hash_data;

    return status;
}

static sai_status_t
_ctc_sai_ld_hash_remove_db(uint8 lchip, sai_object_id_t hash_obj_id)
{
    ctc_sai_ld_hash_t* p_hash_data = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_MIRROR);
    p_hash_data = ctc_sai_db_get_object_property(lchip, hash_obj_id);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, hash_obj_id);
    mem_free(p_hash_data);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_ld_hash_set_udf_hash_mask(uint8 lchip, sai_object_id_t udf_group_id, uint8 hash_usage, uint8 is_clear) /* called when set hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST */
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint16 hash_udf_bmp = 0;
    uint32 udf_group_value = 0;
    ctc_linkagg_psc_t ctc_sdk_linkagg_psc;
    ctc_parser_ecmp_hash_ctl_t ctc_sdk_ecmp_hash_ctl;

    sal_memset(&ctc_sdk_linkagg_psc, 0, sizeof(ctc_linkagg_psc_t));
    sal_memset(&ctc_sdk_ecmp_hash_ctl, 0, sizeof(ctc_parser_ecmp_hash_ctl_t));

    CTC_SAI_ERROR_GOTO(ctc_sai_udf_get_hash_mask(lchip, udf_group_id, &hash_udf_bmp, &udf_group_value),status,out);
    if (is_clear)
    {
        hash_udf_bmp = 0;
    }
    if(CTC_SAI_HASH_USAGE_LINKAGG == hash_usage)
    {
        ctc_sdk_linkagg_psc.psc_type_bitmap = CTC_LINKAGG_PSC_TYPE_UDF;
        ctc_sdk_linkagg_psc.udf_id = udf_group_value;
        ctc_sdk_linkagg_psc.udf_bitmap= hash_udf_bmp;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_linkagg_set_psc(lchip,&ctc_sdk_linkagg_psc), status, out);
    }
    else if(CTC_SAI_HASH_USAGE_ECMP == hash_usage)
    {
        ctc_sdk_ecmp_hash_ctl.hash_type_bitmap = CTC_PARSER_HASH_TYPE_FLAGS_UDF;
        ctc_sdk_ecmp_hash_ctl.udf_id = udf_group_value;
        ctc_sdk_ecmp_hash_ctl.udf_bitmap = hash_udf_bmp;
        CTC_SAI_CTC_ERROR_GOTO(ctcs_parser_set_ecmp_hash_field(lchip, &ctc_sdk_ecmp_hash_ctl), status, out);
    }

out:
    return status;
}

sai_status_t
_ctc_sai_set_linkagg_hash(sai_object_id_t sai_hash_id)
{
    uint8 lchip = 0;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_linkagg_psc_t          ctc_linkagg_psc;
    ctc_parser_global_cfg_t    ctc_parser_global_ctl;
    ctc_lb_hash_config_t       ctc_lb_hash_config;
    ctc_lb_hash_offset_t     ctc_lb_hash_offset;
    uint8 loop_i = 0;

    sal_memset(&ctc_linkagg_psc, 0, sizeof(ctc_linkagg_psc_t));
    sal_memset(&ctc_parser_global_ctl, 0 , sizeof(ctc_parser_global_cfg_t));
    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    sal_memset(&ctc_lb_hash_offset, 0 , sizeof(ctc_lb_hash_offset_t));
    
    /*for don't clear table, set default select id use 2*/
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    /* for update, only fields updated are valid, so must clean default value */
    CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);

    ctc_sai_oid_get_lchip(sai_hash_id, &lchip);
    CTC_SAI_LOG_ENTER(SAI_API_HASH);
    p_hash_data = ctc_sai_db_get_object_property(lchip, sai_hash_id);
    if (NULL == p_hash_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HASH, "Failed to binding hash, invalid sai_hash_id 0x%"PRIx64"!\n", sai_hash_id);
    }

    /* SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST */
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_SRC_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPSA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_DST_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPDA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPSA);

        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_IP] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_MPLS_VPN] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_MPLS] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPDA);

        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_IP] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_MPLS_VPN] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
        ctc_parser_global_ctl.linkagg_tunnel_hash_mode[CTC_PARSER_TUNNEL_TYPE_MPLS] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));

    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_VLAN_ID))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_VLAN);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_PROTOCOL);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_ETHERTYPE);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_SRC_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_DST_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACSA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_DST_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACDA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_IN_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_IP_HASH_FLAGS_PROTOCOL);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }

        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_L2_HASH_FLAGS_ETHERTYPE);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_L4_HASH_FLAGS_SRC_PORT);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_L4_HASH_FLAGS_DST_PORT);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_L2_HASH_FLAGS_MACSA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_PARSER_L2_HASH_FLAGS_MACDA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.linkagg_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_linkagg_set_psc(lchip, &ctc_linkagg_psc));

    /* MPLS Hash process*/
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_DISABLE_MPLS);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
        sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
        
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL0_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL0_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_HI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_MI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_MI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_SA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_SA_LO);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_DA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_DA_LO);
    }
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && (CTC_SAI_HASH_USAGE_LINKAGG == ctc_lb_hash_config.sel_id))
    {
        for(loop_i= CTC_LB_HASH_SELECT_L2; loop_i <= CTC_LB_HASH_SELECT_MPLS_L3VPN_INNER_IPV6; loop_i++)
        {
            CTC_SET_FLAG(ctc_lb_hash_config.hash_select, loop_i);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
            CTC_UNSET_FLAG(ctc_lb_hash_config.hash_select, loop_i);
        }
    }
    /* SAI_HASH_ATTR_UDF_GROUP_LIST */
    if(p_hash_data->udf_group_list.count> 0)
    {
        for(loop_i= 0; loop_i < p_hash_data->udf_group_list.count; loop_i++)
        {
             CTC_SAI_ERROR_RETURN(_ctc_sai_ld_hash_set_udf_hash_mask(lchip, p_hash_data->udf_group_list.list[loop_i], CTC_SAI_HASH_USAGE_LINKAGG, 0));
        }
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_set_ecmp_hash(sai_object_id_t sai_hash_id)
{
    uint8 lchip = 0;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_parser_ecmp_hash_ctl_t ctc_ecmp_ctl;
    ctc_parser_global_cfg_t    ctc_parser_global_ctl;
    ctc_lb_hash_config_t       ctc_lb_hash_config;
    ctc_lb_hash_offset_t     ctc_lb_hash_offset;
    uint8 loop_i = 0;

    sal_memset(&ctc_ecmp_ctl, 0, sizeof(ctc_parser_ecmp_hash_ctl_t));
    sal_memset(&ctc_parser_global_ctl, 0 , sizeof(ctc_parser_global_cfg_t));
    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    sal_memset(&ctc_lb_hash_offset, 0 , sizeof(ctc_lb_hash_offset_t));
    
    /*for don't clear table, set default select id use 2*/
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    /* for update, only fields updated are valid, so must clean default value */
    CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2); /* last alredeady */

    ctc_sai_oid_get_lchip(sai_hash_id, &lchip);
    CTC_SAI_LOG_ENTER(SAI_API_HASH);
    p_hash_data = ctc_sai_db_get_object_property(lchip, sai_hash_id);
    if (NULL == p_hash_data)
    {
        CTC_SAI_LOG_ERROR(SAI_API_HASH, "Failed to binding hash, invalid sai_hash_id 0x%"PRIx64"!\n", sai_hash_id);
    }

    /* SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST */
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_SRC_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPSA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_DST_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPDA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPSA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPDA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_VLAN_ID))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_CTAG_VID);  /* sai: vlan id; centec: svlan id,cvaln id */
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_STAG_VID);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_PROTOCOL);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_ETHERTYPE);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_SRC_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_DST_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACSA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_DST_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACDA);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_IN_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_PORT);
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_PROTOCOL);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }

        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_L2_HASH_FLAGS_ETHERTYPE);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_L4_HASH_FLAGS_SRC_PORT);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_L4_HASH_FLAGS_DST_PORT);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_L2_HASH_FLAGS_MACSA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    if(CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_L2_HASH_FLAGS_MACDA);

        for(loop_i= CTC_PARSER_TUNNEL_TYPE_UDP; loop_i < CTC_PARSER_TUNNEL_TYPE_MAX; loop_i++)
        {
            ctc_parser_global_ctl.ecmp_tunnel_hash_mode[loop_i] = CTC_PARSER_TUNNEL_HASH_MODE_INNER;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_ecmp_hash_field(lchip, &ctc_ecmp_ctl));

    /* MPLS Hash process*/
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_DISABLE_MPLS);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
        sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
        
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL0_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL0_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_HI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACSA_MI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_MACDA_MI);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_SA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_SA_LO);
    }
    if((CTC_IS_BIT_SET(p_hash_data->field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP)) && (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_DA_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_IP_DA_LO);
    }
    if((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) && (CTC_SAI_HASH_USAGE_ECMP == ctc_lb_hash_config.sel_id))
    {
        for(loop_i= CTC_LB_HASH_SELECT_L2; loop_i <= CTC_LB_HASH_SELECT_MPLS_L3VPN_INNER_IPV6; loop_i++)
        {
            CTC_SET_FLAG(ctc_lb_hash_config.hash_select, loop_i);
            CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
            CTC_UNSET_FLAG(ctc_lb_hash_config.hash_select, loop_i);
        }
    }
    /* SAI_HASH_ATTR_UDF_GROUP_LIST */
    if(p_hash_data->udf_group_list.count> 0)
    {
        for(loop_i= 0; loop_i < p_hash_data->udf_group_list.count; loop_i++)
        {
             CTC_SAI_ERROR_RETURN(_ctc_sai_ld_hash_set_udf_hash_mask(lchip, p_hash_data->udf_group_list.list[loop_i], CTC_SAI_HASH_USAGE_ECMP, 0));
        }
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_sai_ld_hash_t hash_data_old;
    ctc_linkagg_psc_t          ctc_linkagg_psc;
    ctc_parser_ecmp_hash_ctl_t ctc_ecmp_ctl;
    uint32 loop_i = 0;
    sal_memset(&ctc_linkagg_psc, 0, sizeof(ctc_linkagg_psc_t));
    sal_memset(&ctc_ecmp_ctl, 0, sizeof(ctc_parser_ecmp_hash_ctl_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_hash_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    sal_memset(&hash_data_old, 0, sizeof(ctc_sai_ld_hash_t));
    sal_memcpy(&hash_data_old, p_hash_data, sizeof(ctc_sai_ld_hash_t));
    p_hash_data->field_bmp = 0; /* for update, only fields updated are valid, so must clean default value */
    CTC_SAI_ERROR_RETURN(_ctc_sai_ld_hash_set_info(attr, p_hash_data));

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HASH, key->key.object_id, &ctc_object_id);
    if(ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_ECMP)       /* ecmp hash:   sub_type = 0; */
    {
        if(SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST == attr->id)
        {
            /* clean last hash field value updated */
            ctc_ecmp_ctl.hash_type_bitmap = CTC_PARSER_HASH_TYPE_FLAGS_IP | CTC_PARSER_HASH_TYPE_FLAGS_L4 | CTC_PARSER_HASH_TYPE_FLAGS_MPLS |CTC_PARSER_HASH_TYPE_FLAGS_FCOE
                                        | CTC_PARSER_HASH_TYPE_FLAGS_TRILL | CTC_PARSER_HASH_TYPE_FLAGS_L2 |CTC_PARSER_HASH_TYPE_FLAGS_PBB | CTC_PARSER_HASH_TYPE_FLAGS_COMMON;
            CTC_SAI_CTC_ERROR_GOTO((ctcs_parser_set_ecmp_hash_field(lchip, &ctc_ecmp_ctl)),status,error0);
        }
        else if(SAI_HASH_ATTR_UDF_GROUP_LIST == attr->id)
        {
            if (hash_data_old.udf_group_list.count > 0)  /* SAI_HASH_ATTR_UDF_GROUP_LIST */
            {
                for (loop_i = 0; loop_i < hash_data_old.udf_group_list.count; loop_i++)
                {
                    CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_ld_hash_set_udf_hash_mask(lchip, hash_data_old.udf_group_list.list[loop_i], CTC_SAI_HASH_USAGE_ECMP, 1), status,error0);
                }
            }
        }
        CTC_SAI_ERROR_GOTO(_ctc_sai_set_ecmp_hash(key->key.object_id), status, error0);
    }
    else if(ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_LINKAGG)  /* linkagg hash: sub_type = 1; */
    {
        if(SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST == attr->id)
        {
            /* clean last hash field value updated */
            ctc_linkagg_psc.psc_type_bitmap = CTC_LINKAGG_PSC_TYPE_L2 | CTC_LINKAGG_PSC_TYPE_IP | CTC_LINKAGG_PSC_TYPE_L4 |CTC_LINKAGG_PSC_TYPE_PBB \
                                        | CTC_LINKAGG_PSC_TYPE_MPLS| CTC_LINKAGG_PSC_TYPE_FCOE |CTC_LINKAGG_PSC_TYPE_TRILL |CTC_LINKAGG_PSC_TYPE_COMMON;
            CTC_SAI_CTC_ERROR_GOTO((ctcs_linkagg_set_psc(lchip, &ctc_linkagg_psc)),status,error0);
        }
        else if(SAI_HASH_ATTR_UDF_GROUP_LIST == attr->id)
        {
            if (hash_data_old.udf_group_list.count > 0)  /* SAI_HASH_ATTR_UDF_GROUP_LIST */
            {
                for (loop_i = 0; loop_i < hash_data_old.udf_group_list.count; loop_i++)
                {
                    CTC_SAI_CTC_ERROR_GOTO(_ctc_sai_ld_hash_set_udf_hash_mask(lchip, hash_data_old.udf_group_list.list[loop_i], CTC_SAI_HASH_USAGE_LINKAGG, 1), status,error0);
                }
            }
        }

        CTC_SAI_ERROR_GOTO(_ctc_sai_set_linkagg_hash(key->key.object_id), status, error0);
    }
    else
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error0;
    }

    if (SAI_HASH_ATTR_UDF_GROUP_LIST == attr->id)
    {
        mem_free(hash_data_old.udf_group_list.list);
    }
    goto out;

error0:
    sal_memcpy(p_hash_data, &hash_data_old, sizeof(ctc_sai_ld_hash_t));
out:
    return status;
}

static sai_status_t
_ctc_sai_ld_hash_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    uint8 loop_i = 0;
    uint8 count = 0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_hash_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
            {
                int32_t s32list[SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK];
                for (loop_i = SAI_NATIVE_HASH_FIELD_SRC_IP; loop_i <= SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK; loop_i++)
                {
                    if (CTC_IS_BIT_SET(p_hash_data->field_bmp, loop_i))
                    {
                        s32list[count++] = loop_i;
                    }
                }
                CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(int32_t),
                           s32list, count, &attr->value.objlist));
                break;
            }
        case SAI_HASH_ATTR_UDF_GROUP_LIST:
            {
                CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(sai_object_id_t),
                           p_hash_data->udf_group_list.list, p_hash_data->udf_group_list.count, &attr->value.objlist));
                break;
            }
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    int32 ret = 0;
    ctc_wb_data_t wb_data;
    sai_object_id_t hash_id = *(sai_object_id_t*)key;
    uint32  max_entry_cnt = 0;
    ctc_sai_ld_hash_t* p_hash_db = (ctc_sai_ld_hash_t*)data;
    ctc_sai_ld_hash_wb_t hash_wb;
    uint32 index = 0;
    uint32 offset = 0;

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);
    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_ld_hash_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_HASH);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);
    for (index = 0; index < p_hash_db->udf_group_list.count; index++)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        hash_wb.oid = hash_id;
        hash_wb.index = index;
        sal_memcpy(&hash_wb.udf_grp_id, &(p_hash_db->udf_group_list.list[index]), sizeof(sai_object_id_t));
        sal_memcpy((uint8*)wb_data.buffer + offset, &hash_wb, (wb_data.key_len + wb_data.data_len));
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
    return ret;
}

static sai_status_t
_ctc_sai_ld_hash_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t hash_id = *(sai_object_id_t*)key;
    ctc_sai_ld_hash_t* p_hash_db = (ctc_sai_ld_hash_t*)data;
    uint16 entry_cnt = 0;
    ctc_sai_ld_hash_wb_t hash_wb;
    ctc_wb_query_t wb_query;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, hash_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    p_hash_db->udf_group_list.list = (sai_object_id_t*)mem_malloc(MEM_SYSTEM_MODULE, p_hash_db->udf_group_list.count * sizeof(sai_object_id_t));
    if (NULL == p_hash_db->udf_group_list.list)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(p_hash_db->udf_group_list.list, 0, p_hash_db->udf_group_list.count * sizeof(sai_object_id_t));
    sal_memset(&wb_query, 0, sizeof(wb_query));
    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_ld_hash_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_HASH);
    wb_query.query_type = 1; /*query by key*/
    wb_query.buffer = (ctc_wb_key_data_t*)(&hash_wb);
    for (entry_cnt = 0; entry_cnt < p_hash_db->udf_group_list.count; entry_cnt++)
    {
        wb_query.valid_cnt = 0;
        hash_wb.oid = hash_id;
        hash_wb.index = entry_cnt;
        wb_query.key = (uint8*)(&hash_wb);
        ctc_wb_query_entry(&wb_query);
        if(wb_query.valid_cnt)
        {
            sal_memcpy(&(p_hash_db->udf_group_list.list[entry_cnt]), &hash_wb.udf_grp_id,  sizeof(sai_object_id_t));
        }
        else
        {
            mem_free(p_hash_db->udf_group_list.list);
            return SAI_STATUS_FAILURE;
        }
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_db_deinit_cb(ctc_sai_oid_property_t* bucket_data, void* user_data)
{
    ctc_sai_ld_hash_t* p_hash_info = (ctc_sai_ld_hash_t*)(bucket_data->data);

    if (NULL == bucket_data)
    {
        return SAI_STATUS_SUCCESS;
    }
    if (p_hash_info && p_hash_info->udf_group_list.list)
    {
        if (p_hash_info->udf_group_list.list)
        {
            mem_free(p_hash_info->udf_group_list.list);
        }
    }
    return SAI_STATUS_SUCCESS;
}

static  ctc_sai_attr_fn_entry_t hash_attr_fn_entries[] = {
    { SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
      _ctc_sai_ld_hash_get_attr,
      _ctc_sai_ld_hash_set_attr},
    { SAI_HASH_ATTR_UDF_GROUP_LIST,
      _ctc_sai_ld_hash_get_attr,
      _ctc_sai_ld_hash_set_attr},
    { CTC_SAI_FUNC_ATTR_END_ID,
       NULL,
       NULL }
};


#define ________SAI_DUMP________

static sai_status_t
_ctc_sai_ld_hash_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  hash_oid_cur = 0;
    ctc_sai_ld_hash_t    ctc_ld_hash_cur;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint8 hash_type = 0;
    uint8 ii = 0;

    sal_memset(&ctc_ld_hash_cur, 0, sizeof(ctc_sai_ld_hash_t));

    hash_oid_cur = bucket_data->oid;
    ctc_sai_oid_get_sub_type(hash_oid_cur, &hash_type);
    sal_memcpy((ctc_sai_ld_hash_t*)(&ctc_ld_hash_cur), bucket_data->data, sizeof(ctc_sai_ld_hash_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (hash_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_SUCCESS;
    }

   // CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-9s %-10s %-13s %-18s\n", "No.", "Hash_oid", "Hash_TYPE", "Field_bmp", "UDF_Group_Cnt", "UDF_Grp_oid");

    if(0 == ctc_ld_hash_cur.udf_group_list.count)
    {
        CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64 " %-9d 0x%-8x %-13d %-18s\n", num_cnt, hash_oid_cur, hash_type,\
            ctc_ld_hash_cur.field_bmp, ctc_ld_hash_cur.udf_group_list.count, "-");
    }
    else
    {
        CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64 " %-9d 0x%-8x %-13d 0x%016"PRIx64"\n",num_cnt, hash_oid_cur, hash_type,\
            ctc_ld_hash_cur.field_bmp, ctc_ld_hash_cur.udf_group_list.count, *(ctc_ld_hash_cur.udf_group_list.list));
    }
    if(1 < ctc_ld_hash_cur.udf_group_list.count)
    {
        for (ii = 1; ii < ctc_ld_hash_cur.udf_group_list.count; ii++)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-76s 0x%016"PRIx64"\n", " ",\
                ctc_ld_hash_cur.udf_group_list.list[ii]);
        }
    }

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________

void ctc_sai_ld_hash_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 1;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));

    CTC_SAI_LOG_DUMP(p_file, "\n%s\n", "# SAI Hash MODULE");
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_HASH))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "Hash");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_ld_hash_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-9s %-10s %-13s %-18s\n", "No.", "Hash_oid", "Hash_TYPE", "Field_bmp", "UDF_Group_Cnt", "UDF_Grp_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");

        sai_cb_data.value0 = p_file;
        sai_cb_data.value1 = &num_cnt;
        sai_cb_data.value2 = dump_grep_param;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HASH,
                                            (hash_traversal_fn)_ctc_sai_ld_hash_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________

static sai_status_t
ctc_sai_ld_hash_create_hash(sai_object_id_t *sai_hash_id,
                                         sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    CTC_SAI_LOG_ERROR(SAI_API_HASH, "create hash not support\n");
    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_ld_hash_remove_hash(sai_object_id_t sai_hash_id)
{
    CTC_SAI_LOG_ERROR(SAI_API_HASH, "remove hash not support\n");
    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_ld_hash_set_hash_attribute(sai_object_id_t sai_hash_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    ctc_sai_ld_hash_t* p_hash = NULL;
    sai_object_key_t key;
    sal_memset(&key, 0, sizeof(sai_object_key_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_hash_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    p_hash = ctc_sai_db_get_object_property(lchip, sai_hash_id);
    if(NULL == p_hash)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    key.key.object_id = sai_hash_id;

    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_HASH, hash_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_ld_hash_get_hash_attribute(sai_object_id_t sai_hash_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    ctc_sai_ld_hash_t*          p_hash = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(sai_hash_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    p_hash = ctc_sai_db_get_object_property(lchip, sai_hash_id);
    if(NULL == p_hash)
    {
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    key.key.object_id = sai_hash_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_HASH, loop, hash_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_hash_api_t ctc_sai_hash_api = {
    ctc_sai_ld_hash_create_hash,
    ctc_sai_ld_hash_remove_hash,
    ctc_sai_ld_hash_set_hash_attribute,
    ctc_sai_ld_hash_get_hash_attribute
};

sai_status_t
ctc_sai_ld_hash_api_init()
{
    ctc_sai_register_module_api(SAI_API_HASH, (void*)&ctc_sai_hash_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_ld_hash_db_init(uint8 lchip) /* called when create switch */
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    sai_object_key_t key;
    ctc_sai_ld_hash_t* p_oid_property = NULL;
    uint8 loop_i = 0;
    int32 list[4] = /* default field */
       {SAI_NATIVE_HASH_FIELD_SRC_MAC,
        SAI_NATIVE_HASH_FIELD_DST_MAC,
        SAI_NATIVE_HASH_FIELD_IN_PORT,
        SAI_NATIVE_HASH_FIELD_ETHERTYPE};

    sai_attribute_t sai_hash_attr;
    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(ctc_sai_db_wb_t));
    wb_info.version = SYS_WB_VERSION_HASH;
    wb_info.data_len = sizeof(ctc_sai_ld_hash_t);
    wb_info.wb_sync_cb = _ctc_sai_ld_hash_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_ld_hash_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HASH, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    sal_memset(&sai_hash_attr, 0, sizeof(sai_attribute_t));
    sai_hash_attr.id = SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST;
    sai_hash_attr.value.s32list.count = 4;
    sai_hash_attr.value.s32list.list = list;

    sal_memset(&key, 0, sizeof(sai_object_key_t));

    for (loop_i = 0; loop_i < CTC_SAI_HASH_USAGE_NUM; loop_i++)
    {   /* sub_type: 0 is CTC_SAI_HASH_USAGE_ECMP; 1 is CTC_SAI_HASH_USAGE_LINKAGG */
        key.key.object_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, loop_i, 0, 0);
        CTC_SAI_ERROR_GOTO(_ctc_sai_ld_hash_build_db(lchip, key.key.object_id, &p_oid_property),status,out); /* key.key.object_id is not alloced by opf,no need do roolback */
        CTC_SAI_ERROR_GOTO(_ctc_sai_ld_hash_set_attr(&key, &sai_hash_attr),status,error1);
    }
    return SAI_STATUS_SUCCESS;

error1:
    _ctc_sai_ld_hash_remove_db(lchip, key.key.object_id);
out:
    CTC_SAI_LOG_ERROR(SAI_API_HASH, "add hash default error, status= %d\n", status);
    return status;
}

sai_status_t
ctc_sai_ld_hash_db_deinit(uint8 lchip)
{
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_HASH, (hash_traversal_fn)_ctc_sai_ld_hash_db_deinit_cb, NULL);
    return SAI_STATUS_SUCCESS;
}
