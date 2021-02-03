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

struct ctc_sai_ld_hash_wb_s
{
    /* ld_hash id */
    sai_object_id_t oid;
    uint32 calc_key_len[0];

    /*data*/
    sai_object_id_t group_id;
};
typedef struct ctc_sai_ld_hash_wb_s ctc_sai_ld_hash_wb_t;

sai_status_t
_ctc_sai_ld_hash_check_udf_attr(uint8 lchip, const sai_attribute_t* attr, sai_object_id_t ld_hash_oid, uint8* p_udf_sel)
{
    uint8 ii = 0, jj = 0;
    uint8 chip_type = 0;
    uint8 udf_offset[CTC_SAI_UDF_OFFSET_NUM] = {0};
    uint8 offset_num = 0;
    uint8 offset_len = 0;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    p_hash_data = ctc_sai_db_get_object_property(lchip, ld_hash_oid);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    if (SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST == attr->id)
    {
        *p_udf_sel = CTC_LB_HASH_UDF_SEL_MAX_MODE;
    }
    else if (SAI_HASH_ATTR_UDF_GROUP_LIST == attr->id)
    {
        chip_type = ctcs_get_chip_type(lchip);
        *p_udf_sel = p_hash_data->udf_sel;

        if (attr->value.objlist.count == 0)
        {
            return SAI_STATUS_SUCCESS;
        }

        for (ii = 0; ii < attr->value.objlist.count; ii++)
        {
            p_udf_group = ctc_sai_db_get_object_property(lchip, attr->value.objlist.list[ii]);
            if (NULL == p_udf_group)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF group id is not exist\n");
                return SAI_STATUS_ITEM_NOT_FOUND;
            }

            for (jj = 0; jj < p_udf_group->length/CTC_SAI_UDF_OFFSET_BYTE_LEN; jj++)
            {
                udf_offset[offset_num] = p_udf_group->offset[jj];
                offset_num++;
            }
            offset_len += p_udf_group->length;
        }

        if (offset_len > sizeof(uint32))
        {
            CTC_SAI_LOG_ERROR(SAI_API_HASH, "Total udf group's length:%u exceed max byte length 4!\n", offset_len);
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
        }

        if (CTC_CHIP_TSINGMA == chip_type)
        {
            switch (udf_offset[0])
            {
                case 0:
                    *p_udf_sel = 0;
                    break;
                case 1:
                    *p_udf_sel = 1;
                    break;
                case 2:
                    *p_udf_sel = 2;
                    break;
                case 3:
                    *p_udf_sel = 3;
                    break;
                default:
                    CTC_SAI_LOG_ERROR(SAI_API_HASH, "udf offset[0]:%u is not support!\n", udf_offset[0]);
                    return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
        }
        else if (CTC_CHIP_TSINGMA_MX == chip_type)
        {
            if ((offset_num == 1 && (udf_offset[0] == 0 || udf_offset[0] == 1)) || (offset_num == 2 && udf_offset[0] == 0 && udf_offset[1] == 1))
            {
                *p_udf_sel = 0;
            }
            else if ((offset_num == 1 && (udf_offset[0] == 2 || udf_offset[0] == 3)) || (offset_num == 2 && udf_offset[0] == 2 && udf_offset[1] == 3))
            {
                *p_udf_sel = 1;
            }
            else if ((offset_num == 1 && (udf_offset[0] == 4 || udf_offset[0] == 5)) || (offset_num == 2 && udf_offset[0] == 4 && udf_offset[1] == 5))
            {
                *p_udf_sel = 2;
            }
            else if ((offset_num == 1 && (udf_offset[0] == 6 || udf_offset[0] == 7)) || (offset_num == 2 && udf_offset[0] == 6 && udf_offset[1] == 7))
            {
                *p_udf_sel = 3;
            }
            else
            {
                CTC_SAI_LOG_ERROR(SAI_API_HASH, "udf offset[0]:%u and offset[1]:%u is not support!\n", udf_offset[0], udf_offset[1]);
                return SAI_STATUS_ATTR_NOT_SUPPORTED_0;
            }
        }
    }
    else
    {
        CTC_SAI_LOG_ERROR(SAI_API_HASH, "set hash attribute not support: attribute_id %d\n", attr->id);
        return  SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_ld_hash_update_udf_group(uint8 lchip, const sai_attribute_t* attr, sai_object_id_t ld_hash_oid)
{
    uint8 ii = 0;
	uint8 jj = 0;
    ctc_object_id_t ctc_object_id = {0};
    ctc_slist_t* udf_group_list = NULL;
    ctc_slistnode_t* entry_node = NULL;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_ld_hash_group_t* p_hash_data_group = NULL;
    ctc_lb_hash_config_t ctc_lb_hash_config;

    uint32 template_ip[] = {
        CTC_LB_HASH_SELECT_IPV4,
        CTC_LB_HASH_SELECT_IPV4_TCP_UDP,
        CTC_LB_HASH_SELECT_IPV4_TCP_UDP_PORTS_EQUAL,
        CTC_LB_HASH_SELECT_IPV4_VXLAN,
        CTC_LB_HASH_SELECT_IPV4_GRE,
        CTC_LB_HASH_SELECT_IPV4_NVGRE,
        CTC_LB_HASH_SELECT_IPV6,
        CTC_LB_HASH_SELECT_IPV6_TCP_UDP,
        CTC_LB_HASH_SELECT_IPV6_TCP_UDP_PORTS_EQUAL,
        CTC_LB_HASH_SELECT_IPV6_VXLAN,
        CTC_LB_HASH_SELECT_IPV6_GRE,
        CTC_LB_HASH_SELECT_IPV6_NVGRE,
        CTC_LB_HASH_SELECT_NVGRE_INNER_IPV4,
        CTC_LB_HASH_SELECT_NVGRE_INNER_IPV6,
        CTC_LB_HASH_SELECT_VXLAN_INNER_IPV4,
        CTC_LB_HASH_SELECT_VXLAN_INNER_IPV6,
        CTC_LB_HASH_SELECT_MPLS_L2VPN_INNER_IPV4,
        CTC_LB_HASH_SELECT_MPLS_L2VPN_INNER_IPV6,
        CTC_LB_HASH_SELECT_MPLS_L3VPN_INNER_IPV4,
        CTC_LB_HASH_SELECT_MPLS_L3VPN_INNER_IPV6,
        CTC_LB_HASH_SELECT_TRILL_INNER_IPV4,
        CTC_LB_HASH_SELECT_TRILL_INNER_IPV6,
        CTC_LB_HASH_SELECT_TRILL_DECAP_INNER_IPV4,
        CTC_LB_HASH_SELECT_TRILL_DECAP_INNER_IPV6,
        CTC_LB_HASH_SELECT_FCOE,
        CTC_LB_HASH_SELECT_FLEX_TNL_INNER_IPV4,
        CTC_LB_HASH_SELECT_FLEX_TNL_INNER_IPV6
    };

    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    p_hash_data = ctc_sai_db_get_object_property(lchip, ld_hash_oid);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HASH, ld_hash_oid, &ctc_object_id);

    if (SAI_HASH_ATTR_UDF_GROUP_LIST == attr->id)
    {
        udf_group_list = ctc_slist_new();
        if (NULL == udf_group_list)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Fail to allocate udf group list memory\n");
            return SAI_STATUS_NO_MEMORY;
        }

        for (ii = 0; ii < attr->value.objlist.count; ii++)
        {
            MALLOC_ZERO(MEM_ACL_MODULE, p_hash_data_group, sizeof(ctc_sai_ld_hash_group_t));
            if (NULL == p_hash_data_group)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Fail to allocate ld hash udf group memory\n");
                goto error1;
            }
            p_udf_group = ctc_sai_db_get_object_property(lchip, attr->value.objlist.list[ii]);
            p_udf_group->ref_cnt++;
            p_hash_data_group->group_id = attr->value.objlist.list[ii];
            ctc_slist_add_head(udf_group_list, &(p_hash_data_group->head));
        }

        CTC_SLIST_LOOP(p_hash_data->udf_group_list, entry_node)
        {
            p_hash_data_group = (ctc_sai_ld_hash_group_t*)entry_node;
            p_udf_group = ctc_sai_db_get_object_property(lchip, p_hash_data_group->group_id);
            p_udf_group->ref_cnt--;
        }
        ctc_slist_delete(p_hash_data->udf_group_list);
        p_hash_data->udf_group_list = udf_group_list;

        //set select
        for (jj = 0; jj < sizeof(template_ip) / 4; jj++)
        {
            sal_memset(&ctc_lb_hash_config, 0, sizeof(ctc_lb_hash_config_t));
            CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
            CTC_SET_FLAG(ctc_lb_hash_config.sel_id, (ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_LINKAGG) ? CTC_SAI_HASH_USAGE_LINKAGG : CTC_SAI_HASH_USAGE_ECMP);
            CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
			ctc_lb_hash_config.hash_select = template_ip[jj];
            CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_UDF_LO);
            CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_UDF_HI);
			CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
        }

        sal_memset(&ctc_lb_hash_config, 0, sizeof(ctc_lb_hash_config_t));
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, (ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_LINKAGG) ? CTC_SAI_HASH_USAGE_LINKAGG : CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_L2_ONLY);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
        ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config);

        sal_memset(&ctc_lb_hash_config, 0, sizeof(ctc_lb_hash_config_t));
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, (ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_LINKAGG) ? CTC_SAI_HASH_USAGE_LINKAGG : CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_UDF_SELECT_MODE);
        CTC_SET_FLAG(ctc_lb_hash_config.value, p_hash_data->udf_sel);
        CTC_SAI_LOG_INFO(SAI_API_HASH, "udf sel = %d\n", p_hash_data->udf_sel);
        ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config);
    }
    goto error0;

