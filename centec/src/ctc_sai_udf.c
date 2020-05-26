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


/* centec duet2 udf byte length is 4 bytes,goldengate udf byte length is 1 bytes */
#define CTC_SAI_UDF_GROUP_LENGTH(lchip) (((CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip)) || (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))?4:1)

/* centec duet2 have 16 udf entry,goldengate have 4udf entry */
#define CTC_SAI_UDF_GROUP_MAX_NUM(lchip) (((CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip)) || (CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)))?16:4)

#define CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP  4
#define CTC_SAI_UDF_HASH_MASK_BYTE_CNT    4   /* The count in the list must be equal to the UDF byte length. */

enum ctc_sai_udf_op_type_e
{
    CTC_SAI_UDF_OP_REMOVE,     /**< hash application for ecmp */
    CTC_SAI_UDF_OP_SET,        /**< hash application for linkagg */
    CTC_SAI_UDF_OP_NUM,        /**< hash application num */
};
typedef enum ctc_sai_udf_op_type_e ctc_sai_udf_op_type_t;

typedef struct ctc_sai_udf_match_s
{
    uint8  udf_ref_cnt;           /* indicate used by acl cnt */
    uint16 ethertype[2];          /* data: ethertype[0];          mask: ethertype[1]. */
	uint8  ip_protocal[2];        /* data: ip_protocal[0];        mask: ip_protocal[1]. */
	uint16 gre_protocal_type[2];  /* data: gre_protocal_type[0];  mask: gre_protocal_type[1]. */
	uint8  priority;              /* corresponding to cam 0-15 */
}ctc_sai_udf_match_t;

typedef struct ctc_sai_udf_s
{
    uint64   group_id;      /* udf binding to group */
    uint64   match_id;      /* udf binding to match */
    uint8    offset;        /* udf ad: offset */
    uint8    hash_mask[4];  /* udf ad: 4 hash_mask */
}ctc_sai_udf_t;


uint16 _ctc_sai_udf_bubble_sort(uint8 a[][4], int n)
{
    uint16 tmp;
    int i = 0;
    int j = 0;
    for ( i = 0; i < n - 1; i++)
    {
        for ( j = 0; j < n - i - 1; j++)
        {
            if (a[0][j] > a[0][j + 1])
            {
                tmp = a[0][j];
                a[0][j] = a[0][j + 1];
                a[0][j + 1] = tmp;

                tmp = a[1][j];
                a[1][j] = a[1][j + 1];
                a[1][j + 1] = tmp;
            }
        }
    }
    tmp = 0;
    for (i = 0; i < n; i++)
    {
       tmp |= (a[1][i]& 0xF) << (i*4);
    }
    return tmp;
}

static sai_status_t
_ctc_sai_udf_judged_used(uint8 lchip, uint8 operate_type, sai_object_id_t udf_group_id, ctc_sai_udf_t* p_udf)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t*   p_udf_group = NULL;
    ctc_sai_ld_hash_t*        p_hash = NULL;
    uint8 loop_i = 0;
    sai_object_id_t udf_group_id_judge = 0;
    char* print_str1 = NULL;
    char* print_str2 = NULL;

    udf_group_id_judge = p_udf == NULL ? udf_group_id:p_udf->group_id;
    print_str1 = p_udf == NULL ? "udf gruop" :"udf";
    print_str2 = operate_type == CTC_SAI_UDF_OP_REMOVE ? "remove" :"set";

    /* check udf group is or not used by hash */
    p_hash = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, CTC_SAI_HASH_USAGE_ECMP,0,0));
    if (NULL != p_hash)
    {
        for (loop_i = 0; loop_i < p_hash->udf_group_list.count; loop_i++) /* ecmp hash using udf group  */
        {
            if (p_hash->udf_group_list.list[loop_i] == udf_group_id_judge)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to %s %s, udf_group_id 0x%"PRIx64" is used by ecmp hash!\n", print_str2, print_str1, udf_group_id_judge);
                status = SAI_STATUS_OBJECT_IN_USE;
                goto out;
            }
        }
    }

    p_hash = ctc_sai_db_get_object_property(lchip, ctc_sai_create_object_id(SAI_OBJECT_TYPE_HASH, lchip, CTC_SAI_HASH_USAGE_LINKAGG,0,0));
    if (NULL != p_hash)
    {
        for (loop_i = 0; loop_i < p_hash->udf_group_list.count; loop_i++) /* linkagg hash using udf group */
        {
            if (p_hash->udf_group_list.list[loop_i] == udf_group_id_judge)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to %s %s, udf_group_id 0x%"PRIx64" is used by linkagg hash!\n", print_str2, print_str1,udf_group_id_judge);
                status = SAI_STATUS_OBJECT_IN_USE;
                goto out;
            }
        }
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_id_judge);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to %s %s, invalid group_id 0x%"PRIx64"!\n", print_str2, print_str1, udf_group_id_judge);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    if((p_udf_group->acl_ref_cnt !=0))  /* check udf group is or not used by acl */
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to %s %s, udf_group_id 0x%"PRIx64" is used by acl!\n", print_str2, print_str1, udf_group_id_judge);
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

out:
    return status;

}

static sai_status_t
_ctc_sai_udf_build_udf_group_db(uint8 lchip, sai_object_id_t udf_group_obj_id, ctc_sai_udf_group_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t*   p_udf_group = NULL;

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
   ctc_sai_udf_group_t*   p_udf_group = NULL;

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
_ctc_sai_udf_build_udf_match_db(uint8 lchip, sai_object_id_t udf_match_obj_id, ctc_sai_udf_match_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_match_t*   p_udf_match = NULL;

    p_udf_match = mem_malloc(MEM_ACL_MODULE, sizeof(ctc_sai_udf_match_t));
    if (NULL == p_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_udf_match, 0, sizeof(ctc_sai_udf_match_t));
    status = ctc_sai_db_add_object_property(lchip, udf_match_obj_id, (void*)p_udf_match);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_udf_match);
    }
    *oid_property = p_udf_match;

    return status;
}

static sai_status_t
_ctc_sai_udf_remove_udf_match_db(uint8 lchip, sai_object_id_t udf_match_obj_id)
{
    ctc_sai_udf_match_t*   p_udf_match = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_obj_id);
    if (NULL == p_udf_match)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    ctc_sai_db_remove_object_property(lchip, udf_match_obj_id);
    mem_free(p_udf_match);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_build_udf_db(uint8 lchip, sai_object_id_t udf_obj_id, ctc_sai_udf_t** oid_property)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_t*   p_udf = NULL;

    p_udf = mem_malloc(MEM_ACL_MODULE, sizeof(ctc_sai_udf_t));
    if (NULL == p_udf)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "no memory\n");
        return SAI_STATUS_NO_MEMORY;
    }

    sal_memset(p_udf, 0, sizeof(ctc_sai_udf_t));
    status = ctc_sai_db_add_object_property(lchip, udf_obj_id, (void*)p_udf);
    if (CTC_SAI_ERROR(status))
    {
        mem_free(p_udf);
    }
    *oid_property = p_udf;

    return status;
}

