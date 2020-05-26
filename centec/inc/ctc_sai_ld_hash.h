/**
 @file ctc_sai_hash.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
This module defines SAI HASH.
\b
\p
 The HASH Module APIs supported by centec devices:
\p
\b
\t  |   API                                |       SUPPORT CHIPS LIST       |
\t  |  create_hash                         |              -                 |
\t  |  remove_hash                         |              -                 |
\t  |  set_hash_attribute                  |    CTC8096,CTC7148,CTC7132     |
\t  |  get_hash_attribute                  |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The HASH attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST|    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_HASH_ATTR_UDF_GROUP_LIST        |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The Hash Field supported by centec devices:
\p
\b
\t  |   Hash Field                         |       SUPPORT CHIPS LIST       |
\t  |  SAI_NATIVE_HASH_FIELD_SRC_IP        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_DST_IP        |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_INNER_SRC_IP  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_INNER_DST_IP  |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_VLAN_ID       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_IP_PROTOCOL   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_ETHERTYPE     |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_L4_SRC_PORT   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_L4_DST_PORT   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_SRC_MAC       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_DST_MAC       |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_NATIVE_HASH_FIELD_IN_PORT       |    CTC8096,CTC7148,CTC7132     |
\b
*/

#ifndef _CTC_SAI_LD_HASH_H
#define _CTC_SAI_LD_HASH_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

enum ctc_ld_hash_usage_e
{
    CTC_SAI_HASH_USAGE_ECMP,     /**< hash application for ecmp */
    CTC_SAI_HASH_USAGE_LINKAGG,  /**< hash application for linkagg */
    CTC_SAI_HASH_USAGE_NUM,      /**< hash application num */
};
typedef enum ctc_ld_hash_usage_e ctc_ld_hash_usage_t;

typedef struct ctc_sai_ld_hash_s
{
    uint32 field_bmp;
    sai_object_list_t udf_group_list;  /* count: duet2 max 16 */
}ctc_sai_ld_hash_t;

extern sai_status_t
ctc_sai_ld_hash_api_init();

extern sai_status_t
ctc_sai_ld_hash_db_init(uint8 lchip); /* called when ctc_sai_switch_create_db; create switch
                                          ctc_sai_switch_remove_switch,ctc_sai_db_deinit */
extern void
ctc_sai_ld_hash_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

extern sai_status_t
ctc_sai_ld_hash_db_deinit(uint8 lchip);

#endif /*_CTC_SAI_LD_HASH_H*/