error1:
    ctc_slist_delete(udf_group_list);

error0:
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_build_db(uint8 lchip, sai_object_id_t hash_obj_id, ctc_sai_ld_hash_t** oid_property)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
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
    p_hash_data->udf_sel = CTC_LB_HASH_UDF_SEL_MAX_MODE;
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
_ctc_sai_ld_hash_set_udf(uint8 lchip, uint8 hash_usage, sai_object_id_t ld_hash_oid)
{
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_lb_hash_config_t ctc_lb_hash_config;

    p_hash_data = ctc_sai_db_get_object_property(lchip, ld_hash_oid);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    sal_memset(&ctc_lb_hash_config, 0, sizeof(ctc_lb_hash_config_t));

    CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, (CTC_SAI_HASH_USAGE_LINKAGG == hash_usage) ? CTC_SAI_HASH_USAGE_LINKAGG : CTC_SAI_HASH_USAGE_ECMP);
    CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
    CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_UDF_SELECT_MODE);
    CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_set_lag_hash(uint8 lchip, uint32 field_bmp)
{
    ctc_linkagg_psc_t ctc_linkagg_psc;
    ctc_lb_hash_config_t ctc_lb_hash_config;
    ctc_lb_hash_offset_t ctc_lb_hash_offset;

    sal_memset(&ctc_linkagg_psc, 0, sizeof(ctc_linkagg_psc_t));
    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    sal_memset(&ctc_lb_hash_offset, 0 , sizeof(ctc_lb_hash_offset_t));

    /*for don't clear table, set default select id use 2*/
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    /* for update, only fields updated are valid, so must clean default value */
    //CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);

    /* SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST */
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_SRC_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_DST_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_IPDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_VLAN_ID))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_VLAN);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_PROTOCOL);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_ETHERTYPE);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_SRC_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_DST_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_DST_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_IN_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_IP);
        CTC_SET_FLAG(ctc_linkagg_psc.ip_flag, CTC_LINKAGG_PSC_IP_PROTOCOL);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_ETHERTYPE);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_SRC_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L4);
        CTC_SET_FLAG(ctc_linkagg_psc.l4_flag, CTC_LINKAGG_PSC_L4_DST_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC))
    {
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_INNER);
        CTC_SET_FLAG(ctc_linkagg_psc.psc_type_bitmap, CTC_LINKAGG_PSC_TYPE_L2);
        CTC_SET_FLAG(ctc_linkagg_psc.l2_flag, CTC_LINKAGG_PSC_L2_MACDA);
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_linkagg_set_psc(lchip, &ctc_linkagg_psc));

    /* MPLS Hash process*/
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_ALL))
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

        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_0))
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
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_1))
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
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_2))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_DISABLE_MPLS);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));

        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_MPLS_LABEL2_EN);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 1);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
        sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));

        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_set_ecmp_hash(uint8 lchip, uint32 field_bmp)
{
    ctc_parser_ecmp_hash_ctl_t ctc_ecmp_ctl;
    ctc_parser_global_cfg_t ctc_parser_global_ctl;
    ctc_lb_hash_config_t ctc_lb_hash_config;
    ctc_lb_hash_offset_t ctc_lb_hash_offset;

    sal_memset(&ctc_ecmp_ctl, 0, sizeof(ctc_parser_ecmp_hash_ctl_t));
    sal_memset(&ctc_parser_global_ctl, 0 , sizeof(ctc_parser_global_cfg_t));
    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    sal_memset(&ctc_lb_hash_offset, 0 , sizeof(ctc_lb_hash_offset_t));

    /*for don't clear table, set default select id use 2*/
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    /* for update, only fields updated are valid, so must clean default value */
    //CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2); /* last alredeady */

    CTC_SAI_LOG_ENTER(SAI_API_HASH);

    /* SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST */
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_SRC_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_DST_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_IP))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_IPDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_VLAN_ID))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_CTAG_VID);  /* sai: vlan id; centec: svlan id,cvaln id */
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_STAG_VID);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_PROTOCOL);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_ETHERTYPE);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_SRC_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_DST_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_DST_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACDA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_IN_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_IP);
        CTC_SET_FLAG(ctc_ecmp_ctl.ip_flag, CTC_PARSER_IP_HASH_FLAGS_PROTOCOL);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_ETHERTYPE);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_SRC_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L4);
        CTC_SET_FLAG(ctc_ecmp_ctl.l4_flag, CTC_PARSER_L4_HASH_FLAGS_DST_PORT);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACSA);
    }
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC))
    {
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_INNER);
        CTC_SET_FLAG(ctc_ecmp_ctl.hash_type_bitmap, CTC_PARSER_HASH_TYPE_FLAGS_L2);
        CTC_SET_FLAG(ctc_ecmp_ctl.l2_flag, CTC_PARSER_L2_HASH_FLAGS_MACDA);
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_ecmp_hash_field(lchip, &ctc_ecmp_ctl));

    /* MPLS Hash process*/
    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_ALL))
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

        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_0))
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
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_1))
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
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL1_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    if (CTC_IS_BIT_SET(field_bmp, SAI_NATIVE_HASH_FIELD_MPLS_LABEL_2))
    {
        CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_DISABLE_MPLS);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 0);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));

        CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_MPLS_LABEL2_EN);
        CTC_SET_FLAG(ctc_lb_hash_config.value, 1);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
        sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));

        CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
        CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_SELECT);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_LO);
        CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_FIELD_LABEL2_HI);
        CTC_SET_FLAG(ctc_lb_hash_config.hash_select, CTC_LB_HASH_SELECT_MPLS);
        CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));
    }

    ctc_parser_global_ctl.ecmp_hash_type = CTC_PARSER_GEN_HASH_TYPE_XOR;
    CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 udf_sel = 0;
    uint32 ii = 0;
    /* for update, only fields updated are valid, so must clean default value */
    uint32 field_bmp = 0;
    ctc_object_id_t ctc_object_id;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_linkagg_psc_t ctc_linkagg_psc;
    ctc_parser_ecmp_hash_ctl_t ctc_ecmp_ctl;

    sal_memset(&ctc_linkagg_psc, 0, sizeof(ctc_linkagg_psc_t));
    sal_memset(&ctc_ecmp_ctl, 0, sizeof(ctc_parser_ecmp_hash_ctl_t));
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_hash_data = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_hash_data)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    CTC_SAI_ERROR_RETURN(_ctc_sai_ld_hash_check_udf_attr(lchip, attr, key->key.object_id, &udf_sel));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_HASH, key->key.object_id, &ctc_object_id);

    for (ii = 0; ii < attr->value.s32list.count; ii++)
    {
        CTC_BIT_SET(field_bmp, attr->value.s32list.list[ii]);
    }
    /* ecmp hash:   sub_type = 0; */
    if (ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_ECMP)
    {
        if (SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST == attr->id)
        {
            /* clean last hash field value updated */
            ctc_ecmp_ctl.hash_type_bitmap = CTC_PARSER_HASH_TYPE_FLAGS_IP | CTC_PARSER_HASH_TYPE_FLAGS_L4 | CTC_PARSER_HASH_TYPE_FLAGS_MPLS
                                           | CTC_PARSER_HASH_TYPE_FLAGS_FCOE | CTC_PARSER_HASH_TYPE_FLAGS_TRILL | CTC_PARSER_HASH_TYPE_FLAGS_L2;
            CTC_SAI_CTC_ERROR_GOTO((ctcs_parser_set_ecmp_hash_field(lchip, &ctc_ecmp_ctl)), status, error0);
			CTC_SAI_ERROR_GOTO(_ctc_sai_set_ecmp_hash(lchip, field_bmp), status, error0);
        }
    }
    else if (ctc_object_id.sub_type == CTC_SAI_HASH_USAGE_LINKAGG)  /* linkagg hash: sub_type = 1; */
    {
        if (SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST == attr->id)
        {
            /* clean last hash field value updated */
            ctc_linkagg_psc.psc_type_bitmap = CTC_LINKAGG_PSC_TYPE_L2 | CTC_LINKAGG_PSC_TYPE_IP | CTC_LINKAGG_PSC_TYPE_L4 \
                                             | CTC_LINKAGG_PSC_TYPE_MPLS| CTC_LINKAGG_PSC_TYPE_FCOE |CTC_LINKAGG_PSC_TYPE_TRILL;
            CTC_SAI_CTC_ERROR_GOTO((ctcs_linkagg_set_psc(lchip, &ctc_linkagg_psc)),status,error0);
			CTC_SAI_ERROR_GOTO(_ctc_sai_set_lag_hash(lchip, field_bmp), status, error0);
        }
    }
    else
    {
        status = SAI_STATUS_INVALID_PARAMETER;
        goto error0;
    }
    p_hash_data->field_bmp = field_bmp;
    p_hash_data->udf_sel = udf_sel;
    _ctc_sai_ld_hash_update_udf_group(lchip, attr, key->key.object_id);

