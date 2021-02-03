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

struct ctc_sai_udf_group_member_wb_s
{
    /* ld_hash id */
    sai_object_id_t oid;
    uint32 calc_key_len[0];

    /* data */
    sai_object_id_t udf_id;
};
typedef struct ctc_sai_udf_group_member_wb_s ctc_sai_udf_group_member_wb_t;

struct ctc_sai_udf_group_hash_wb_s
{
    /* key */
    sai_object_id_t oid;
    uint32 calc_key_len[0];

    /* data */
    sai_object_id_t ld_hash_id;
};
typedef struct ctc_sai_udf_group_hash_wb_s ctc_sai_udf_group_hash_wb_t;

static sai_status_t
_ctc_sai_udf_build_udf_group_db(uint8 lchip, sai_object_id_t udf_group_obj_id, ctc_sai_udf_group_t** oid_property)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t* p_udf_group = NULL;

    p_udf_group = mem_malloc(MEM_ACL_MODULE, sizeof(ctc_sai_udf_group_t));
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_udf_group, 0, sizeof(ctc_sai_udf_group_t));
    status = ctc_sai_db_add_object_property(lchip, udf_group_obj_id, (void*)p_udf_group);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_udf_group);
    }
    *oid_property = p_udf_group;

    return status;
}

static sai_status_t
_ctc_sai_udf_remove_udf_group_db(uint8 lchip, sai_object_id_t udf_group_obj_id)
{
   ctc_sai_udf_group_t* p_udf_group = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_obj_id);
    if (NULL == p_udf_group)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, udf_group_obj_id);
    mem_free(p_udf_group);
    return SAI_STATUS_SUCCESS;
}


static sai_status_t
_ctc_sai_udf_build_udf_match_db(uint8 lchip, sai_object_id_t udf_match_oid, ctc_sai_udf_match_t** oid_property)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_match_t* p_udf_match = NULL;

    p_udf_match = mem_malloc(MEM_ACL_MODULE, sizeof(ctc_sai_udf_match_t));
    if (NULL == p_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_udf_match, 0, sizeof(ctc_sai_udf_match_t));
    status = ctc_sai_db_add_object_property(lchip, udf_match_oid, (void*)p_udf_match);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_udf_match);
    }
    *oid_property = p_udf_match;

    return status;
}

static sai_status_t
_ctc_sai_udf_remove_udf_match_db(uint8 lchip, sai_object_id_t udf_match_oid)
{
    ctc_sai_udf_match_t* p_udf_match = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_oid);
    if (NULL == p_udf_match)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, udf_match_oid);
    mem_free(p_udf_match);

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_remove_udf_db(uint8 lchip, sai_object_id_t udf_obj_id)
{
    ctc_sai_udf_entry_t*   p_udf = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf = ctc_sai_db_get_object_property(lchip, udf_obj_id);
    if (NULL == p_udf)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_db_remove_object_property(lchip, udf_obj_id);
    mem_free(p_udf);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_oid_get_udf_group_id(sai_object_id_t oid, uint32* udf_group_id)
{
    ctc_object_id_t ctc_object_id = {0};

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, oid, &ctc_object_id));
    if (ctc_object_id.type != SAI_OBJECT_TYPE_UDF_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Invalid udf group object type 0x%"PRIx64" \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }
    *udf_group_id = ctc_object_id.value;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_group_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 group_type = 0;
    ctc_slistnode_t* p_member_node = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf_group = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_udf_group)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_UDF_GROUP_ATTR_UDF_LIST:
        {
            CTC_SLIST_LOOP(p_udf_group->member_list, p_member_node)
            {
                p_udf_group_member = (ctc_sai_udf_group_member_t*)p_member_node;
                p_udf_entry = ctc_sai_db_get_object_property(lchip, p_udf_group_member->udf_oid);

                if (NULL == p_udf_entry)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_UDF,
                                      "Failed to get udf property of group_id 0x%"PRIx64"'s udf member udf_id 0x%"PRIx64"!\n",
                                      key->key.object_id, p_udf_group_member->udf_oid);
                    return SAI_STATUS_ITEM_NOT_FOUND;
                }
                attr->value.objlist.list[attr->value.objlist.count++] = p_udf_group_member->udf_oid;
            }
            break;
        }
        case SAI_UDF_GROUP_ATTR_TYPE:
            CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_sub_type(key->key.object_id, &group_type));
            attr->value.s32 = group_type;
            break;
        case SAI_UDF_GROUP_ATTR_LENGTH:
            attr->value.u16 = p_udf_group->length;
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
            break;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_match_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_udf_match_t*         p_udf_match = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf_match = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf match, invalid udf_match_id 0x%"PRIx64"!\n", key->key.object_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_UDF_MATCH_ATTR_L2_TYPE:   /* @flags CREATE_ONLY */
            attr->value.aclfield.data.u16 = p_udf_match->ethertype[0];
            attr->value.aclfield.mask.u16 = p_udf_match->ethertype[1];
            break;
        case SAI_UDF_MATCH_ATTR_L3_TYPE:   /* @flags CREATE_ONLY */
            attr->value.aclfield.data.u8 = p_udf_match->ip_protocal[0];
            attr->value.aclfield.mask.u8 = p_udf_match->ip_protocal[1];
            break;
        case SAI_UDF_MATCH_ATTR_GRE_TYPE:  /* @flags CREATE_ONLY */
            attr->value.aclfield.data.u16 = p_udf_match->gre_protocal_type[0];
            attr->value.aclfield.mask.u16 = p_udf_match->gre_protocal_type[1];
            break;
        case SAI_UDF_MATCH_ATTR_PRIORITY:  /* @flags CREATE_ONLY */
            attr->value.u8 = p_udf_match->priority;
            break;
        case SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM: /* @flags CREATE_ONLY */
            attr->value.u8 = p_udf_match->mpls_label_num;
            break;
        case SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT: /* @flags CREATE_ONLY */
            attr->value.aclfield.data.u16 = p_udf_match->l4_src_port[0];
            attr->value.aclfield.mask.u16 = p_udf_match->l4_src_port[1];
            break;
        case SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT: /* @flags CREATE_ONLY */
            attr->value.aclfield.data.u16 = p_udf_match->l4_dst_port[0];
            attr->value.aclfield.mask.u16 = p_udf_match->l4_dst_port[1];
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    sai_status_t status = SAI_STATUS_SUCCESS;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf_entry = ctc_sai_db_get_object_property(lchip, key->key.object_id);

    if (NULL == p_udf_entry)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch (attr->id)
    {
        case SAI_UDF_ATTR_MATCH_ID:    /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.oid = p_udf_entry->match_oid;
            break;
        case SAI_UDF_ATTR_GROUP_ID:    /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.oid = p_udf_entry->group_oid;
            break;
        case SAI_UDF_ATTR_BASE:        /* @flags CREATE_AND_SET */
            attr->value.s32 = p_udf_entry->base;
            break;
        case SAI_UDF_ATTR_OFFSET:      /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.u16 = p_udf_entry->offset;
            break;
        case SAI_UDF_ATTR_HASH_MASK:   /* @flags CREATE_AND_SET */
            p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf_entry->group_oid);
            if (NULL == p_udf_group)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "The udf_group_id 0x%"PRIx64" of UDF entry id 0x%"PRIx64" is invalid!\n", p_udf_entry->group_oid, key->key.object_id);
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error0;
            }
            attr->value.u8list.count = p_udf_group->length;
            sal_memcpy(attr->value.u8list.list, p_udf_entry->hash_mask, p_udf_group->length);
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }

error0:
    return status;
}

static sai_status_t
_ctc_sai_udf_entry_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf_entry = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf, invalid udf_id 0x%"PRIx64"!\n", key->key.object_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_UDF_ATTR_HASH_MASK:
            sal_memcpy(p_udf_entry->hash_mask, attr->value.u8list.list, attr->value.u8list.count);
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_add_udf(sai_object_id_t udf_entry_oid, sai_object_id_t udf_match_oid, sai_object_id_t udf_group_oid, uint32 ctc_udf_group_id, uint8* p_free_offset)
{
    int8 field_num = 0;
    uint8 lchip = 0;
    uint8 chip_type = 0;
    uint8 layer4_type = 0;
    uint32 ii = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_object_id_t ctc_object_id = {0};
    ctc_acl_classify_udf_t ctc_udf_entry;
    ctc_field_key_t ctc_field_key;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_entry_oid, &lchip));

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_oid);
    p_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_oid);
    p_udf_entry = ctc_sai_db_get_object_property(lchip, udf_entry_oid);

    sal_memset(&ctc_udf_entry, 0, sizeof(ctc_acl_classify_udf_t));

    ctc_udf_entry.udf_ad_id = ctc_udf_group_id;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_MATCH, udf_match_oid, &ctc_object_id);

    chip_type = ctcs_get_chip_type(lchip);
    if (CTC_CHIP_TSINGMA == chip_type)
    {
        ctc_udf_entry.priority = ctc_object_id.value + 1;
    }
    else if (CTC_CHIP_TSINGMA_MX == chip_type)
    {
        ctc_udf_entry.priority = p_udf_match->priority;
    }
    ctc_udf_entry.priority = ctc_object_id.value;

    ctc_udf_entry.udf_id = ctc_object_id.value;
    ctc_udf_entry.shared_udf = 1;
    ctc_udf_entry.granularity = 1;
    ctc_udf_entry.query_type = 0;

    ctcs_acl_get_udf_entry(lchip, &ctc_udf_entry);
    field_num = p_udf_group->length/CTC_SAI_UDF_OFFSET_BYTE_LEN;

    for (ii = 0; ii < field_num; ii++)
    {
        ctc_udf_entry.offset[p_free_offset[ii]] = p_udf_entry->offset + ii*CTC_SAI_UDF_OFFSET_BYTE_LEN;
        ctc_udf_entry.offset_type_array[p_free_offset[ii]] = p_udf_entry->base + 1;
        ctc_udf_entry.offset_num += ((p_free_offset[ii]==ctc_udf_entry.offset_num)?1:0);
    }
    CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry(lchip, &ctc_udf_entry));
    p_udf_match->ctc_group_id = ctc_udf_group_id;

    sal_memset(&ctc_field_key, 0, sizeof(ctc_field_key_t));
    if (p_udf_match->ethertype[1])
    {
        ctc_field_key.type = CTC_FIELD_KEY_ETHER_TYPE;
        ctc_field_key.data = p_udf_match->ethertype[0];
        ctc_field_key.mask = p_udf_match->ethertype[1];
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
    }
    if (p_udf_match->ip_protocal[1])
    {
        if( p_udf_match->ip_protocal[0] == 6 )
        {
            layer4_type = CTC_PARSER_L4_TYPE_TCP;
        }
        else if( p_udf_match->ip_protocal[0] == 17 )
        {
            layer4_type = CTC_PARSER_L4_TYPE_UDP;
        }
        else if( p_udf_match->ip_protocal[0] == 27 )
        {
            layer4_type = CTC_PARSER_L4_TYPE_RDP;
        }
        else if( p_udf_match->ip_protocal[0] == 132 )
        {
            layer4_type = CTC_PARSER_L4_TYPE_SCTP;
        }
        else if( p_udf_match->ip_protocal[0] == 33 )
        {
            layer4_type = CTC_PARSER_L4_TYPE_DCCP;
        }

        if (layer4_type)
        {
            ctc_field_key.type = CTC_FIELD_KEY_L4_TYPE;
            ctc_field_key.data = layer4_type;
            ctc_field_key.mask = 0xF;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));

            if(p_udf_match->l4_src_port[1])
            {
                ctc_field_key.type = CTC_FIELD_KEY_L4_SRC_PORT;
                ctc_field_key.data = p_udf_match->l4_src_port[0];
                ctc_field_key.mask = p_udf_match->l4_src_port[1];
                CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
            }

            if(p_udf_match->l4_dst_port[1])
            {
                ctc_field_key.type = CTC_FIELD_KEY_L4_DST_PORT;
                ctc_field_key.data = p_udf_match->l4_dst_port[0];
                ctc_field_key.mask = p_udf_match->l4_dst_port[1];
                CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
            }
        }
        else
        {
            ctc_field_key.type = CTC_FIELD_KEY_IP_PROTOCOL;
            ctc_field_key.data = p_udf_match->ip_protocal[0];
            ctc_field_key.mask = p_udf_match->ip_protocal[1];
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
        }
    }
    if (p_udf_match->gre_protocal_type[1])
    {
        ctc_field_key.type = CTC_FIELD_KEY_L4_TYPE;
        ctc_field_key.data = CTC_PARSER_L4_TYPE_GRE;
        ctc_field_key.mask = 0xF;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));

        ctc_field_key.type = CTC_FIELD_KEY_GRE_PROTOCOL_TYPE;
        ctc_field_key.data = p_udf_match->gre_protocal_type[0];
        ctc_field_key.mask = p_udf_match->gre_protocal_type[1];
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
    }
    if (p_udf_match->mpls_label_num)
    {
        ctc_field_key.type = CTC_FIELD_KEY_LABEL_NUM;
        ctc_field_key.data = p_udf_match->mpls_label_num;
        ctc_field_key.mask = 0xF;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
    }
    if (p_udf_match->ethertype[1] || p_udf_match->ip_protocal[1] || p_udf_match->gre_protocal_type[1] || p_udf_match->mpls_label_num)
    {
        ctc_field_key.type = CTC_FIELD_KEY_UDF_ENTRY_VALID;
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_field_key));
    }

    return status;
}