static sai_status_t
_ctc_sai_udf_remove_udf_db(uint8 lchip, sai_object_id_t udf_obj_id)
{
    ctc_sai_udf_t*   p_udf = NULL;

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
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_UDF_GROUP)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Invalid udf group object type 0x%"PRIx64" \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    *udf_group_id = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_oid_get_udf_match_id(sai_object_id_t oid, uint32* udf_match_id)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_MATCH, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_UDF_MATCH)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Invalid udf match object type 0x%"PRIx64" \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    *udf_match_id = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}

sai_status_t
_ctc_sai_oid_get_udf_id(sai_object_id_t oid, uint32* udf_id)
{
    ctc_object_id_t ctc_oid;

    CTC_SAI_ERROR_RETURN(ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF, oid, &ctc_oid));
    if (ctc_oid.type != SAI_OBJECT_TYPE_UDF)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Invalid udf object type 0x%"PRIx64" \n", oid);
        return SAI_STATUS_INVALID_OBJECT_ID;
    }

    *udf_id = ctc_oid.value;

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_group_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    uint8 udf_cnt= 0;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    uint8 loop_i = 0;
    uint8 group_type = 0;

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
                for(loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++)
                {
                    if(p_udf_group->udf_id[loop_i])
                    {
                        attr->value.objlist.list[udf_cnt++] = p_udf_group->udf_id[loop_i];
                    }
                }
                attr->value.objlist.count = udf_cnt;
            }
            break;
        case SAI_UDF_GROUP_ATTR_TYPE:
            CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_sub_type(key->key.object_id, &group_type));
            attr->value.s32 = group_type;
            break;
        case SAI_UDF_GROUP_ATTR_LENGTH:
            attr->value.u16 = CTC_SAI_UDF_GROUP_LENGTH(lchip);
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
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_get_attr(sai_object_key_t* key, sai_attribute_t* attr, uint32 attr_idx)
{
    uint8 lchip = 0;
    ctc_sai_udf_t*         p_udf = NULL;
    uint8 udf_base =0;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_udf)
    {
        return SAI_STATUS_ITEM_NOT_FOUND;
    }
    switch (attr->id)
    {
        case SAI_UDF_ATTR_MATCH_ID:   /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.oid = p_udf->match_id;
            break;
        case SAI_UDF_ATTR_GROUP_ID:   /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.oid = p_udf->group_id;
            break;
        case SAI_UDF_ATTR_BASE:       /* @flags CREATE_AND_SET */
            CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_sub_type(key->key.object_id, &udf_base));
            attr->value.s32= udf_base; /* @default SAI_UDF_BASE_L2 */
            break;
        case SAI_UDF_ATTR_OFFSET:     /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
            attr->value.u16 = p_udf->offset;
            break;
        case SAI_UDF_ATTR_HASH_MASK:  /* @flags CREATE_AND_SET */
            attr->value.u8list.count = CTC_SAI_UDF_HASH_MASK_BYTE_CNT;  /* Default to 2 bytes, value 0xFF, 0xFF */
            sal_memcpy(attr->value.u8list.list, p_udf->hash_mask, sizeof(p_udf->hash_mask));
            break;
        default:
            return SAI_STATUS_ATTR_NOT_SUPPORTED_0 + attr_idx;
    }
    return SAI_STATUS_SUCCESS;
}

sai_status_t   /* called when create udf or set udf : SAI_UDF_ATTR_HASH_MASK */
_ctc_sai_udf_set_hash_mask(uint8 lchip, uint8 is_default, const sai_attribute_value_t *attr_value, ctc_sai_udf_t* p_udf )
{
    uint8 loop_i = 0;
    uint8 loop_j = 0;
    uint8 hash_bmp = 0;   /* 4bit */
    uint8 offset_mask[2][4] = {{0}};
    ctc_sai_udf_group_t* p_udf_group = NULL;
    uint8 udf_cnt_in_group = 0;

    if (!is_default)
    {
        if (attr_value->u8list.count != CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP) /* The count in the list must be equal to the UDF byte length */
        {
            return SAI_STATUS_INVALID_PARAMETER;
        }

        for (loop_i = 0; loop_i < CTC_SAI_UDF_HASH_MASK_BYTE_CNT; loop_i++)
        {
            if ((0xFF != attr_value->u8list.list[loop_i]) && (0 != attr_value->u8list.list[loop_i]))
            {
                return SAI_STATUS_INVALID_PARAMETER;
            }
        }
        sal_memcpy(p_udf->hash_mask, attr_value->u8list.list, attr_value->u8list.count);
    }

    p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf->group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf hash mask, invalid udf_group_id;udf_group_id = 0x%"PRIx64"!\n", p_udf->group_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    for (loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++) /* get udf in group */
    {
        if (0 == p_udf_group->udf_id[loop_i])
        {
            continue;
        }

        hash_bmp = 0;
        p_udf = ctc_sai_db_get_object_property(lchip, p_udf_group->udf_id[loop_i]);
        if (NULL == p_udf)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") not in the group !\n", p_udf_group->udf_id[loop_i]);
            return SAI_STATUS_INVALID_PARAMETER;
        }
        for (loop_j = 0; loop_j < CTC_SAI_UDF_HASH_MASK_BYTE_CNT; loop_j++)
        {
            if (0xFF == p_udf->hash_mask[loop_j])
            {
                CTC_BIT_SET(hash_bmp, loop_j);
            }
        }
        offset_mask[0][udf_cnt_in_group] = p_udf->offset;
        offset_mask[1][udf_cnt_in_group] = hash_bmp;
        udf_cnt_in_group++;
    }

    p_udf_group->hash_udf_bmp = _ctc_sai_udf_bubble_sort(offset_mask, udf_cnt_in_group);
    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_set_attr(sai_object_key_t* key, const sai_attribute_t* attr)
{
    uint8 lchip = 0;
    ctc_sai_udf_t*       p_udf = NULL;

    ctc_sai_oid_get_lchip(key->key.object_id, &lchip);
    p_udf = ctc_sai_db_get_object_property(lchip, key->key.object_id);
    if (NULL == p_udf)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf, invalid udf_id 0x%"PRIx64"!\n", key->key.object_id);
        return SAI_STATUS_ITEM_NOT_FOUND;
    }

    switch(attr->id)
    {
        case SAI_UDF_ATTR_BASE:
            /* complex=> need to save SAI_UDF_ATTR_BASE to udf db,not in sub_type */
            return SAI_STATUS_NOT_SUPPORTED;
        case SAI_UDF_ATTR_HASH_MASK:
            CTC_SAI_ERROR_RETURN(_ctc_sai_udf_set_hash_mask(lchip, 0, &(attr->value), p_udf));
            break;
        default:
            return SAI_STATUS_NOT_SUPPORTED;
    }

    return SAI_STATUS_SUCCESS;
}