error0:
    return status;
}

static sai_status_t
_ctc_sai_ld_hash_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 ii = 0;
    uint8 count = 0;
    ctc_slistnode_t* p_group_node = NULL;
    ctc_sai_ld_hash_t* p_hash_data = NULL;
    ctc_sai_ld_hash_group_t* p_hash_data_group = NULL;

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
            int32_t s32list[SAI_NATIVE_HASH_FIELD_MPLS_LABEL_ALL];
            for (ii = SAI_NATIVE_HASH_FIELD_SRC_IP; ii <= SAI_NATIVE_HASH_FIELD_MPLS_LABEL_ALL; ii++)
            {
                if (CTC_IS_BIT_SET(p_hash_data->field_bmp, ii))
                {
                    s32list[count++] = ii;
                }
            }
            CTC_SAI_ERROR_RETURN(ctc_sai_fill_object_list(sizeof(int32_t),
                       s32list, count, &attr->value.objlist));
            break;
        }
        case SAI_HASH_ATTR_UDF_GROUP_LIST:
        {
            CTC_SLIST_LOOP(p_hash_data->udf_group_list, p_group_node)
            {
                p_hash_data_group = (ctc_sai_ld_hash_group_t*)p_group_node;
                attr->value.objlist.list[ii++] = p_hash_data_group->group_id;
            }
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
    int32 ret = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    ctc_wb_data_t wb_data;
    ctc_slistnode_t* entry_node = NULL;
    sai_object_id_t ld_hash_id = *(sai_object_id_t*)key;
    ctc_sai_ld_hash_t* p_ld_hash = (ctc_sai_ld_hash_t*)data;
    ctc_sai_ld_hash_wb_t wb_ld_hash;
    ctc_sai_ld_hash_group_t* p_ld_hash_group = NULL;

    sal_memset(&wb_ld_hash, 0, sizeof(ctc_sai_ld_hash_wb_t));
    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_ld_hash_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_HASH);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_ld_hash->udf_group_list, entry_node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_ld_hash_group = (ctc_sai_ld_hash_group_t*)entry_node;
        wb_ld_hash.oid = ld_hash_id;
        wb_ld_hash.group_id = p_ld_hash_group->group_id;

        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_ld_hash, (wb_data.key_len + wb_data.data_len));
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
    ctc_sai_ld_hash_t *p_ld_hash = (ctc_sai_ld_hash_t*)data;

    p_ld_hash->udf_group_list = ctc_slist_new();

    if (NULL == p_ld_hash->udf_group_list)
    {
        return SAI_STATUS_NO_MEMORY;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_ld_hash_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_ld_hash_wb_t wb_ld_hash;
    ctc_sai_ld_hash_t *p_ld_hash = NULL;
    ctc_sai_ld_hash_group_t *p_ld_hash_group = NULL;

    sal_memset(&wb_ld_hash, 0, sizeof(ctc_sai_ld_hash_wb_t));
    sal_memset(&wb_query, 0, sizeof(wb_query));

    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_ld_hash_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_HASH);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_ld_hash, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_ld_hash_wb_t));
        p_ld_hash = ctc_sai_db_get_object_property(lchip, wb_ld_hash.oid);
        if (!p_ld_hash)
        {
            continue;
        }

        p_ld_hash_group = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_ld_hash_group_t));
        if (!p_ld_hash_group)
        {
            continue;
        }
        p_ld_hash_group->group_id = wb_ld_hash.group_id;
        ctc_slist_add_tail(p_ld_hash->udf_group_list, &(p_ld_hash_group->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static sai_status_t
_ctc_sai_ld_hash_db_deinit_cb(ctc_sai_oid_property_t* bucket_data, void* user_data)
{
    ctc_slistnode_t *cur_node = NULL;
    ctc_slistnode_t *next_node = NULL;
    ctc_sai_oid_property_t *p_oid_property = NULL;
    ctc_sai_ld_hash_t* p_ld_hash = NULL;
    ctc_sai_ld_hash_group_t *p_ld_hash_group = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_ld_hash = (ctc_sai_ld_hash_t*)(p_oid_property->data);

    CTC_SLIST_LOOP_DEL(p_ld_hash->udf_group_list, cur_node, next_node)
    {
        p_ld_hash_group = (ctc_sai_ld_hash_group_t*)cur_node;
        mem_free(p_ld_hash_group);
    }
    ctc_slist_free(p_ld_hash->udf_group_list);

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
    ctc_slistnode_t *entry_node = NULL;
    uint8 count = 0;

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

    CTC_SAI_LOG_DUMP(p_file, "%-3d 0x%016"PRIx64 " %-9d 0x%-8x %-13d \n", num_cnt, hash_oid_cur, hash_type,
                     ctc_ld_hash_cur.field_bmp, ctc_ld_hash_cur.udf_group_list->count);

    if(0 < ctc_ld_hash_cur.udf_group_list->count)
    {
        if (ctc_ld_hash_cur.udf_group_list)
        {
            ctc_sai_ld_hash_group_t* p_hash_udf_group = NULL;
            entry_node = NULL;
            count = 0;
            CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF group list:");
            CTC_SLIST_LOOP(ctc_ld_hash_cur.udf_group_list, entry_node)
            {
                p_hash_udf_group = (ctc_sai_ld_hash_group_t*)entry_node;
                CTC_SAI_LOG_DUMP(p_file, "0x%016"PRIx64"  ", p_hash_udf_group->group_id);
                if (count++ >= 5)
                {
                    CTC_SAI_LOG_DUMP(p_file, "\n");
                }
            }
            CTC_SAI_LOG_DUMP(p_file, "\n");
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
        CTC_SAI_LOG_DUMP(p_file, "%-3s %-18s %-9s %-10s %-13s \n", "No.", "Hash_oid", "Hash_TYPE", "Field_bmp", "UDF_Group_Cnt");
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
    uint8 ii = 0;
    /* default field */
    int32 list[4] = {SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE};
    sai_attribute_t sai_hash_attr;
    //ctc_parser_global_cfg_t ctc_parser_global_ctl;

    ctc_sai_db_wb_t wb_info;
    sal_memset(&wb_info, 0, sizeof(ctc_sai_db_wb_t));
    wb_info.version = SYS_WB_VERSION_HASH;
    wb_info.data_len = sizeof(ctc_sai_ld_hash_t);
    wb_info.wb_sync_cb = _ctc_sai_ld_hash_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_ld_hash_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_ld_hash_wb_reload_cb1;

    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_HASH, (void*)(&wb_info));

    CTC_SAI_WARMBOOT_STATUS_CHECK(lchip);

    sal_memset(&sai_hash_attr, 0, sizeof(sai_attribute_t));
    sai_hash_attr.id = SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST;
    sai_hash_attr.value.s32list.count = 4;
    sai_hash_attr.value.s32list.list = list;

    sal_memset(&key, 0, sizeof(sai_object_key_t));

    for (ii = 0; ii < CTC_SAI_HASH_USAGE_NUM; ii++)
    {   /* sub_type: 0 is CTC_SAI_HASH_USAGE_ECMP; 1 is CTC_SAI_HASH_USAGE_LINKAGG */
        key.key.object_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, ii, 0, 0);
        /* key.key.object_id is not alloced by opf,no need do roolback */
        CTC_SAI_ERROR_GOTO(_ctc_sai_ld_hash_build_db(lchip, key.key.object_id, &p_oid_property), status, out);
        p_oid_property->udf_group_list = ctc_slist_new();
        if (!p_oid_property->udf_group_list)
        {
            status = SAI_STATUS_NO_MEMORY;
            goto error1;
        }
        CTC_SAI_ERROR_GOTO(_ctc_sai_ld_hash_set_attr(&key, &sai_hash_attr), status, error2);
    }

    //sal_memset(&ctc_parser_global_ctl, 0, sizeof(ctc_parser_global_cfg_t));
    //ctc_parser_global_ctl.ecmp_hash_type = CTC_PARSER_GEN_HASH_TYPE_XOR;
    //ctc_parser_global_ctl.linkagg_hash_type = CTC_PARSER_GEN_HASH_TYPE_XOR;
    //CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_global_cfg(lchip, &ctc_parser_global_ctl));

    ctc_lb_hash_config_t ctc_lb_hash_config;
    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_LINKAGG);
    CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
    CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_HASH_TYPE_A);
    CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_TYPE_CRC16_POLY1);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));

    sal_memset(&ctc_lb_hash_config, 0 , sizeof(ctc_lb_hash_config_t));
    CTC_UNSET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_NUM);
    CTC_SET_FLAG(ctc_lb_hash_config.sel_id, CTC_SAI_HASH_USAGE_ECMP);
    CTC_SET_FLAG(ctc_lb_hash_config.cfg_type, CTC_LB_HASH_CFG_HASH_CONTROL);
    CTC_SET_FLAG(ctc_lb_hash_config.hash_control, CTC_LB_HASH_CONTROL_HASH_TYPE_A);
    CTC_SET_FLAG(ctc_lb_hash_config.value, CTC_LB_HASH_TYPE_CRC16_POLY2);
    CTC_SAI_CTC_ERROR_RETURN(ctcs_global_ctl_set(lchip, CTC_GLOBAL_LB_HASH_KEY, &ctc_lb_hash_config));

    return SAI_STATUS_SUCCESS;

error2:
    mem_free(p_oid_property->udf_group_list);
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