static sai_status_t
_ctc_sai_udf_remove_udf(sai_object_id_t udf_entry_oid)
{
    uint8 lchip = 0;
    uint8 field_num = 0;
    uint8 field_free = 0;
    int32 ret = 0;
    int32 ii = 0;
    ctc_object_id_t ctc_object_id = {0};
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_acl_classify_udf_t ctc_udf_entry;

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&ctc_udf_entry, 0, sizeof(ctc_acl_classify_udf_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_entry_oid, &lchip));
    p_udf_entry = ctc_sai_db_get_object_property(lchip, udf_entry_oid);
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get sai udf entry!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf_entry->group_oid);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get sai udf group!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_MATCH, p_udf_entry->match_oid, &ctc_object_id);
    sal_memset(&ctc_udf_entry, 0, sizeof(ctc_acl_classify_udf_t));
    ctc_udf_entry.udf_id = ctc_object_id.value;
    ctc_udf_entry.query_type = 0;

    ret = ctcs_acl_get_udf_entry(lchip, &ctc_udf_entry);
    if (ret == CTC_E_NOT_EXIST)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get ctc udf entry!\n");
        return SAI_STATUS_ITEM_NOT_FOUND;
    }


    field_num = p_udf_group->length/CTC_SAI_UDF_OFFSET_BYTE_LEN;
    for (ii = 0; ii < CTC_SAI_UDF_OFFSET_NUM; ii++)
    {
        field_free += (CTC_ACL_UDF_TYPE_NONE == ctc_udf_entry.offset_type_array[ii]);
    }

    if (CTC_SAI_UDF_OFFSET_NUM == (field_num+field_free))
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_remove_udf_entry(lchip, &ctc_udf_entry));
    }
    else
    {
        ctc_udf_entry.offset_type = CTC_ACL_UDF_TYPE_NONE;
        for (ii = field_num-1; ii >= 0; ii--)
        {
            ctc_udf_entry.offset_type_array[p_udf_group->offset[ii]] = CTC_ACL_UDF_TYPE_NONE;
            ctc_udf_entry.offset_num -= ((p_udf_group->offset[ii]==ctc_udf_entry.offset_num)?1:0);
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry(lchip, &ctc_udf_entry));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_remove_udf_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t* p_lookup_match_id = (sai_object_id_t*)p_cb_data;
    ctc_sai_udf_entry_t* p_search_udf_entry = (ctc_sai_udf_entry_t*)(bucket_data->data);

    if (p_search_udf_entry->match_oid == *p_lookup_match_id)
    {
        CTC_SAI_ERROR_RETURN(_ctc_sai_udf_remove_udf(bucket_data->oid));
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_traverse_match_cb(void* bucket_data, void* user_data)
{
    ctc_sai_oid_property_t *p_oid_property = NULL;
    ctc_sai_udf_match_t* p_search_udf_match = NULL;
    ctc_sai_udf_match_t* p_exist_udf_match = NULL;

    p_oid_property = (ctc_sai_oid_property_t*)bucket_data;
    p_exist_udf_match = (ctc_sai_udf_match_t*)user_data;
    p_search_udf_match = (ctc_sai_udf_match_t*)(p_oid_property->data);

    if (((p_exist_udf_match->ethertype[0]&p_exist_udf_match->ethertype[1]) == (p_search_udf_match->ethertype[0]&p_search_udf_match->ethertype[1]))
       && ((p_exist_udf_match->ip_protocal[0]&p_exist_udf_match->ip_protocal[1]) == (p_search_udf_match->ip_protocal[0]&p_search_udf_match->ip_protocal[1]))
       && ((p_exist_udf_match->l4_src_port[0]&p_exist_udf_match->l4_src_port[1]) == (p_search_udf_match->l4_src_port[0]&p_search_udf_match->l4_src_port[1]))
       && ((p_exist_udf_match->l4_dst_port[0]&p_exist_udf_match->l4_dst_port[1]) == (p_search_udf_match->l4_dst_port[0]&p_search_udf_match->l4_dst_port[1]))
       && ((p_exist_udf_match->gre_protocal_type[0]&p_exist_udf_match->gre_protocal_type[1]) == (p_search_udf_match->gre_protocal_type[0]&p_search_udf_match->gre_protocal_type[1]))
       && (p_exist_udf_match->mpls_label_num == p_search_udf_match->mpls_label_num))
    {
        return SAI_STATUS_ITEM_ALREADY_EXISTS;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_entry_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id = {0};
    sai_object_id_t obj_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_UDF_ENTRY, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_match_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id = {0};
    sai_object_id_t obj_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_UDF_MATCH, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_group_wb_sync_cb(uint8 lchip, void* key, void* data)
{
    int32 ret = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint32 offset = 0;
    uint32 max_entry_cnt = 0;
    ctc_wb_data_t wb_data;
    ctc_slistnode_t* node = NULL;
    sai_object_id_t udf_group_id = *(sai_object_id_t*)key;
    ctc_sai_udf_group_t* p_udf_group = (ctc_sai_udf_group_t*)data;
    ctc_sai_udf_group_member_wb_t wb_udf_group_member;
    ctc_sai_udf_group_hash_wb_t wb_udf_group_hash;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;

    sal_memset(&wb_udf_group_member, 0, sizeof(ctc_sai_udf_group_member_wb_t));
    sal_memset(&wb_udf_group_hash, 0, sizeof(ctc_sai_udf_group_hash_wb_t));

    CTC_WB_ALLOC_BUFFER(&wb_data.buffer);
    if (NULL == wb_data.buffer)
    {
        return SAI_STATUS_NO_MEMORY;
    }
    sal_memset(wb_data.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_DATA_T((&wb_data), ctc_sai_udf_group_member_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_UDF_GROUP_MEMBER);
    max_entry_cnt = CTC_WB_DATA_BUFFER_LENGTH / (wb_data.key_len + wb_data.data_len);

    CTC_SLIST_LOOP(p_udf_group->member_list, node)
    {
        offset = wb_data.valid_cnt * (wb_data.key_len + wb_data.data_len);
        p_udf_group_member = (ctc_sai_udf_group_member_t*)node;
        wb_udf_group_member.oid = udf_group_id;
        wb_udf_group_member.udf_id = p_udf_group_member->udf_oid;

        sal_memcpy((uint8*)wb_data.buffer + offset, &wb_udf_group_member, (wb_data.key_len + wb_data.data_len));
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
_ctc_sai_udf_group_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id = {0};
    sai_object_id_t obj_id = *(sai_object_id_t*)key;

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_UDF_GROUP, ctc_object_id.value));

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_group_wb_reload_cb1(uint8 lchip)
{
    uint16 entry_cnt = 0;
    uint32 offset = 0;
    sai_status_t ret = SAI_STATUS_SUCCESS;
    ctc_wb_query_t wb_query;
    ctc_sai_udf_group_member_wb_t wb_udf_group_member;
    ctc_sai_udf_group_hash_wb_t wb_udf_group_hash;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;

    sal_memset(&wb_udf_group_member, 0, sizeof(ctc_sai_udf_group_member_wb_t));
    sal_memset(&wb_udf_group_hash, 0, sizeof(ctc_sai_udf_group_hash_wb_t));
    sal_memset(&wb_query, 0, sizeof(wb_query));

    wb_query.buffer = mem_malloc(MEM_SYSTEM_MODULE,  CTC_WB_DATA_BUFFER_LENGTH);
    if (NULL == wb_query.buffer)
    {
        return CTC_E_NO_MEMORY;
    }
    sal_memset(wb_query.buffer, 0, CTC_WB_DATA_BUFFER_LENGTH);

    CTC_WB_INIT_QUERY_T((&wb_query), ctc_sai_udf_group_member_wb_t, CTC_SAI_WB_TYPE_USER_DEF, CTC_SAI_WB_USER_DEF_SUB_TYPE_UDF_GROUP_MEMBER);
    CTC_WB_QUERY_ENTRY_BEGIN((&wb_query));
        offset = entry_cnt * (wb_query.key_len + wb_query.data_len);
        entry_cnt++;
        sal_memcpy(&wb_udf_group_member, (uint8*)(wb_query.buffer) + offset,  sizeof(ctc_sai_udf_group_member_wb_t));
        p_udf_group = ctc_sai_db_get_object_property(lchip, wb_udf_group_member.oid);
        if (!p_udf_group)
        {
            continue;
        }

        p_udf_group_member = mem_malloc(MEM_SYSTEM_MODULE, sizeof(ctc_sai_udf_group_member_t));
        if (!p_udf_group_member)
        {
            continue;
        }
        p_udf_group_member->udf_oid = wb_udf_group_member.udf_id;
        ctc_slist_add_tail(p_udf_group->member_list, &(p_udf_group_member->head));
    CTC_WB_QUERY_ENTRY_END((&wb_query));

done:
    if (wb_query.buffer)
    {
        mem_free(wb_query.buffer);
    }

    return ret;
}

static  ctc_sai_attr_fn_entry_t udf_group_attr_fn_entries[] = {
    { SAI_UDF_GROUP_ATTR_UDF_LIST,
      _ctc_sai_udf_group_get_attr,
      NULL},
    { SAI_UDF_GROUP_ATTR_TYPE,
      _ctc_sai_udf_group_get_attr,
      NULL},
    { SAI_UDF_GROUP_ATTR_LENGTH,
      _ctc_sai_udf_group_get_attr,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static  ctc_sai_attr_fn_entry_t udf_match_attr_fn_entries[] = {
    { SAI_UDF_MATCH_ATTR_L2_TYPE,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_L3_TYPE,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_GRE_TYPE,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_PRIORITY,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT,
      _ctc_sai_udf_match_get_attr,
      NULL},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

static  ctc_sai_attr_fn_entry_t udf_attr_fn_entries[] = {
    { SAI_UDF_ATTR_MATCH_ID,
      _ctc_sai_udf_get_attr,
      NULL},
    { SAI_UDF_ATTR_GROUP_ID,
      _ctc_sai_udf_get_attr,
      NULL},
    { SAI_UDF_ATTR_BASE,
      _ctc_sai_udf_get_attr,
      NULL},
    { SAI_UDF_ATTR_OFFSET,
      _ctc_sai_udf_get_attr,
      NULL},
    { SAI_UDF_ATTR_HASH_MASK,
      _ctc_sai_udf_get_attr,
      _ctc_sai_udf_entry_set_attr},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

#define ________SAI_DUMP________

static
sai_status_t _ctc_sai_udf_group_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t udf_group_oid = 0;
    sal_file_t p_file = NULL;
    uint32* p_count = NULL;
    uint8 udf_group_type = 0;
    ctc_slistnode_t* p_member_node = NULL;
    ctc_sai_udf_group_t udf_group;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;

    sal_memset(&udf_group_oid, 0, sizeof(ctc_sai_udf_group_t));

    udf_group_oid = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_group_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }
    sal_memcpy(&udf_group, bucket_data->data, sizeof(ctc_sai_udf_group_t));

    ctc_sai_oid_get_sub_type(udf_group_oid, &udf_group_type);
    p_file = (sal_file_t)p_cb_data->value0;
    p_count = (uint32 *)(p_cb_data->value1);

    CTC_SLIST_LOOP(udf_group.member_list, p_member_node)
    {
        p_udf_group_member = (ctc_sai_udf_group_member_t*)p_member_node;
        CTC_SAI_LOG_DUMP(p_file,
                         "%-4d 0x%016"PRIx64 " %-12d %-11d %-12s 0x%016"PRIx64"\n",
                         *p_count, udf_group_oid, udf_group_type,
                         0, "-", p_udf_group_member->udf_oid);
        (*p_count)++;
    }

    return SAI_STATUS_SUCCESS;
}

static
sai_status_t _ctc_sai_udf_match_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t udf_match_oid = 0;
    ctc_sai_udf_match_t udf_match;
    sal_file_t p_file = NULL;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&udf_match, 0, sizeof(ctc_sai_udf_match_t));

    udf_match_oid  = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_match_oid != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }

    sal_memcpy((ctc_sai_udf_match_t*)(&udf_match), bucket_data->data, sizeof(ctc_sai_udf_match_t));
    p_file = (sal_file_t)p_cb_data->value0;

    CTC_SAI_LOG_DUMP(p_file,
                     "%-4d 0x%016"PRIx64 " %-11d %-8d 0x%-4x/0x%-9x 0x%-2x/0x%-10x 0x%-4x/0x%-14x 0x%-4x 0x%-4x 0x%-4x\n",
                     *((uint32 *)(p_cb_data->value1)), udf_match_oid, udf_match.ref_cnt, udf_match.priority,
                     udf_match.ethertype[0], udf_match.ethertype[1], udf_match.ip_protocal[0],
                     udf_match.ip_protocal[1], udf_match.gre_protocal_type[0], udf_match.gre_protocal_type[1],
                     udf_match.l4_dst_port[0], udf_match.l4_src_port[1], udf_match.mpls_label_num);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static
sai_status_t _ctc_sai_udf_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t udf_oid_cur = 0;
    ctc_sai_udf_entry_t udf_entry;
    sal_file_t p_file = NULL;
    uint8 ii = 0;
    uint8 hash_mask_cnt = 0;
    uint8 udf_base = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&udf_entry, 0, sizeof(ctc_sai_udf_entry_t));

    udf_oid_cur = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }

    ctc_sai_oid_get_sub_type(udf_oid_cur, &udf_base);
    sal_memcpy((ctc_sai_udf_entry_t*)(&udf_entry), bucket_data->data, sizeof(ctc_sai_udf_entry_t));

    for (ii = 0; ii < 4; ii++)
    {
        if (0 != udf_entry.hash_mask[ii])
        {
            hash_mask_cnt++;
        }
    }

    p_file = (sal_file_t)p_cb_data->value0;
    CTC_SAI_LOG_DUMP(p_file,
                     "%-4d 0x%016"PRIx64 " 0x%016"PRIx64 " 0x%016"PRIx64 " %-4d %-6d 0x%-2x 0x%-2x 0x%-2x 0x%-2x\n",
                     *((uint32 *)(p_cb_data->value1)), udf_oid_cur, udf_entry.group_oid, udf_entry.match_oid, udf_base, udf_entry.offset,
                     udf_entry.hash_mask[0], udf_entry.hash_mask[1], udf_entry.hash_mask[2], udf_entry.hash_mask[3]);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

#define ________INTERNAL_API________

void ctc_sai_udf_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param)
{
    ctc_sai_db_traverse_param_t    sai_cb_data;
    uint32 num_cnt = 0;
    sal_memset(&sai_cb_data, 0, sizeof(ctc_sai_db_traverse_param_t));
    sai_cb_data.value0 = p_file;
    sai_cb_data.value1 = &num_cnt;
    sai_cb_data.value2 = dump_grep_param;

    CTC_SAI_LOG_DUMP(p_file, "\n# SAI UDF MODULE\n");

    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_UDF_GROUP))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF GROUP");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_udf_group_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-11s %-12s %-18s\n", "No.", "UDF_Group_oid", "UDF_Group_TYPE", "ref_cnt", "hash_udf_bmp", "UDF_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF_GROUP,
                                            (hash_traversal_fn)_ctc_sai_udf_group_dump_print_cb, (void*)(&sai_cb_data));
    }
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_UDF_MATCH))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF MATCH");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_udf_match_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-11s %-8s %-18s %-17s %-23s\n", "No.", "Match_oid", "ref_cnt", "Priority", "ethtype(data/mask)", "ip_pro(data/mask)", "gre_pro_type(data/mask)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF_MATCH,
                                            (hash_traversal_fn)_ctc_sai_udf_match_dump_print_cb, (void*)(&sai_cb_data));
    }
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_UDF))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_udf_entry_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-18s %-4s %-4s %-9s\n", "No.", "UDF_oid", "UDF_Group_oid", "Match_oid", "Base", "Offset", "Hash_mask");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF,
                                           (hash_traversal_fn)_ctc_sai_udf_dump_print_cb, (void*)(&sai_cb_data));
    }
}

