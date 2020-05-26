

/**
 @file ctc_warmboot.h

 @date 2016-04-13

 @version v5.0

 The file defines warmboot api
*/
#ifndef _CTC_APP_WARMBOOT_H_
#define _CTC_APP_WARMBOOT_H_
#ifdef __cplusplus
extern "C" {
#endif
/****************************************************************
 *
 * Header Files
 *
 ***************************************************************/
#include "sal.h"
#include "ctc_const.h"
#include "ctc_mix.h"
#include "ctc_error.h"

#include "ctc_warmboot.h"

/****************************************************************
*
* Defines and Macros
*
****************************************************************/

/**********************************************************************************
                      Define API function interfaces
 ***********************************************************************************/
extern int32
ctc_sai_wb_func_init(uint8 lchip, uint8 reloading);
extern int32
ctc_sai_wb_func_init_done(uint8 lchip);
extern int32
ctc_sai_wb_func_sync(uint8 lchip);
extern int32
ctc_sai_wb_func_sync_done(uint8 lchip, int32 result);
extern int32
ctc_sai_wb_func_add_entry(ctc_wb_data_t *data);
extern int32
ctc_sai_wb_func_query_entry(ctc_wb_query_t *query);

#ifdef __cplusplus
}
#endif

#endif  /* _CTC_APP_WARMBOOT_H_*/