static sai_status_t
_ctc_sai_udf_update_ctc_udf_entry(uint8 lchip, ctc_sai_udf_group_t* p_udf_group, sai_object_id_t udf_group_id)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    ctc_sai_udf_t* p_udf = NULL;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_acl_classify_udf_t udf_entry;
    ctc_object_id_t ctc_object_id;
    ctc_field_key_t ctc_sdk_key_field;

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&udf_entry, 0, sizeof(ctc_acl_classify_udf_t));
    sal_memset(&ctc_sdk_key_field, 0, sizeof(ctc_field_key_t));

    /* remove + add ==>> update */
    if (p_udf_group->add_valid)
    {
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, udf_group_id, &ctc_object_id);
        udf_entry.udf_id = ctc_object_id.value;

        ctc_sdk_key_field.type = CTC_FIELD_KEY_L4_TYPE; /* clear udf entry db which is for checking key union */
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_remove_udf_entry_key_field(lchip, udf_entry.udf_id, &ctc_sdk_key_field));

        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_remove_udf_entry(lchip, &udf_entry));
        p_udf_group->add_valid = 0;
    }

    for (loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++) /* get udf in group */
    {
        if (0 == p_udf_group->udf_id[loop_i])
        {
            continue;
        }
        p_udf = ctc_sai_db_get_object_property(lchip, p_udf_group->udf_id[loop_i]);
        if (NULL == p_udf)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") not in the group !\n", p_udf_group->udf_id[loop_i]);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        p_udf_match = ctc_sai_db_get_object_property(lchip, p_udf->match_id);
        udf_entry.priority = p_udf_match->priority;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, p_udf->group_id, &ctc_object_id);
        udf_entry.udf_id = ctc_object_id.value;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF, p_udf_group->udf_id[loop_i], &ctc_object_id);
        udf_entry.offset_type = ctc_object_id.sub_type+1;
        udf_entry.offset[udf_entry.offset_num++] = p_udf->offset;
    }

    if (udf_entry.offset_num)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry(lchip, &udf_entry));
        p_udf_group->add_valid = 1;

        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, udf_group_id, &ctc_object_id);
        sal_memset(&ctc_sdk_key_field, 0, sizeof(ctc_field_key_t));
        if (p_udf_match->ethertype[1])
        {
            ctc_sdk_key_field.type = CTC_FIELD_KEY_ETHER_TYPE;
            ctc_sdk_key_field.data = p_udf_match->ethertype[0];
            ctc_sdk_key_field.mask = p_udf_match->ethertype[1];
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_sdk_key_field));
        }
        if (p_udf_match->ip_protocal[1])
        {
            ctc_sdk_key_field.type = CTC_FIELD_KEY_IP_PROTOCOL;
            ctc_sdk_key_field.data = p_udf_match->ip_protocal[0];
            ctc_sdk_key_field.mask = p_udf_match->ip_protocal[1];
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_sdk_key_field));
        }
        if (p_udf_match->gre_protocal_type[1])
        {
            ctc_sdk_key_field.type = CTC_FIELD_KEY_L4_TYPE;
            ctc_sdk_key_field.data = CTC_PARSER_L4_TYPE_GRE;
            ctc_sdk_key_field.mask = 0xF;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_sdk_key_field));

            ctc_sdk_key_field.type = CTC_FIELD_KEY_GRE_PROTOCOL_TYPE;
            ctc_sdk_key_field.data = p_udf_match->gre_protocal_type[0];
            ctc_sdk_key_field.mask = p_udf_match->gre_protocal_type[1];
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_sdk_key_field));
        }
        if (p_udf_match->ethertype[1] || p_udf_match->ip_protocal[1] || p_udf_match->gre_protocal_type[1])
        {
            ctc_sdk_key_field.type = CTC_FIELD_KEY_UDF_ENTRY_VALID;
            CTC_SAI_CTC_ERROR_RETURN(ctcs_acl_add_udf_entry_key_field(lchip, ctc_object_id.value, &ctc_sdk_key_field));
        }
    }

    return status;
}

static sai_status_t
_ctc_sai_udf_update_goldengate_ctc_udf_entry(uint8 lchip, ctc_sai_udf_group_t* p_udf_group)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 loop_i = 0;
    ctc_sai_udf_t* p_udf = NULL;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_parser_udf_t udf_entry;
    uint32 index = 0;
    ctc_object_id_t ctc_object_id;

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&udf_entry, 0, sizeof(ctc_parser_udf_t));

    /* remove + add ==>> update */
    if (p_udf_group->add_valid)
    {   /* remove udf entry */
        for (loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++) /* get udf in group */
        {
            if (0 == p_udf_group->udf_id[loop_i])
            {
                continue;
            }
            p_udf = ctc_sai_db_get_object_property(lchip, p_udf_group->udf_id[loop_i]);
            if (NULL == p_udf)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") not in the group !\n", p_udf_group->udf_id[loop_i]);
                return SAI_STATUS_ITEM_NOT_FOUND;
            }
            p_udf_match = ctc_sai_db_get_object_property(lchip, p_udf->match_id);
            index = p_udf_match->priority;
            break;
        }
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_udf(lchip, index, &udf_entry));
        p_udf_group->add_valid = 0;
    }

    for (loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++) /* get udf in group */
    {
        if (0 == p_udf_group->udf_id[loop_i])
        {
            continue;
        }
        p_udf = ctc_sai_db_get_object_property(lchip, p_udf_group->udf_id[loop_i]);
        if (NULL == p_udf)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") not in the group !\n", p_udf_group->udf_id[loop_i]);
            return SAI_STATUS_ITEM_NOT_FOUND;
        }
        p_udf_match = ctc_sai_db_get_object_property(lchip, p_udf->match_id);
        index = p_udf_match->priority;
        ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF, p_udf_group->udf_id[loop_i], &ctc_object_id);
        udf_entry.type = ctc_object_id.sub_type-1;
        udf_entry.udf_offset[udf_entry.udf_num++] = p_udf->offset;

        udf_entry.ether_type = p_udf_match->ethertype[0];
        udf_entry.ip_version = (uint8)((p_udf_match->ethertype[0] == 0x0800) ? CTC_IP_VER_4 : CTC_IP_VER_6);
        udf_entry.l3_header_protocol = p_udf_match->ip_protocal[0];
    }

    if (udf_entry.udf_num)
    {
        CTC_SAI_CTC_ERROR_RETURN(ctcs_parser_set_udf(lchip, index, &udf_entry));
        p_udf_group->add_valid = 1;
    }
    return status;
}