#define ________SAI_API________
#define ________SAI_API_UDF_GROUP________

static sai_status_t
ctc_sai_udf_create_group(sai_object_id_t* udf_group_id, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    sai_object_id_t udf_group_obj_id = 0;
    uint8 lchip = 0;
    uint8 type = SAI_UDF_GROUP_TYPE_GENERIC;
    uint16 length = 0;
    uint32 attr_index = 0;
    uint32 ctc_udf_group_id = 0;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    const sai_attribute_value_t *attr_value;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(udf_group_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_GROUP_ATTR_LENGTH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (CTC_SAI_UDF_GROUP_LENGTH(lchip) < attr_value->u16 || attr_value->u16 < CTC_SAI_UDF_OFFSET_BYTE_LEN)
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
        length = attr_value->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_GROUP_ATTR_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        type = attr_value->s32;
    }

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_GROUP, &ctc_udf_group_id);
    if (SAI_STATUS_SUCCESS != status)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Exceed to create udf group max number, udf entry have alredy used out!\n");
        goto error0;
    }

    udf_group_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF_GROUP, lchip, type, 0, ctc_udf_group_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_build_udf_group_db(lchip, udf_group_obj_id, &p_udf_group), status, error1);

    p_udf_group->member_list = ctc_slist_new();
    p_udf_group->length = length;
    p_udf_group->type = type;
    sal_memset(p_udf_group->offset, CTC_SAI_UDF_OFFSET_NUM, sizeof(p_udf_group->offset));
    *udf_group_id = udf_group_obj_id;
    goto error0;

