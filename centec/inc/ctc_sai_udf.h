/**
 @file ctc_sai_udf.h

  @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI UDF.
\b
\p
 The UDF Module APIs supported by centec devices:
\p
\b
\t  |   API                                |          SUPPORT CHIPS LIST           |
\t  |  create_udf                          |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  remove_udf                          |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  set_udf_attribute                   |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  get_udf_attribute                   |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  create_udf_match                    |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  remove_udf_match                    |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  set_udf_match_attribute             |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  get_udf_match_attribute             |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  create_udf_group                    |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  remove_udf_group                    |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  set_udf_group_attribute             |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  get_udf_group_attribute             |    CTC8096,CTC7148,CTC7132,CTC8180    |
\b

\p
 The UDF GROUP attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |          SUPPORT CHIPS LIST           |
\t  |  SAI_UDF_GROUP_ATTR_UDF_LIST         |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_GROUP_ATTR_TYPE             |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_GROUP_ATTR_LENGTH           |    CTC8096,CTC7148,CTC7132,CTC8180    |
\b

\p
 The UDF MATCH attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                                  |          SUPPORT CHIPS LIST           |
\t  |  SAI_UDF_MATCH_ATTR_L2_TYPE                  |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_MATCH_ATTR_L3_TYPE                  |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_MATCH_ATTR_GRE_TYPE                 |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_MATCH_ATTR_PRIORITY                 |    CTC8096,CTC7148,CTC7132,CTC8180    |
\e  |  SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM    |    CTC8096,CTC7148,CTC7132,CTC8180    |
\e  |  SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT       |    CTC8096,CTC7148,CTC7132,CTC8180    |
\e  |  SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT       |    CTC8096,CTC7148,CTC7132,CTC8180    |
\b

\p
 The UDF attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |          SUPPORT CHIPS LIST           |
\t  |  SAI_UDF_ATTR_MATCH_ID               |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_ATTR_GROUP_ID               |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_ATTR_BASE                   |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_ATTR_OFFSET                 |    CTC8096,CTC7148,CTC7132,CTC8180    |
\t  |  SAI_UDF_ATTR_HASH_MASK              |                   -                   |
\b

*/

#ifndef _CTC_SAI_UDF_H
#define _CTC_SAI_UDF_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

#define CTC_SAI_UDF_GROUP_LENGTH(lchip)  ((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) ? 16 : ((CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))? 16:0))
#define CTC_SAI_UDF_ENTRY_MAX_NUM(lchip) ((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) ? 16 : ((CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))? 256:0))
#define CTC_SAI_UDF_GROUP_MAX_NUM(lchip) ((CTC_CHIP_TSINGMA == ctcs_get_chip_type(lchip)) ? 16 : ((CTC_CHIP_TSINGMA_MX == ctcs_get_chip_type(lchip))? 256:0))
#define CTC_SAI_UDF_HASH_MASK_LENGTH     16

struct ctc_sai_udf_group_member_s
{
    ctc_slistnode_t head;
    sai_object_id_t udf_id;
};
typedef struct ctc_sai_udf_group_member_s ctc_sai_udf_group_member_t;

struct ctc_sai_udf_group_hash_s
{
    ctc_slistnode_t head;
    sai_object_id_t ld_hash_id;
};
typedef struct ctc_sai_udf_group_hash_s ctc_sai_udf_group_hash_t;

struct ctc_sai_udf_entry_s
{
    sai_object_id_t match_id;
    sai_object_id_t group_id;
    uint8   hash_mask[CTC_SAI_UDF_HASH_MASK_LENGTH];
    uint8   base;
    uint16  offset;
};
typedef struct ctc_sai_udf_entry_s ctc_sai_udf_entry_t;

struct ctc_sai_udf_match_s
{
    uint8   ref_cnt;
    uint16  ethertype[2];
    uint8   ip_protocal[2];
    uint16  gre_protocal_type[2];
    uint8   mpls_label_num;
    uint16  l4_src_port[2];
    uint16  l4_dst_port[2];

    uint8   priority;
};
typedef struct ctc_sai_udf_match_s ctc_sai_udf_match_t;

struct ctc_sai_udf_group_s
{
    uint8  type;
    uint8  length;
    uint16 hash_udf_bmp;
    uint32 ref_cnt;

    ctc_slist_t* hash_list;
    ctc_slist_t* member_list;
};
typedef struct ctc_sai_udf_group_s ctc_sai_udf_group_t;

extern sai_status_t
ctc_sai_udf_api_init();

extern sai_status_t
ctc_sai_udf_db_init(uint8 lchip);

/* called when set hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST */
extern sai_status_t
ctc_sai_udf_get_hash_mask(uint8 lchip, sai_object_id_t udf_group_id, uint16* hash_udf_bmp);

extern void
ctc_sai_udf_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_UDF_H*/