static sai_status_t
_ctc_sai_udf_wb_reload_cb(uint8 lchip, void* key, void* data)
{
    ctc_object_id_t ctc_object_id;
    sai_object_id_t obj_id = *(sai_object_id_t*)key;
    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_NULL, obj_id, &ctc_object_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_db_alloc_id_from_position(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_object_id.value));
    return SAI_STATUS_SUCCESS;
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
      _ctc_sai_udf_set_attr},
    { SAI_UDF_ATTR_OFFSET,
      _ctc_sai_udf_get_attr,
      NULL},
    { SAI_UDF_ATTR_HASH_MASK,
      _ctc_sai_udf_get_attr,
      _ctc_sai_udf_set_attr},
    { CTC_SAI_FUNC_ATTR_END_ID,
      NULL,
      NULL }
};

#define ________SAI_DUMP________

static
sai_status_t _ctc_sai_udf_grp_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  udf_grp_oid_cur = 0;
    ctc_sai_udf_group_t    udf_grp_cur;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint8 udf_grp_type = 0;
    uint8 ii = 0;
    uint8 jj = 0;
    uint8 udf_cnt = 0;
    sai_object_id_t     udf_id_tmp[4] = {0};
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&udf_grp_cur, 0, sizeof(ctc_sai_udf_group_t));

    udf_grp_oid_cur = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_grp_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }

    ctc_sai_oid_get_sub_type(udf_grp_oid_cur, &udf_grp_type);
    sal_memcpy((ctc_sai_udf_group_t*)(&udf_grp_cur), bucket_data->data, sizeof(ctc_sai_udf_group_t));
    for(ii= 0; ii<4; ii++)
    {
        if (0 != udf_grp_cur.udf_id[ii])
        {
            udf_cnt++;
            udf_id_tmp[jj++] = udf_grp_cur.udf_id[ii];
        }
    }

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    if(SAI_UDF_GROUP_TYPE_GENERIC == udf_grp_type)
    {
        if(0 == udf_cnt)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d %-12s %-18s\n",num_cnt, udf_grp_oid_cur, udf_grp_type,\
                    udf_grp_cur.acl_ref_cnt, "-", "-");
        }
        else
        {
            if(1 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d %-12s 0x%016"PRIx64 "\n", num_cnt, udf_grp_oid_cur, udf_grp_type, \
                    udf_grp_cur.acl_ref_cnt, "-", udf_id_tmp[0]);
            }
            else if(2 <= udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d %-12s 0x%016"PRIx64 " 0x%016"PRIx64"\n", num_cnt, udf_grp_oid_cur, udf_grp_type, \
                    udf_grp_cur.acl_ref_cnt, "-", udf_id_tmp[0], udf_id_tmp[1]);
            }

            if(3 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-61s 0x%016"PRIx64"\n", " ", udf_id_tmp[2]);
            }
            else if(4 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-61s 0x%016"PRIx64 " 0x%016"PRIx64"\n", " ", udf_id_tmp[2], udf_id_tmp[3]);
            }
        }
    }
    else if(SAI_UDF_GROUP_TYPE_HASH == udf_grp_type)
    {
        if(0 == udf_cnt)
        {
            CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d 0x%-10x %-18s\n", num_cnt, udf_grp_oid_cur, udf_grp_type,\
                    udf_grp_cur.acl_ref_cnt, udf_grp_cur.hash_udf_bmp,"-");
        }
        else
        {
            if(1 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d 0x%-10x 0x%016"PRIx64"\n", num_cnt, udf_grp_oid_cur, udf_grp_type, \
                    udf_grp_cur.acl_ref_cnt, udf_grp_cur.hash_udf_bmp, udf_id_tmp[0]);
            }
            else if(2 <= udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-12d %-11d 0x%-10x 0x%016"PRIx64 " 0x%016"PRIx64"\n", num_cnt, udf_grp_oid_cur, udf_grp_type, \
                    udf_grp_cur.acl_ref_cnt, udf_grp_cur.hash_udf_bmp, udf_id_tmp[0], udf_id_tmp[1]);
            }

            if(3 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-61s 0x%016"PRIx64"\n", " ", udf_id_tmp[2]);
            }
            else if(4 == udf_cnt)
            {
                CTC_SAI_LOG_DUMP(p_file, "%-61s 0x%016"PRIx64 " 0x%016"PRIx64"\n", " ", udf_id_tmp[2], udf_id_tmp[3]);
            }
        }
    }
    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static
sai_status_t _ctc_sai_udf_match_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  udf_match_oid_cur = 0;
    ctc_sai_udf_match_t    udf_match_cur;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&udf_match_cur, 0, sizeof(ctc_sai_udf_match_t));

    udf_match_oid_cur = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_match_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }

    sal_memcpy((ctc_sai_udf_match_t*)(&udf_match_cur), bucket_data->data, sizeof(ctc_sai_udf_match_t));

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " %-11d %-8d 0x%-4x/0x%-9x 0x%-2x/0x%-10x 0x%-4x/0x%-14x\n", num_cnt, udf_match_oid_cur, udf_match_cur.udf_ref_cnt,udf_match_cur.priority, \
        udf_match_cur.ethertype[0], udf_match_cur.ethertype[1], udf_match_cur.ip_protocal[0],udf_match_cur.ip_protocal[1],udf_match_cur.gre_protocal_type[0],udf_match_cur.gre_protocal_type[1]);

    (*((uint32 *)(p_cb_data->value1)))++;
    return SAI_STATUS_SUCCESS;
}