error1:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_GROUP, ctc_udf_group_id);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_group(sai_object_id_t udf_group_id)
{
    uint8 lchip = 0;
    sai_status_t status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    uint32 ctc_udf_group_id = 0;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf group, invalid udf_group_id 0x%"PRIx64"!\n", udf_group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if (!((NULL == p_udf_group->member_list || CTC_LIST_ISEMPTY(p_udf_group->member_list)) && 0 == p_udf_group->ref_cnt))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf group, group member is not empty!\n", udf_group_id);
        goto error0;
    }
    mem_free(p_udf_group->member_list);

    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_remove_udf_group_db(lchip, udf_group_id), status, error0);
    CTC_SAI_ERROR_GOTO(_ctc_sai_oid_get_udf_group_id(udf_group_id, &ctc_udf_group_id), status, error0);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_GROUP, ctc_udf_group_id), status, error0);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_set_group_attribute(sai_object_id_t udf_group_id, const sai_attribute_t *attr)
{
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "set udf group attribute not support\n");

    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_udf_get_group_attribute(sai_object_id_t udf_group_oid, uint32_t attr_count, sai_attribute_t* attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 ii = 0;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_group_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_oid);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf group, invalid udf_group_id 0x%"PRIx64"!\n", udf_group_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    key.key.object_id = udf_group_oid;
    while (ii < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF_GROUP, ii, udf_group_attr_fn_entries, &attr_list[ii]), status, error0);
        ii++;
    }

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_API_UDF_MATCH________

