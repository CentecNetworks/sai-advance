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
\t  |   API                                |       SUPPORT CHIPS LIST       |
\t  |  create_udf                          |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_udf                          |    CTC8096,CTC7148,CTC7132     |
\t  |  set_udf_attribute                   |    CTC8096,CTC7148,CTC7132     |
\t  |  get_udf_attribute                   |    CTC8096,CTC7148,CTC7132     |
\t  |  create_udf_match                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_udf_match                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_udf_match_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_udf_match_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  create_udf_group                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_udf_group                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_udf_group_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_udf_group_attribute             |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The UDF GROUP attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_UDF_GROUP_ATTR_UDF_LIST         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_GROUP_ATTR_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_GROUP_ATTR_LENGTH           |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The UDF MATCH attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_UDF_MATCH_ATTR_L2_TYPE          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_MATCH_ATTR_L3_TYPE          |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_MATCH_ATTR_GRE_TYPE         |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_MATCH_ATTR_PRIORITY         |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The UDF attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_UDF_ATTR_MATCH_ID               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_ATTR_GROUP_ID               |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_ATTR_BASE                   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_ATTR_OFFSET                 |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_UDF_ATTR_HASH_MASK              |         CTC7148,CTC7132        |
\b

*/

#ifndef _CTC_SAI_UDF_H
#define _CTC_SAI_UDF_H


#include "ctc_sai.h"
#include "sal.h"
#include "ctcs_api.h"
/*don't need include other header files*/

typedef struct ctc_sai_udf_group_s
{
    uint8               acl_ref_cnt;
    uint8               add_valid;
    sai_object_id_t     udf_id[4];    /* udf_oid must be not 0 */
    uint16              hash_udf_bmp; /* corresponding to hash 16bit bitbmp */
}ctc_sai_udf_group_t;

extern sai_status_t
ctc_sai_udf_api_init();

extern sai_status_t
ctc_sai_udf_db_init(uint8 lchip);

extern sai_status_t   /* called when set hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST */
ctc_sai_udf_get_hash_mask(uint8 lchip, sai_object_id_t udf_group_id, uint16* hash_udf_bmp, uint32* udf_group_value);

extern void
ctc_sai_udf_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_UDF_H*/