static
sai_status_t _ctc_sai_udf_dump_print_cb(ctc_sai_oid_property_t* bucket_data, ctc_sai_db_traverse_param_t *p_cb_data)
{
    sai_object_id_t  udf_oid_cur = 0;
    ctc_sai_udf_t    udf_cur;
    sal_file_t p_file = NULL;
    uint32 num_cnt = 0;
    uint8 ii = 0;
    uint8 hash_mask_cnt = 0;
    uint8 udf_base = 0;
    ctc_sai_dump_grep_param_t* p_dmp_grep = NULL;

    sal_memset(&udf_cur, 0, sizeof(ctc_sai_udf_t));

    udf_oid_cur = bucket_data->oid;
    p_dmp_grep = (ctc_sai_dump_grep_param_t*)p_cb_data->value2;

    if ((0 != p_dmp_grep->key.key.object_id) && (udf_oid_cur != p_dmp_grep->key.key.object_id))
    {
        return SAI_STATUS_FAILURE;
    }

    ctc_sai_oid_get_sub_type(udf_oid_cur, &udf_base);
    sal_memcpy((ctc_sai_udf_t*)(&udf_cur), bucket_data->data, sizeof(ctc_sai_udf_t));

    for (ii = 0; ii < 4; ii++)
    {
        if (0 != udf_cur.hash_mask[ii])
        {
            hash_mask_cnt++;
        }
    }

    p_file = (sal_file_t)p_cb_data->value0;
    num_cnt = *((uint32 *)(p_cb_data->value1));

    CTC_SAI_LOG_DUMP(p_file, "%-4d 0x%016"PRIx64 " 0x%016"PRIx64 " 0x%016"PRIx64 " %-4d %-6d 0x%-2x 0x%-2x 0x%-2x 0x%-2x\n", num_cnt, udf_oid_cur, udf_cur.group_id, \
        udf_cur.match_id, udf_base, udf_cur.offset, udf_cur.hash_mask[0], udf_cur.hash_mask[1], udf_cur.hash_mask[2], udf_cur.hash_mask[3]);

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
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-12s %-11s %-12s %-18s\n", "No.", "UDF_Grp_oid", "UDF_Grp_TYPE", "acl_ref_cnt", "hash_udf_bmp", "UDF_oid");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF_GROUP,
                                            (hash_traversal_fn)_ctc_sai_udf_grp_dump_print_cb, (void*)(&sai_cb_data));
    }
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_UDF_MATCH))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF MATCH");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_udf_match_t");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-11s %-8s %-18s %-17s %-23s\n", "No.", "Match_oid", "udf_ref_cnt", "priority", "ethtype(data/mask)", "ip_pro(data/mask)", "gre_pro_type(data/mask)");
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
        num_cnt = 1;
        ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF_MATCH,
                                            (hash_traversal_fn)_ctc_sai_udf_match_dump_print_cb, (void*)(&sai_cb_data));
    }
    if (CTC_BMP_ISSET(dump_grep_param->object_bmp, SAI_OBJECT_TYPE_UDF))
    {
        CTC_SAI_LOG_DUMP(p_file, "%s\n", "UDF");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "ctc_sai_udf_t");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    CTC_SAI_LOG_DUMP(p_file, "%-4s %-18s %-18s %-18s %-4s %-4s %-9s\n", "No.", "UDF_oid", "UDF_Grp_oid", "Match_oid", "Base", "Offset", "Hash_mask");
    CTC_SAI_LOG_DUMP(p_file, "%s\n", "-----------------------------------------------------------------------------------------------------------------------");
    num_cnt = 1;
    ctc_sai_db_traverse_object_property(lchip, SAI_OBJECT_TYPE_UDF,
                                        (hash_traversal_fn)_ctc_sai_udf_dump_print_cb, (void*)(&sai_cb_data));
    }
}

sai_status_t   /* called when set hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST */
ctc_sai_udf_get_hash_mask(uint8 lchip, sai_object_id_t udf_group_id, uint16* hash_udf_bmp, uint32* udf_group_value)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    uint8 udf_group_type =0;
    ctc_object_id_t ctc_object_id;

    CTC_PTR_VALID_CHECK(hash_udf_bmp);
    CTC_PTR_VALID_CHECK(udf_group_value);

    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf hash mask, invalid udf_group_id; udf_group_id = 0x%"PRIx64"!\n", udf_group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_sub_type(udf_group_id, &udf_group_type), status, out);
    if(SAI_UDF_GROUP_TYPE_HASH != udf_group_type)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf hash mask, udf group type is not hash; udf_group_id = 0x%"PRIx64"!\n", udf_group_id);
        status = SAI_STATUS_INVALID_PARAMETER;
        goto out;
    }

    ctc_sai_get_ctc_object_id(SAI_OBJECT_TYPE_UDF_GROUP, udf_group_id, &ctc_object_id);

    *hash_udf_bmp = p_udf_group->hash_udf_bmp;
    *udf_group_value = ctc_object_id.value;

out:
    return status;
}


#define ________SAI_API________

#define ________SAI_API_UDF_GROUP________

