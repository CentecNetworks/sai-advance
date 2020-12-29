#ifndef _CTC_SAI_META_CLI_H
#define _CTC_SAI_META_CLI_H

#ifdef __cplusplus
extern "C" {
#endif

#include "ctc_sai_meta_db.h"

extern int32
ctc_sai_cli_init(void);

extern int
ctc_sai_metadata_apis_query(sai_api_query_fn, sai_apis_t*);

#ifdef __cplusplus
}
#endif

#endif