static sai_status_t
ctc_sai_udf_create_match(sai_object_id_t* p_udf_match_oid, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint32 attr_index = 0;
    uint32 ctc_match_id = 0;
    sai_object_id_t udf_match_oid = 0;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_sai_udf_match_t udf_match;
    const sai_attribute_value_t *attr_value;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(p_udf_match_oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    sal_memset(&udf_match, 0, sizeof(ctc_sai_udf_match_t));
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_L2_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.ethertype[0]= attr_value->aclfield.data.u16;
        udf_match.ethertype[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_L3_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.ip_protocal[0]= attr_value->aclfield.data.u8;
        udf_match.ip_protocal[1]= attr_value->aclfield.mask.u8;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_GRE_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.gre_protocal_type[0]= attr_value->aclfield.data.u16;
        udf_match.gre_protocal_type[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.mpls_label_num= attr_value->u8;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.l4_src_port[0]= attr_value->aclfield.data.u16;
        udf_match.l4_src_port[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.l4_dst_port[0]= attr_value->aclfield.data.u16;
        udf_match.l4_dst_port[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_PRIORITY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        udf_match.priority = attr_value->u8;
    }
    CTC_SAI_ERROR_GOTO(ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF_MATCH, _ctc_sai_udf_traverse_match_cb, (void*)(&udf_match)), status, error0);

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_MATCH, &ctc_match_id);
    if (status)
    {
        goto error0;
    }

    udf_match_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF_MATCH, lchip, 0, 0, ctc_match_id);
    status = _ctc_sai_udf_build_udf_match_db(lchip, udf_match_oid, &p_udf_match);
    if (CTC_SAI_ERROR(status))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Fail to build udf match db!\n");
        goto error1;
    }
    sal_memcpy(p_udf_match, &udf_match, sizeof(ctc_sai_udf_match_t));
    *p_udf_match_oid = udf_match_oid;
    goto error0;

error1:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error1\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_MATCH, ctc_match_id);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_match(sai_object_id_t udf_match_oid)
{
    uint8 lchip = 0;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_object_id_t ctc_object_id = {0};
    ctc_acl_classify_udf_t acl_classify_udf;
    sai_status_t status = SAI_STATUS_SUCCESS;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_match_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_oid);
    if (NULL == p_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf match, invalid udf_match_id 0x%"PRIx64"!\n", udf_match_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    /* check udf match is or not used by udf entry*/
    if (0 != p_udf_match->ref_cnt)
    {
        CTC_SAI_LOG_INFO(SAI_API_UDF, "The udf match oid 0x%"PRIx64" to be removed is used by udf entry!\n", udf_match_oid);
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF, (hash_traversal_fn)_ctc_sai_udf_remove_udf_cb, &udf_match_oid);
    }

    sal_memset(&acl_classify_udf, 0, sizeof(ctc_acl_classify_udf_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_MATCH, udf_match_oid, &ctc_object_id);
    acl_classify_udf.udf_id = ctc_object_id.value;

    ctcs_acl_remove_udf_entry(lchip, &acl_classify_udf);
    _ctc_sai_udf_remove_udf_match_db(lchip, udf_match_oid);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_MATCH, ctc_object_id.value);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_set_match_attribute(sai_object_id_t udf_match_id, const sai_attribute_t *attr)
{
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "set udf match attribute not support\n");
    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_udf_get_match_attribute(sai_object_id_t udf_match_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 ii = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_match_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    key.key.object_id = udf_match_id;
    while (ii < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF_MATCH, ii, udf_match_attr_fn_entries, &attr_list[ii]), status, error0);
        ii++;
    }

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_API_UDF________