static sai_status_t
ctc_sai_udf_create_udf_group(sai_object_id_t *udf_group_id,
                                         sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_udf_group_id = 0;
    sai_object_id_t udf_group_obj_id = 0;
    uint8 lchip = 0;
    uint8 udf_group_type = SAI_UDF_GROUP_TYPE_GENERIC;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    const sai_attribute_value_t *attr_value;
    uint32 attr_index = 0;
    ctc_sai_switch_master_t* p_switch_master = NULL;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(udf_group_id);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    if(NULL != p_switch_master) /* check udf group cnt  */
    {
        if(p_switch_master->udf_group_cnt > CTC_SAI_UDF_GROUP_MAX_NUM(lchip))
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf group, udf group have alredy used out!\n");
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_GROUP_ATTR_LENGTH, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if (CTC_SAI_UDF_GROUP_LENGTH(lchip) != attr_value->u16) /* dt2 group length must be 4 byte, gg group length must be 1 byte */
        {
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_GROUP_ATTR_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        chip_type = ctcs_get_chip_type(lchip);
        if((CTC_CHIP_GOLDENGATE == chip_type) && (attr_value->s32 == SAI_UDF_GROUP_TYPE_HASH))
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf group, goldengate udf only used for acl, udf group type invalid, group_type=%d!\n",attr_value->s32);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
        udf_group_type = attr_value->s32;
    }

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_udf_group_id);
    if (status)
    {
        goto out;
    }

    udf_group_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF_GROUP, lchip, udf_group_type, 0, ctc_udf_group_id);
    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_build_udf_group_db(lchip, udf_group_obj_id, &p_udf_group),status,error0);
    *udf_group_id = udf_group_obj_id;
    p_switch_master->udf_group_cnt++;
    goto out;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error0\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_group_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_udf_group(sai_object_id_t udf_group_id)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_group_t*     p_udf_group = NULL;
    uint32 ctc_udf_group_id = 0;
    uint8 loop_i =0;
    ctc_sai_switch_master_t* p_switch_master = NULL;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf group, invalid udf_group_id 0x%"PRIx64"!\n", udf_group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_judged_used(lchip,CTC_SAI_UDF_OP_REMOVE, udf_group_id, NULL),status,out);

    for(loop_i=0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++)
    {
        if(p_udf_group->udf_id[loop_i])/* check udf group have udf; can't remove */
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf group, udf_group_id 0x%"PRIx64" still have no less one udf!\n", udf_group_id);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto out;
        }
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_remove_udf_group_db(lchip, udf_group_id),status,out);
    CTC_SAI_ERROR_GOTO(_ctc_sai_oid_get_udf_group_id(udf_group_id, &ctc_udf_group_id),status,out);
    CTC_SAI_ERROR_GOTO(ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_group_id),status,out);
    p_switch_master = ctc_sai_get_switch_property(lchip);
    p_switch_master->udf_group_cnt--;

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_set_udf_group_attribute(sai_object_id_t udf_group_id, const sai_attribute_t *attr)
{
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "set udf group attribute not support\n");
    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_udf_get_udf_group_attribute(sai_object_id_t udf_group_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    ctc_sai_udf_group_t*     p_udf_group = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_group_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf_group = ctc_sai_db_get_object_property(lchip, udf_group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf group, invalid udf_group_id 0x%"PRIx64"!\n", udf_group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    key.key.object_id = udf_group_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF_GROUP, loop, udf_group_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


#define ________SAI_API_UDF_MATCH________

static sai_status_t
ctc_sai_udf_create_udf_match(sai_object_id_t *udf_match_id,
                                         sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_udf_match_id = 0;
    sai_object_id_t udf_match_obj_id = 0;
    uint8 lchip = 0;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    const sai_attribute_value_t *attr_value;
    uint32 attr_index = 0;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(udf_match_id);

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));

    CTC_SAI_DB_LOCK(lchip);

    status = ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_udf_match_id);
    if (status)
    {
        goto out;
    }

    udf_match_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF_MATCH, lchip, 0, 0, ctc_udf_match_id);
    status = _ctc_sai_udf_build_udf_match_db(lchip, udf_match_obj_id, &p_udf_match);
    if (CTC_SAI_ERROR(status))
    {
        ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_match_id);
        goto out;
    }

    chip_type = ctcs_get_chip_type(lchip);
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_L2_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if((CTC_CHIP_GOLDENGATE == chip_type) && (attr_value->aclfield.mask.u16 != 0xFFFF))
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf match, goldengate SAI_UDF_MATCH_ATTR_L2_TYPE's mask must be 0xFFFF,mask= 0x%x!\n",attr_value->aclfield.mask.u16);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
        p_udf_match->ethertype[0]= attr_value->aclfield.data.u16;
        p_udf_match->ethertype[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_L3_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if((CTC_CHIP_GOLDENGATE == chip_type) && (attr_value->aclfield.mask.u8 != 0xFF))
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf match, goldengate SAI_UDF_MATCH_ATTR_L3_TYPE's mask must be 0xFF,mask= 0x%x!\n",attr_value->aclfield.mask.u8);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
        p_udf_match->ip_protocal[0]= attr_value->aclfield.data.u8;
        p_udf_match->ip_protocal[1]= attr_value->aclfield.mask.u8;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_GRE_TYPE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if(CTC_CHIP_GOLDENGATE == chip_type)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf match, goldengate not support SAI_UDF_MATCH_ATTR_GRE_TYPE!\n");
            status = SAI_STATUS_NOT_SUPPORTED;
            goto error0;
        }
        p_udf_match->gre_protocal_type[0]= attr_value->aclfield.data.u16;
        p_udf_match->gre_protocal_type[1]= attr_value->aclfield.mask.u16;
    }
    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_MATCH_ATTR_PRIORITY, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_udf_match->priority= attr_value->u8;
    }
    *udf_match_id = udf_match_obj_id;
    goto out;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error0\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_match_id);
    _ctc_sai_udf_remove_udf_match_db(lchip, udf_match_obj_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_udf_match(sai_object_id_t udf_match_id)
{
    uint8 lchip = 0;
    sai_status_t           status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    uint32 ctc_udf_match_id = 0;

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_match_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf_match = ctc_sai_db_get_object_property(lchip, udf_match_id);
    if (NULL == p_udf_match)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf match, invalid udf_match_id 0x%"PRIx64"!\n", udf_match_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    if((p_udf_match->udf_ref_cnt !=0))  /* check udf match is or not used by udf */
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf match, udf_match_id 0x%"PRIx64" is used by udf!\n", udf_match_id);
        status = SAI_STATUS_OBJECT_IN_USE;
        goto out;
    }

    _ctc_sai_udf_remove_udf_match_db(lchip, udf_match_id);
    _ctc_sai_oid_get_udf_match_id(udf_match_id, &ctc_udf_match_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_match_id);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


static sai_status_t
ctc_sai_udf_set_udf_match_attribute(sai_object_id_t udf_match_id, const sai_attribute_t *attr)
{
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "set udf match attribute not support\n");
    return SAI_STATUS_NOT_SUPPORTED;
}

