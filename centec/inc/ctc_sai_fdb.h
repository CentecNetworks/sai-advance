/**
 @file ctc_sai_fdb.h

 @author  Copyright (C) 2018 Centec Networks Inc.  All rights reserved.

 @date 2018-02-1

 @version v2.0

\p
 This module defines SAI FDB.
\b
\p
 The FDB Module APIs supported by centec devices:
\p
\b
\t  |   API                                |       SUPPORT CHIPS LIST       |
\t  |  create_fdb_entry                    |    CTC8096,CTC7148,CTC7132     |
\t  |  remove_fdb_entry                    |    CTC8096,CTC7148,CTC7132     |
\t  |  set_fdb_entry_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  get_fdb_entry_attribute             |    CTC8096,CTC7148,CTC7132     |
\t  |  flush_fdb_entries                   |    CTC8096,CTC7148,CTC7132     |
\b

\p
 The FDB attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_FDB_ENTRY_ATTR_TYPE             |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_ENTRY_ATTR_PACKET_ACTION    |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_ENTRY_ATTR_USER_TRAP_ID     |              -                 |
\t  |  SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_ENTRY_ATTR_META_DATA        |        CTC7148,CTC7132         |
\t  |  SAI_FDB_ENTRY_ATTR_ENDPOINT_IP      |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_ENTRY_ATTR_COUNTER_ID       |              -                 |
\b

\p
 The FDB FLUSH attributes supported by centec devices:
\p
\b
\t  |   ATTRIBUTE                          |       SUPPORT CHIPS LIST       |
\t  |  SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID   |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_FLUSH_ATTR_BV_ID            |    CTC8096,CTC7148,CTC7132     |
\t  |  SAI_FDB_FLUSH_ATTR_ENTRY_TYPE       |    CTC8096,CTC7148,CTC7132     |
\b

*/

#ifndef _CTC_SAI_FDB_H
#define _CTC_SAI_FDB_H

#include "ctc_sai.h"

#include "sal.h"
#include "ctcs_api.h"

/*don't need include other header files*/

#define NOT_CARE_FID 0xffff
extern sai_status_t
ctc_sai_fdb_api_init();
extern sai_status_t
ctc_sai_fdb_db_init(uint8 lchip);
extern sai_status_t
ctc_sai_fdb_flush_fdb( sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list);
extern uint32
ctc_sai_fdb_get_fdb_count(uint8 lchip);
extern sai_status_t
ctc_sai_fdb_dump_fdb_entrys(uint8 lchip, uint32_t object_count, sai_object_key_t *object_list);
extern sai_status_t
ctc_sai_fdb_dump(uint8 lchip, sal_file_t p_file, ctc_sai_dump_grep_param_t *dump_grep_param);

#endif /*_CTC_SAI_FDB_H*/