static sai_status_t
ctc_sai_udf_create_udf(sai_object_id_t* p_udf_oid, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 offset_num = 0;
    uint8 free_index = 0;
    uint8 group_exist_udf = 0;
    uint8 alloc_udf_group_id = 0;
    uint8 free_offset[CTC_SAI_UDF_OFFSET_NUM] = {0};
    uint16 udf_offset = 0;
    uint16 udf_base = 0;
    uint32 ii = 0;
    uint32 jj = 0;
    uint32 index = 0;
    uint32 ctc_sai_udf_id = 0;
    uint32 ctc_udf_group_id = 0;
    ctc_object_id_t ctc_object_id = {0};
    sai_object_id_t udf_entry_oid = 0;
    sai_object_id_t udf_match_oid = 0;
    sai_object_id_t udf_group_oid = 0;
    ctc_slistnode_t* p_member_node = NULL;
    ctc_acl_classify_udf_t ctc_udf_entry;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_match_t* p_lookup_udf_match = NULL;
    ctc_sai_udf_match_t* p_search_udf_match = NULL;
    ctc_sai_udf_group_member_t* p_udf_group_member = NULL;
    uint8 hash_mask[CTC_SAI_UDF_HASH_MASK_LENGTH] = {0};
    const sai_attribute_value_t* attr_value;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(p_udf_oid);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_MATCH_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        udf_match_oid = attr_value->oid;
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Must specify udf match id\n");
        goto error0;
    }

    p_lookup_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_oid);
    if (NULL == p_lookup_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF match id is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_GROUP_ID, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        udf_group_oid = attr_value->oid;
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Must specify udf group id\n");
        goto error0;
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_oid);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF group id is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    sal_memset(&ctc_udf_entry, 0, sizeof(ctc_acl_classify_udf_t));
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_MATCH, udf_match_oid, &ctc_object_id);
    ctc_udf_entry.udf_id = ctc_object_id.value;
    ctc_udf_entry.query_type = 0;

    offset_num = p_udf_group->length/CTC_SAI_UDF_OFFSET_BYTE_LEN;
    ctcs_acl_get_udf_entry(lchip, &ctc_udf_entry);
    group_exist_udf = (CTC_SAI_UDF_OFFSET_NUM != p_udf_group->offset[0])?1:0;

    for (ii = 0; ii < CTC_SAI_UDF_OFFSET_NUM; ii++)
    {
        if (!group_exist_udf)
        {
            if (CTC_ACL_UDF_TYPE_NONE == ctc_udf_entry.offset_type_array[ii])
            {
                free_offset[free_index++] = ii;
            }
        }
        else
        {
            if (CTC_ACL_UDF_TYPE_NONE == ctc_udf_entry.offset_type_array[ii])
            {
                for (jj = 0; jj < offset_num; jj++)
                {
                    if (p_udf_group->offset[jj] == ii)
                    {
                        free_offset[free_index++] = ii;
                    }
                }
            }
        }
        if (free_index == offset_num)
        {
            break;
        }
    }
    if (CTC_SAI_UDF_OFFSET_NUM == ii)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF field in entry is exhausted!\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_OFFSET, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        udf_offset = attr_value->u16;
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Must provide udf offset.\n");
        goto error0;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_BASE, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        udf_base = attr_value->s32;
    }
    else
    {
        udf_base = SAI_UDF_BASE_L2;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_HASH_MASK, &attr_value, &index);
    if (!CTC_SAI_ERROR(status))
    {
        if (SAI_UDF_GROUP_TYPE_HASH == p_udf_group->type)
        {
            if (p_udf_group->length != attr_value->u8list.count)
            {
                status = SAI_STATUS_INVALID_PARAMETER;
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "udf hash mask byte %u is mismatch with its group's length %u.\n", attr_value->s8list.count, p_udf_group->length);
                goto error0;
            }

            for (ii = 0; ii < p_udf_group->length; ii++)
            {
                if (0xFF != attr_value->u8list.list[ii])
                {
                    status = SAI_STATUS_INVALID_PARAMETER;
                    CTC_SAI_LOG_ERROR(SAI_API_UDF, "udf hash mask must be all masked.\n");
                    goto error0;
                }
            }
        }
        sal_memcpy(hash_mask, attr_value->u8list.list, attr_value->u8list.count);
    }
    else
    {
        if (SAI_UDF_GROUP_TYPE_HASH == p_udf_group->type)
        {
            sal_memset(hash_mask, 0xFF, p_udf_group->length);
        }
    }

    CTC_SLIST_LOOP(p_udf_group->member_list, p_member_node)
    {
        p_udf_group_member = (ctc_sai_udf_group_member_t*)p_member_node;
        if (NULL != p_udf_group_member)
        {
            break;
        }
    }

    if (p_lookup_udf_match->ref_cnt > 0)
    {
        /* the udf match allocate ctc_group_id alreay */
        ctc_udf_group_id = p_lookup_udf_match->ctc_group_id;
    }
    else
    {
        /* new udf match, not attach to group yet, the group which require the match maybe attached other match entry already.*/
        if (NULL == p_udf_group_member)
        {
            alloc_udf_group_id = 1;
            CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_UDF_MAPPED_ID, &ctc_udf_group_id), status, error0);
        }
        else
        {
            p_udf_entry = ctc_sai_db_get_object_property(lchip, p_udf_group_member->udf_oid);
            if (NULL == p_udf_entry)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF entry id is not exist\n");
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error0;
            }

            p_search_udf_match = ctc_sai_db_get_object_property(lchip, p_udf_entry->match_oid);
            if (NULL == p_search_udf_match)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF match id is not exist\n");
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error0;
            }

            if (0 != p_search_udf_match->ref_cnt && 0 != p_lookup_udf_match->ref_cnt && p_search_udf_match->ctc_group_id != p_lookup_udf_match->ctc_group_id)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF match ctc group id is different!\n");
                status = SAI_STATUS_INVALID_PARAMETER;
                goto error0;
            }
            ctc_udf_group_id = p_search_udf_match->ctc_group_id;
        }
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_ENTRY, &ctc_sai_udf_id), status, error1);
    udf_entry_oid = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF, lchip, 0, 0, ctc_sai_udf_id);

    p_udf_entry = NULL;
    MALLOC_ZERO(MEM_ACL_MODULE, p_udf_entry, sizeof(ctc_sai_udf_entry_t));
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Fail to allocate udf entry memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error2;
    }

    p_udf_entry->match_oid = udf_match_oid;
    p_udf_entry->group_oid = udf_group_oid;
    p_udf_entry->base =  udf_base;
    p_udf_entry->offset = udf_offset;
    sal_memcpy(p_udf_entry->hash_mask, hash_mask, sizeof(hash_mask));

    MALLOC_ZERO(MEM_ACL_MODULE, p_udf_group_member, sizeof(ctc_sai_udf_group_member_t));
    if (NULL == p_udf_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Fail to allocate udf group member memory\n");
        status = SAI_STATUS_NO_MEMORY;
        goto error3;
    }
    p_udf_group_member->udf_oid = udf_entry_oid;

    CTC_SAI_ERROR_GOTO(ctc_sai_db_add_object_property(lchip, udf_entry_oid, (void*)p_udf_entry), status, error4);
    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_add_udf(udf_entry_oid, udf_match_oid, udf_group_oid, ctc_udf_group_id, free_offset), status, error5);

    ctc_slist_add_tail(p_udf_group->member_list, &(p_udf_group_member->head));
    p_lookup_udf_match->ref_cnt++;
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "udf_entry_id = 0x%"PRIx64"\n", udf_entry_oid);

    sal_memcpy(p_udf_group->offset, free_offset, sizeof(free_offset));
    *p_udf_oid = udf_entry_oid;
    goto error0;