static sai_status_t
ctc_sai_udf_get_udf_match_attribute(sai_object_id_t udf_match_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_match_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    key.key.object_id = udf_match_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF_MATCH, loop, udf_match_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

#define ________SAI_API_UDF________

static sai_status_t
ctc_sai_udf_create_udf(sai_object_id_t *udf_id,
                                         sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint32 ctc_udf_id = 0;
    sai_object_id_t udf_obj_id = 0;
    uint8 lchip = 0;
    uint8 current_udf_base = 0;
    ctc_sai_udf_t* p_udf = NULL;
    ctc_sai_udf_t* p_udf_cmp = NULL;
    ctc_sai_udf_match_t* p_udf_match = NULL;
    ctc_sai_udf_group_t* p_udf_group = NULL;
    ctc_sai_udf_group_t  sai_udf_group_old;
    ctc_sai_udf_match_t  sai_udf_match_old;
    const sai_attribute_value_t *attr_value;
    uint32 attr_index = 0;
    uint8  loop_i = 0;
    uint8  udf_cnt_in_group  = 0;
    uint8  udf_base_cmp = 0;
    uint64 current_match_id = 0;
    uint64 udf_id_cmp = 0;
    uint8 valid_index = 0;
    ctc_object_id_t ctc_object_id;
    uint8 hash_mask_default[CTC_SAI_UDF_HASH_MASK_BYTE_CNT] = {0xFF,0xFF,0xFF,0xFF};
    uint8 udf_group_type = 0;
    uint8 chip_type = 0;

    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    CTC_SAI_PTR_VALID_CHECK(udf_id);
    sal_memset(&ctc_object_id, 0, sizeof(ctc_object_id_t));
    sal_memset(&sai_udf_group_old, 0 , sizeof(ctc_sai_udf_group_t));
    sal_memset(&sai_udf_match_old, 0 , sizeof(ctc_sai_udf_match_t));

    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(switch_id, &lchip));
    chip_type = ctcs_get_chip_type(lchip);

    CTC_SAI_DB_LOCK(lchip);

    CTC_SAI_ERROR_GOTO(ctc_sai_db_alloc_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, &ctc_udf_id),status,out);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_BASE, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        if(CTC_CHIP_GOLDENGATE == chip_type && attr_value->s32 != SAI_UDF_BASE_L3 && attr_value->s32 != SAI_UDF_BASE_L4)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, goldengate offset_type must be L3 or L4!\n");
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error0;
        }
        current_udf_base = attr_value->s32;
    }

    /* sub_type is udf_base; 0:SAI_UDF_BASE_L2; 1: SAI_UDF_BASE_L3; 2: SAI_UDF_BASE_L4;*/
    udf_obj_id = ctc_sai_create_object_id(SAI_OBJECT_TYPE_UDF, lchip, current_udf_base, 0, ctc_udf_id);
    CTC_SAI_ERROR_GOTO( _ctc_sai_udf_build_udf_db(lchip, udf_obj_id, &p_udf), status, error0);

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_MATCH_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )  /* @flags MANDATORY_ON_CREATE | CREATE_ONLY */
    {
        p_udf_match = ctc_sai_db_get_object_property(lchip, attr_value->oid); /* match id must exists */
        if (NULL == p_udf_match)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, match id not exists 0x%"PRIx64"!\n", attr_value->oid);
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error1;
        }
        sal_memcpy(&sai_udf_match_old, p_udf_match, sizeof(ctc_sai_udf_match_t));

        if(CTC_CHIP_GOLDENGATE == chip_type)
        {
            if((SAI_UDF_BASE_L3 == current_udf_base) && (p_udf_match->ip_protocal[1] != 0))
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, goldengate L3 UDF Key only support ethertype!\n");
                status = SAI_STATUS_NOT_SUPPORTED;
                goto error1;
            }
            else if(SAI_UDF_BASE_L4 == current_udf_base)
            {
                if(p_udf_match->ethertype[1] != 0 && p_udf_match->ip_protocal[1]==0)
                {
                    CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, goldengate L4 UDF Key not support ethertype!\n");
                    status = SAI_STATUS_NOT_SUPPORTED;
                    goto error1;
                }
                else if(!(p_udf_match->ethertype[1]==0x0800 || p_udf_match->ethertype[1]==0x86dd))
                {
                    CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, goldengate L4 UDF Key ethertype must be 0x0800 or 0x86dd,!\n");
                    status = SAI_STATUS_INVALID_PARAMETER;
                    goto error1;
                }
            }
        }
        p_udf->match_id = attr_value->oid;
        current_match_id = attr_value->oid;
        p_udf_match->udf_ref_cnt++;
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto error1;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_GROUP_ID, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS )
    {
        p_udf_group = ctc_sai_db_get_object_property(lchip, attr_value->oid); /* group id must exists */
        if (NULL == p_udf_group)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, group id must exists 0x%"PRIx64"!\n", attr_value->oid);
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto error2;
        }
        sal_memcpy(&sai_udf_group_old, p_udf_group, sizeof(ctc_sai_udf_group_t));
        for(loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++)
        {
            if(p_udf_group->udf_id[loop_i])
            {
                udf_id_cmp = p_udf_group->udf_id[loop_i];
                udf_cnt_in_group++;
            }
            else
            {
                valid_index = loop_i;
            }
        }
        if(CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP == udf_cnt_in_group)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, group (0x%"PRIx64") already exists 4 udf!\n", attr_value->oid);
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error2;
        }
        if (udf_cnt_in_group)
        {
            p_udf_cmp = ctc_sai_db_get_object_property(lchip, udf_id_cmp);
            if (NULL == p_udf_cmp)
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") not in the group !\n", udf_id_cmp);
                status = SAI_STATUS_ITEM_NOT_FOUND;
                goto error2;
            }
            CTC_SAI_ERROR_GOTO(ctc_sai_oid_get_sub_type(udf_id_cmp, &udf_base_cmp), status, error2);
            if ((current_udf_base != udf_base_cmp) || (current_match_id != p_udf_cmp->match_id))
            {
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") and udf(0x%"PRIx64") base is not same!\n", udf_id_cmp, udf_obj_id);
                CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, udf(0x%"PRIx64") and udf(0x%"PRIx64") match_id is not same!\n", udf_id_cmp, udf_obj_id);
                status = SAI_STATUS_INVALID_PARAMETER;
                goto error2;
            }
        }
        p_udf_group->udf_id[valid_index] = udf_obj_id;
        p_udf->group_id = attr_value->oid;
    }
    else
    {
        status = SAI_STATUS_MANDATORY_ATTRIBUTE_MISSING;
        goto error2;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_OFFSET, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        p_udf->offset= attr_value->u16;
    }

    status = ctc_sai_find_attrib_in_list(attr_count, attr_list, SAI_UDF_ATTR_HASH_MASK, &attr_value, &attr_index);
    if (status == SAI_STATUS_SUCCESS)
    {
        if (CTC_CHIP_GOLDENGATE == chip_type)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to create udf, golddengate udf only used for acl, not support SAI_UDF_ATTR_HASH_MASK !\n");
            status = SAI_STATUS_INVALID_PARAMETER;
            goto error3;
        }
        CTC_SAI_ERROR_GOTO(_ctc_sai_udf_set_hash_mask(lchip, 0, attr_value, p_udf),status,error3);
    }
    else
    {
        if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
        {
            /* Default to 2 bytes, value 0xFF, 0xFF ???? ==>> Default to 4 bytes, value 0xFF, 0xFF, 0xFF, 0xFF */
            ctc_sai_oid_get_sub_type(p_udf->group_id, &udf_group_type);
            if (SAI_UDF_GROUP_TYPE_HASH == udf_group_type)
            {
                sal_memcpy(p_udf->hash_mask, hash_mask_default, CTC_SAI_UDF_HASH_MASK_BYTE_CNT);
                CTC_SAI_ERROR_GOTO(_ctc_sai_udf_set_hash_mask(lchip, 1, attr_value, p_udf), status, error3);
            }
        }
    }

    if ((CTC_CHIP_DUET2 == chip_type) || (CTC_CHIP_TSINGMA == chip_type))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_udf_update_ctc_udf_entry(lchip, p_udf_group, p_udf->group_id), status, error3);
    }
    else if(CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_udf_update_goldengate_ctc_udf_entry(lchip, p_udf_group), status, error3);
    }

    *udf_id = udf_obj_id;
    goto out;

error3:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error3\n");
    sal_memcpy(p_udf_group, &sai_udf_group_old, sizeof(ctc_sai_udf_group_t));
error2:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error2\n");
    sal_memcpy(p_udf_match, &sai_udf_match_old, sizeof(ctc_sai_udf_match_t));
error1:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error1\n");
    _ctc_sai_udf_remove_udf_db(lchip, udf_obj_id);
error0:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error0\n");
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_id);
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_remove_udf(sai_object_id_t udf_id)
{
    uint8 lchip = 0;
    sai_status_t             status = SAI_STATUS_SUCCESS;
    ctc_sai_udf_t*           p_udf = NULL;
    ctc_sai_udf_group_t*     p_udf_group = NULL;
    ctc_sai_udf_group_t      sai_udf_group_old;
    ctc_sai_udf_match_t*     p_udf_match = NULL;
    uint32 ctc_udf_id = 0;
    uint8  loop_i =0;
    uint16 offset_rm =0;

    sal_memset(&sai_udf_group_old, 0 , sizeof(ctc_sai_udf_group_t));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);
    p_udf = ctc_sai_db_get_object_property(lchip, udf_id);
    if (NULL == p_udf)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf, invalid udf_id 0x%"PRIx64"!\n", udf_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_judged_used(lchip,CTC_SAI_UDF_OP_REMOVE, 0, p_udf),status,out);
    offset_rm = p_udf->offset;

    p_udf_group = ctc_sai_db_get_object_property(lchip, p_udf->group_id);
    if (NULL == p_udf_group)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf, invalid udf_group_id 0x%"PRIx64" !\n", p_udf->group_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }
    sal_memcpy(&sai_udf_group_old, p_udf_group, sizeof(ctc_sai_udf_group_t));

    for (loop_i = 0; loop_i < CTC_SAI_UDF_MAX_UDF_CNT_IN_GROUP; loop_i++) /* get udf in group */
    {
        if (0 == p_udf_group->udf_id[loop_i])
        {
            continue;
        }
        p_udf = ctc_sai_db_get_object_property(lchip, p_udf_group->udf_id[loop_i]);
        if (NULL == p_udf)
        {
            CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to remove udf, udf(0x%"PRIx64") not in the group !\n", p_udf_group->udf_id[loop_i]);
            status = SAI_STATUS_ITEM_NOT_FOUND;
            goto out;
        }
        if (offset_rm == p_udf->offset)
        {
            p_udf_group->udf_id[loop_i]= 0;
        }
    }

    if (CTC_CHIP_DUET2 == ctcs_get_chip_type(lchip))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_udf_update_ctc_udf_entry(lchip, p_udf_group, p_udf->group_id), status, error0);
    }
    else if(CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
    {
        CTC_SAI_ERROR_GOTO(_ctc_sai_udf_update_goldengate_ctc_udf_entry(lchip, p_udf_group), status, error0);
    }

    p_udf_match= ctc_sai_db_get_object_property(lchip, p_udf->match_id);
    p_udf_match->udf_ref_cnt--;
    _ctc_sai_udf_remove_udf_db(lchip, udf_id);
    _ctc_sai_oid_get_udf_id(udf_id, &ctc_udf_id);
    ctc_sai_db_free_id(lchip, CTC_SAI_DB_ID_TYPE_COMMON, ctc_udf_id);
    goto out;

error0:
    CTC_SAI_LOG_ERROR(SAI_API_UDF, "rollback to error0\n");
    sal_memcpy(p_udf_group, &sai_udf_group_old, sizeof(ctc_sai_udf_group_t));
out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_set_udf_attribute(sai_object_id_t udf_id, const sai_attribute_t *attr)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip  = 0;
    ctc_sai_udf_t*           p_udf = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    if (CTC_CHIP_GOLDENGATE == ctcs_get_chip_type(lchip))
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf, goldengate not support set udf attribute!\n");
        status = SAI_STATUS_NOT_SUPPORTED;
        goto out;
    }

    p_udf = ctc_sai_db_get_object_property(lchip, udf_id); /* exsits or not */
    if (NULL == p_udf)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to set udf, invalid udf_id 0x%"PRIx64"!\n", udf_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    CTC_SAI_ERROR_GOTO(_ctc_sai_udf_judged_used(lchip, CTC_SAI_UDF_OP_SET, 0, p_udf),status,out);

    key.key.object_id = udf_id;
    CTC_SAI_ERROR_GOTO(ctc_sai_set_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF, udf_attr_fn_entries, attr), status, out);

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}

static sai_status_t
ctc_sai_udf_get_udf_attribute(sai_object_id_t udf_id, uint32_t attr_count, sai_attribute_t *attr_list)
{
    sai_status_t           status = SAI_STATUS_SUCCESS;
    uint8 lchip = 0;
    uint8 loop = 0;
    ctc_sai_udf_t*         p_udf = NULL;
    sai_object_key_t key;

    sal_memset(&key, 0, sizeof(key));
    CTC_SAI_ERROR_RETURN(ctc_sai_oid_get_lchip(udf_id, &lchip));
    CTC_SAI_DB_LOCK(lchip);
    CTC_SAI_LOG_ENTER(SAI_API_UDF);

    p_udf = ctc_sai_db_get_object_property(lchip, udf_id);
    if (NULL == p_udf)
    {
        CTC_SAI_LOG_ERROR(SAI_API_UDF, "Failed to get udf, invalid udf_id 0x%"PRIx64"!\n", udf_id);
        status = SAI_STATUS_ITEM_NOT_FOUND;
        goto out;
    }

    key.key.object_id = udf_id;
    while(loop < attr_count)
    {
        CTC_SAI_ERROR_GOTO(ctc_sai_get_attribute(&key, NULL, SAI_OBJECT_TYPE_UDF, loop, udf_attr_fn_entries, &attr_list[loop]), status, out);
        loop++ ;
    }

out:
    CTC_SAI_DB_UNLOCK(lchip);
    return status;
}


const sai_udf_api_t ctc_sai_udf_api =
{
    ctc_sai_udf_create_udf,
    ctc_sai_udf_remove_udf,
    ctc_sai_udf_set_udf_attribute,
    ctc_sai_udf_get_udf_attribute,
    ctc_sai_udf_create_udf_match,
    ctc_sai_udf_remove_udf_match,
    ctc_sai_udf_set_udf_match_attribute,
    ctc_sai_udf_get_udf_match_attribute,
    ctc_sai_udf_create_udf_group,
    ctc_sai_udf_remove_udf_group,
    ctc_sai_udf_set_udf_group_attribute,
    ctc_sai_udf_get_udf_group_attribute,
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
    wb_info.data_len = sizeof(ctc_sai_udf_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_udf_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_UDF;
    wb_info.data_len = sizeof(ctc_sai_udf_match_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_udf_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF_MATCH, (void*)(&wb_info));

    sal_memset(&wb_info, 0, sizeof(wb_info));
    wb_info.version = SYS_WB_VERSION_UDF;
    wb_info.data_len = sizeof(ctc_sai_udf_group_t);
    wb_info.wb_sync_cb = NULL;
    wb_info.wb_reload_cb = _ctc_sai_udf_wb_reload_cb;
    ctc_sai_warmboot_register_cb(lchip, CTC_SAI_WB_TYPE_OID, SAI_OBJECT_TYPE_UDF_GROUP, (void*)(&wb_info));
    return SAI_STATUS_SUCCESS;
}