error5:
    ctc_sai_db_remove_object_property(lchip, udf_entry_oid);
error4:
    mem_free(p_udf_group_member);
error3:
    mem_free(p_udf_entry);
error2:
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_ENTRY, ctc_sai_udf_id);
error1:
    if (alloc_udf_group_id)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_UDF_MAPPED_ID, ctc_udf_group_id);
    }
error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_udf(sai_object_id_t udf_oid)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 ctc_mapped_id_refer_cnt = 0;
    ctc_object_id_t ctc_object_id = {0};
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_match_t* p_lookup_udf_match = NULL;
    ctc_sai_udf_match_t* p_search_udf_match = NULL;
    ctc_slistnode_t* p_member_node = NULL;
    ctc_sai_udf_group_member_t* p_lookup_udf_group_member = NULL;
    ctc_sai_udf_group_member_t* p_search_udf_group_member = NULL;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf_entry = ctc_sai_db_get_object_property(lchip, udf_oid);
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf entry, invalid udf_id 0x%"PRIx64"!\n", udf_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf_entry->group_oid);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf_entry_id 0x%"PRIx64", invalid udf_group_id 0x%"PRIx64" !\n", udf_oid, p_udf_entry->group_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    p_search_udf_match = ctc_sai_db_get_object_property(lchip, p_udf_entry->match_oid);
    if (NULL == p_search_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf entry, invalid match_id 0x%"PRIx64"!\n", p_udf_entry->match_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    if (0 != p_udf_group->ref_cnt)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf entry 0x%"PRIx64", Its group has been refered by hash!\n", p_udf_entry->group_oid);
        goto error0;
    }

    CTC_SLIST_LOOP(p_udf_group->member_list, p_member_node)
    {
        p_lookup_udf_group_member = (ctc_sai_udf_group_member_t*)p_member_node;
        p_udf_entry = ctc_sai_db_get_object_property(lchip, p_lookup_udf_group_member->udf_oid);

        if (NULL == p_udf_entry)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF entry id is not exist\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error0;
        }

        p_lookup_udf_match = ctc_sai_db_get_object_property(lchip, p_udf_entry->match_oid);
        if (NULL == p_lookup_udf_match)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF match id is not exist\n");
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error0;
        }

        ctc_mapped_id_refer_cnt += p_lookup_udf_match->ref_cnt;

        if (p_lookup_udf_group_member->udf_oid == udf_oid)
        {
            p_search_udf_group_member = (ctc_sai_udf_group_member_t*)p_member_node;
        }
    }

    if (NULL == p_search_udf_group_member)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF group id 0x%"PRIx64" is not exist udf entry id 0x%"PRIx64"\n", p_udf_entry->group_oid, udf_oid);
        goto error0;
    }

    if (1 == ctc_mapped_id_refer_cnt)
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_SDK_UDF_MAPPED_ID, p_search_udf_match->ctc_group_id);
    }

    p_search_udf_match->ref_cnt--;
    ctc_slist_delete_node(p_udf_group->member_list, (ctc_slistnode_t*)p_search_udf_group_member);
    mem_free(p_member_node);
    _ctc_sai_udf_remove_udf(udf_oid);
    _ctc_sai_udf_remove_udf_db(lchip, udf_oid);

    if (CTC_LIST_ISEMPTY(p_udf_group->member_list))
    {
        sal_memset(p_udf_group->offset, CTC_SAI_UDF_OFFSET_NUM, sizeof(p_udf_group->offset));
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF, udf_oid, &ctc_object_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_UDF_ENTRY, ctc_object_id.value);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_set_udf_attribute(sai_object_id_t udf_oid, const sai_attribute_t *attr)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    sai_object_key_t key;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf_entry = ctc_sai_db_get_object_property(lchip, udf_oid); /* exsits or not */
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf, invalid udf_id 0x%"PRIx64"!\n", udf_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf_entry->group_oid);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "UDF group id is not exist\n");
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    key.key.object_id = udf_oid;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF, udf_attr_fn_entries, attr), status, error0);

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_get_udf_attribute(sai_object_id_t udf_oid, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    ctc_sai_udf_entry_t* p_udf_entry = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_oid, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf_entry = ctc_sai_db_get_object_property(lchip, udf_oid);
    if (NULL == p_udf_entry)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf, invalid udf_id 0x%"PRIx64"!\n", udf_oid);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto error0;
    }

    key.key.object_id = udf_oid;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF, loop, udf_attr_fn_entries, &attr_list[loop]), status, error0);
        loop++ ;
    }

error0:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

const sai_udf_api_t ctc_sai_udf_api =
{
    ctc_sai_udf_create_udf,
    ctc_sai_udf_remove_udf,
    ctc_sai_udf_set_udf_attribute,
    ctc_sai_udf_get_udf_attribute,
    ctc_sai_udf_create_match,
    ctc_sai_udf_remove_match,
    ctc_sai_udf_set_match_attribute,
    ctc_sai_udf_get_match_attribute,
    ctc_sai_udf_create_group,
    ctc_sai_udf_remove_group,
    ctc_sai_udf_set_group_attribute,
    ctc_sai_udf_get_group_attribute,
};

sai_status_t
ctc_sai_udf_api_init()
{
    ctc_sai_register_module_api(SAI_API_UDF, (void*)&ctc_sai_udf_api);
    return SAI_STATUS_SUCCESS;
}

sai_status_t
ctc_sai_udf_db_init(uint8 lchip)
{
    ctc_sai_db_wb_t wb_info;

    sal_memset(&wb_info, 0, sizeof(ctc_sai_db_wb_t));
    wb_info.version = SYS_WB_VERSION_UDF;
    wb_info.data_len = sizeof(ctc_sai_udf_entry_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_udf_entry_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_UDF;
    wb_info.data_len = sizeof(ctc_sai_udf_match_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_udf_match_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF_MATCH, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_UDF;
    wb_info.data_len = sizeof(ctc_sai_udf_group_t);
    wb_info.wb_sync_cb = _ctc_sai_udf_group_wb_sync_cb;
    wb_info.wb_reload_cb = _ctc_sai_udf_group_wb_reload_cb;
    wb_info.wb_reload_cb1 = _ctc_sai_udf_group_wb_reload_cb1;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF_GROUP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}

